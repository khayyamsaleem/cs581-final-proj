import os
from dotenv import load_dotenv, find_dotenv
from groupy.client import Client
from pprint import pprint
import itertools
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

load_dotenv(find_dotenv(),override=True)
API_TOKEN = os.getenv("GROUPME_ACCESS_TOKEN")

client = Client.from_token(API_TOKEN)

def get_group_matrix():
    groups = list(client.groups.list_all())
    return list(itertools.product(groups, groups))

def member_intersections():
    return {(x.name,y.name):set(map(lambda z: z.user_id, x.members)).intersection(map(lambda z: z.user_id, y.members)) for (x,y) in get_group_matrix()}

def get_df_of_counts():
    groups = list(client.groups.list_all())
    groupnames = [x.name for x in groups]
    df = pd.DataFrame(np.zeros((len(groups), len(groups))), index=groupnames, columns=groupnames)
    m_i = member_intersections()
    for (x,y) in m_i:
        df.loc[x,y] = len(m_i[(x,y)]) if not x == y else -1
    return df

def heatmap(df, savename):
    fig = plt.figure(1, figsize=(20,20))
    ax = plt.subplot(111)
    sns.heatmap(df, ax=ax)
    plt.savefig(savename)
    plt.close(fig)


def test():
    groups = {}
    for g in client.groups.list_all():
        groups[g.name]=list(map(lambda m: m.user_id, g.members))
    pprint(groups.keys())

if __name__ == '__main__':
    print(get_df_of_counts())
