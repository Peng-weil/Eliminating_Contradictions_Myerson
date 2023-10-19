from docplex.mp.model import Model


def solving_cardinal_minimum_solution(variables, constraints):
    '''
    Solving for the cardinal minimum solution
    '''
    solve = False

    model = Model('CMS')
    ILP_var_dict = {}
    result = []

    # variable
    for variable in list(variables):
        ILP_var_dict[variable] = model.binary_var(name=variable)

    while not solve:

        # constraint
        for constraint in constraints:
            mups_cons = sorted(list(constraint.keys()))
            mups_var = [ILP_var_dict[formula_id] for formula_id in mups_cons]

            model.add_constraint(model.sum(mups_var) >= 1)

        model.minimize(model.sum([v for v in ILP_var_dict.values()]))
        n_variable = model.number_of_variables
        n_constraint = model.number_of_constraints
        solve = model.solve()

        for k, v in ILP_var_dict.items():

            if int(solve[k]) == 1:
                result.append(k)

        model.end()
        return result, n_variable, n_constraint


def solving_myerson_weighted_solution(variables, constraints, myerson_weights):
    '''
    Solving for the myerson weighted solution
    '''
    solve = False

    model = Model('Myerson Weighted')
    ILP_var_dict = {}
    result = []

    # variable
    for variable in list(variables):
        ILP_var_dict[variable] = model.binary_var(name=variable)

    while not solve:

        # constraint
        for constraint in constraints:
            mups_cons = sorted(list(constraint.keys()))
            mups_var = [ILP_var_dict[formula_id] for formula_id in mups_cons]

            model.add_constraint(model.sum(mups_var) >= 1)

        model.minimize(model.sum([v for v in ILP_var_dict.values()]))
        solve_first_step = model.solve()

        minimal_cardinal_num = int(solve_first_step.get_objective_value())

        model.add_constraint(model.sum([v for v in ILP_var_dict.values()]) <= minimal_cardinal_num)

        model.minimize(
            model.sum([(-1) * v * float(round(myerson_weights[str(v.name)], 2)) for v in ILP_var_dict.values()])
        )

        n_constraint = model.number_of_constraints
        n_variable = model.number_of_variables
        solve = model.solve()

        for k, v in ILP_var_dict.items():

            if int(solve[k]) == 1:
                result.append(k)

        model.end()
        return result, n_variable, n_constraint
