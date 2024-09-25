# Feedback Analysis Using Streamlit

## Description
This program is designed to help you understand customer feedback received from the RTS chatbot by visualizing various graphs and charts. If the application is already deployed, you can simply upload your document to start receiving insights. If the program has not been deployed and you need to set it up on your local system, please follow the instructions below.

---

## Instructions

In this repository, there are two important files (excluding `.gitignore` and this `README.md`), which are:

1. `requirements.txt`
2. `main.py`

### 1. `requirements.txt`
This text file contains the necessary Python libraries that need to be installed in the virtual environment.

#### Setting Up the Virtual Environment
To create a virtual environment in Windows, follow these steps:

1. Open the command prompt and run the following command:
    ```bash
    python -m venv venv
    ```

2. After creating the virtual environment, activate it with this command:
    ```bash
    venv\Scripts\activate.bat
    ```

3. Once the virtual environment is activated, the terminal prompt will change to indicate that the environment is active (`(venv)`).

4. Now, install the required Python libraries by running the following command:
    ```bash
    pip install -r requirements.txt
    ```

#### Notes:
- Ensure that Python is installed and added to your system’s PATH before running the above commands.
- If you're using another operating system (macOS/Linux), the commands for activating the virtual environment will differ:
    - macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

### 2. `main.py`
Once the virtual environment is set up and the required libraries are installed, you can start the Streamlit server.

To start the server, run the following command in the command prompt (or your preferred terminal/IDE):
```bash
streamlit run main.py
```

Once the server starts, it will automatically open your default web browser where you can interact with the app and upload your CSV file for analysis.

### Contributors
Jagadeesh Akkineni
