from random import randint, sample
import math
from matplotlib import pyplot as plt

class Ville:
    """
    Une ville est represente par une coordonnee x, y et un identifiant unique

    """
    n = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ident = Ville.n
        Ville.n+=1


def distance(v1, v2):
    return math.sqrt((v1.x-v2.x)**2 + (v1.y-v2.y)**2)

def tour_cost(tour):
    cpt = 0
    for i in range(-1, len(tour)-1):
        cpt += distance(tour[i], tour[i+1])
    return cpt

nbr_ville = 40

villes = [Ville(randint(0,1000), randint(0,1000)) for _ in range(nbr_ville)]

########################
# ALGO DE LA PANTHERE  #
########################

class Panthere:

    def __init__(self, villes):

        self.tour = sample(villes, len(villes))
    
    def placeAfter(self, villeA, villeB):
        a = self.tour.index(villeA)
        b = self.tour.index(villeB)
        l = []
        for i in range(len(self.tour)):
            if i != a and i != b:
                l.append(self.tour[i])
            elif i == a:
                l.append(self.tour[i])
                l.append(self.tour[b])
        
        self.tour = l


    def grow(self, f):

        nbVoisins = 5

        l = []

        for _ in range(nbVoisins):

            l.append(permuter(self.tour, 1))
    
        self.tour = min(l + [self.tour], key=tour_cost)


def permuter(l, nbr):
    l2 = l[:]
    for _ in range(nbr):
        a = randint(0,len(l)-1)
        b = randint(0,len(l)-1)
        l2[a],l2[b] = l[b],l[a]
    return l2


def teach_hunting(pop, best):
    coefficient = 0.10
    numbers = int(len(best.tour) * coefficient)
    
    for panthere in pop:
        if panthere != best:
            for _ in range(numbers):
                a = randint(0,len(best.tour)-1)
                b = (a+1)%len(best.tour)

                panthere.placeAfter(best.tour[a], best.tour[b])


def make_child(panthereA, panthereB):
    p = Panthere(panthereA.tour)
    teach_hunting([p], panthereA)
    return p



# test d'une solution aleatoire
first = Panthere(villes)
print("random solution",tour_cost(first.tour))


pop_size = 40
iterations = 500
mature = 30
objective_function = lambda x : tour_cost(x.tour)
population = [Panthere(villes) for _ in range(pop_size)]
print("best without iteration", objective_function(min(population, key = objective_function)))
first = min(population, key = objective_function)
for _ in range(iterations):
    for panthere in population:
        for _ in range(mature):
            panthere.grow(objective_function)
    
    best_panthere = min(population, key = objective_function)
    teach_hunting(population, best_panthere)
    population = sorted(population, key = objective_function)[:pop_size//2]
    
    for _ in range(pop_size//2):
      population.append(make_child(population[0], population[1]))





best = population[0]

print("solution panthereuse", objective_function(best))

lines = []

for i in range(-1,len(best.tour)-1):

    x = [best.tour[i].x, best.tour[i+1].x]
    y = [best.tour[i].y, best.tour[i+1].y]
    lines.append([x,y])

plt.figure("Panthere")
plt.plot([t.x for t in best.tour], [t.y for t in best.tour],'ro')
plt.plot([t[0] for t in lines], [t[1] for t in lines])
plt.axis([0,1000,0,1000])



lines2 = []

for i in range(-1,len(first.tour)-1):

    x = [first.tour[i].x, first.tour[i+1].x]
    y = [first.tour[i].y, first.tour[i+1].y]
    lines2.append([x,y])


plt.figure("random")
plt.plot([t.x for t in best.tour], [t.y for t in best.tour],'ro')
plt.plot([t[0] for t in lines2], [t[1] for t in lines2])
plt.axis([0,1000,0,1000])
plt.show()
