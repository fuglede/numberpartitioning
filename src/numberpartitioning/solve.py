#!python3

""" 
Utility functions for solving optimization problems using a sequence of CVXPY solvers.

CVXPY supports many solvers, but some of them fail for some problems. 
Therefore, for robustness, it may be useful to try a list of solvers, one at a time,
   until the first one that succeeds.
"""

import cvxpy

DEFAULT_SOLVERS=[cvxpy.XPRESS, cvxpy.OSQP, cvxpy.SCS]

import logging
logger = logging.getLogger(__name__)

def solve(problem:cvxpy.Problem, solvers:list=DEFAULT_SOLVERS)  -> None:
	"""
	Try to solve the given cvxpy problem using the given solvers, in order, until one succeeds.
    See here https://www.cvxpy.org/tutorial/advanced/index.html for a list of supported solvers.

    Parameters
    ----------
    problem
        a cvxpy Problem instance.
    solvers
        a list of one or more cvxpy solvers (optional).

    Returns
    -------
    Nothing; the "problem" variable is automatically updated by cvxpy.
	"""
	is_solved=False
	for solver in solvers[:-1]:  # Try the first n-1 solvers.
		try:
			problem.solve(solver=solver)
			logger.info("Solver %s succeeds",solver)
			is_solved = True
			break
		except cvxpy.SolverError as err:
			logger.info("Solver %s fails: %s", solver, err)
	if not is_solved:
		problem.solve(solver=solvers[-1])   # If the first n-1 fail, try the last one.
	if problem.status == "infeasible":
		raise ValueError("Problem is infeasible")
	elif problem.status == "unbounded":
		raise ValueError("Problem is unbounded")


def maximize(objective, constraints:list, solvers:list=DEFAULT_SOLVERS):
	"""
	A utility function for finding the maximum of a general objective function.

    Parameters
    ----------
    objective
        an expression containing cvxpy variables. Should be a concave function of the variables.
	constraints
	    a list of cvxpy constraints.
    solvers
        a list of one or more cvxpy solvers (optional).

    Returns
    -------
	the maximum value of the objective function given the constraints.

	>>> import numpy as np
	>>> x = cvxpy.Variable()
	>>> np.round( maximize(x, [x>=1, x<=3]), 3)
	3.0
	"""

	problem = cvxpy.Problem(cvxpy.Maximize(objective), constraints)
	solve(problem, solvers=solvers)
	return objective.value.item()

def minimize(objective, constraints, solvers:list=DEFAULT_SOLVERS):
	"""
	A utility function for finding the minimum of a general objective function.

    Parameters
    ----------
    objective
        an expression containing cvxpy variables. Should be a concave function of the variables.
	constraints
	    a list of cvxpy constraints.
    solvers
        a list of one or more cvxpy solvers (optional).

    Returns
    -------
	the minimum value of the objective function given the constraints.


	>>> import numpy as np
	>>> x = cvxpy.Variable()
	>>> np.round(minimize(x, [x>=1, x<=3]),3)
	1.0
	"""
	problem = cvxpy.Problem(cvxpy.Minimize(objective), constraints)
	solve(problem, solvers=solvers)
	return objective.value.item()




if __name__ == '__main__':
	import sys
	logger.addHandler(logging.StreamHandler(sys.stdout))
	logger.setLevel(logging.INFO)

	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))
