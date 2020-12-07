from pymongo import MongoClient
#from bson.json_util import dumps
#from bson.objectid import ObjectId

def run():
    print("Running...")
    username = "boss"
    password = "ZeP-iFc-jwZ-q46"
    dbname = "test"

    client = MongoClient("mongodb://" + username + ":" + password + "@test.839ly.mongodb.net/" + dbname + "?retryWrites=true&w=majority")

    print("\nClient:")
    print(client)

    db = client[dbname]

    print("\nDB:")
    print(db)

    users_db = db["users"]

    print("\nUsers DB:")
    print(users_db)

    # SOS
#     Traceback (most recent call last):
#   File "c:/Users/Upirj/git/rvt/AutoNoma/mongodb_test.py", line 30, in <module>
#     run()
#   File "c:/Users/Upirj/git/rvt/AutoNoma/mongodb_test.py", line 27, in run
#     users_db.insert_one({"name": "Kek", "surname": "Petrovich", "password": "qwerty12345"})
#   File "C:\Users\Upirj\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\collection.py", line 698, in insert_one
#     self._insert(document,
#   File "C:\Users\Upirj\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\collection.py", line 613, in _insert
#     return self._insert_one(
#   File "C:\Users\Upirj\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\collection.py", line 602, in _insert_one
#     self.__database.client._retryable_write(
#   File "C:\Users\Upirj\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\mongo_client.py", line 1497, in _retryable_write
#     with self._tmp_session(session) as s:
#   File "C:\Users\Upirj\AppData\Local\Programs\Python\Python38-32\lib\contextlib.py", line 113, in __enter__
#     return next(self.gen)
#   File "C:\Users\Upirj\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\mongo_client.py", line 1829, in _tmp_session
#     s = self._ensure_session(session)
#   File "C:\Users\Upirj\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\mongo_client.py", line 1816, in _ensure_session
#     return self.__start_session(True, causal_consistency=False)
#   File "C:\Users\Upirj\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\mongo_client.py", line 1766, in __start_session
#     server_session = self._get_server_session()
#   File "C:\Users\Upirj\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\mongo_client.py", line 1802, in _get_server_session
#     return self._topology.get_server_session()
#   File "C:\Users\Upirj\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\topology.py", line 485, in get_server_session
#     self._select_servers_loop(
#   File "C:\Users\Upirj\AppData\Local\Programs\Python\Python38-32\lib\site-packages\pymongo\topology.py", line 215, in _select_servers_loop
#     raise ServerSelectionTimeoutError(
# pymongo.errors.ServerSelectionTimeoutError: test.839ly.mongodb.net:27017: [Errno 11001] getaddrinfo failed, Timeout: 30s, Topology Description: <TopologyDescription id: 5fce4522c47a5ef58573d051, topology_type: Single, servers: [<ServerDescription ('test.839ly.mongodb.net', 27017) server_type: Unknown, rtt: None, error=AutoReconnect('test.839ly.mongodb.net:27017: [Errno 11001] getaddrinfo failed')>]>

    users_db.insert_one({"name": "Kek", "surname": "Petrovich", "password": "qwerty12345"})

if __name__ == "__main__":
    run()