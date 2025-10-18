import os
import pytest
from pytest import fixture
from mydb import MyDB

def describe_MyDB():
    
    @fixture
    def test_db_file():
        filename = "test_mydb.db"
    
        if os.path.exists(filename):
            os.remove(filename)
        yield filename
     
        if os.path.exists(filename):
            os.remove(filename)
    
    def describe_init():
        def create_new_file(test_db_file):
            db = MyDB(test_db_file)
            assert os.path.exists(test_db_file)
        
        def initialize_empty_array(test_db_file):
            db = MyDB(test_db_file)
            result = db.loadStrings()
            assert result == []
        
        def does_not_overwrite_existing_file(test_db_file):
            db1 = MyDB(test_db_file)
            db1.saveStrings(["existing", "data"])
            db2 = MyDB(test_db_file)
            result = db2.loadStrings()
            assert result == ["existing", "data"]
    
    def describe_saveStrings():
        def save_empty_array(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings([])
            result = db.loadStrings()
            assert result == []
        
        def save_single_string(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings(["hi"])
            result = db.loadStrings()
            assert result == ["hi"]
        
        def save_multiple_strings(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings(["this", "should", "work"])
            result = db.loadStrings()
            assert result == ["this", "should", "work"]
        
        def overwrite_existing_data(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings(["before", "data"])
            db.saveStrings(["after", "data"])
            result = db.loadStrings()
            assert result == ["after", "data"]
    
    def describe_loadStrings():
        def load_empty_array(test_db_file):
            db = MyDB(test_db_file)
            result = db.loadStrings()
            assert result == []
        
        def load_saved_strings(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings(["beta", "ray", "bill"])
            result = db.loadStrings()
            assert result == ["beta", "ray", "bill"]
        
        def returns_list_type(test_db_file):
            db = MyDB(test_db_file)
            result = db.loadStrings()
            assert isinstance(result, list)
        
        def load_correct_order(test_db_file):
            db = MyDB(test_db_file)
            ordered_data = ["should", "be", "the", "order"]
            db.saveStrings(ordered_data)
            result = db.loadStrings()
            assert result == ordered_data
        
    def describe_saveString():
        def append_to_empty_array(test_db_file):
            db = MyDB(test_db_file)
            db.saveString("first")
            result = db.loadStrings()
            assert result == ["first"]
        
        def appends_to_existing_array(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings(["existing"])
            db.saveString("new")
            result = db.loadStrings()
            assert result == ["existing", "new"]
        
        def append_multiple_times(test_db_file):
            db = MyDB(test_db_file)
            db.saveString("uno")
            db.saveString("dos")
            db.saveString("tres")
            result = db.loadStrings()
            assert result == ["uno", "dos", "tres"]
        
        def preserve_previous_strings(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings(["keep1", "keep2"])
            db.saveString("new")
            result = db.loadStrings()
            assert "keep1" in result
            assert "keep2" in result
            assert "new" in result
        
        def append_empty_string(test_db_file):
            db = MyDB(test_db_file)
            db.saveString("")
            result = db.loadStrings()
            assert result == [""]
        
        def append_duplicate_strings(test_db_file):
            db = MyDB(test_db_file)
            db.saveString("dupe")
            db.saveString("dupe")
            result = db.loadStrings()
            assert result == ["dupe", "dupe"]
        
        def maintain_append_order(test_db_file):
            db = MyDB(test_db_file)
            db.saveString("A")
            db.saveString("B")
            db.saveString("C")
            result = db.loadStrings()
            assert result[0] == "A"
            assert result[1] == "B"
            assert result[2] == "C"
        
        def persist_appended_string(test_db_file):
            db1 = MyDB(test_db_file)
            db1.saveString("persistent")
            db2 = MyDB(test_db_file)
            result = db2.loadStrings()
            assert "persistent" in result