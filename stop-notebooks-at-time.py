from datetime import datetime
import getopt, sys
import urllib3
import boto3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def is_time_to_shutdown():
    now = datetime.now().time()
    if (now.hour == 13 and now.minute > 30):
        print("It's over 23:00, time to shutdown the notebooks instance")
        return True
    else:
        print("It's not over 23:00, not time to shutdown the notebook instance")
        return False


def get_notebook_name():
    log_path = '/opt/ml/metadata/resource-metadata.json'
    with open(log_path, 'r') as logs:
        _logs = json.load(logs)
    return _logs['ResourceName']

if (is_time_to_shutdown()==True):
    print('Closing idle notebook')
    client = boto3.client('sagemaker')
    client.stop_notebook_instance(
        NotebookInstanceName=get_notebook_name()
    )
else:
    print('Not time to shutdown the notebook instance. Pass.')
