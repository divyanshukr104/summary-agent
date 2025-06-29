To run this tool in your local machine, clone the repository and setup in your machine locally.

This tool uses openai's gpt-4o model and requires you to have credits in your openai account when using it to perform queries.
Create a .env file in the root of your project directory, and add the OPENAI_API_KEY to it.

Once you have imported the repo in your machine, open terminal/command prompt/bash and perform the following commands:

python -m venv .venv
.venv\Scripts\activate
pip install strands-agents strands-agents-tools
pip install python-dotenv
cd .\summary_agent\
pip install 'strands-agents[openai]'
python main.py "<path_to_your_pdf_file>" 
