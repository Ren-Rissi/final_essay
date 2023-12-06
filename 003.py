import networkx as nx
import random as rd
import numpy as np
import plotly.express as px
import multiprocessing as mp
from pathlib import Path
# from time import time


# Set the seed for randomness reproducibility 
seed = 42
rd.seed(seed)

# Fix the number of nodes for each network
n = 500 # 500

# set a number of nodes to be excluded per iteration batch
n_ex = 10 # 10

# set a number of different initial networks
n_ntk = 10 # 10

# set a number of repetiotions on each network
n_rep = 10 # 10

# Function to create the ER graphs
def generate_gnp(n, ad):
    # given N and the average_degree, fix p
    p = ad/(n-1)
    G = nx.gnp_random_graph(n, p)
    return(G)

# Function to create the BA graphs
def generate_BA(n, ad):
    # given N and the average_degree, fix p
    m = int(ad/2)
    G = nx.barabasi_albert_graph(n, m)
    return(G)

# Function that will repeat for all the networks
def attack(G):
    H = G.copy()

    # start the list of measurement values
    gc = []
    ef = []

    # get initial measurements
    gc.append(max([len(l) for l in nx.connected_components(H)]))
    ef.append(nx.global_efficiency(H))

    # start the attacks iterations until the graph vanishes
    for k in range(1, (n//n_ex)):
        picked_nodes = rd.sample(sorted(H.nodes()), 10)
        H.remove_nodes_from(picked_nodes)

        # recalculate and save the measurements after the atatck batch
        gc.append(max([len(l) for l in nx.connected_components(H)], default=0))
        ef.append(nx.global_efficiency(H))
    
    return((gc, ef))

def extract_results(results):
    gc, ef = tuple(zip(*results))
    gc = np.array(gc).transpose()
    ef = np.array(ef).transpose()
    gc_mean = [np.mean(x) for x in gc]
    ef_mean = [np.mean(x) for x in ef]    
    gc_sd = [np.std(x) for x in gc]
    ef_sd = [np.std(x) for x in ef]
    return((gc_mean, gc_sd, ef_mean, ef_sd))


# Function to plot and save, same degrees, different networks
def plot_gc_ef_dn(results_ER, results_BA, n, d):

    dir_to_save = Path('html_figures')
    if dir_to_save.is_dir() == False:
        Path.mkdir(dir_to_save)

    gc_mean_ER, gc_sd_ER, ef_mean_ER, ef_sd_ER = extract_results(results_ER)
    gc_mean_BA, gc_sd_BA, ef_mean_BA, ef_sd_BA = extract_results(results_BA)

    x = [x for x in range(0, n, n_ex)]
    rem = [x for x in range(n, 0, -n_ex)]

    # plot the size of the greatest component
    fig_1 = px.scatter(x=x, y=gc_mean_ER, opacity=0,
                     title='Greatest Component Size for ER and BA of average degree: '+str(d),
                     labels={'x':'Number of nodes removed','y':'Mean'})
    fig_1.update_traces(hovertemplate = None, hoverinfo = 'skip')
    fig_1.add_scatter(x=x, y=gc_mean_ER, error_y={'array':gc_sd_ER},
                    legend='legend',
                    name='Erdos-Renyi',
                    mode='markers')
    fig_1.add_scatter(x=x, y=gc_mean_BA, error_y={'array':gc_sd_BA},
                legend='legend',
                name='Barabasi-Albert',
                mode='markers')
    fig_1.add_scatter(x=x, y=rem,
                    legend='legend', name='Remaining nodes',
                    mode='lines') # need to add line
    fig_1.show()
    
    fig_name = (str(dir_to_save)+'/gc_size_same_degree'+'_'+str(n)+
                '_'+str(d)+'_'+str(n_ex)+'_'+str(n_ntk)+
                '_'+str(n_rep)+'.html')
    fig_1.write_html(fig_name, full_html=True)


    # plot the efficiency 
    fig_2 = px.scatter(x=x, y=ef_mean_ER, opacity=0,
                       title='Efficiency for ER and BA of average degree: '+str(d),
                       labels={'x':'Number of nodes removed', 'y':'Mean'})
    fig_2.update_traces(hovertemplate = None, hoverinfo = 'skip')
    fig_2.add_scatter(x=x, y=ef_mean_ER, error_y={'array':ef_sd_ER},
                      legend='legend',
                      name='Erdos-Renyi',
                      mode='markers')
    fig_2.add_scatter(x=x, y=ef_mean_BA, error_y={'array':ef_sd_BA},
                      legend='legend',
                      name='Barabasi-Albert',
                      mode='markers')
    fig_name = (str(dir_to_save)+'/ef_same_degree'+'_'+str(n)+
                '_'+str(d)+'_'+str(n_ex)+'_'+str(n_ntk)+
                '_'+str(n_rep)+'.html')
    fig_2.show()
    fig_2.write_html(fig_name)

    return((fig_1, fig_2))

# Function to plot and save, same networks, different degrees
def plot_gc_ef_sn(results_02, results_04, results_08, results_16, ntk_type):
    gc_mean_02, gc_sd_02, ef_mean_02, ef_sd_02 = extract_results(results_02)
    gc_mean_04, gc_sd_04, ef_mean_04, ef_sd_04 = extract_results(results_04)
    gc_mean_08, gc_sd_08, ef_mean_08, ef_sd_08 = extract_results(results_08)
    gc_mean_16, gc_sd_16, ef_mean_16, ef_sd_16 = extract_results(results_16)
    x = [x for x in range(0, n, n_ex)]
    rem = [x for x in range(n, 0, -n_ex)]

    # plot the size of the greatest component
    fig_1 = px.scatter(x=x, y=gc_mean_02, opacity=0,
                     title='Greatest Component Size for '+str(ntk_type)+' Networks',
                     labels={'x':'Number of nodes removed','y':'Mean'})
    fig_1.update_traces(hovertemplate = None, hoverinfo = 'skip')
    fig_1.add_scatter(x=x, y=gc_mean_02, error_y={'array':gc_sd_02},
                    legend='legend',
                    name='Average Degree: 2',
                    mode='markers')
    fig_1.add_scatter(x=x, y=gc_mean_04, error_y={'array':gc_sd_04},
                    legend='legend',
                    name='Average Degree: 4',
                    mode='markers')
    fig_1.add_scatter(x=x, y=gc_mean_08, error_y={'array':gc_sd_08},
                    legend='legend',
                    name='Average Degree: 8',
                    mode='markers')
    fig_1.add_scatter(x=x, y=gc_mean_16, error_y={'array':gc_sd_16},
                    legend='legend',
                    name='Average Degree: 16',
                    mode='markers')
    fig_1.add_scatter(x=x, y=rem,
                    legend='legend', name='Remaining nodes',
                    mode='lines') # need to add line
    fig_1.show()
    
    fig_name = ('html_figures'+'/gc_size_same_network'+str(ntk_type)+'_'+str(n)+
                '_'+'_'+str(n_ex)+'_'+str(n_ntk)+
                '_'+str(n_rep)+'.html')
    fig_1.write_html(fig_name, full_html=True)

    fig_2 = px.scatter(x=x, y=ef_mean_02, opacity=0,
                       title='Efficiency for '+str(ntk_type)+' Networks',
                       labels={'x':'Number of nodes removed', 'y':'Mean'})
    fig_2.update_traces(hovertemplate = None, hoverinfo = 'skip')
    fig_2.add_scatter(x=x, y=ef_mean_02, error_y={'array':ef_sd_02},
                      legend='legend',
                      name='Average Degree: 2',
                      mode='markers')
    fig_2.add_scatter(x=x, y=ef_mean_04, error_y={'array':ef_sd_04},
                      legend='legend',
                      name='Average Degree: 4',
                      mode='markers')
    fig_2.add_scatter(x=x, y=ef_mean_08, error_y={'array':ef_sd_08},
                      legend='legend',
                      name='Average Degree: 8',
                      mode='markers')
    fig_2.add_scatter(x=x, y=ef_mean_16, error_y={'array':ef_sd_16},
                      legend='legend',
                      name='Average Degree: 16',
                      mode='markers')
    
    fig_name = ('html_figures'+'/ef_same_network'+str(ntk_type)+'_'+str(n)+
                '_'+'_'+str(n_ex)+'_'+str(n_ntk)+
                '_'+str(n_rep)+'.html')
    fig_2.show()
    fig_2.write_html(fig_name)

    return((fig_1, fig_2))

if __name__ == '__main__':
    print('starting...')
    # Preparing data

    graph_list_02_ER = [generate_gnp(n, 2) for l in range(n_ntk)]
    graph_list_02_BA = [generate_BA(n, 2) for l in range(n_ntk)]
    graph_list_04_ER = [generate_gnp(n, 4) for l in range(n_ntk)]
    graph_list_04_BA = [generate_BA(n, 4) for l in range(n_ntk)]
    graph_list_08_ER = [generate_gnp(n, 8) for l in range(n_ntk)]
    graph_list_08_BA = [generate_BA(n, 8) for l in range(n_ntk)]
    graph_list_16_ER = [generate_gnp(n, 16) for l in range(n_ntk)]
    graph_list_16_BA = [generate_BA(n, 16) for l in range(n_ntk)]

    # That was a try do dinnamically generate the lists:
    # graph_list = [x for sublist in graph_list for x in sublist]
    # graph_list = [generate_gnp(n, 2) for l in range(n_ntk)]

    # print(graph_list)

    # Start a parallelization pool
    pool = mp.Pool(mp.cpu_count())

    # Parallel calculation
    results_02_ER = [pool.apply_async(attack, [l]) for i in range(n_rep) for l in graph_list_02_ER]
    results_02_BA = [pool.apply_async(attack, [l]) for i in range(n_rep) for l in graph_list_02_BA]
    results_04_ER = [pool.apply_async(attack, [l]) for i in range(n_rep) for l in graph_list_04_ER]
    results_04_BA = [pool.apply_async(attack, [l]) for i in range(n_rep) for l in graph_list_04_BA]
    results_08_ER = [pool.apply_async(attack, [l]) for i in range(n_rep) for l in graph_list_08_ER]
    results_08_BA = [pool.apply_async(attack, [l]) for i in range(n_rep) for l in graph_list_08_BA]
    results_16_ER = [pool.apply_async(attack, [l]) for i in range(n_rep) for l in graph_list_16_ER]
    results_16_BA = [pool.apply_async(attack, [l]) for i in range(n_rep) for l in graph_list_16_BA]

    results_02_ER = [x.get() for x in results_02_ER]
    results_02_BA = [x.get() for x in results_02_BA]
    results_04_ER = [x.get() for x in results_04_ER]
    results_04_BA = [x.get() for x in results_04_BA]
    results_08_ER = [x.get() for x in results_08_ER]
    results_08_BA = [x.get() for x in results_08_BA]
    results_16_ER = [x.get() for x in results_16_ER]
    results_16_BA = [x.get() for x in results_16_BA]
    
    # Closing the pool
    pool.close()

    # Removing references to unused variables, so garbage collector can deal with them 
    del(graph_list_02_ER, graph_list_04_ER, graph_list_08_ER, graph_list_16_ER)
    del(graph_list_02_BA, graph_list_04_BA, graph_list_08_BA, graph_list_16_BA)

    plot_gc_ef_dn(results_02_ER, results_02_BA, n, 2)
    plot_gc_ef_dn(results_04_ER, results_04_BA, n, 4)
    plot_gc_ef_dn(results_08_ER, results_08_BA, n, 8)
    plot_gc_ef_dn(results_16_ER, results_16_BA, n, 16)
    plot_gc_ef_sn(results_02_ER, results_04_ER, results_08_ER, results_16_ER, ntk_type='ER')
    plot_gc_ef_sn(results_02_BA, results_04_BA, results_08_BA, results_16_BA, ntk_type='BA')
    


    

