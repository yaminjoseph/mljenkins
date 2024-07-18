import pytest

from pathlib import Path
import os
import sys

# Adding the below path to avoid module not found error
PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from prediction_model.config import config
from prediction_model.processing.data_handling import load_dataset
from prediction_model.predict import generate_predictions


@pytest.fixture
def single_prediction():
    test_dataset = load_dataset(config.TEST_FILE)
    single_row = test_dataset[:1]
    result = generate_predictions(single_row)
    return result

def test_single_pred_not_none(single_prediction): # Output Not Null
    assert single_prediction is not None

def test_single_pred_str_type(single_prediction): # Output Type=STR
    assert isinstance(single_prediction.get('prediction')[0],str)

def test_single_pred_validate(single_prediction): # Output=Y
    assert single_prediction.get('prediction')[0] =='Y'
