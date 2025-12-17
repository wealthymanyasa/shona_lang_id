"""
Unit tests for the data_processor module.
"""
import os
import tempfile
import pandas as pd
import pytest
from pathlib import Path

# Add the app directory to the Python path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent / 'app'))

from data_processor import DataProcessor

# Sample test data
TEST_DATA = """text,language
"Hello, how are you?","en"
"Mhoro, makadii?","sn"
"Good morning!","en"
"Manheru akanaka!","sn"
"",""
"   ",""
"12345",""
"@#$%^",""
"""

@pytest.fixture
def sample_data_file():
    """Create a temporary file with test data."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(TEST_DATA)
        f.flush()
        yield f.name
    # Cleanup
    os.unlink(f.name)

def test_data_processor_init():
    """Test DataProcessor initialization."""
    processor = DataProcessor()
    assert processor.data_dir.exists()
    assert processor.raw_dir.exists()
    assert processor.processed_dir.exists()
    assert processor.splits_dir.exists()

def test_load_data_csv(sample_data_file):
    """Test loading data from a CSV file."""
    processor = DataProcessor()
    df = processor.load_data(sample_data_file)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 8  # 8 lines total, including empty ones
    assert 'text' in df.columns
    assert 'language' in df.columns

def test_clean_text():
    """Test text cleaning functionality."""
    processor = DataProcessor()
    
    # Test basic cleaning
    assert processor.clean_text("  Hello!  ") == "Hello!"
    assert processor.clean_text("") == ""
    assert processor.clean_text("   ") == ""
    assert processor.clean_text(123) == ""
    assert processor.clean_text(None) == ""

def test_preprocess_data():
    """Test data preprocessing."""
    processor = DataProcessor()
    
    # Create a test DataFrame
    data = {
        'text': ['Hello', '   ', 'Mhoro', None, 123],
        'language': ['en', 'sn', 'sn', 'en', 'sn']
    }
    df = pd.DataFrame(data)
    
    # Preprocess the data
    processed_df = processor.preprocess_data(df)
    
    # Check that empty/invalid rows are removed
    assert len(processed_df) == 3  # Only 3 valid rows
    assert all(processed_df['text'].str.strip().astype(bool))  # No empty strings

def test_train_val_test_split():
    """Test data splitting functionality."""
    processor = DataProcessor()
    
    # Create a test DataFrame
    data = {
        'text': [f'sample_{i}' for i in range(100)],
        'language': ['en' if i % 2 == 0 else 'sn' for i in range(100)]
    }
    df = pd.DataFrame(data)
    
    # Test splitting with validation set
    train_df, val_df, test_df = processor.train_val_test_split(
        df, test_size=0.2, val_size=0.1, random_state=42
    )
    
    # Check the sizes with some flexibility for floating point arithmetic
    # Expected: 100 * 0.8 = 80 for train+val, 20 for test
    # Then 80 * 0.9 = 72 for train, 8 for val
    # Allow for small variations due to floating-point arithmetic
    assert abs(len(train_df) - 72) <= 2  # Allow ±2 difference
    assert abs(len(val_df) - 8) <= 1     # Allow ±1 difference
    assert len(test_df) == 20            # Test size should be exact
    
    # Check that all data is accounted for
    total_samples = len(train_df) + len(val_df) + len(test_df)
    assert total_samples == len(df), f"Expected {len(df)} samples total, got {total_samples}"
    
    # Check that the split is stratified (roughly equal class distribution)
    en_count = len(train_df[train_df['language'] == 'en'])
    sn_count = len(train_df[train_df['language'] == 'sn'])
    assert abs(en_count - sn_count) <= 2, f"Class imbalance too large: {en_count} en vs {sn_count} sn"

def test_save_splits(tmp_path):
    """Test saving split datasets."""
    processor = DataProcessor()
    
    # Create test DataFrames
    train_df = pd.DataFrame({'text': ['train1', 'train2'], 'language': ['en', 'sn']})
    val_df = pd.DataFrame({'text': ['val1', 'val2'], 'language': ['en', 'sn']})
    test_df = pd.DataFrame({'text': ['test1', 'test2'], 'language': ['en', 'sn']})
    
    # Save the splits
    output_dir = tmp_path / "test_splits"
    processor.save_splits(train_df, val_df, test_df, output_dir=str(output_dir))
    
    # Check that files were created
    assert (output_dir / 'train.csv').exists()
    assert (output_dir / 'val.csv').exists()
    assert (output_dir / 'test.csv').exists()
    
    # Check that the data was saved correctly
    loaded_train = pd.read_csv(output_dir / 'train.csv')
    assert len(loaded_train) == 2
    assert 'train1' in loaded_train['text'].values

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
