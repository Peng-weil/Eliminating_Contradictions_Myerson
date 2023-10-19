import os
import argparse
import networkx as nx
import matplotlib.pyplot as plt

from src.OWL_tool import OWLLoad


def get_parser():
    parser = argparse.ArgumentParser(description="MyersonOntology_visual")

    parser.add_argument("--ontology", type=str, default="all", help="all")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--density", type=float, default=0.15)
    parser.add_argument("--nx_seed", type=int, default=0)

    return parser


def get_subdirectories(folder):
    subdirectories = []
    for entry in os.scandir(folder):
        if entry.is_dir():
            subdirectories.append(entry.name)
    return subdirectories


def mkdir_tool(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


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


def draw_graph_single(graph,
                      is_save=False,
                      save_pth='',
                      ):
    plt.subplots(figsize=(8, 8))
    pos = nx.spring_layout(graph, k=0.75)

    nx.draw_networkx_nodes(graph, pos, node_color='blue', node_size=350, alpha=0.6)
    nx.draw_networkx_edges(graph, pos, edge_color='grey', arrowsize=10, alpha=0.8)

    nx.draw_networkx_labels(graph, pos, font_size=8, font_color='w')

    plt.axis('off')
    if not is_save:
        plt.show()
    else:
        plt.savefig(save_pth, dpi=300)
    plt.close()


def main(args, onto):
    # Load ontology by MUPS.
    mups_path = os.path.join('./data/mups', onto, 'res.txt')
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

    # save in directory

    draw_path = os.path.join('./draw', onto)
    mkdir_tool(draw_path)
    mkdir_tool(os.path.join(draw_path, 'mups'))

    draw_graph_single(ontology_graph,
                      is_save=True,
                      save_pth=os.path.join(draw_path, str(onto) + '_onto_graph'))

    i_mups = 1
    for mups_f in onto_mups_f_dict:
        formula_in_mups = [int(i) for i in list(mups_f.keys())]

        mups_graph = ontology_graph.subgraph(formula_in_mups)
        draw_graph_single(mups_graph,
                          is_save=True,
                          save_pth=os.path.join(draw_path, 'mups', 'mups' + str(i_mups)))

        i_mups += 1


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    if args.ontology == "all":
        mups_dirname = get_subdirectories("./data/mups")
        for mups in mups_dirname:
            main(args, mups)
    else:
        main(args, args.ontology)