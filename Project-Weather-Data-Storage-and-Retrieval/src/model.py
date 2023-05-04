# Imports Database class from the project to provide basic functionality for database access
from database import Database
import math
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId


# User document contains username (String), email (String), and role (String) fields
class UserModel:
    USER_COLLECTION = 'users'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error


    def has_admin_access(self, username):
        user_doc = self.find_by_username(username)
        if user_doc == None:
            return False
        else:
            if user_doc['role'] == 'admin':
                return True
            elif user_doc['role'] == 'default':
                return False

    def has_device_access(self, username, dev_id):
        key = {'username': username, 'access_list': {'$elemMatch': {'dev_id': dev_id}}}
        user_doc = self._db.get_by_username_and_device_id(UserModel.USER_COLLECTION, username, key)
        if user_doc:
            return user_doc
        else:
            return False
    
    # Since username should be unique in users collection, this provides a way to fetch the user document based on the username
    def find_by_username(self, username):
        key = {'username': username}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        user_document = self._db.get_single_data(UserModel.USER_COLLECTION, key)
        return user_document
    
    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, username, email, role, access_list):
        self._latest_error = ''
        user_document = self.find_by_username(username)
        if (user_document):
            self._latest_error = f'Username {username} already exists'
            return -1
        
        user_data = {'username': username, 'email': email, 'role': role, 'access_list': access_list}
        user_obj_id = self._db.insert_single_data(UserModel.USER_COLLECTION, user_data)
        return self.find_by_object_id(user_obj_id)

    def drop_document(self, username):
        self._db.drop_doc(UserModel.USER_COLLECTION, username)


# Device document contains device_id (String), desc (String), type (String - temperature/humidity) and manufacturer (String) fields
class DeviceModel:
    DEVICE_COLLECTION = 'devices'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id should be unique in devices collection, this provides a way to fetch the device document based on the device id
    def find_by_device_id(self, device_id):
        key = {'device_id': device_id}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        device_document = self._db.get_single_data(DeviceModel.DEVICE_COLLECTION, key)
        return device_document
    
    # This first checks if a device already exists with that device id. If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, desc, type, manufacturer):
        self._latest_error = ''
        device_document = self.find_by_device_id(device_id)
        if (device_document):
            self._latest_error = f'Device id {device_id} already exists'
            return -1
        
        device_data = {'device_id': device_id, 'desc': desc, 'type': type, 'manufacturer': manufacturer}
        device_obj_id = self._db.insert_single_data(DeviceModel.DEVICE_COLLECTION, device_data)
        return self.find_by_object_id(device_obj_id)


# Weather data document contains device_id (String), value (Integer), and timestamp (Date) fields
class WeatherDataModel:
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id and timestamp should be unique in weather_data collection, this provides a way to fetch the data document based on the device id and timestamp
    def find_by_device_id_and_timestamp(self, device_id, timestamp):
        key = {'device_id': device_id, 'timestamp': timestamp}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        wdata_document = self._db.get_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
        return wdata_document
    
    # This first checks if a data item already exists at a particular timestamp for a device id. If it does, it populates latest_error and returns -1.
    # If it doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, value, timestamp):
        self._latest_error = ''
        wdata_document = self.find_by_device_id_and_timestamp(device_id, timestamp)
        if (wdata_document):
            self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
            return -1
        
        weather_data = {'device_id': device_id, 'value': value, 'timestamp': timestamp}
        wdata_obj_id = self._db.insert_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, weather_data)
        return self.find_by_object_id(wdata_obj_id)

# DailyReportModel document contains
# device_id (String), value(Array),date(Date), avg_value(Double),min_value(Integer),man_value(Integer)
class DailyReportModel:
    DAILY_REPORT_COLLECTION = 'daily_report'
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Finds a document based on the unique auto-generated MongoDB object id
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)

    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        report_document = self._db.get_single_data(DailyReportModel.DAILY_REPORT_COLLECTION, key)
        return report_document

    # Finds all Documents from weather_data collection
    def __find_all_weather_data(self):
        report_document = self._db.find_all(DailyReportModel.WEATHER_DATA_COLLECTION)
        return report_document

    # Finds all Documents from daily_report collection
    def __find_all_report_data(self):
        report_document = self._db.find_all(DailyReportModel.DAILY_REPORT_COLLECTION)
        return report_document

    # Since device id and timestamp should be unique in weather_data collection, this provides a way to fetch the data document based on the device id and timestamp
    def find_by_device_id_and_date(self, device_id, timestamp):
        smallerdate = timestamp.strftime('%Y-%m-%d')
        key = {'device_id': device_id, 'date': smallerdate}
        return self.__find(key)

    # Finds documents based on device_id and between date range
    def find_by_device_id_and_range(self, device_id, from_date, to_date):
        smallerdate_from = from_date.strftime('%Y-%m-%d')
        smallerdate_to = to_date.strftime('%Y-%m-%d')
        key = {'device_id': device_id, 'date': {'$gte': smallerdate_from, '$lte': smallerdate_to}}
        specific_row_return = {'_id': 0, 'device_id': 1, 'avg_value': 1, 'min_value': 1, 'max_value': 1}
        print(f"for range {smallerdate_from} - {smallerdate_to}")
        document = self._db.get_all_data(DailyReportModel.DAILY_REPORT_COLLECTION, key, specific_row_return)
        for doc in document:
            if doc:
                print(doc)
            else:
                return f'No data found'

    # Creates daily_report Collection
    def create_reports(self):
        self._latest_error = ''
        # Dropping the collection
        self._db._db.drop_collection(DailyReportModel.DAILY_REPORT_COLLECTION)
        for document in self.__find_all_weather_data():
            smallerdate = document['timestamp'].strftime('%Y-%m-%d')
            (device_id, value, date) = (
                document['device_id'], document['value'], smallerdate)
            if not self.__find({'device_id': document['device_id'], 'date': smallerdate}):
                list1 = [document['value']]
                key = {'device_id': device_id, 'value': list1, 'date': date}
                dailyreport_obj_id = self._db.insert_single_data(DailyReportModel.DAILY_REPORT_COLLECTION, key)
            else:
                myquery = {'device_id': document['device_id'], 'date': smallerdate}
                old_result = self.__find(myquery)
                list1 = (old_result['value'])
                list1.append(document['value'])
                data = {'$set': {'value': list1}}
                self._db.update_query(DailyReportModel.DAILY_REPORT_COLLECTION, myquery, data)
            for document in self.__find_all_report_data():
                min_value = min(document['value'])
                myquery = document
                data = {'$set': {'min_value': min_value}}
                self._db.update_query(DailyReportModel.DAILY_REPORT_COLLECTION, myquery, data)
                max_value = max(document['value'])
                myquery = document
                data = {'$set': {'max_value': max_value}}
                self._db.update_query(DailyReportModel.DAILY_REPORT_COLLECTION, myquery, data)  
                sum_val = sum(document['value'])
                count = 0
                for i in document['value']:
                    count = count + 1

                avg_value = round((sum_val / count), 2)
                myquery = document
                data = {'$set': {'avg_value': avg_value}}
                self._db.update_query(DailyReportModel.DAILY_REPORT_COLLECTION, myquery, data)          