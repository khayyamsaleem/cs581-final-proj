import os
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv, find_dotenv
from groupy.client import Client
from pprint import pprint
import itertools
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

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
    ax.set_title("Heatmap of Common Friends")
    sns.heatmap(df, ax=ax)
    plt.savefig(savename)
    plt.close(fig)

def visualize_groups():
    G = nx.Graph()
    groups = list(client.groups.list_all())

    for group in groups:
        for member in group.members:
            G.add_node(member.user_id)

    for group in groups:
        for pair in itertools.combinations(group.members, 2):
            G.add_edge(pair[0].user_id, pair[1].user_id)

    fig = plt.figure(1, figsize=(128,128))
    ax = plt.subplot(111)
    nx.draw_networkx(G, ax=ax)
    plt.savefig('social_network.png')


def test():
    groups = {}
    for g in client.groups.list_all():
        groups[g.name]=list(map(lambda m: m.user_id, g.members))
    pprint(groups.keys())

if __name__ == '__main__':
    heatmap(get_df_of_counts(), "heatmap.png")
    visualize_groups()
