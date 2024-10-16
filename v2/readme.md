python3 -m venv venv

source venv/bin/activate

pip install python-dotenv
pip install requests

pip freeze > requirements.txt
