# unbiased-request
Repository accompanying the paper:

Malagon J, Haelermans C. _Reading between the lines: biases and reproducibility challenges in efficiency of education reviews. 2023_

### Instructions
1. On Python 3.11 install the requirements:

    `pip install -r requirements.txt`

    _Note:_ Windows users may experience issues because Windows still uses legacy encodings for the system encoding (the ANSI Code Page). This may cause issues because UTF-8 is widely used on the internet and most Unix systems, including WSL (Windows Subsystem for Linux).
    
    If you find encoding problems, you can use the Python UTF-8 Mode to change the default text encoding to UTF-8 by running in the command prompt:
    
    `set PYTHONUTF8=1`

    (More info at Using Python on Windows https://docs.python.org/3/using/windows.html)


2. Request your Elsevier API key at https://dev.elsevier.com/apikey/manage

    (See also:

    Elsevier Developer Portal API Authentication docs https://dev.elsevier.com/tecdoc_api_authentication.html
    
    API Interface Specification https://dev.elsevier.com/documentation/AuthenticationAPI)

3. Create a `config.json` file with your API key with contents
    ```
    {
        "apikey": "your_api_key_goes_here"
    }
    ```
4. Store your `config.json` file at the `/scopus/` folder
5. Open `env_variables.py` and change `project_dir` to your current project directory
6. Open a terminal and run

    `streamlit run unbiased_requester.py`
