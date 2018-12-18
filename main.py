import os
from dotenv import load_dotenv, find_dotenv
from groupy.client import Client
from pprint import pprint
import itertools

load_dotenv(find_dotenv(),override=True)
API_TOKEN = os.getenv("GROUPME_ACCESS_TOKEN")

client = Client.from_token(API_TOKEN)

def get_group_matrix():
    groups = list(client.groups.list_all())
    return list(itertools.product(groups, groups))

def count_members():
    return {(x.name,y.name):set(map(lambda z: z.user_id, x.members)).intersection(map(lambda z: z.user_id, y.members)) for (x,y) in get_group_matrix()}

def test():
    groups = {}
    for g in client.groups.list_all():
        groups[g.name]=list(map(lambda m: m.user_id, g.members))
    pprint(groups.keys())

if __name__ == '__main__':
    pprint(count_members())
