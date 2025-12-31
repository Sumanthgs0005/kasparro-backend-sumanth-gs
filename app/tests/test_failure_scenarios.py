import pytest
from fastapi.testclient import TestClient
from app.main import app
import tempfile
import os

client = TestClient(app)

@pytest.mark.parametrize("invalid_file", [
    b"not a csv file",
    b"name,symbol\ninvalid data",
])
def test_invalid_csv_upload(invalid_file):
    """Test invalid CSV file handling."""
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(invalid_file)
        tmp.flush()
        
        with open(tmp.name, 'rb') as f:
            response = client.post(
                "/api/v1/data/ingest/csv",
                files={"file": ("test.txt", f, "text/plain")}
            )
    
    assert response.status_code == 422  # Validation error
