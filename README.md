# Document Event Extractor

This agentintic application allows user to add events to their Google Calendar from Google Docs and Google Sheets. App can extract information specified by user, add events to spefic calendar, extract from needed Google Sheets lists.

## Installation and Setup

**Prerequisites:**
*   Python 3.7+ installed.
*   A Google Account.

**Step 1: Get the Code & Set Up Environment**

    pip install -r requirements.txt

**Step 2: Configure Your Google Cloud APIs**

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a **new project**.
2.  **Enable APIs:** Go to **APIs & Services > Library**. Search for and **Enable** these three APIs:
    *   Google Docs API
    *   Google Sheets API
    *   Google Calendar API
3.  **Configure Consent Screen:** Go to **APIs & Services > OAuth consent screen**.
    *   Choose **External** and click **Create**.
    *   App name: `AI Event Scheduler` (or anything you like).
    *   User support email: Select your email.
    *   Developer contact information: Enter your email.
    *   Click **Save and Continue** through the "Scopes" page.
    *   **Add Test User:** On the "Test users" page, click **Add Users** and enter your own Google email address. This is critical for allowing the app to run.
4.  **Create Credentials:** Go to **APIs & Services > Credentials**.
    *   Click **+ Create Credentials > OAuth client ID**.
    *   Application type: **Desktop app**.
    *   Click **Create**. A pop-up will appear. Click **Download JSON**.
    *   **Rename the downloaded file to `credentials.json` and place it directly inside your project folder.**

**Step 3: Get Your Gemini API Key**
1.  Go to [Google AI Studio](https://aistudio.google.com/).
2.  Click **Get API key > Create API key in new project**.
3.  Copy the generated key.

**Step 4: Create Your `.env` Secrets File**
1.  In the project folder, find the `example.env` file.
2.  Make a copy of it and rename the copy to `.env`.
3.  Open the new `.env` file and paste your Gemini API key into it.
    ```
    GOOGLE_API_KEY="paste_your_key_here"
    ```

**Important note:**

Environment variable for Gemini should be strictly GOOGLE_API_KEY (not GEMINI_API_KEY, AI_API_KEY etc.)


**Step 5: Install the Google Cloud CLI (`gcloud`)**

*   Follow the official installation instructions: [Google Cloud CLI Installation Guide](https://cloud.google.com/sdk/docs/install)

After installation, close and reopen your terminal, or run `gcloud init` to ensure it's configured.

**Step 6: Log in and Create the Default Credentials**

1.  Make sure you are in your project directory and your virtual environment is activated.
2.  Run the following command in your terminal:

    ```bash
    gcloud auth application-default login
    ```

    *   Your web browser will open to a Google login page.
    *   Log in with the **same Google account** you used to create your Google Cloud project and enable the APIs.
    *   You will be asked to grant permissions to the "Google Cloud SDK". Click **Allow**.
    *   You'll see a confirmation page, and your terminal will show "Credentials saved!".

This command creates a JSON file with your authentication info in a hidden folder on your computer (e.g., `~/.config/gcloud/application_default_credentials.json` on Linux/macOS).