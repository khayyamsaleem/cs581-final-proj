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
import operator

load_dotenv(find_dotenv(),override=True)
API_TOKEN = os.getenv("GROUPME_ACCESS_TOKEN")

client = Client.from_token(API_TOKEN)
all_groups = list(client.groups.list_all())

def get_group_matrix():
    return list(itertools.product(all_groups, all_groups))

def member_intersections():
    return {(x.name,y.name):set(map(lambda z: z.user_id, x.members)).intersection(map(lambda z: z.user_id, y.members)) for (x,y) in get_group_matrix()}

def get_df_of_counts():
    groupnames = [x.name for x in all_groups]
    df = pd.DataFrame(np.zeros((len(all_groups), len(all_groups))), index=groupnames, columns=groupnames)
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

def get_name_by_id(pid):
    for group in all_groups:
        for member in group.members:
            if(member.user_id==pid):
                return member.nickname

def rebuild_graph_w_names(g):
    G = nx.Graph()
    for node in list(g.nodes):
        G.add_node(get_name_by_id(node))
    for edge in list(g.edges):
        G.add_edge(get_name_by_id(edge[0]), get_name_by_id(edge[1]))

    return G

def build_social_network():
    G = nx.Graph()

    for group in all_groups:
        for member in group.members:
            G.add_node(member.user_id)

    for group in all_groups:
        for pair in itertools.combinations(group.members, 2):
            G.add_edge(pair[0].user_id, pair[1].user_id)

    return G

def visualize_groups(names=False):
    G = build_social_network()

    if(names):
        G = rebuild_graph_w_names(G)

    fig = plt.figure(1, figsize=(128,128))
    ax = plt.subplot(111)
    nx.draw_networkx(G, ax=ax, font_color='green')
    plt.savefig('./artifacts/social_network.png')

def rate_friends():
    # Morally wrong to run this function
    g = build_social_network()
    centers = nx.algorithms.centrality.degree_centrality(g)
    sorted_friends = sorted(centers.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_friends

if __name__ == '__main__':
    heatmap(get_df_of_counts(), "./artifacts/heatmap.png")
    visualize_groups(names=False)
    pprint(rate_friends())
