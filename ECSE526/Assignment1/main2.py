__author__ = 'nathaniel'

from simpleai.search import CspProblem, backtrack, min_conflicts, MOST_CONSTRAINED_VARIABLE

variables = ('one', 'two', 'three', 'four', 'five')

domains = dict((v, range(11)) for v in variables)

# print domains

def const_different(variables, values):
    return values[0] != values[1] and abs(values[0] - values[1]) < 11

constraints = []

for v in variables:
    for x in variables:
        if v != x:
            va = (v, x)
            constraint = (va, const_different)
            constraints.append(constraint)

print constraints

my_problem = CspProblem(variables, domains, constraints)

print backtrack(my_problem)
