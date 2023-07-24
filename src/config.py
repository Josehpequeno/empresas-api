import os
from dotenv import load_dotenv
load_dotenv() 

SECRET_KEY = os.environ.get("SECRET")
DEBUG = os.environ.get("DEBUG")
