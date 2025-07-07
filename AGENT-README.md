### Set Up Application Default Credentials

**Important note:**

Environment variable for Gemini should be strictly GOOGLE_API_KEY (not GEMINI_API_KEY, AI_API_KEY etc.)

**Step 1: Install the Google Cloud CLI (`gcloud`)**

*   Follow the official installation instructions: [Google Cloud CLI Installation Guide](https://cloud.google.com/sdk/docs/install)

After installation, close and reopen your terminal, or run `gcloud init` to ensure it's configured.

**Step 2: Log in and Create the Default Credentials**

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