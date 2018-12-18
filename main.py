import os
from dotenv import load_dotenv, find_dotenv
from groupy.client import Client

load_dotenv(find_dotenv(),override=True)

API_TOKEN = os.getenv("GROUPME_ACCESS_TOKEN")

client = Client.from_token(API_TOKEN)

def test():
    for g in client.groups.list():
        print(g.name)

if __name__ == '__main__':
    test()
