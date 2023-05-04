from model import UserModel, DeviceModel, WeatherDataModel, DailyReportModel
import datetime


# Shows how to initiate and search in the users collection based on a username
user_coll = UserModel()
device_coll = DeviceModel() 
wdata_coll = WeatherDataModel()
daily_report_model = DailyReportModel()

#Dropping user_1 and user_2
user_coll.drop_document('user_1')
user_coll.drop_document('user_2')
#inserting two values for testing
user_doc = user_coll.insert('user_1', 'user_1@example.com', 'default', [{'dev_id': 'DT001', 'access_type': 'r'}, {'dev_id': 'DH001', 'access_type': 'rw'}])
user_doc = user_coll.insert('user_2', 'user_2@example.com', 'default', [{'dev_id': 'DT002', 'access_type': 'r'}, {'dev_id': 'DH003', 'access_type': 'r'}])

# Control Access Validataion for admin/default
username = 'admin'
print(f'Does {username} have read/write access ?')
print(user_coll.has_admin_access(username), end='\n\n')

#Varifying Admin -- User Read Access
print(f'Is find by username allowed for {username}?')
if user_coll.has_admin_access(username):
    user_doc = user_coll.find_by_username('user_2')
    if(user_doc == -1):
        print(user_coll.latest_error, end='\n\n')
    else:
        print(user_doc, end='\n\n')
else:
    print("Permission denied!\n")

# Varifying Admin -- User Insert Access
print(f"Can {username} add a new user?")
if user_coll.has_admin_access(username):
    user_doc = user_coll.insert('user_3', 'user_3@example.com', 'default', [{'dev_id': 'DT004', 'access_type': 'r'}, {'dev_id': 'DH004', 'access_type': 'rw'}])
    if(user_doc == -1):
        print(user_coll.latest_error, end='\n\n')
    else:
        print(user_doc, end='\n\n')
else: 
    print("Permission denied!\n")

#Varifying Admin --- Device Read Access
print(f"Can {username} access device DT004?")
if user_coll.has_admin_access(username):
    device_doc = device_coll.find_by_device_id('DT004')
    if (device_doc == -1):
        print(device_coll.latest_error, end='\n\n')
    else:
        print(device_doc, end='\n\n')
else:
    print("Permission denied!\n")
    
    
# Varifying Admin --- Device Write Access
print(f"Can {username} create device DT201?")
if user_coll.has_admin_access(username):
    device_doc = device_coll.insert('DT201', 'Temperature Sensor', 'Temperature', 'Acme')
    if (device_doc == -1):
        print(device_coll.latest_error, end='\n\n')
    else:
        print(device_doc, end='\n\n')
else:
    print("Permission denied!\n")
    
# Varifying Admin --- Device Data Access
print(f"Can {username} read DT001 device data?")
if user_coll.has_admin_access(username):
    wdata_doc = wdata_coll.find_by_device_id_and_timestamp('DT001', datetime.datetime(2020, 12, 2, 13, 30, 0))
    if (wdata_doc == -1):
        print(device_coll.latest_error, end='\n\n')
    else:
        print(wdata_doc, end='\n\n')
else:
    print("Permission denied!\n")

# admin access path from Problem 2
print("Daily Report - \n\n")
daily_report_model.create_reports()
print("Daily reports for one day")
daily_report = daily_report_model.find_by_device_id_and_date('DT004', datetime.datetime(2020, 12, 2))
print(daily_report, end='\n\n')
print("Daily report for multiple days")
daily_reports = daily_report_model.find_by_device_id_and_range('DT004', datetime.datetime(2020, 12, 2), datetime.datetime(2020, 12, 4))
print('\n\n')

# default (user_1) access path for problem 1
user_coll = UserModel()
device_coll = DeviceModel()
wdata_coll = WeatherDataModel()
username = 'user_1'
    
# Control Access Validation  -- admin/default
print(f"Does {username} have admin access ?")
print(user_coll.has_admin_access(username), end='\n\n')

# Varifying Default --- User Read Access
print(f"Is find by username allowed for {username}?")
if user_coll.has_admin_access(username):
    user_doc = user_coll.find_by_username('user_2')
    if (user_doc == -1):
        print(user_coll.latest_error, end='\n\n')
    else:
        print(user_doc, end='\n\n')
else:
    print("Permission denied!\n")
    
# Varifying Default --- User insert Access
print(f"Can {username} add a new user?")
if user_coll.has_admin_access(username):
    user_doc = user_coll.insert('user_3', 'user_3@example.com', 'default', [{'dev_id': 'DT004', 'access_type': 'r'}, {'dev_id': 'DH004','access_type': 'rw'}])
    if (user_doc == -1):
        print(user_coll.latest_error, end='\n\n')
    else:
        print(user_doc, end='\n\n')
else:
    print("Permission denied!\n")

# Varifying Default --- Device Read Access
print(f"Can {username} access device DT004?")
device_id = 'DT004'
user_doc = user_coll.has_device_access(username, device_id)
if user_doc == False:
    print(f"No Read access to {device_id}\n\n")
else:
    for doc in user_doc['access_list']:
        if doc['access_type'] in ('r'):
            device_doc = device_coll.find_by_device_id(device_id)
            if (device_doc == -1):
                print(user_coll.latest_error, end='\n\n')
            else:
                print(device_doc, end='\n\n')

# Varifying Default --- User Read Access
print(f"Can {username} access device DT001?")
device_id = 'DT001'
user_doc = user_coll.has_device_access(username, device_id)
if user_doc == False:
    print(f"No Read access to {device_id}\n\n")
else:
    for doc in user_doc['access_list']:
        if doc['access_type'] in ('r'):
            device_doc = device_coll.find_by_device_id(device_id)
            if (device_doc == -1):
                print(user_coll.latest_error, end='\n\n')
            else:
                print(device_doc, end='\n\n')

# Varifying Default --- User insert Access
print(f"Can {username} create device DT202?")
device_id = 'DT202'
user_doc = user_coll.has_device_access(username, device_id)
if user_doc == False:
    print("Permission denied!\n\n")
else:
    for doc in user_doc['access_list']:
        if doc['access_type'] in ('rw'):
            device_doc = device_coll.insert('DT202', 'Temperature Sensor', 'Temperature', 'Acme')
            if (user_doc == -1):
                print("Permission denied!")
            else:
                print(user_doc, end='\n\n')

# Varifying Default --- Device Data Read Access
print(f"Can {username} read DT001 device data ?")
device_id = 'DT001'
user_doc = user_coll.has_device_access(username, device_id)
if user_doc == False:
    print("Permission denied!\n\n")
else:
    for doc in user_doc['access_list']:
        if doc['access_type'] in ('r', 'rw'):
            wdata_doc = wdata_coll.find_by_device_id_and_timestamp(device_id, datetime.datetime(2020, 12, 2, 13, 30, 0))
            if (wdata_doc == -1):
                print(wdata_coll.latest_error, end='\n\n')
            else:
                print(wdata_doc, end='\n\n')
                break

# Varifying Default --- Device Data Read Access
print(f"Can {username} read DT002 device data ?")
device_id = 'DT002'
user_doc = user_coll.has_device_access(username, device_id)
if user_doc == False:
    print(f"No Read access to {device_id} \n\n")
else:
    for doc in user_doc['access_list']:
        if doc['access_type'] in ('r', 'rw'):
            wdata_doc = wdata_coll.find_by_device_id_and_timestamp(device_id, datetime.datetime(2020, 12, 2, 13, 30, 0))
            if (wdata_doc == -1):
                print(wdata_coll.latest_error, end='\n\n')
            else:
                print(wdata_doc, end='\n\n')
                break
