import pytest
from src.helm.utils import is_helm_chart

# Test cases
def test_valid_helm_chart():
    folder_path = './snyk/helm-valid'
    assert is_helm_chart(folder_path) is True

def test_invalid_helm_chart_missing_file():
    folder_path = './snyk/helm-invalid-missing-files'
    assert is_helm_chart(folder_path) is False

def test_invalid_helm_chart_missing_required_fields():
    folder_path = './snyk/helm-invalid-missing-fields'
    assert is_helm_chart(folder_path) is False

if __name__ == "__main__":
    pytest.main()
    
# To run the tests, you can execute the following command in the terminal:
# pytest test_is_chart.py
