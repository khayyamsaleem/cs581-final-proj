from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(),override=True)

API_TOKEN = os.getenv("GROUPME_ACCESS_TOKEN")

