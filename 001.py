import networkx as nx
import random as rd
import numpy as np
# import matplotlib.pyplot as plt
import plotly.express as px

# Set the seed for randomness reproducibility 
seed = 42
rd.seed(seed)

# Fix the quantity of different p
n_p = 100
# Fix the number of cases for each p
n_cases = 15
# Fix the number of nodes for each network
n = 500

# Get different values for p, between 0 and 1
p = list()
for i in range(n_p):
    p.append(rd.random()/100)


# Generate the networks for each value of p
graphs = list()
for i in range(n_p):
    graphs.append(list())
    for j in range(n_cases):
        graphs[i].append(nx.gnp_random_graph(n, p[i]))
   


# Measure the largest component and the efficiency of each network
gc_measurement = []
ef_measurement = []
for i in range(n_p):
    gc_measurement.append(list())
    ef_measurement.append(list())
    for j in range(n_cases):
        gc_measurement[i].append(max([len(i) for i in nx.connected_components(graphs[i][j])]))
        ef_measurement[i].append(nx.global_efficiency(graphs[i][j]))



# Create a "table" to record mesurements 
means_gc = []
sds_gc = []
means_ef = []
sds_ef = []

for i in range(n_p):
    means_gc.append(np.mean(gc_measurement[i]))
    sds_gc.append(np.std(gc_measurement[i]))
    means_ef.append(np.mean(ef_measurement[i]))
    sds_ef.append(np.std(ef_measurement[i]))
    


# Create two graphs


# plt.scatter(p, means_gc)
# plt.errorbar(p, means_gc, yerr=sds_gc, ls='none')
# plt.show()

# plt.scatter(p, means_ef)
# plt.errorbar(p, means_ef, yerr=sds_ef, ls='none')
# plt.show()

fig = px.scatter(x=p, y=means_gc, error_y=sds_gc,
                 labels={'x':'Values of p', 'y':'Mean'},
                 title='Largest Component Size')
fig.show()

fig = px.scatter(x=p, y=means_ef, error_y=sds_ef,
                 labels={'x':'Values of p', 'y':'Mean'},
                 title='Efficiency')
fig.show()

# def show(fig):
#     import io
#     import plotly.io as pio
#     from PIL import Image
#     buf = io.BytesIO()
#     pio.write_image(fig, buf)
#     img = Image.open(buf)
#     img.show() 

# show(fig)