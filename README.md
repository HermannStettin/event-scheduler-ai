### What Your Friend Should Do (Their Setup Guide)

Here is a complete, step-by-step guide you can send to your friend.

---

### **Guide: How to Set Up the AI Event Scheduler**

Follow these steps to get the project running on your machine.

**Prerequisites:**
*   Python 3.7+ installed.
*   A Google Account.

**Step 1: Get the Code & Set Up Environment**
1.  Unzip the project folder you received (or clone it from GitHub).
2.  Open a terminal or command prompt and navigate into the project directory.
3.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
4.  **Activate the environment:**
    *   On Windows: `venv\Scripts\activate`
    *   On macOS/Linux: `source venv/bin/activate`
5.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

**Step 2: Configure Your Google Cloud APIs**
This is the most detailed step. You need to tell Google that your application is allowed to access your data.

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
    GEMINI_API_KEY="paste_your_key_here"
    ```

**Step 5: Run the Application!**
1.  **First Run (Authentication):** The very first time you run the script, a browser window will open asking you to log in to Google and grant permission. This is normal. Log in with the same account you added as a "Test User". A `token.json` file will be created automatically.
2.  **Get a Doc/Sheet ID:** Create a test Google Doc or Sheet with some event text and copy its ID from the URL.
3.  **Run from your terminal:**
    ```bash
    # For a Google Doc
    python main.py --doc-id "the-id-of-your-doc"

    # For a Google Sheet
    python main.py --sheet-id "the-id-of-your-sheet"
    ```

---