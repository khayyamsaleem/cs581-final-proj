import os
from dotenv import load_dotenv, find_dotenv
from groupy.client import Client
from pprint import pprint

load_dotenv(find_dotenv(),override=True)

API_TOKEN = os.getenv("GROUPME_ACCESS_TOKEN")

client = Client.from_token(API_TOKEN)


def test():
    groups = {}
    for g in client.groups.list_all():
        groups[g.name]=list(map(lambda m: m.user_id, g.members))
    pprint(groups)

if __name__ == '__main__':
    test()
