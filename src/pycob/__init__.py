"""
# Services
## Store Dataframes
This works for any objects that can be pickled but the most common use case is for storing pandas dataframes.

`store_pickle`
`fetch_pickle`

## Store Dictionaries
`store_dict`
`fetch_dict`

## Secrets
`store_secret`
`fetch_secret`

## Background Jobs
You can also configure these to run on a schedule on https://www.pycob.com

`start_script`

## User Authentication
When using Pycob Cloud, there is a built in user authentication system. You can use this to store and retrieve user data.
An invisible 'token' is passed as a parameter to your app URL if a user is logged in. You can use this token to retrieve the user's data.

Your app will see URLs like this:

`https://my_app.pycob.app/page?my_param=hello&token=...`

`store_user_data`
`fetch_user_data`

## Other

`send_email`

# Deploy

`pycob.deploy`

"""
import os
import random
import string
import pickle
import requests
from pathlib import Path

from .app import *
from .request import *
from .component_interface import *
from .all_components import *

api_key = None
temp_dir = os.getcwd() + '/tmp/' + ''.join(random.choices(string.ascii_uppercase, k=5))

def send_email(from_email: str, to_email: str, subject: str, content: str) -> None:
    """
    ### Sends an email

    #### Example
    ```python
    send_email(
        from_email='user1@example.com', 
        to_email='user2@example.com', 
        subject='Hello', 
        content='Hello World!'
    )
    ```
    """
    global api_key
    if api_key is None:
        __set_api_key()

    email = {
        "from_email": from_email,
        "to_email": to_email,
        "subject": subject,
        "content": content,
    }
    __send_api_request("send_email", email, api_key)


def start_script(script_name: str, script_args: dict) -> str:
    """
    ### Starts a script with given script name and arguments

    :param script_name: Name of the script to be started
    :type script_name: str
    :param script_args: Arguments to be passed to the script
    :type script_args: dict
    :return: Returns the job ID of the started script
    :rtype: str

    #### Example
    ```python
    start_script(
        script_name='my_script.py',
        script_args={
            'arg1': 'value1',
            'arg2': 'value2'
        }
    )
    ```
    """
    global api_key
    if api_key is None:
        __set_api_key()

    script = {
        "script_name": script_name,
        "args": script_args,
    }
    rv = __send_api_request("run_job", script, api_key)

    if 'job_id' in rv:
        return rv['job_id']
    
    return ""

def store_pickle(data, filename: str):
    """
    ### Pickles a given data and stores it in the cloud with the given filename

    :param data: Data to be pickled
    :type data: any
    :param filename: Name of the file to be created and stored
    :type filename: str
    :return: None

    #### Example
    ```python
    to_cloud_pickle(
        data=[1,2,3],
        filename='my_data.pkl'
    )
    ```
    ```python
    to_cloud_pickle(
        data={'key': 'value'},
        filename='my_dict.pkl'
    )
    ```
    ```python
    to_cloud_pickle(
        data=42,
        filename='my_integer.pkl'
    )
    ```
    """
    # Turn data into a pickle with the given filename

    Path(temp_dir).mkdir(parents=True, exist_ok=True)

    file = open(temp_dir + "/" + filename, 'wb')    
    pickle.dump(data, file)
    file.close()

    url = _url_for_file_storage(filename)

    if url == "":
        print("Error: Unable to store file")
        return
    
    # Put file with Content-Type: application/octet-stream
    file = open(temp_dir + "/" + filename, 'rb')
    requests.put(url, data=file, headers={'Content-Type': 'application/octet-stream'})
    file.close()

def fetch_pickle(filename: str):
    """
    ### Loads and returns pickled data from a file in cloud storage

    :param filename: Name of the pickled file to be loaded
    :type filename: str
    :return: Returns the loaded pickled data
    :rtype: Any

    #### Example
    ```python
    data = from_cloud_pickle('my_data.pkl')
    ```
    ```python
    data = from_cloud_pickle('path/to/my_data.pkl')
    ```
    ```python
    data = from_cloud_pickle('data/my_data.pkl')
    ```
    """
    try:
        with open(temp_dir + "/" + filename, 'rb') as existing_file:
            data = pickle.load(existing_file)
            existing_file.close()
            return data
    except:
        pass

    # Get the pickle with the given filename

    url = _url_for_file_retrieval(filename)

    if url == "":
        print("Error: Unable to fetch file")
        return

    # Get file with Accept: application/octet-stream
    rv = requests.get(url, headers={'Accept': 'application/octet-stream'})
    Path(temp_dir).mkdir(parents=True, exist_ok=True)
    file = open(temp_dir + "/" + filename, 'wb')
    file.write(rv.content)
    file.close()

    file = open(temp_dir + "/" + filename, 'rb')
    data = pickle.load(file)
    file.close()

    return data


def _url_for_file_storage(file_name: str) -> str:
    global api_key
    if api_key is None:
        __set_api_key()

    file = {
        "filename": file_name,
    }
    rv = __send_api_request("store_file", file, api_key)

    if 'url' in rv:
        return rv['url']

    return ""

def _url_for_file_retrieval(file_name: str) -> str:
    global api_key
    if api_key is None:
        __set_api_key()

    file = {
        "filename": file_name,
    }
    rv = __send_api_request("fetch_file", file, api_key)

    if 'url' in rv:
        return rv['url']

    return ""

def store_dict(table_id: str, object_id: str, value: dict):
    """
    ### Stores a dictionary in the database

    :param table_id: Identifier of the table in which the object has to be stored
    :type table_id: str
    :param object_id: Identifier of the object in the table
    :type object_id: str
    :param value: Dictionary to be stored
    :type value: dict
    :return: None

    #### Example
    ```python
    store_dict(
        table_id='my_table',
        object_id='my_object',
        value={
            'key1': 'value1',
            'key2': 2,
            'key3': [1, 2, 3]
        }
    )
    ```
    """
    global api_key
    if api_key is None:
        __set_api_key()

    type_name = type(value).__name__
    print("Attempting to save a value of type = ", type_name)
    is_int = "int" in type_name
    is_float = "float" in type_name
    is_str = "str" in type_name
    is_list = "list" in type_name


    to_store = {"table_id": table_id, "object_id": object_id}

    if is_int or is_float or is_str:
        print("Saving flat value to DB")
        to_store['flat_value'] = value
    elif is_list:
        print("Saving list to DB")
        to_store['object_array'] = value
    else:
        print("Saving object to DB")
        to_store['object'] = value

    __send_api_request("store_object", to_store, api_key)

def fetch_dict(table_id: str, object_id: str) -> dict:
    """
    ### fetch a dictionary
    
    :param table_id: ID of the table to fetch the object from
    :type table_id: str
    :param object_id: ID of the object to be fetchd
    :type object_id: str
    :return: Returns the object as a dictionary
    :rtype: dict
    
    #### Example
    ```python
    data = fetch_dict(
        table_id='table_123',
        object_id='object_456'
    )
    ```
    """
    global api_key
    if api_key is None:
        __set_api_key()

    server_response = __send_api_request("fetch_object", {"object_id": object_id, "table_id": table_id}, api_key)

    if 'object' in server_response:
        return server_response['object']

def delete_dict(table_id: str, object_id: str):
    """
    ### Deletes the object with given object ID from the table with given table ID

    :param table_id: ID of the table
    :type table_id: str
    :param object_id: ID of the object to be deleted
    :type object_id: str
    :return: None
    :rtype: None

    #### Example
    ```python
    delete_dict(table_id='table_1', object_id='obj_1')
    ```
    """
    global api_key
    if api_key is None:
        __set_api_key()

    __send_api_request("delete_object", {"object_id": object_id, "table_id": table_id}, api_key)        

def query_dict(table_id: str, field_name: str, field_value) -> list:
    """
    ### Queries a table in the database and returns a list of objects matching the given field-value pair

    :param table_id: ID of the table to be queried
    :type table_id: str
    :param field_name: Name of the field to be queried
    :type field_name: str
    :param field_value: Value of the field to be queried
    :param: field_value: str or int
    :return: Returns a list of objects matching the given field-value pair
    :rtype: list of dicts

    #### Example
    ```python
    query_dict(
        table_id='my_table',
        field_name='name',
        field_value='John'
    )
    ```
    """    
    global api_key
    if api_key is None:
        __set_api_key()

    server_response = __send_api_request("query_objects", {"field_name": field_name, "table_id": table_id, "field_value": field_value}, api_key)

    if type(server_response) is list:
        arr = list(map(lambda x:  x['object'] if 'object' in x else None, server_response))
        num_items = len(arr)
        print(f"Got {num_items} items from the database table {table_id} where {field_name} == {field_value}")
        return arr

def list_objects(table_id: str) -> list:
    """
    ### Get a list of objects from a table

    This function fetchs a list of objects from a table using the provided table ID.

    :param table_id: ID of the table from which to fetch the objects
    :type table_id: str
    :return: Returns a list of objects from the specified table
    :rtype: list

    #### Example
    ```python
    list_objects(table_id='my_table')
    ```
    """
    global api_key
    if api_key is None:
        __set_api_key()

    server_response = __send_api_request("list_objects", {"table_id": table_id}, api_key)

    if type(server_response) is list:
        arr = list(map(lambda x:  x['object'] if 'object' in x else None, server_response))
        num_items = len(arr)
        print(f"Got {num_items} total items from the database table {table_id}")
        return arr

def list_object_ids(table_id: str) -> list:
    """
    ### Lists object IDs of a table

    :param table_id: ID of the table
    :type table_id: str
    :return: Returns a list of object IDs of the given table
    :rtype: list

    #### Example
    ```python
    list_object_ids(table_id='my_table')
    ```
    """
    global api_key
    if api_key is None:
        __set_api_key()

    server_response = __send_api_request("list_object_ids", {"table_id": table_id}, api_key)

    if server_response is not None and 'object_ids' in server_response:
        return server_response['object_ids']

def store_secret(secret_name: str, secret_value: str):
    """
    ### Stores a secret with given name and value

    :param secret_name: Name of the secret to be stored
    :type secret_name: str
    :param secret_value: Value of the secret to be stored
    :type secret_value: str
    :return: None
    :rtype: None

    #### Example
    ```python
    store_secret(
        secret_name='my_secret',
        secret_value='my_secret_value'
    )
    ```
    """
    store_dict("_secrets", secret_name, {"value": secret_value})

def fetch_secret(secret_name: str) -> str:
    """
    ### fetchs the value of a secret 

    :param secret_name: Name of the secret to be fetchd
    :type secret_name: str
    :return: Returns the value of the secret if it exists, otherwise None
    :rtype: str

    #### Example
    ```python
    fetch_secret("my_secret")
    ``` 
    """
    try:
        return fetch_dict("_secrets", secret_name)['value']
    except:
        return None

def get_quota_status() -> dict:
    global api_key
    if api_key is None:
        __set_api_key()

    server_response = __send_api_request("get_quota_status", {}, api_key)

    return server_response

def __set_api_key():
    global api_key
    if api_key is None:
        # Check PYCOB_API_KEY environment variable
        api_key = os.environ.get("PYCOB_API_KEY")

        if api_key is None:

            if Path("pycob_api_key.txt").is_file():
                # Check for api_key.txt file
                f = open("pycob_api_key.txt", "r")
                api_key = f.read()

            if api_key is None:
                print("No API key found. ")
                print("Go to https://www.pycob.com to get an API key.")
                # Exit
                error = 'No API key found. Go to <a href="https://www.pycob.com">https://www.pycob.com</a> to get an API key.'

def __send_api_request(endpoint: str, data: dict, api_key: str) -> dict:
    response = requests.post("https://api.pycob.com/rpc/"+endpoint, json=data, headers={"PYCOB-API-KEY": api_key})
    
    if response.status_code != 200:
        error_str = "API request failed with status code " + str(response.status_code)
        print(error_str)
        return {"error": error_str}

    try:
        json_response = response.json()
        # print("API request returned: " + str(json_response))
        # print("Class of json_response: " + str(type(json_response)))
        return json_response
    except:
        print("API request failed to return valid JSON.")
        return {"error": "API request failed to return valid JSON."}