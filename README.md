
Install [gcloudcli](https://cloud.google.com/sdk/docs/install)


pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib google-cloud-texttospeech


1. Set up Google Cloud Project and Enable the Google Sheets API:

* Go to the Google Cloud Console.
* Create a new project or select an existing one.
* Enable the Google Sheets API. You can do this by searching for "Google Sheets API" in the API Library and clicking "Enable".  

2. Create Credentials (Service Account Recommended):

* For accessing Google Sheets programmatically, using a Service Account is generally the most secure and manageable approach.
* In your Google Cloud Project, navigate to "IAM & Admin" -> "Service accounts".
* Click "Create service account".
* Give your service account a name and description.
* Grant the service account the "Editor" role (or a more specific role if you prefer to limit permissions).
* Click "Done".
* Now, click on the newly created service account.
* Go to the "Keys" tab.
* Click "Add Key" and choose "JSON" as the key type.
* Click "Create". This will download a JSON file containing your service account credentials. Keep this file secure!
