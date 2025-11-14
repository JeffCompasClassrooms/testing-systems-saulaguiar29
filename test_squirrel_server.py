import os
import json
import shutil
import subprocess
import time
import pytest
import requests
from pytest import fixture

BASE_URL = "http://127.0.0.1:8082"
DB_FILE = "squirrel_db.db"
TEMPLATE_DB = "squirrel_db_template.db"

def describe_SquirrelServer():   
    @fixture(scope="session")
    def server_process():
        process = subprocess.Popen(
            ["python3", "squirrel_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        time.sleep(2)
        yield process

        process.terminate()
        process.wait()
    
    @fixture
    def clean_db():
        if os.path.exists(TEMPLATE_DB):
            shutil.copy(TEMPLATE_DB, DB_FILE)
        yield

    def describe_GET_squirrels(): 
        def it_return_200_status(server_process, clean_db):
            response = requests.get(f"{BASE_URL}/squirrels")
            assert response.status_code == 200
        
        def it_return_json_content_type(server_process, clean_db):
            response = requests.get(f"{BASE_URL}/squirrels")
            assert "application/json" in response.headers["Content-Type"]
        
        def it_return_array(server_process, clean_db):
            response = requests.get(f"{BASE_URL}/squirrels")
            data = response.json()
            assert isinstance(data, list)
        
        def it_return_empty_array(server_process, clean_db):
            response = requests.get(f"{BASE_URL}/squirrels")
            data = response.json()
            assert len(data) == 0
        
        def it_return_created_squirrel(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Sanchez", "size": "small"})
            response = requests.get(f"{BASE_URL}/squirrels")
            data = response.json()
            assert len(data) == 1
        
        def it_return_multiple_squirrels(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Salty", "size": "large"})
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Oreo", "size": "small"})
            response = requests.get(f"{BASE_URL}/squirrels")
            data = response.json()
            assert len(data) == 2
        
        def it_return_squirrels_ordered_by_id(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Uno", "size": "large"})
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Dos", "size": "small"})
            response = requests.get(f"{BASE_URL}/squirrels")
            data = response.json()
            assert data[0]["name"] == "Uno"
            assert data[1]["name"] == "Dos"
    
    def describe_GET_squirrels_id():
        def it_return_200_for_existing_squirrel(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Biggy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            assert response.status_code == 200
        
        def it_return_json_content_type(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            assert "application/json" in response.headers["Content-Type"]
        
        def it_return_object(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Stark", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            data = response.json()
            assert isinstance(data, dict)
        
        def it_return_correct_id(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Tony", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            data = response.json()
            assert data["id"] == squirrel_id
        
        def it_return_correct_name(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Panther", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            data = response.json()
            assert data["name"] == "Panther"
        
        def it_return_correct_size(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fern", "size": "small"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            data = response.json()
            assert data["size"] == "small"
        
        def it_return_specific_squirrel(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Sonic", "size": "large"})
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Thisone", "size": "small"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            second_id = list_response.json()[1]["id"]
            response = requests.get(f"{BASE_URL}/squirrels/{second_id}")
            data = response.json()
            assert data["name"] == "Thisone"
    
    def describe_POST_squirrels():
        def it_return_201_status(server_process, clean_db):
            response = requests.post(f"{BASE_URL}/squirrels", data={"name": "Strange", "size": "large"})
            assert response.status_code == 201
        
        def it_create_retrievable_squirrel(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Golden", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrels = list_response.json()
            assert len(squirrels) == 1
        
        def it_create_squirrel_with_correct_name(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Correct?", "size": "medium"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel = list_response.json()[0]
            assert squirrel["name"] == "Correct?"
        
        def it_create_squirrel_with_correct_size(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Parmesan", "size": "tiny"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel = list_response.json()[0]
            assert squirrel["size"] == "tiny"
        
        def it_assign_id_to_created_squirrel(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Ida", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel = list_response.json()[0]
            assert "id" in squirrel
        
        def it_create_multiple_squirrels(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Thing1", "size": "large"})
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Thing2", "size": "small"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrels = list_response.json()
            assert len(squirrels) == 2
        
        def it_returns_400_when_name_missing(server_process, clean_db):
        
            response = requests.post(f"{BASE_URL}/squirrels", data={"size": "large"})
            assert response.status_code == 400

        def it_returns_400_when_size_missing(server_process, clean_db):
        
            response = requests.post(f"{BASE_URL}/squirrels", data={"name": "Rocky"})
            assert response.status_code == 400

        def it_returns_400_when_both_fields_missing(server_process, clean_db):
        
            response = requests.post(f"{BASE_URL}/squirrels", data={})
            assert response.status_code == 400
    
    def describe_PUT_squirrels_id():   
        def it_returns_204_status(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Wheeler", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.put(f"{BASE_URL}/squirrels/{squirrel_id}", data={"name": "Updated", "size": "small"})
            assert response.status_code == 204
        
        def it_updates_squirrel_name(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Pichu", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.put(f"{BASE_URL}/squirrels/{squirrel_id}", data={"name": "Pikachu", "size": "large"})
            get_response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            updated = get_response.json()
            assert updated["name"] == "Pikachu"
        
        def it_update_squirrel_size(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "tiny"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.put(f"{BASE_URL}/squirrels/{squirrel_id}", data={"name": "Fluffy", "size": "large"})
            get_response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            updated = get_response.json()
            assert updated["size"] == "large"
        
        def it_preserves_squirrel_id(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fossil", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            original_id = list_response.json()[0]["id"]
            requests.put(f"{BASE_URL}/squirrels/{original_id}", data={"name": "Dinosaur", "size": "small"})
            get_response = requests.get(f"{BASE_URL}/squirrels/{original_id}")
            updated = get_response.json()
            assert updated["id"] == original_id
        
        def it_update_both_fields(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Charmander", "size": "small"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.put(f"{BASE_URL}/squirrels/{squirrel_id}", data={"name": "Charmeleon", "size": "medium"})
            get_response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            updated = get_response.json()
            assert updated["name"] == "Charmeleon" and updated["size"] == "medium"

        def it_returns_400_when_update_missing_name_or_size(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Testy", "size": "small"})
            squirrel_id = requests.get(f"{BASE_URL}/squirrels").json()[0]["id"]

            
            res1 = requests.put(f"{BASE_URL}/squirrels/{squirrel_id}", data={"size": "big"})
            assert res1.status_code == 400

            
            res2 = requests.put(f"{BASE_URL}/squirrels/{squirrel_id}", data={"name": "Testy2"})
            assert res2.status_code == 400
        
    
    def describe_DELETE_squirrels_id():
        def it_returns_204_status(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Hamlet", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            response = requests.delete(f"{BASE_URL}/squirrels/{squirrel_id}")
            assert response.status_code == 204
        
        def it_remove_squirrel_from_list(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Ben", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.delete(f"{BASE_URL}/squirrels/{squirrel_id}")
            after_delete = requests.get(f"{BASE_URL}/squirrels")
            assert len(after_delete.json()) == 0
        
        def it_make_squirrel_unretrievable(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Fluffy", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.delete(f"{BASE_URL}/squirrels/{squirrel_id}")
            get_response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            assert get_response.status_code == 404
        
        def it_only_delete_target_squirrel(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Keep", "size": "large"})
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Delete", "size": "small"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            delete_id = list_response.json()[1]["id"]
            requests.delete(f"{BASE_URL}/squirrels/{delete_id}")
            after_delete = requests.get(f"{BASE_URL}/squirrels")
            squirrels = after_delete.json()
            assert len(squirrels) == 1
            assert squirrels[0]["name"] == "Keep"
        
    
    def describe_404_errors():    
        def it_return_404_for_nonexistent_squirrel_get(server_process, clean_db):
            response = requests.get(f"{BASE_URL}/squirrels/9000")
            assert response.status_code == 404
        
        def it_return_404_for_nonexistent_squirrel_put(server_process, clean_db):
            response = requests.put(f"{BASE_URL}/squirrels/9000", data={"name": "Test", "size": "large"})
            assert response.status_code == 404
        
        def it_return_404_for_nonexistent_squirrel_delete(server_process, clean_db):
            response = requests.delete(f"{BASE_URL}/squirrels/9000")
            assert response.status_code == 404
        
        def it_return_404_for_invalid_resource(server_process, clean_db):
            response = requests.get(f"{BASE_URL}/invalid")
            assert response.status_code == 404
        
        def it_return_404_for_post_with_id(server_process, clean_db):
            response = requests.post(f"{BASE_URL}/squirrels/1", data={"name": "Test", "size": "large"})
            assert response.status_code == 404
        
        def it_return_404_for_put_without_id(server_process, clean_db):
            response = requests.put(f"{BASE_URL}/squirrels", data={"name": "Test", "size": "large"})
            assert response.status_code == 404
        
        def it_return_404_for_delete_without_id(server_process, clean_db):
            response = requests.delete(f"{BASE_URL}/squirrels")
            assert response.status_code == 404
        
        def it_return_404_text_content_type(server_process, clean_db):
            response = requests.get(f"{BASE_URL}/invalid")
            assert "text/plain" in response.headers["Content-Type"]
        
        def it_return_404_message(server_process, clean_db):
            response = requests.get(f"{BASE_URL}/invalid")
            assert response.text == "404 Not Found"
        
        def it_return_404_for_deleted_squirrel(server_process, clean_db):
            requests.post(f"{BASE_URL}/squirrels", data={"name": "Temp", "size": "large"})
            list_response = requests.get(f"{BASE_URL}/squirrels")
            squirrel_id = list_response.json()[0]["id"]
            requests.delete(f"{BASE_URL}/squirrels/{squirrel_id}")
            response = requests.get(f"{BASE_URL}/squirrels/{squirrel_id}")
            assert response.status_code == 404
        
        def it_return_404_for_invalid_path(server_process, clean_db):
            response = requests.get(f"{BASE_URL}/squirrels/1/invalid")
            assert response.status_code == 404