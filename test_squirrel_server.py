import os
import json
import shutil
import subprocess
import time
import pytest
import requests
from pytest import fixture

BASE_URL = "http://127.0.0.1:8080"
DB_FILE = "squirrel_db.db"
TEMPLATE_DB = "squirrel_db_template.db"

def describe_SquirrelServer():
    """Test suite for Squirrel Server API using black-box system testing"""
    
    @fixture(scope="session")
    def server_process():
        """Start server process for entire test session"""
        # Start the server
        process = subprocess.Popen(
            ["python3", "squirrel_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Wait for server to start
        time.sleep(2)
        yield process
        # Cleanup: terminate server
        process.terminate()
        process.wait()
    
    @fixture
    def clean_db():
        """Reset database to clean state before each test"""
        # Copy template database to working database
        if os.path.exists(TEMPLATE_DB):
            shutil.copy(TEMPLATE_DB, DB_FILE)
        yield
        # No cleanup needed as each test resets the DB
    
    def describe_GET_squirrels():
        """Test GET /squirrels endpoint"""
        
        def it_returns_200_status(server_process, clean_db):
            """Should return 200 OK status"""
            response = requests.get(f"{BASE_URL}/squirrels")
            assert response.status_code == 200
        
        def it_returns_json_content_type(server_process, clean_db):
            """Should return application/json content type"""
            response = requests.get(f"{BASE_URL}/squirrels")
            assert "application/json" in response.headers["Content-Type"]
        
        def it_returns_array(server_process, clean_db):
            """Should return JSON array"""
            response = requests.get(f"{BASE_URL}/squirrels")
            data = response.json()
            assert isinstance(data, list)
        
        def it_returns_empty_array_initially(server_process, clean_db):
            """Should return empty array when no squirrels exist"""
            response = requests.get(f"{BASE_URL}/squirrels")
            data = response.json()
            assert len(data) == 0
        
        def it_returns_created_squirrel(server_process, clean_db):
            """Should return squirrel after creation"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            response = requests.get(f"{BASE_URL}/squirrels")
            data = response.json()
            assert len(data) == 1
        
        def it_returns_multiple_squirrels(server_process, clean_db):
            """Should return all squirrels"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Nutkin", "size": "small"})
            response = requests.get(f"{BASE_URL}/squirrels")
            data = response.json()
            assert len(data) == 2
        
        def it_returns_squirrels_ordered_by_id(server_process, clean_db):
            """Should return squirrels ordered by ID"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "First", "size": "large"})
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Second", "size": "small"})
            response = requests.get(f"{BASE_URL}/squirrels")
            data = response.json()
            assert data[0]["name"] == "First"
            assert data[1]["name"] == "Second"
    
    def describe_GET_squirrels_id():
        """Test GET /squirrels/{id} endpoint"""
        
        def it_returns_200_for_existing_squirrel(server_process, clean_db):
            """Should return 200 OK for existing squirrel"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            assert response.status_code == 200
        
        def it_returns_json_content_type(server_process, clean_db):
            """Should return application/json content type"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            assert "application/json" in response.headers["Content-Type"]
        
        def it_returns_object(server_process, clean_db):
            """Should return JSON object"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            data = response.json()
            assert isinstance(data, dict)
        
        def it_returns_correct_id(server_process, clean_db):
            """Should return squirrel with correct ID"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            data = response.json()
            assert data["id"] == squirrel_id
        
        def it_returns_correct_name(server_process, clean_db):
            """Should return squirrel with correct name"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            data = response.json()
            assert data["name"] == "Fluffy"
        
        def it_returns_correct_size(server_process, clean_db):
            """Should return squirrel with correct size"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            data = response.json()
            assert data["size"] == "large"
        
        def it_returns_specific_squirrel(server_process, clean_db):
            """Should return requested squirrel when multiple exist"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "First", "size": "large"})
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Second", "size": "small"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            second_id = list_response.json()[1]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{second_id}")
            data = response.json()
            assert data["name"] == "Second"
    
    def describe_POST_squirrels():
        """Test POST /squirrels endpoint"""
        
        def it_returns_201_status(server_process, clean_db):
            """Should return 201 Created status"""
            response = requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            assert response.status_code == 201
        
        def it_creates_retrievable_squirrel(server_process, clean_db):
            """Should create squirrel that can be retrieved"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrels = list_response.json()
            assert len(squirrels) == 1
        
        def it_creates_squirrel_with_correct_name(server_process, clean_db):
            """Should create squirrel with provided name"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "TestName", "size": "medium"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel = list_response.json()[0]
            assert squirrel["name"] == "TestName"
        
        def it_creates_squirrel_with_correct_size(server_process, clean_db):
            """Should create squirrel with provided size"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "tiny"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel = list_response.json()[0]
            assert squirrel["size"] == "tiny"
        
        def it_assigns_id_to_created_squirrel(server_process, clean_db):
            """Should assign ID to created squirrel"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel = list_response.json()[0]
            assert "id" in squirrel
        
        def it_creates_multiple_squirrels(server_process, clean_db):
            """Should create multiple squirrels independently"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "First", "size": "large"})
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Second", "size": "small"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrels = list_response.json()
            assert len(squirrels) == 2
        
        def it_persists_created_squirrel(server_process, clean_db):
            """Should persist created squirrel across requests"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Persistent", "size": "large"})
            first_get = requests.get(f"{BASE_URL}/squirrels")
            second_get = requests.get(f"{BASE_URL}/squirrels")
            assert first_get.json() == second_get.json()
    
    def describe_PUT_squirrels_id():
        """Test PUT /squirrels/{id} endpoint"""
        
        def it_returns_204_status(server_process, clean_db):
            """Should return 204 No Content status"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.put(f"{BASE_URL}/squirrels/{squirrel_id}", data={"name": "Updated", "size": "small"})
            assert response.status_code == 204
        
        def it_updates_squirrel_name(server_process, clean_db):
            """Should update squirrel name"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Original", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.put(f"{BASE_URL}/squirrels/{squirrel_id}", data={"name": "NewName", "size": "large"})
            get_response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            updated = get_response.json()
            assert updated["name"] == "NewName"
        
        def it_updates_squirrel_size(server_process, clean_db):
            """Should update squirrel size"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.put(f"{BASE_URL}/squirrels/{squirrel_id}", data={"name": "Fluffy", "size": "tiny"})
            get_response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            updated = get_response.json()
            assert updated["size"] == "tiny"
        
        def it_preserves_squirrel_id(server_process, clean_db):
            """Should not change squirrel ID"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            original_id = list_response.json()[0]["id"]
            requests.put(f"{BASE_URL}/squirrels/{original_id}", data={"name": "Updated", "size": "small"})
            get_response = requests.get(f"{BASE_URL}/squirrels/{original_id}")
            updated = get_response.json()
            assert updated["id"] == original_id
        
        def it_updates_both_fields(server_process, clean_db):
            """Should update both name and size simultaneously"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Old", "size": "big"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.put(f"{BASE_URL}/squirrels/{squirrel_id}", data={"name": "New", "size": "small"})
            get_response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            updated = get_response.json()
            assert updated["name"] == "New" and updated["size"] == "small"
        
        def it_persists_update(server_process, clean_db):
            """Should persist update across requests"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Original", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.put(f"{BASE_URL}/squirrels/{squirrel_id}", data={"name": "Updated", "size": "small"})
            first_get = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            second_get = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            assert first_get.json()["name"] == "Updated"
            assert second_get.json()["name"] == "Updated"
        
        def it_only_updates_target_squirrel(server_process, clean_db):
            """Should only update specified squirrel"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "First", "size": "large"})
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Second", "size": "small"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            first_id = list_response.json()[0]["id"]
            requests.put(f"{BASE_URL}/squirrels/{first_id}", data={"name": "Changed", "size": "medium"})
            get_response = requests.get(f"{BASE_URL}/squirrels")
            squirrels = get_response.json()
            assert squirrels[0]["name"] == "Changed"
            assert squirrels[1]["name"] == "Second"
    
    def describe_DELETE_squirrels_id():
        """Test DELETE /squirrels/{id} endpoint"""
        
        def it_returns_204_status(server_process, clean_db):
            """Should return 204 No Content status"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.delete(f"{BASE_URL}/squirrels/{squirrel_id}")
            assert response.status_code == 204
        
        def it_removes_squirrel_from_list(server_process, clean_db):
            """Should remove squirrel from list endpoint"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.delete(f"{BASE_URL}/squirrels/{squirrel_id}")
            after_delete = requests.get(f"{BASE_URL}/squirrels")
            assert len(after_delete.json()) == 0
        
        def it_makes_squirrel_unretrievable(server_process, clean_db):
            """Should make squirrel unretrievable by ID"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.delete(f"{BASE_URL}/squirrels/{squirrel_id}")
            get_response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            assert get_response.status_code == 404
        
        def it_only_deletes_target_squirrel(server_process, clean_db):
            """Should only delete specified squirrel"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Keep", "size": "large"})
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Delete", "size": "small"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            delete_id = list_response.json()[1]["id"]
            requests.delete(f"{BASE_URL}/squirrels/{delete_id}")
            after_delete = requests.get(f"{BASE_URL}/squirrels")
            squirrels = after_delete.json()
            assert len(squirrels) == 1
            assert squirrels[0]["name"] == "Keep"
        
        def it_persists_deletion(server_process, clean_db):
            """Should persist deletion across requests"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.delete(f"{BASE_URL}/squirrels/{squirrel_id}")
            first_check = requests.get(f"{BASE_URL}/squirrels")
            second_check = requests.get(f"{BASE_URL}/squirrels")
            assert len(first_check.json()) == 0
            assert len(second_check.json()) == 0
    
    def describe_404_errors():
        """Test 404 error conditions"""
        
        def it_returns_404_for_nonexistent_squirrel_get(server_process, clean_db):
            """Should return 404 for GET with nonexistent ID"""
            response = requests.get(f"{BASE_URL}/squirrels/99999")
            assert response.status_code == 404
        
        def it_returns_404_for_nonexistent_squirrel_put(server_process, clean_db):
            """Should return 404 for PUT with nonexistent ID"""
            response = requests.put(f"{BASE_URL}/squirrels/99999", data={"name": "Test", "size": "large"})
            assert response.status_code == 404
        
        def it_returns_404_for_nonexistent_squirrel_delete(server_process, clean_db):
            """Should return 404 for DELETE with nonexistent ID"""
            response = requests.delete(f"{BASE_URL}/squirrels/99999")
            assert response.status_code == 404
        
        def it_returns_404_for_invalid_resource(server_process, clean_db):
            """Should return 404 for unknown resource path"""
            response = requests.get(f"{BASE_URL}/invalid")
            assert response.status_code == 404
        
        def it_returns_404_for_post_with_id(server_process, clean_db):
            """Should return 404 for POST with ID in path"""
            response = requests.post(f"{BASE_URL}/squirrels/1", data={"name": "Test", "size": "large"})
            assert response.status_code == 404
        
        def it_returns_404_for_put_without_id(server_process, clean_db):
            """Should return 404 for PUT without ID"""
            response = requests.put(f"{BASE_URL}/squirrels", data={"name": "Test", "size": "large"})
            assert response.status_code == 404
        
        def it_returns_404_for_delete_without_id(server_process, clean_db):
            """Should return 404 for DELETE without ID"""
            response = requests.delete(f"{BASE_URL}/squirrels")
            assert response.status_code == 404
        
        def it_returns_404_text_content_type(server_process, clean_db):
            """Should return text/plain content type for 404"""
            response = requests.get(f"{BASE_URL}/invalid")
            assert "text/plain" in response.headers["Content-Type"]
        
        def it_returns_404_message(server_process, clean_db):
            """Should return '404 Not Found' message"""
            response = requests.get(f"{BASE_URL}/invalid")
            assert response.text == "404 Not Found"
        
        def it_returns_404_for_deleted_squirrel(server_process, clean_db):
            """Should return 404 for previously deleted squirrel"""
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Temp", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.delete(f"{BASE_URL}/squirrels/{squirrel_id}")
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            assert response.status_code == 404
        
        def it_returns_404_for_nested_invalid_path(server_process, clean_db):
            """Should return 404 for deeply nested invalid paths"""
            response = requests.get(f"{BASE_URL}/squirrels/1/invalid")
            assert response.status_code == 404