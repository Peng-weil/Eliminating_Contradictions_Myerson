import copy
import pandas as pd
import numpy as np


class OWLLoad:
    def __init__(self, pth):

        self.mups_path = pth
        self.mups_list = None
        self.formula_dict = None
        self.mups_f_dict = None
        self.mups_read()
        self.find_formula_in_mups()

    def mups_read(self):
        mups_file = open(self.mups_path)
        mups_start = False
        mups_single = []
        self.formula_dict = {}
        self.mups_list = []
        var_x = 0

        line = mups_file.readline()
        while line:
            if (not line.strip().startswith('Found explanation <')) \
                    and (not line.strip().startswith('Explanation <')):
                if len(line.strip()) != 0 and line.strip().startswith('['):
                    if mups_start:
                        mups_str = line[line.find(']') + 1:len(line)].strip()
                        if mups_str not in mups_single:
                            mups_single.append(mups_str)
                        if mups_str not in self.formula_dict.keys():
                            self.formula_dict[mups_str] = str(var_x)
                            var_x += 1
                else:
                    mups_start = False
                    if not len(mups_single) == 0:
                        if not set(mups_single) in self.mups_list:
                            self.mups_list.append(copy.deepcopy(set(mups_single)))
                        mups_single.clear()
            else:
                mups_start = True
            line = mups_file.readline()
        mups_file.close()

        self.formula_dict = {value: key for key, value in self.formula_dict.items()}

    def find_formula_in_mups(self):
        var2mups = []
        check_find_axiom = False

        for s_mups in self.mups_list:
            var_mups = {}
            for s_axiom in s_mups:
                for var_x, var_axiom in self.formula_dict.items():
                    if var_axiom == s_axiom:
                        check_find_axiom = True
                        var_mups[var_x] = var_axiom
                        break
                assert check_find_axiom
                check_find_axiom = False
            var2mups.append(var_mups)

        self.mups_f_dict = var2mups


# def generate_random_und_adj_pd(node_vars, density):
#     adj_pd = pd.DataFrame(index=node_vars, columns=node_vars)
#
#     adj_matrix_numpy = np.random.choice([0, 1], size=adj_pd.shape, p=[1 - density, density])
#     # adj_matrix_numpy = np.triu(adj_matrix_numpy) + np.triu(adj_matrix_numpy, k=1).T
#
#     adj_np_r, adj_np_c = np.diag_indices_from(adj_matrix_numpy)
#     adj_matrix_numpy[adj_np_r, adj_np_c] = 0
#
#     for i, row_label in enumerate(adj_pd.index):
#         for j, col_label in enumerate(adj_pd.columns):
#             adj_pd.loc[row_label, col_label] = adj_matrix_numpy[i, j]
#
#     return adj_pd.astype(int)
