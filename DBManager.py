import pymongo
import datetime

class DBManager:
    """
    Input:
        conString - Connection string for the database
        dbName - Name of the database
        collection - Name of collection inside database
    Misc:
        _manager - Used to interact with database
    """
    def __init__(self, conString, dbName, collection):
        self.connectionString = conString
        self.databaseName = dbName
        self.collection = collection
        self._manager = "";

    """
    Purpose: Assign manager to an instance of our database collection
    Input:
        None
    Output:
        None
    """
    def connect(self):
        try:
            self._manager = pymongo.MongoClient(self.connectionString)[self.databaseName][self.collection]
        except Exception as e:
            print("Error connecting: {}".format(e))

    """
    Purpose: Insert multiple records
    Input:
        records - List of TweetObjects
    Output:
        None
    """
    def insert_list(self, records):
        try:
            print("Inserting {} records".format(len(records)))
            self._manager.insert_many(list(map(lambda x: x.get_dict(), records)))
        except Exception as e:
            print("Error inserting records.\n{}".format(e))

    """
    Purpose: Search all records for dates less than or equal to current time in UTC, and create a list of said records.
    Input:
        None
    Output:
        records - Records that need to be delete/tweeted
    """
    def search_records(self):
        try:
            records = []
            currentTime = datetime.datetime.utcnow()
            for record in self._manager.find().sort("deadline", 1):
                print("Comparing {} to {}, and the result is {}".format(record['deadline'], currentTime, record['deadline']<=currentTime))
                if record['deadline'] <= currentTime:
                    records.append(record)
                else:
                    break
        except Exception as e:
            print("Error searching records\n{}".format(e))
        print("Found {} records to update".format(len(records)))
        return records

    """
    Purpose: Delete records in database that match given records
    Input:
        records - List of database records previously extracted
    Output:
        None
    """
    def update_database(self, records):
        try:
            print("Removing {} records".format(len(records)))
            for record in records:
                self._manager.delete_one(record)
        except Exception as e:
            print("Error updating database\n{}".format(e))

    """
    Purpose: Search and upadte database
    Input:
        None
    Output:
        records - List of recrods that need to be tweeted
    """
    def search_and_update(self):
        try:
            records = self.search_records();
            if(len(records) != 0):
                self.update_database(records)
        except Exception as e:
            print("Error in searching or updating\nError: {}".format(e))
        return records