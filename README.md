# py-pdf-chat

FTO - First time only
## Setup:

1. Install poetry if not already installed: `pipx install poetry`
1. [FTO] Create a new project with poetry: `poetry new py-pdf-chat`
1. [FTO] cd into the newly created project: `cd py-pdf-chat`
1. [FTO] Test everything is working fine:

   - Create a file in root: `touch main.py`
   - Write some print statement: `print("Hello")`
   - Run file using poetry: `poetry run python main.py`

1. Activate the environment in terminal with: `poetry shell`
1. Activate the environtemt for vscode:

   - `cmd + shift + p` to open the command pallete.
   - Search for `select interpreter`
   - Provide the path of poetry venv for the current project (copy from terminal).

1. To deactivate the environment use command: `deactivate`.
1. [FTO] To add any dependency/package (say fastapi) use command: `poetry add fastapi` similarly for following:

   - streamlit
   - google-generativeai
   - python-dotenv
   - langchain
   - PyPDF2
   - faiss-cpu
   - > [!CAUTION]
     > Due to some issue with poetry not able to install mentioned, download `langchain-google-genai = "^0.0.9"` manually with pip seperately.

1. Create 2 env files: `.env` and `.env.example` enter `GOOGLE_API_KEY`.

1. In order to run the py files use: `poetry run python app.py`

1. To run the project: `streamlit run app/app.py`
