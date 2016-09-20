from deap import tools, creator, base, algorithms
import numpy
import random
import matplotlib.pyplot as plt
%matplotlib inline

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

    return (err,)

#uncertain here
def mutfloat(individual, indpb):
	for i in individual:
   		if random.uniform(0,1) <= indpb:
   			i = i + random.uniform(-5,5)	            
	return (individual,)

def model ():
    creator.create("bestFit", base.Fitness, weights = (-1.0,))
    creator.create("Individual",list,fitness=creator.bestFit)

    toolbox = base.Toolbox()
    toolbox.register("Coeff",random.uniform,-30,30)
    toolbox.register("individual",tools.initRepeat,creator.Individual,toolbox.Coeff, 3) 
    toolbox.register("population",tools.initRepeat,list,toolbox.individual, n = 50)
    toolbox.register("evaluate",test_regress)

    toolbox.register("mate",tools.cxTwoPoint)
    toolbox.register("mutate",mutfloat,indpb = 0.05)
    toolbox.register("select", tools.selTournament,tournsize =3)
    toolbox.register("map",map)

    cxprob, mutprob, ngens = 0.5,0.2,300
    pop = toolbox.population()
    ind = toolbox.individual()
    hof = tools.HallOfFame(1)
    pop = algorithms.eaMuPlusLambda(pop, toolbox,10,50, cxprob, mutprob, ngens,halloffame = hof, verbose = 0)
    return hof[0]

random.seed(10)
xi,yi = [],[] #empty lists for plotting

#getting data
f = open('data.txt', 'r')
points = []
for line in f:
    point = map(float,line.split())
    plt.plot(point[0],point[1],"b"+"o")
    points.append(point)
    
f.close()

#end setting up, begin main 

for point in points:
    mean = mean + point[1]

mean = mean/len(points)

c = model() #GA
#c = (X^t * X)^-1 * X^t * y
print c

#plotting
for point in points:
    xi.append(point[0])
    yi.append(c[0] * point[0]**2 + c[1]*point[0] + c[2])

plt.plot(xi, yi, "-")
plt.show()

#theory
#Get new quadratic
#find new min 
#plug new min into rosenbrock
#take output and place into points 
#repeat from recalc mean