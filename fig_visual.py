import os
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from src.OWL_tool import OWLLoad


def get_parser():
    parser = argparse.ArgumentParser(description="MyersonOntology_visual")

    parser.add_argument("--ontology", type=str, default="AROMA-cmt-cocus")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--density", type=float, default=0.15)
    parser.add_argument("--nx_seed", type=int, default=0)

    return parser


def generate_random_graph(nodes, onto_mups_f_dict, nx_seed, density):
    graph = nx.gnp_random_graph(nodes, density, seed=nx_seed, directed=True)

    g_nodes = graph.nodes

    illegal_edges = set(((i, j) for i in g_nodes for j in g_nodes))

    for mups_dict in onto_mups_f_dict:
        mups_f_list = [int(n) for n in list(mups_dict.keys())]
        permit_edges = set(((i, j) for i in mups_f_list for j in mups_f_list if i != j))
        illegal_edges = illegal_edges - permit_edges

    del_edge = []
    for e in graph.edges:
        if e in illegal_edges:
            del_edge.append(e)

    for de in del_edge:
        graph.remove_edge(de[0], de[1])

    return graph


def main(args, onto):
    # Load ontology by MUPS.
    mups_path = os.path.join('./data/mups', args.ontology, 'res.txt')
    ontology = OWLLoad(mups_path)
    onto_mups_list = ontology.mups_list
    onto_formula_dict = ontology.formula_dict
    onto_mups_f_dict = ontology.mups_f_dict
    formula_vars = onto_formula_dict.keys()

    print(f"ontology name: {onto}")
    print(f"seed of networkX: {args.nx_seed}")
    print(f"number of formulas: {len(onto_formula_dict)}")
    print(f"number of MUPSs: {len(onto_mups_f_dict)}")

    # Create a randomized directed graph of the ontology.
    graph_density = args.density
    ontology_graph = generate_random_graph(len(onto_formula_dict), onto_mups_f_dict, args.nx_seed, graph_density)
    print("")
    print(f"ontology graph: {len(ontology_graph.nodes)} nodes, {len(ontology_graph.edges)} edges, {args.density} density.")

    mups_graph_list = []

    i_mups = 1
    for mups_f in onto_mups_f_dict:
        formula_in_mups = [int(i) for i in list(mups_f.keys())]

        mups_graph = ontology_graph.subgraph(formula_in_mups)
        mups_graph_list.append(mups_graph)
        i_mups += 1

        if i_mups == 10:
            break

    fig = plt.figure(dpi=185,
                     constrained_layout=True,
                     figsize=(16, 9))

    gs = GridSpec(3, 6, figure=fig)

    ns1 = 180
    ns2 = 220
    plt.rc('font', family='Times New Roman')

    fs = 24

    plt.rcParams['mathtext.fontset'] = 'custom'
    plt.rcParams['mathtext.rm'] = 'Times New Roman'
    plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
    plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'

    ax1 = fig.add_subplot(gs[0:3, 0:3])
    ax1.text(0.5, 0.03, 'Ontology\'s Graph', fontsize=fs, ha='center', transform=ax1.transAxes)
    pos = nx.spring_layout(ontology_graph, k=0.8, iterations=20)
    nx.draw_networkx_nodes(ontology_graph, pos, node_color='blue', node_size=240, ax=ax1)
    nx.draw_networkx_edges(ontology_graph, pos, edge_color='grey', alpha=0.5, ax=ax1)
    nx.draw_networkx_labels(ontology_graph, pos, font_size=8, font_color='w', ax=ax1)
    ax1.axis('off')

    ax2 = fig.add_subplot(gs[0, 3])
    ax2.text(0.5, -0.2, '$conf_1$', fontsize=fs, ha='center', transform=ax2.transAxes)
    pos2 = nx.circular_layout(mups_graph_list[0])
    nx.draw_networkx_nodes(mups_graph_list[0], pos2, node_color='green', node_size=ns2, ax=ax2)
    nx.draw_networkx_edges(mups_graph_list[0], pos2, edge_color='grey', alpha=0.5, ax=ax2)
    nx.draw_networkx_labels(mups_graph_list[0], pos2, font_size=6, font_color='w', ax=ax2)
    # ax2.axis('off')

    ax3 = fig.add_subplot(gs[0, 4])
    ax3.text(0.5, -0.2, '$conf_2$', fontsize=fs, ha='center', transform=ax3.transAxes)
    pos3 = nx.circular_layout(mups_graph_list[1])
    nx.draw_networkx_nodes(mups_graph_list[1], pos3, node_color='green', node_size=ns2, ax=ax3)
    nx.draw_networkx_edges(mups_graph_list[1], pos3, edge_color='grey', alpha=0.5, ax=ax3)
    nx.draw_networkx_labels(mups_graph_list[1], pos3, font_size=6, font_color='w', ax=ax3)
    # ax3.axis('off')

    ax4 = fig.add_subplot(gs[0, 5])
    ax4.text(0.5, -0.2, '$conf_3$', fontsize=fs, ha='center', transform=ax4.transAxes)
    pos4 = nx.circular_layout(mups_graph_list[2])
    nx.draw_networkx_nodes(mups_graph_list[2], pos4, node_color='green', node_size=ns2, ax=ax4)
    nx.draw_networkx_edges(mups_graph_list[2], pos4, edge_color='grey', alpha=0.5, ax=ax4)
    nx.draw_networkx_labels(mups_graph_list[2], pos4, font_size=6, font_color='w', ax=ax4)
    # ax4.axis('off')

    ax5 = fig.add_subplot(gs[1, 3])
    ax5.text(0.5, -0.2, '$conf_4$', fontsize=fs, ha='center', transform=ax5.transAxes)
    pos5 = nx.circular_layout(mups_graph_list[3])
    nx.draw_networkx_nodes(mups_graph_list[3], pos5, node_color='green', node_size=ns2, ax=ax5)
    nx.draw_networkx_edges(mups_graph_list[3], pos5, edge_color='grey', alpha=0.5, ax=ax5)
    nx.draw_networkx_labels(mups_graph_list[3], pos5, font_size=6, font_color='w', ax=ax5)
    # ax5.axis('off')

    ax6 = fig.add_subplot(gs[1, 4])
    ax6.text(0.5, -0.2, '$conf_5$', fontsize=fs, ha='center', transform=ax6.transAxes)
    pos6 = nx.circular_layout(mups_graph_list[4])
    nx.draw_networkx_nodes(mups_graph_list[4], pos6, node_color='green', node_size=ns2, ax=ax6)
    nx.draw_networkx_edges(mups_graph_list[4], pos6, edge_color='grey', alpha=0.5, ax=ax6)
    nx.draw_networkx_labels(mups_graph_list[4], pos6, font_size=6, font_color='w', ax=ax6)
    # ax6.axis('off')

    ax7 = fig.add_subplot(gs[1, 5])
    ax7.text(0.5, -0.2, '$conf_6$', fontsize=fs, ha='center', transform=ax7.transAxes)
    pos7 = nx.circular_layout(mups_graph_list[5])
    nx.draw_networkx_nodes(mups_graph_list[5], pos7, node_color='green', node_size=ns2, ax=ax7)
    nx.draw_networkx_edges(mups_graph_list[5], pos7, edge_color='grey', alpha=0.5, ax=ax7)
    nx.draw_networkx_labels(mups_graph_list[5], pos7, font_size=6, font_color='w', ax=ax7)
    # ax7.axis('off')

    ax8 = fig.add_subplot(gs[2, 3])
    ax8.text(0.5, -0.2, '$conf_7$', fontsize=fs, ha='center', transform=ax8.transAxes)
    pos8 = nx.circular_layout(mups_graph_list[6])
    nx.draw_networkx_nodes(mups_graph_list[6], pos8, node_color='green', node_size=ns2, ax=ax8)
    nx.draw_networkx_edges(mups_graph_list[6], pos8, edge_color='grey', alpha=0.5, ax=ax8)
    nx.draw_networkx_labels(mups_graph_list[6], pos8, font_size=6, font_color='w', ax=ax8)
    # ax8.axis('off')

    ax9 = fig.add_subplot(gs[2, 4])
    ax9.text(0.5, -0.2, '$conf_8$', fontsize=fs, ha='center', transform=ax9.transAxes)
    pos9 = nx.circular_layout(mups_graph_list[7])
    nx.draw_networkx_nodes(mups_graph_list[7], pos9, node_color='green', node_size=ns2, ax=ax9)
    nx.draw_networkx_edges(mups_graph_list[7], pos9, edge_color='grey', alpha=0.5, ax=ax9)
    nx.draw_networkx_labels(mups_graph_list[7], pos9, font_size=6, font_color='w', ax=ax9)
    # ax9.axis('off')

    ax10 = fig.add_subplot(gs[2, 5])
    ax10.text(0.5, -0.2, '$conf_9$', fontsize=fs, ha='center', transform=ax10.transAxes)
    pos10 = nx.circular_layout(mups_graph_list[7])
    nx.draw_networkx_nodes(mups_graph_list[7], pos10, node_color='green', node_size=ns2, ax=ax10)
    nx.draw_networkx_edges(mups_graph_list[7], pos10, edge_color='grey', alpha=0.5, ax=ax10)
    nx.draw_networkx_labels(mups_graph_list[7], pos10, font_size=6, font_color='w', ax=ax10)
    # pos10.axis('off')

    # plt.show()
    plt.savefig('./figureIMG1.png')


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    main(args, args.ontology)
