1. Open the Google Cloud Console
2. Enable the API
3. Create API Credentials (If Not Done Already)
- Go to Google Cloud Credentials
- Click "Create Credentials" --> "Service Account".
- Fill in the details (name, description).
- Assign the "Editor" role (or "Owner" if you need full access).
- Click "Create Key" --> Select JSON --> Download the JSON file.
- Move the downloaded file (.json) to your Python project directory.
4. Share the Google Sheet with Your Service Account
- Open your Google Sheet.
- Click Share.
- Add the email from your service account JSON key (it looks like something@project-id.iam.gserviceaccount.com).
- Give Editor access.
5. Add your Sheet name and JSON key to the code in the 10th and 11th lines
