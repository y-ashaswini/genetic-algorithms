from random import *

class Genetic:

    def __init__(self, each_size, pop_size, num_gen, mutation_prob = 0.8):
        self.each_size = each_size # length of [0,1,1]
        self.pop_size = pop_size # how many agents in each generation?
        self.num_gen = num_gen # how many generations?
        self.curr_gen = 0
        self.mutation_prob = mutation_prob
        self.pop = {} # agent number : agent {0:[0,1,0], 1:[1,1,1], ...}
        self.pop_scores = {} # agent number : current score {0:5, 1:8, 3:2, ...}
        self.score_history = {} # {generation number : {population agent : score}, ...}
        self.score_ordered = [] # ascending order list of agent numbers = [5, 2, 1, ...]
        self.goal = self.each_size;


    def create(self):
        self.pop = {i:[randint(0,1) for _ in range(self.each_size)] for i in range(self.pop_size)}
        
        # calculate scores of each agent in population
        for each_pop in self.pop:
                self.pop_scores[each_pop] =  self.calc_score(self.pop[each_pop])

        # save current scores in history
        self.score_history[self.curr_gen] = self.pop_scores
        # generation number = 1
        self.curr_gen +=1
    
    def iterate(self):
        
        while self.curr_gen < self.num_gen and not self.is_goal_reached():
            
            # order by fitness scores - saved in list self.score_ordered
            self.order_pop()

            # choosing parents = choosing the best 2 to reproduce
            # take top 2 - crossover + mutate + reproduce
            parent_1 = self.pop[self.score_ordered[len(self.score_ordered) - 1]]
            parent_2 = self.pop[self.score_ordered[len(self.score_ordered) - 2]]

            # reproduce
            child = self.reproduce(parent_1, parent_2)

            # calculate score of child
            child_score = self.calc_score(child)

            # if child score > least scorer in current position, replace least with this one
            # else, do not replace (creates new child in next iteration)
            if(child_score >= self.score_ordered[0]):
                self.pop_scores[0] =  child_score # replace weakest's score with child score
                self.pop[0] = child # relace weakest agent with child

                # reorder   
                self.order_pop()
                # changes self.score_ordered                                
            
            # save current generation's scores in history
            self.score_history[self.curr_gen] = self.pop_scores
            self.curr_gen+=1
            print(self.pop_scores)

    def calc_score(self, agent):
        print("calculating score for agent ",agent)
        return agent.count(1)

    def order_pop(self):
        print("reordering population based on fitness scores")
        # saved in list self.score_ordered

        temp = {k: v for k, v in sorted(self.pop.items(), key=lambda item: item[1])}
        self.score_ordered = [i for i in temp.keys()]                
            

    def reproduce(self, parent_1, parent_2):
        print("reproducing")

        # random index = crossover point
        crossover_point = randint(0, self.each_size -1)
        
        # crossover, produce child
        child = parent_1[:crossover_point] + parent_2[crossover_point:]
        print("child without mutation:",child)
        # random index to mutate upon
        mutation_point = randint(0, self.each_size-1)
        print("mutation point:",mutation_point)
        # mutate according to probability
        if random() < self.mutation_prob:
            # mutate child
            child[mutation_point] = 1 - child[mutation_point]
        
        return child
    
    def output(self):
        print("last agent:", self.pop)
        print("is goal reached? ",self.is_goal_reached())
        print("number of iterations: ",self.curr_gen)

    def is_goal_reached(self):
        for key, val in self.pop_scores.items():
            if(val != self.goal):
                return False
            
        return True

        
def main():
    print("hi, im main")
    g = Genetic(5, 1, 200, 1)
    g.create()
    g.iterate()
    g.output()

if __name__ == "__main__":
    main()
        