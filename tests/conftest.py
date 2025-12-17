"""
Configuration file for pytest.
This file is automatically discovered and used by pytest.
"""
import sys
from pathlib import Path

# Add the app directory to the Python path
app_path = str(Path(__file__).parent.parent / 'app')
if app_path not in sys.path:
    sys.path.insert(0, app_path)

# Configure logging for tests
import logging
logging.basicConfig(level=logging.INFO)

# Test configuration
TEST_DATA_DIR = Path(__file__).parent / 'data'
