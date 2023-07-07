# -------------------------------------------------------------------------------------------------
# import required packages/libraries
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# A class for a Genetic Algorithm 
# -------------------------------------------------------------------------------------------------
from SnakeGame import *
import random
from statistics import mean

import matplotlib.pyplot as plt

class GeneticAlgorithm:

    #contador pais iguais
    countpi = 0
    #kescolher pai
    kselectp = 4 #4

    #numero de movimentos por individuo
    numMoves = 700 #700

    directs = ["RIGHT","LEFT","UP","DOWN"]
  
    # attributes
    population = []
    # number of Generations to execute
    numberOfGenerations = 250 #250
    # stop GA execution is no improvement is observed after some generations
    stopEarlyCriteria = 10
    # population size
    populationSize = 650 # 650
    # mutation rate
    mutationRate = 0.01 # 0.01
    # best individual(s) returned after the GA is executed
    bestIndividual = [0]
    # best fitness value(s) obtained by the best individuals 
    bestFitness = [-1000]
    
    medias = []
  
    # elitism?
    
    # constructor
    def __init__(self,seed):
       	random.seed(seed)
        pass
    
    # generate the initial population
    def generateInitialPopulation(self):
      
      pop = [["RIGHT"] *self.numMoves] * self.populationSize
      for ind in range(0,self.populationSize):
        pop[ind] = random.choices(self.directs, k=self.numMoves)
      return pop
    
    # fitness function to evaluate an individual
    def fitnessFunction(self, moves):
        #executa movimentos com velocidade multiplicada
        game = SnakeGame(moves, 100,s=False)
        fit = game.run()+2000#Impedir de fitness ficar negativo
        if fit < 0:
          fit = 10
        return fit
    
    # receive an individual and evaluate its fitness
    def evaluateIndividual(self, moves):
        return self.fitnessFunction(moves)
    
    # Seleciona por campeonato
    def selectParents(self,pop,fits, kp = 3):
        
        pais = []
        #ROLETA
        #pais = random.choices(pop, weights=fits, k=kp)
        #return pais[0], pais[1]
      
        #CAMPEONATO
        #Escolhe primeiro pai
        candidatos1 = random.choices(pop, k=kp)
        fitsc = []
        for c in candidatos1:
          fitsc.append(fits[pop.index(c)])
        #print(fits.index(max(fitsc)))
        pais.append(pop[fits.index(max(fitsc))])
	
	
        #Escolhe segundo pai
        candidatos2 =  random.choices(pop, k=kp)
        fitsc = []
        for c in candidatos2:
          fitsc.append(fits[pop.index(c)])
      
        pais.append(pop[fits.index(max(fitsc))])
        #print(fits.index(max(fitsc)))

        return pais[0], pais[1]
    
    # given two parents, generate two children recombining them
    def generateChildren(self,p1,p2):
        f1 = []
        f2 = []
        if p1 == p2:
          self.countpi+=1
          p2.reverse()
        for i in range(0,self.numMoves):
          chance = random.randint(0,1)
          if chance > 0:
            f1.append(p1[i])
            f2.append(p2[i])
          else:
            f1.append(p2[i])
            f2.append(p1[i])
        
        return f1,f2
    
    # selects an individual and apply a mutation
    def mutationOperator(self, ind, chance):
      #(1)Testa para todos as posições
      for i in range(0,self.numMoves):
        randc = random.randint(0,100)
        if randc <= chance * 100:
        #(2)Testa chance e realiza mutação em um gene
        #randc = random.randint(0,100)
        #if randc <= chance * 100:
      
        #(3)pega genes baseados na chance
        #for i in range(0, int(chance*self.numMoves)):
          
          #escolhe posição aleatóriao para mutação
          h = random.randint(0,self.numMoves-1)

          #Altera o valor atual colocando um novo aleatório
          ind[h] = random.choices(self.directs, k=1)
        return ind

    # run GA
    def execute(self):
      #Gera população inicial
      self.population = self.generateInitialPopulation()

      #Abre arquivo para salvar valores
      f = open("Melhores_individuos.txt", "a")
      
      self.bestFitness[0] = 0
      #calcula fitness de toda a população
      Popfitness = [0] * self.populationSize
      for i in range(0,self.populationSize):
        Popfitness[i]= self.evaluateIndividual(self.population[i])
        #print(i)
        #print(Popfitness[i])
        #salva melhor individuo
        if Popfitness[i] > self.bestFitness[0]:
          self.bestFitness[0] = Popfitness[i]
          self.bestIndividual[0] = self.population[i]

      #Mostra melhor fitness da primeira geração
      game = SnakeGame(self.bestIndividual[-1], 2, s = False)
      game.run() 

      #Guarda media da primeira população
      self.medias.append(mean(Popfitness))

      cStop = 0#Contador para fitness igual
      #critério de parada: criar todas as gerações
      for g in range(0,self.numberOfGenerations):

        #Sistema para parar antes caso fique repetindo o melhor fitness
        if g > 1 and self.bestFitness[g-1] == self.bestFitness[g-2]:
          cStop+=1
        else:
          cStop = 0
        if cStop == self.stopEarlyCriteria:
          print("<Stop Early>")
          break

        
        print(g)
        self.countpi = 0
        #Gera nova população
        newPop = []
        for i in range(0, int(self.populationSize/2)):
          #Escolhe pais
          p1, p2 = self.selectParents(self.population,Popfitness, kp= self.kselectp)
          
          #Gera filhos dos pais escolhidos
          f1, f2 = self.generateChildren(p1,p2)

          #Chance de mutação para ambos os filhos
          f1 = self.mutationOperator(f1,self.mutationRate)
          f2 = self.mutationOperator(f2,self.mutationRate)

          #Adiciona filhos a população
          newPop.append(f1)
          newPop.append(f2)
        #Sobrescreve população anterior
        self.population = newPop

        #Adiciona nova posição para salvar o melhor resultado desta geração
        self.bestFitness.append(-1000)
        self.bestIndividual.append([])
        #Recalcula os fitness para a nova população
        for i in range(0,self.populationSize):
          Popfitness[i]= self.evaluateIndividual(self.population[i])
          #print(i)
          #print(Popfitness[i])
          #Encontra o melhor individuo desta população
          if Popfitness[i] > self.bestFitness[-1]:
            self.bestFitness[-1] = Popfitness[i]
            self.bestIndividual[-1] = self.population[i]
        print("Media: ",str(mean(Popfitness)))
        self.medias.append(mean(Popfitness))
        print("Melhor fit desta geração: ",str(self.bestFitness[-1]))
        print("Pais iguais:",self.countpi)
        #Mostra melhor fitness desta geração
        #game = SnakeGame(self.bestIndividual[-1], 1)
        #game.run()
      
      #Mostra melhor fitness de todos
      input("Quer ver o melhor?")
      indm = self.bestFitness.index(max(self.bestFitness))
      game = SnakeGame(self.bestIndividual[indm], 1)
      print("Geração do melhor: ",str(indm))
      print("Fitness do melhor: ",str(max(self.bestFitness)))
      game.run()
      
      #Grava no arquivo
      f.write("Tam pop: ",str(self.populationSize)," numMoves: ",str(self.numMoves), " numGeracoes: ",str(self.numberOfGenerations))
      f.write("\nMelhor fitness: "+ str(max(self.bestFitness)))
      f.write("\nSequencia de movimentos: "+str(self.bestIndividual[indm]))
      #Fecha arquivo
      f.close()

      #plotar dados
      plt.plot(self.bestFitness,label="Melhores Individuos")
      plt.plot(self.medias, label="Media gerações")

      
      #Configurações gráfico
      plt.xlabel('Geracao')
      plt.ylabel('Fitness')
      plt.legend()
      
      #Salvar gráfico
      plt.savefig('MelhoresPorGeracao.png')

      #Mostrar gráfico
      plt.show()
      #fechar ferramenta de plotar gráfico
      plt.close()
      #print(self.bestIndividual[self.bestFitness.index(max(self.bestFitness))])
      
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------