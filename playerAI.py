import random
import time

import pygame

from player import *


class PlayerAI:
    def __init__(self):
        self.player = Player()
        self.dna = []
        self.createDNASequence()
        self.currentAllele = 0
        self.delay = 100000000000
        self.nextAct = time.time_ns() + self.delay

    def createDNASequence(self):
        # 0 - junk DNA - 80%
        # 1 - jump - 6%
        # 2 - move left - 7 &
        # 3 - move right - 7%

        for i in range(100):
            choice = random.randint(1, 100)
            if choice <= 80:
                self.dna.append(0)
            elif choice <= 86:
                self.dna.append(1)
            elif choice <= 93:
                self.dna.append(2)
            elif choice <= 100:
                self.dna.append(3)

    def act(self):
        if self.nextAct < time.time_ns():
            if self.dna[self.currentAllele] == 1:
                self.player.jump()
            elif self.dna[self.currentAllele] == 2:
                self.player.moveLeft()
            elif self.dna[self.currentAllele] == 3:
                self.player.moveRight()
            self.nextAct = time.time_ns() + self.delay
            self.currentAllele += 1
            print(str(self.currentAllele))

        return self.player.act()

    def draw(self, screen):
        self.player.draw(screen)

    def setMap(self, map):
        self.player.setMap(map)

    def getScore(self):
        return self.player.getScore()
