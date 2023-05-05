import numpy as np

radius = 1
rule_book = np.array([0 for _ in range(2**(2*radius+1))]) # initial rule is all 0

# Returns a 2D-array of size (num_cells, num_gens) of ones and zeros with one dim being space and the other time
## for given radius, rule_book and first generation
def nextGen(num_cells, gen=None):
	if gen is None:
		gen=np.random.randint(2, size=num_cells)
	return np.random.randint(2, size=num_cells)

# Returns a scalar
def getEnthropy(radius, rule_book):
	pass

# Returns a scalar: Langton factor of given rule book
def getLangton(radius, rule_book):
	pass

# Returns a random rule_book of given langtonFactor
def getRuleByLangton(langtonFactor):
	pass