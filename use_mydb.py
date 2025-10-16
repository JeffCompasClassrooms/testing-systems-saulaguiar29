from mydb import MyDB
import os


#took a picture to catch up with the code

def describe_test_my_db():
    def describe_load_strings_works_when_there_was_no_file():





        # setup

        # ensure that thter is no test_data.dat
        os.remove("test_data.dat")
        a_db = MyDB("test_dat.dat")
        a_list = ['gummy','peanut m&ms', 'caramel reeses', 'werthers']

        #exercise
        a_db.saveStrings(a_list)

        #verify
        os.path.isfile("test_dat.dat")
        b_list = a_db.loadStrings()

        assert(a_list == b_list)

        #teardown
        os.remove("test_dat.dat")