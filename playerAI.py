import random
import time

import pygame

from player import *

BLUE = (0, 0, 255)

class PlayerAI:
    def __init__(self):
        self.player = Player((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.dna = []
        self.alleleCount = 500
        self.createDNASequence()
        self.currentAllele = 0
        self.delay = 100_000_000
        self.nextAct = time.time_ns() + self.delay
        self.vx = 0
        self.forceX = 5
        self.worldForce = .5
        self.distance = 0




    def createDNASequence(self):
        # 0 - junk DNA - 80%
        # 1 - jump - 6%
        # 2 - move left - 7 &
        # 3 - move right - 7%

        for i in range(self.alleleCount):
            choice = random.randint(1, 100)
            if choice <= 80:
                self.dna.append(0)
            elif choice <= 86:
                self.dna.append(1)
            elif choice <= 93:
                self.dna.append(2)
            elif choice <= 100:
                self.dna.append(3)

    def isDone(self):
        return self.currentAllele == self.alleleCount

    def getCurrentAllele(self):
        return self.currentAllele

    def reset(self):
        self.currentAllele = 0
        self.player.setX(400)
        self.player.setY(150)
        self.player.score = 0

    def act(self):
        if self.nextAct < time.time_ns() and self.currentAllele < self.alleleCount:
            if self.dna[self.currentAllele] == 1:
                self.player.jump()
            elif self.dna[self.currentAllele] == 2:
                self.vx -= self.forceX
            elif self.dna[self.currentAllele] == 3:
                self.vx += self.forceX

            # add x velocity to x position
            if self.player.is_map_right_collision() and self.vx > 0:
                self.player.setX(self.player.getX())
            elif self.player.isMapLeftCollision() and self.vx < 0:
                self.player.setX(self.player.getX())
            else:
                self.player.setX(self.player.getX() + self.vx)
            if self.vx < 0:
                self.vx += self.worldForce
            elif self.vx > 0:
                self.vx -= self.worldForce

            self.nextAct = time.time_ns() + self.delay
            self.currentAllele = self.currentAllele + 1
            # print(str(self.currentAllele))

        self.distance = self.player.getX()
        return self.player.act()

    def draw(self, screen):
        self.player.draw(screen)

    def setMap(self, map):
        self.player.setMap(map)

    def getScore(self):
        return self.player.getScore()

    def getDNASequence(self):
        return self.dna

    def getDNAValue(self, index):
        for i in self.dna:
            if i == index:
                return self.dna[index]

