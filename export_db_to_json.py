import json
import argparse
from pymongo import MongoClient
from bson.json_util import dumps, loads 


def write_to_json(data, file_name):
    # Writing data to file data.json 
    with open(file_name + '.json', 'w') as file: 
        file.write(data)
    print("Json created")
    
    
def connect_to_db():
    mongo_client = MongoClient('mongodb://172.17.0.2')
    db = mongo_client['Data']
    return db
    

def count_documents(collection, db):
    col = db[collection]
    counts = db[collection].count_documents({})
    print("{collection} : count-{counts}".format(collection=collection, counts=counts))
    return counts
    

def convert_data_to_json(collection, db):
    # Accessing the collection
    col = db[collection]
    # Now creating a Cursor instance 
    # using find() function 
    cursor = col.find()
    # Converting cursor to the list  
    # of dictionaries 
    list_cur = list(cursor)
    # Converting to the JSON 
    json_data = dumps(list_cur, indent = 2)
    return json_data


def main(collections_list):
    db = connect_to_db()
    for col in collections_list:
        print(col)
        data = convert_data_to_json(col, db)
        write_to_json(data, col)
        counts = count_documents(col, db)


def get_args():
    parser = argparse.ArgumentParser(description='Prepare data for compare')
    parser.add_argument('-c', nargs='+', help='Collections list to export')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    main(args.c)
