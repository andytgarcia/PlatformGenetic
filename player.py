import pygame

class Player:
    def __init__(self):
        self.x = 400
        self.y = 400
        self.width = 30
        self.height = 30
        self.color = (255, 0, 0)
        self.isJumping = False
        self.maxjumpVel = 40
        self.currentJumpVel = 40

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


    def setMap(self, map):
        self.map = map

    def handleKeyPresses(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.isJumping:
            self.isJumping = True


    def act(self):
        oldx = self.x
        oldy = self.y


        self.handleKeyPresses()
        self.handleJump()
        self.y -= self.map.getGravity()
        if self.isMapCollision():
            self.x = oldx
            self.y = oldy
            self.isJumping = False
            self.currentJumpVel = self.maxjumpVel


    def handleJump(self):
        if self.isJumping:
            self.y -= self.currentJumpVel
            self.currentJumpVel += self.map.getGravity()
            # terminal velocity
            if self.currentJumpVel < - self.maxjumpVel:
                self.currentJumpVel = - self.maxjumpVel



    def getPlayerRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def isMapCollision(self):
        myHitBox = self.getPlayerRect()
        mapHitBoxes = self.map.getHitBoxList()
        for box in mapHitBoxes:
            if myHitBox.colliderect(box):
                return True

        return False

class Platform:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.getRect())

class Map:
    def __init__(self, gravity=-.5):
        self.platforms = []
        self.gravity = gravity

    def getGravity(self):
        return self.gravity

    def setGravity(self, gravity):
        self.gravity = gravity

    def add(self, platform):
        self.platforms.append(platform)

    def getPlatformsList(self):
        return self.platforms


    def getHitBoxList(self):
        hitBoxes = []
        for p in self.platforms:
            hitBoxes.append(p.getRect())

        return hitBoxes

    #precondition, the platforms list is a homogenous list of Platform objects
    def draw(self, screen):
        for p in self.platforms:
            p.draw(screen)