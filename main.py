from deap import tools, creator, base, algorithms
import numpy
import random

#point[0] = x, point[1] = y
points = []
mean = 0

def test_regress(coef):
	SSres = 0 
	SStot = 0

	for point in points:
		x = point[0]
		yi = coef[0]*x**2 + coef[1]*x + coef[2]
		SSres = SSres + (point[1] - yi)**2
		SStot = SStot + (point[1] - mean)**2

	err = SSres/SStot

	return (SSres,)

def mutfloat(individual, indpb):
	for i in individual:
   		if random.uniform(0,1) <= indpb:
   			mut = random.uniform(-1,1)
   			if random.randint(0,1) == 0:
   				i -= mut
   			else:
   				i += mut
	            
	return (individual,)

def model ():
	#Fitness = sum of differences, E(ya - (ax^2 + bx + C))^2
	creator.create("bestFit", base.Fitness, weights = (-1.0,))
	creator.create("Individual",list,fitness=creator.bestFit)

	toolbox = base.Toolbox()
	toolbox.register("Coeff",random.uniform,-30,30)
	toolbox.register("individual",tools.initRepeat,creator.Individual,toolbox.Coeff, 3) 
	toolbox.register("population",tools.initRepeat,list,toolbox.individual, n = 100)
	toolbox.register("evaluate",test_regress)

	toolbox.register("mate",tools.cxTwoPoint)
	toolbox.register("mutate",mutfloat,indpb = 0.05)
	toolbox.register("select", tools.selTournament,tournsize =3)
	toolbox.register("map",map)

	cxprob, mutprob, ngens = 0.5,0.1,150
	pop = toolbox.population()
	ind = toolbox.individual()
	hof = tools.HallOfFame(1)
	pop = algorithms.eaSimple(pop, toolbox, cxprob, mutprob, ngens,halloffame = hof, verbose = 0)
	return hof[0]

random.seed(15)
f = open('data.txt', 'r')
for line in f:
	point = map(float,line.split())
	points.append(point)

for point in points:
	mean = mean + point[1]

mean = mean/len(points)

print model()