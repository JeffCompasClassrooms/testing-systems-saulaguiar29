import os.path
import pickle

class MyDB:

    def __init__(self, filename):
        self.fname = filename
        if not os.path.isfile(self.fname):
            self.saveStrings([])

    def loadStrings(self):
        with open(self.fname, 'rb') as f:
            arr = pickle.load(f)
        return arr

    def saveStrings(self, arr):
        with open(self.fname, 'wb') as f:
            pickle.dump(arr, f)

    def saveString(self, s):
        arr = self.loadStrings()
        arr.append(s)
        self.saveStrings(arr)

# curl -X GET http://localhost:5000/squirrels
# curl -X GET http://localhost:5000/squirrels/1
# curl -X POST -H "Content-Type: application/json" -d '{"name":"Rocky","size":"large"}' http://localhost:5000/squirrels
# curl -X PUT -H "Content-Type: application/json" -d '{"name":"Rocky","size":"small"}' http://localhost:5000/squirrels/1
# curl -X DELETE http://localhost:5000/squirrels/1          
# curl -X POST  http://localhost:5000/squirrels -d "name=Rocky&size=large"