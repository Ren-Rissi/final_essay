import networkx as nx
import random as rd
import numpy as np
import plotly.express as px

# Set the seed for randomness reproducibility 
seed = 42
rd.seed(seed)

# Fix the number of nodes for each network
n = 500 #500

# given N, fix p
p = 4/(n-1)

# set a number of nodes to be excluded per iteration batch
n_ex = 10

# set a number of re-runs on each network
n_rep = 10 #10

# set a number of different initial networks
n_ntk = 10 #10

# start a list to save each initial netwotk results
gc_max_net = []
ef_net = []

# generate each one of the networks and iterate over them
for i in range(n_ntk):

    # get a network to start
    G = nx.gnp_random_graph(n, p)

    # start a list to store measurements re-runs of a single network
    gc_sn = []
    ef_sn = []

    # iterate over the same initial network
    for j in range(n_rep):

        # get a copy to iterate on
        H = G.copy()

        # start the list of measurement values
        gc = []
        gf = []

        # get initial measurements
        gc.append(max([len(l) for l in nx.connected_components(H)]))
        gf.append(nx.global_efficiency(H))

        # start the attacks iterations until the graph vanishes
        for k in range(1, (n//n_ex)):
            picked_nodes = rd.sample(sorted(H.nodes()), 10)
            H.remove_nodes_from(picked_nodes)

            # recalculate and save the measurements after the atatck batch
            gc.append(max([len(l) for l in nx.connected_components(H)], default=0))
            gf.append(nx.global_efficiency(H))
        
        # Save the last run of this network
        gc_sn.append(gc)
        ef_sn.append(gf)

    # Save each different network results
    gc_max_net.append(gc_sn)
    ef_net.append(ef_sn)

# flatten to make it easier to work with
df_gc = np.array([x for l in gc_max_net for x in l])
df_gf = np.array([x for l in ef_net for x in l])

# transpose because we are interested on the behavior after each attack batch
df_gc = df_gc.transpose()
df_gf = df_gf.transpose()

# start list of final data to be ploted
mean_gc = []
mean_gf = []
sd_gc = []
sd_gf = []

# collect mean and sd for each line
for i in range(n//n_ex):
    mean_gc.append(np.mean(df_gc[i,:]))
    mean_gf.append(np.mean(df_gf[i,:]))
    sd_gc.append(np.std(df_gc[i,:]))
    sd_gf.append(np.std(df_gf[i,:]))



# plot the figures
x = range(0, n, n_ex)

# remaining nodes
rem = range(n-n_ex, -1, -n_ex)

fig = px.scatter(x=x, y=mean_gc, error_y=sd_gc,
                 labels={'x':'Number of nodes removed', 'y':'Mean'},
                 title='Greatest Component Size')
fig.add_scatter(np.array([x, rem]), x='', y='') # need to add line
fig.show()

fig = px.scatter(x=x, y=mean_gf, error_y=sd_gf,
                 labels={'x':'Number of nodes removed', 'y':'Mean'},
                 title='Efficiency')

fig.show()
