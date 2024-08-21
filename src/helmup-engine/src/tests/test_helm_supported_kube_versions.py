import pytest
from src.supported_kube_versions import SupportedKubeVersions

# Test cases
def test_valid_helm_chart():
    folder_path = './snyk/helm-valid'
    k8s_version = '1.25.0'
    test, list = SupportedKubeVersions().test_helm_on_k8s_version(folder_path, k8s_version)
    assert test == False

if __name__ == "__main__":
    pytest.main()
    
# To run the tests, you can execute the following command in the terminal:
# pytest test_helm_supported_kube_versions.py
