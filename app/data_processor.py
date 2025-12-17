"""
Data processing module for the English-Shona language identification project.
Handles loading, cleaning, and splitting the dataset for model training.
"""
import os
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, List, Optional
from sklearn.model_selection import train_test_split
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Handles loading, cleaning, and processing of the language dataset."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the DataProcessor with data directory paths.
        
        Args:
            data_dir: Base directory containing the raw data
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.splits_dir = self.data_dir / "splits"
        
        # Create necessary directories if they don't exist
        for directory in [self.raw_dir, self.processed_dir, self.splits_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load the dataset from a file.
        
        Args:
            file_path: Path to the data file (CSV, JSON, or Excel)
            
        Returns:
            DataFrame containing the loaded data
        """
        file_path = Path(file_path)
        logger.info(f"Loading data from {file_path}")
        
        if file_path.suffix == '.csv':
            return pd.read_csv(file_path)
        elif file_path.suffix == '.json':
            return pd.read_json(file_path)
        elif file_path.suffix in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text data.
        
        Args:
            text: Input text to clean
            
        Returns:
            Cleaned text
        """
        if not isinstance(text, str):
            return ""
            
        # Basic text cleaning
        text = text.strip()
        # Add more cleaning steps as needed
        
        return text
    
    def preprocess_data(self, df: pd.DataFrame, 
                       text_column: str = "text",
                       label_column: str = "language") -> pd.DataFrame:
        """Preprocess the dataset.
        
        Args:
            df: Input DataFrame
            text_column: Name of the column containing text data
            label_column: Name of the column containing language labels
            
        Returns:
            Preprocessed DataFrame
        """
        logger.info("Preprocessing data...")
        
        # Make a copy to avoid modifying the original
        df = df.copy()
        
        # Clean text data
        df[text_column] = df[text_column].apply(self.clean_text)
        
        # Map labels to standard format if needed
        # Example: df[label_column] = df[label_column].map({'en': 'english', 'sn': 'shona'})
        
        # Drop rows with empty text
        df = df[df[text_column].str.strip().astype(bool)]
        
        # Reset index after dropping rows
        df = df.reset_index(drop=True)
        
        return df
    
    def train_val_test_split(self, 
                           df: pd.DataFrame,
                           test_size: float = 0.2,
                           val_size: float = 0.1,
                           random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Split data into training, validation, and test sets.
        
        Args:
            df: Input DataFrame
            test_size: Proportion of data to use for testing
            val_size: Proportion of training data to use for validation
            random_state: Random seed for reproducibility
            
        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        logger.info(f"Splitting data (train/val/test): {1-test_size-val_size}/{val_size}/{test_size}")
        
        # First split: training + validation vs test
        train_val_df, test_df = train_test_split(
            df, 
            test_size=test_size,
            random_state=random_state,
            stratify=df['language'] if 'language' in df.columns else None
        )
        
        # Second split: training vs validation
        if val_size > 0:
            # Calculate the ratio for the second split
            val_ratio = val_size / (1 - test_size)
            train_df, val_df = train_test_split(
                train_val_df,
                test_size=val_ratio,
                random_state=random_state,
                stratify=train_val_df['language'] if 'language' in train_val_df.columns else None
            )
            return train_df, val_df, test_df
        
        return train_val_df, pd.DataFrame(), test_df
    
    def save_splits(self, 
                   train_df: pd.DataFrame, 
                   val_df: pd.DataFrame, 
                   test_df: pd.DataFrame,
                   output_dir: str = None) -> None:
        """Save the split datasets to disk.
        
        Args:
            train_df: Training data
            val_df: Validation data (can be empty)
            test_df: Test data
            output_dir: Directory to save the split files
        """
        if output_dir is None:
            output_dir = self.splits_dir
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving split datasets to {output_dir}")
        
        # Save each split to a CSV file
        train_df.to_csv(output_dir / "train.csv", index=False)
        if not val_df.empty:
            val_df.to_csv(output_dir / "val.csv", index=False)
        test_df.to_csv(output_dir / "test.csv", index=False)
        
        # Log dataset sizes
        logger.info(f"Dataset sizes - Train: {len(train_df):,}, "
                   f"Val: {len(val_df):,}, Test: {len(test_df):,}")
    
    def process_pipeline(self, 
                        input_file: str,
                        text_column: str = "text",
                        label_column: str = "language",
                        test_size: float = 0.2,
                        val_size: float = 0.1,
                        random_state: int = 42) -> Dict[str, pd.DataFrame]:
        """Run the complete data processing pipeline.
        
        Args:
            input_file: Path to the input data file
            text_column: Name of the text column
            label_column: Name of the label column
            test_size: Proportion of data for testing
            val_size: Proportion of training data for validation
            random_state: Random seed for reproducibility
            
        Returns:
            Dictionary containing the processed data splits
        """
        # Load data
        df = self.load_data(input_file)
        
        # Preprocess data
        processed_df = self.preprocess_data(
            df, 
            text_column=text_column, 
            label_column=label_column
        )
        
        # Split data
        train_df, val_df, test_df = self.train_val_test_split(
            processed_df,
            test_size=test_size,
            val_size=val_size,
            random_state=random_state
        )
        
        # Save splits
        self.save_splits(train_df, val_df, test_df)
        
        return {
            'train': train_df,
            'val': val_df,
            'test': test_df
        }


def main():
    """Example usage of the DataProcessor class."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process language dataset')
    parser.add_argument('input_file', type=str, help='Path to the input data file')
    parser.add_argument('--text-col', type=str, default='text', 
                       help='Name of the text column')
    parser.add_argument('--label-col', type=str, default='language',
                       help='Name of the label column')
    parser.add_argument('--test-size', type=float, default=0.2,
                       help='Proportion of data for testing')
    parser.add_argument('--val-size', type=float, default=0.1,
                       help='Proportion of training data for validation')
    parser.add_argument('--random-state', type=int, default=42,
                       help='Random seed for reproducibility')
    parser.add_argument('--output-dir', type=str, default=None,
                       help='Directory to save the processed data')
    
    args = parser.parse_args()
    
    # Initialize data processor
    processor = DataProcessor()
    
    # Process data
    splits = processor.process_pipeline(
        input_file=args.input_file,
        text_column=args.text_col,
        label_column=args.label_col,
        test_size=args.test_size,
        val_size=args.val_size,
        random_state=args.random_state
    )
    
    logger.info("Data processing completed successfully!")


if __name__ == "__main__":
    main()
