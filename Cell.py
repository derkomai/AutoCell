import random
from Constants import *


class Cell:

    maxAge = cellMaxAge
    maxLifePoints = cellMaxLifePoints

    def __init__(self, team, row, col, parents=None):

        self.team = team
        self.row = row
        self.col = col
        self.age = 0

        if not parents:

            self.lifePoints = random.uniform(cellMinStartingLifeFactor * self.maxLifePoints, self.maxLifePoints)
            self.genes = {'wait': 0.0, 'move': 0.0, 'mate': 0.0, 'attack': 0.0, 'changeTeam': 0.0}

            weight = 0.0
            for gen in self.genes:
                self.genes[gen] = random.random()
                weight += self.genes[gen]

            for gen in self.genes:
                self.genes[gen] /= weight

        else:

            self.lifePoints = sum([p.lifePoints for p in parents]) / len(parents)

            weight = 0.0
            for gen in self.genes:
                self.genes[gen] = sum([p.lifegenes[gen] for p in parents]) / len(parents)
                weight += self.genes[gen]

            for gen in self.genes:
                self.genes[gen] /= float(weight)


    def isAlive(self):
        return self.lifePoints > 0 and self.age <= self.maxAge


    def normalizePosition(self, worldWidth, worldHeight):
        self.row = self.row % worldHeight
        self.col = self.col % worldWidth


    def selectAction(self, environment):

        self.age += 1
        actionSet = ['wait']

        if 'empty' in environment:
            actionSet.append('move')

            # Mating also needs empty space
            if 'friend' in environment:
                actionSet.append('mate')

        if 'foe' in environment:
            actionSet.append('attack')
            actionSet.append('changeTeam')

        weights=[self.genes[action] for action in actionSet]
        action = random.choices(actionSet, weights=weights, k=1)[0]

        targetPositions = []

        if action == 'wait':
            targetPositions.append(4) # 4 is the center of the environment, self
                                      # 0 1 2
                                      # 3 4 5
                                      # 6 7 8

        elif action in ['move', 'mate']:
            for i in range(len(environment)):
                if environment[i] == 'empty':
                    targetPositions.append(i)

        elif action in ['attack', 'changeTeam']:
            for i in range(len(environment)):
                if environment[i] == 'foe':
                    targetPositions.append(i)

        newPosition = random.choice(targetPositions)
        positionDelta = (int(newPosition / 3) - 1, newPosition % 3 - 1)

        return action, positionDelta