import os
import datetime
import argparse
import logging

import networkx as nx
from fractions import Fraction

from src.OWL_tool import OWLLoad
from src.ILP_model import solving_cardinal_minimum_solution, solving_myerson_weighted_solution


def get_logger(log_pth):
    # Log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_pth)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(console)

    return logger


def get_parser():
    parser = argparse.ArgumentParser(description="MyersonOntology")

    parser.add_argument("--dumped", type=str, default="./log")
    parser.add_argument("--ontology", type=str, default="all", help="all")
    parser.add_argument("--density", type=float, default=0.15)
    parser.add_argument("--nx_seed", type=int, default=30)

    return parser


def get_subdirectories(folder):
    subdirectories = []
    for entry in os.scandir(folder):
        if entry.is_dir():
            subdirectories.append(entry.name)
    return subdirectories


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


def main(logger, args, mups, metrics, nx_seed):
    # Load ontology by MUPS.
    mups_path = os.path.join('./data/mups', mups, 'res.txt')
    ontology = OWLLoad(mups_path)
    onto_mups_list = ontology.mups_list
    onto_formula_dict = ontology.formula_dict
    onto_mups_f_dict = ontology.mups_f_dict
    formula_vars = onto_formula_dict.keys()

    logger.info("*" * 48)
    logger.info(f"ontology name: {mups}")
    logger.info(f"seed of networkX: {nx_seed}")
    logger.info(f"number of formulas: {len(onto_formula_dict)}")
    logger.info(f"number of MUPSs: {len(onto_mups_f_dict)}")

    # Create a randomized directed graph of the ontology.
    graph_density = args.density
    ontology_graph = generate_random_graph(len(onto_formula_dict), onto_mups_f_dict, nx_seed, graph_density)
    logger.info(f"ontology graph: {len(ontology_graph.nodes)} nodes, {len(ontology_graph.edges)} edges.")
    logger.info("-" * 48)

    i_mups = 1
    mups_CC_dict = {}
    for mups_f in onto_mups_f_dict:
        formula_in_mups = [int(i) for i in list(mups_f.keys())]

        mups_graph = ontology_graph.subgraph(formula_in_mups)

        # strongly connected components
        mups_graph_CC = list(nx.strongly_connected_components(mups_graph))

        mups_CC_dict[''.join(['mups', str(i_mups)])] = mups_graph_CC
        i_mups += 1

    # Basic Model
    basic_start_time = datetime.datetime.now()
    basic_result, basic_n_variable, basic_n_constraint = solving_cardinal_minimum_solution(onto_formula_dict.keys(),
                                                                                           onto_mups_f_dict)
    basic_end_time = datetime.datetime.now()

    logger.info("|------ BASIC MODEl INFO")
    logger.info(f"|--- model variables: {basic_n_variable}")
    logger.info(f"|--- model constraints: {basic_n_constraint}")
    logger.info(f"|--- formula id in solution: {basic_result}")

    # evaluation
    basic_graph = ontology_graph.copy()
    basic_graph.remove_nodes_from([int(node) for node in basic_result])

    logger.info("|------ EVALUATION")
    logger.info(f"|--- solve time: {round((basic_end_time - basic_start_time).total_seconds() * 1000)} ms")
    logger.info(f"|--- remain nodes: {len(basic_graph.nodes)}")
    logger.info(f"|--- remain edges: {len(basic_graph.edges)}")
    basic_RP = ((len(ontology_graph.edges) - len(basic_graph.edges)) / len(ontology_graph.edges) * 100)

    if metrics[mups][0] is None:
        metrics[mups][0] = [basic_RP]
    else:
        metrics[mups][0].append(basic_RP)

    logger.info(f"|--- reduction percentage (edges): {basic_RP:.2f} %")
    logger.info("-" * 48)

    # Myerson Weighted Model
    myerson_start_time = datetime.datetime.now()
    myerson_dict = {f: [] for f in list(formula_vars)}

    for mups_key, mups_CC_set in mups_CC_dict.items():
        for CC in mups_CC_set:
            for f_in_cc in CC:
                myerson_dict[str(f_in_cc)].append(Fraction(Fraction(1, len(CC)), len(mups_CC_set)))

    myerson_weights = {k: sum(v) / len(v) for k, v in myerson_dict.items()}
    myerson_result, myerson_n_variable, myerson_n_constraint = solving_myerson_weighted_solution(onto_formula_dict.keys(),
                                                                                                 onto_mups_f_dict,
                                                                                                 myerson_weights)
    myerson_end_time = datetime.datetime.now()

    logger.info("|------ MYERSON WEIGHTED MODEl INFO")
    logger.info(f"|--- model variables: {myerson_n_variable}")
    logger.info(f"|--- model constraints: {myerson_n_constraint}")
    logger.info(f"|--- formula id in solution: {myerson_result}")

    # evaluation
    myerson_graph = ontology_graph.copy()
    myerson_graph.remove_nodes_from([int(node) for node in myerson_result])

    logger.info("|------ EVALUATION")
    logger.info(f"|--- solve time: {round((myerson_end_time - myerson_start_time).total_seconds() * 1000)} ms")
    logger.info(f"|--- remain nodes: {len(myerson_graph.nodes)}")
    logger.info(f"|--- remain edges: {len(myerson_graph.edges)}")
    myerson_RP = ((len(ontology_graph.edges) - len(myerson_graph.edges)) / len(ontology_graph.edges) * 100)

    if metrics[mups][1] is None:
        metrics[mups][1] = [myerson_RP]
    else:
        metrics[mups][1].append(myerson_RP)
    logger.info(f"|--- reduction percentage (edges): {myerson_RP:.2f} %")

    logger.info("*" * 48)
    return metrics


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    ONTOLOGY = args.ontology

    log_pth = os.path.join(args.dumped, ONTOLOGY + ".log")
    logger = get_logger(log_pth)

    metrics = {}

    if args.ontology == "all":

        mups_dirname = get_subdirectories("./data/mups")
        logger.info(f"ONTOLOGY: {mups_dirname}")
        for mups in mups_dirname:
            metrics[mups] = [[], []]
            for nx_seed in range(args.nx_seed):
                metrics = main(logger, args, mups, metrics, nx_seed)

    else:
        metrics[args.ontology] = [[], []]
        for nx_seed in range(args.nx_seed):
            metrics = main(logger, args, args.ontology, metrics, nx_seed)

    logger.info(f"complete. Metrics: {metrics}")

    logger.info("Summary")
    for k, v in metrics.items():
        logger.info(f"ONTOLOGY {k}: BASIC MODEL reduces edges by {(sum(v[0]) / len(v[0])):.2f} %, Myerson MODEL reduces edges by {(sum(v[1]) / len(v[1])):.2f} %.")
