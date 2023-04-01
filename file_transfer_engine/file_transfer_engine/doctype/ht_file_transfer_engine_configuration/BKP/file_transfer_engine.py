import paramiko
import os
import json
import urllib.request
import requests
import sys
from stat import S_ISDIR, S_ISREG
import shutil
from pathlib import Path
from datetime import datetime

print('Current Time is : '+ datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
print('Engine ID is : '+ sys.argv[1])

# Frappe login credentials
login_input = {
    'usr': 'david.alexander@hephzibahtech.com',
    'pwd': 'temporarY@123'
}

# Send POST request to login endpoint
response = requests.post('http://35.244.11.110:8000/api/method/login', data = login_input)

# Check if login was successful
if response.status_code == 200 and response.json().get('message') == 'Logged In':
    print('Login successful')
    session_cookie = response.headers.get('Set-Cookie')
    session_id = response.cookies.get('sid')
else:
    print('Login failed')

# Set up the API endpoint URL to fetch engine scheduler output
api_url = 'http://35.244.11.110:8000/api/method/file_transfer_engine.file_transfer_engine.doctype.ht_file_transfer_engine_configuration.api.fetchJobConfig?engineID='+ sys.argv[1]

# Set up the request headers, including your API key
headers = {
	'Authorization':'3d50e221ae7b8a6',        # '7ac7e268d21122b'69a48e8dc07fff8
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Cookie': 'sid={}'.format(session_id)
}

# Send the GET request to the API endpoint
response = requests.get(api_url, headers = headers)

source_file_transfer_mode = ''
source_ip_address = ''
source_username = ''
source_password = ''
source_file_path = ''
destination_file_transfer_mode = ''
destination_api_url = ''
destination_port = ''
destination_api_token = ''
destination_username = ''
destination_password = ''
destination_folder = ''

# If the request was successful (status code 200), extract the data
if response.status_code == 200:
    data = response.json()
    #print('data is : '+ str(data['message']))
    #for key in data['message']:
    #    print(key)
    #    print(data['message'][key])
    source_file_transfer_mode = data['message']['source_file_transfer_type']
    source_ip_address = data['message']['source_hostname_or_ip_address']
    source_username = data['message']['source_username']
    source_password = data['message']['source_password']
    source_file_path = data['message']['source_folder']
    destination_file_transfer_mode = data['message']['destination_file_transfer_type']
    destination_api_url = data['message']['destination_api_url']
    destination_port = data['message']['destination_port']
    destination_api_token = data['message']['destination_api_token']
    destination_username = data['message']['destination_username']
    destination_password = data['message']['destination_password']
    destination_folder = data['message']['destination_folder']

else:
    print('Engine Information fetch Failure. HTTP Error Code is : '+ str(response.status_code))

temp_filepath = '/home/frappe-alex/FILES/'+ source_ip_address + source_username
isExist = os.path.exists(temp_filepath)
if not isExist:
    os.mkdir(temp_filepath)

print('Received required inputs from File Transfer System')
print('Job Started')
print('Connecting to Source System')

if source_file_transfer_mode == 'SFTP':
    # Create an SSH client object
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the instance using the provided credentials
    ssh.connect(hostname = source_ip_address, username = source_username, password = source_password)

    # Create an SFTP client object
    sftp = ssh.open_sftp()

    try:
        sftp.chdir(source_file_path + '/PROCESSED')  # Test if remote_path exists
    except IOError:
        sftp.mkdir(source_file_path + '/PROCESSED')  # Create remote_path

    # Download the file
    for file in sftp.listdir_attr(source_file_path):
        if S_ISREG(file.st_mode):
            sftp.get(source_file_path +'/'+ file.filename, temp_filepath + '/'+ file.filename)
    
    for file in sftp.listdir_attr(source_file_path):
        if S_ISREG(file.st_mode):
            sftp.rename(source_file_path +'/'+ file.filename, source_file_path + '/PROCESSED/' + file.filename)
 
    sftp.close()
    ssh.close()

print('File received from Source System and transferred original file within Source system to newly created parallel PROCESSED folder')
print('Source system connection closed')
print('Connecting to Destination System')

if destination_file_transfer_mode == 'HTTPS':

    for file in os.listdir(temp_filepath):
        path = Path(temp_filepath +'/'+ file)
        if path.is_file():
            #Find Site ID from File
            subFolderID = file[3:6]
            print('File is : '+ file)
            print('Site ID is : '+ subFolderID)

            #Validate Site ID to proceed further
            if subFolderID.isnumeric() != True: 
                print('Site ID is not valid. Please check. Calculated site ID from file name is : '+ subFolderID)
                break 
            else:
                api_url = "https://{0}/public/api/v1/docs/topics/{1}/files".format(destination_api_url, destination_folder)
                #api_url = "https://{0}/{1}/files".format(destination_api_url, destination_folder)

            print('Destination API URL is '+ api_url)

            # generate file label
            my_file_label, my_file_ext = os.path.splitext(file)

            login_parameters = { 'next': '/core/home' }
            file_obj = { 'source_file': open(temp_filepath + '/'+ file,'rb') }

            try:
                loginResponse = requests.get('https://'+ destination_api_url +'/accounts/login/?next=/core/home', data = login_parameters)
                csrftoken = loginResponse.cookies.get('csrftoken')

            except Exception as e:
                raise Exception (e)

            headers = {
                'Authorization': "Token {}".format(destination_api_token),
                'cookie': 'csrftoken='+ csrftoken,
                'referer': 'https://'+ destination_api_url +'/document_repository/t/'+ destination_folder,
                'X-CSRFToken': csrftoken
            }
    
            parameters = {
                'topic_code': destination_folder,
                'site_code': subFolderID,
                'label': my_file_label
            }

            transferStatus = ''
            transferFailureReason = ''
            try:
                uploadResponse = requests.post(api_url, files = file_obj, data = parameters, headers = headers)
                print('Response content is : '+ str(uploadResponse.content))
                print('Upload File Successfully')
                transferStatus = 'SUCCESS'

                # get cookies from response
                #cookies = response.cookies
                #print(cookies)
                # get specific cookie by name
                #csrftoken = cookies.get('csrftoken')
                #sessionid = cookies.get('sessionid')
                # print cookie value
                #print(csrftoken)
                #print(sessionid)
            except Exception as e:
                raise Exception (e)
                transferStatus = 'FAILURE'
                transferFailureReason = str(e)

            #if (source_ip_address == 'localhost'):
            #    isExist = os.path.exists(temp_filepath +'/PROCESSED')
            #    if not isExist:
            #        os.mkdir(temp_filepath +'/PROCESSED')
            #    shutil.move(source_file_path +'/'+ file, temp_filepath +'/PROCESSED/'+ file)
            file_size = os.path.getsize(temp_filepath +'/'+ file)
            os.remove(temp_filepath +'/'+ file)
            
            # Set up the API endpoint URL to fetch engine scheduler output
            api_url = 'http://35.244.11.110:8000/api/method/file_transfer_engine.file_transfer_engine.doctype.ht_file_transfer_results.api.updateReport?engineID='+ sys.argv[1] +'&filename='+ file +'&status='+ transferStatus +'&fileSize='+ str(file_size) +'&failureReason='+ transferFailureReason + '&sourceFolder='+ source_file_path +'&destinationFolder='+ "https://{0}/public/api/v1/docs/topics/{1}/files/{2}".format(destination_api_url, destination_folder, subFolderID)

            # Set up the request headers, including your API key
            headers = {
                'Authorization':'3d50e221ae7b8a6',        # '7ac7e268d21122b'
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Cookie': 'sid={}'.format(session_id)
            }

            # Send the GET request to the API endpoint
            response = requests.get(api_url, headers = headers)

        else:
            print('This is a Folder. Not a file. Folder Name is : '+ str(path))

    print('Destination system connection closed')
    print('Job Ended')

