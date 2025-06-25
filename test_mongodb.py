
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://23cs2042:<password>@cluster0.udigol7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"#password me apna dal dena to check mongodb is connected or not

# Create a new client and connect to the server
client = MongoClient(uri)#for connection to mongodb database

# Send a ping to confirm a successful connection
try:#checking whether we are able to pick tha database or not
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)