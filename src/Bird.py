#contains the OOP for the birds and half of the physics of the game (physics from bird's perspective/reference)

#Used graphics framework from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
#Used image from https://www.clipartwiki.com/clipimg/detail/52-521448_d-sprites-pinterest-and-all-angry-birds.png
#Used image from https://vignette.wikia.nocookie.net/angrybirds/images/2/2b/INGAME_BLOCKS_STONE_1.png/revision/latest?cb=20110723175248
#Used image from https://vignette.wikia.nocookie.net/angrybirds/images/d/d3/INGAME_BLOCKS_WOOD_1.png/revision/latest?cb=20110723175423

from cmu_112_graphics import *
from tkinter import *
from PIL import *
import random
import math

class Projectile(object):
    def __init__(self, mode, x0, y0, theta):
        self.x0 = x0
        self.y0 = y0
        self.x = x0
        self.y = y0
        self.tempX = self.y
        self.tempY = self.y
        self.v0 = 0
        self.theta = theta
        self.mode = mode
        self.width = 50
        self.timer = 0
        self.height = 50
        self.collisionV0 = 0
        self.collisionV1 = 0
        self.collided = False
        self.gravity = 9.8
        self.accel = 0
        self.imageChangeTimer = 0
    
    def getHorizVelocity(self):
        return self.v0*math.cos(self.theta) + self.accel*self.timer

    def timerFired(self):
        if self.launched == True:
            self.timer+=1
            position = self.getCurrPosition()
            self.x = self.tempX
            self.y = self.tempY
            if position == None:
                self.launched = False
                self.selected = False
        if self.collided == True or self.y >= self.mode.height - self.mode.marginY - self.h/2:
            self.imageChangeTimer += 1
            
    def getHorizRange(self, v0 = None, theta = None):
        if v0 == None and theta == None:
            horizRange = (self.v0**2)*math.sin(2*self.theta)/2
        else:
            horizRange = (v0**2)*math.sin(2*theta)/2
        return horizRange
    
    def getCurrVertVelocity(self):
        seconds = self.timer
        currVertVelocity = self.v0*math.sin(self.theta) - self.gravity*seconds/100
        return currVertVelocity
    
    def hypotheticHorizVel(self, v0, theta):
        return v0*math.cos(theta)
    
    def hypotheticVertVel(self, seconds, v0, theta):
        currVertVelocity = v0*math.sin(theta) - self.gravity*seconds/100
        return currVertVelocity
    
    def getCurrPosition(self):
        seconds = self.timer
        x = self.x0 + self.getHorizVelocity()*seconds/4
        y = self.y0 - self.getCurrVertVelocity()*seconds + (1/2)*(self.gravity)*((seconds/100)**2)
        if y <= self.mode.height - self.mode.marginY - self.h/5:
            self.tempX = x
            self.tempY = y
            return (x, y)
    
    def getTime(self, xPos):
        return 4*(xPos - self.x)/(self.getHorizVelocity())
        
    def getYPosition(self, xPos, v0, theta):
        seconds = 4*(xPos - self.x)/(self.hypotheticHorizVel(v0, theta))
        y = self.y - self.hypotheticVertVel(seconds, v0, theta)*seconds + (1/2)*(self.gravity)*((seconds/100)**2)
        return y
    
    def getKineticEnergy(self, currX):
        seconds = self.getTime(currX)
        currVertVel = self.hypotheticVertVel(seconds, self.v0, self.theta)
        vertKE = (1/2)*self.mass*(currVertVel**2)
        horizKE = (1/2)*self.mass*(self.getHorizVelocity()**2)
        return (horizKE, vertKE)
    
    def getMomentum(self, currX):
        seconds = self.getTime(currX)
        vertMomentum = self.mass*self.hypotheticVertVel(seconds, self.v0, self.theta)
        horizMomentum = self.mass*self.getHorizVelocity()
        return (horizMomentum, vertMomentum)

class Bird(Projectile):
    def __init__(self, mode, x, y):
        self.mode = mode
        super().__init__(mode, x, y, 0)
        self.mass = 7
        self.selected = False
        self.launched = False
        
    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.image))
    
    def clickOnBird(self, mouseX, mouseY):
        if mouseX >= self.x - self.w/2 and mouseX <= self.x + self.w/2:
            if mouseY >= self.y - self.h/2 and mouseY <= self.y + self.h/2:
                return True
        return False
    
    def timerFired(self):
        super().timerFired()
        if self.y >= self.mode.height - self.mode.marginY - self.h/2:
            self.image = self.collideImage
    
class RedBird(Bird):
    def __init__(self, mode, x, y):
        super().__init__(mode, x, y)
        
        self.image = mode.loadImage("../images/redbird.png")
        self.w, self.h = self.image.size
        self.flyImage = mode.loadImage("../images/red bird fly.png")
        self.collideImage = mode.loadImage("../images/red bird collide.png")

class YellowBird(Bird):
    def __init__(self, mode, x, y):
        super().__init__(mode, x, y)
        self.image = self.mode.loadImage("../images/yellow bird.png")
        self.w, self.h = self.image.size
        self.flyImage = self.mode.loadImage("../images/yellow bird fly.png")
        self.collideImage = self.mode.loadImage("../images/yellow bird collided.png")
        self.powerImage = self.mode.loadImage("../images/yellow bird fast.png")
        self.mass = 9
    
class Obstacle(object):
    def __init__(self, mode, x0, y0, imageURL, tier, objectBelow = None):
        self.mode = mode
        self.img = self.mode.loadImage(imageURL)
        self.fallImg = self.img
        self.w, self.h = self.img.size
        self.x = x0
        self.y = y0
        self.collisionV0 = 0
        self.collisionV1 = 0
        self.objectBelow = objectBelow
        self.collided = False
        self.fallDirection = 1
        self.impactAngle = 0
        self.grassFriction = 2
        self.woodFriction = .7
        self.fall = False
        self.fallTier = False
        self.gravity = 9.8
        self.tier = tier
        self.timer = 0
        
    def getBounds(self):
        x0 = self.x - self.w/2
        y0 = self.y - self.h/2
        x1 = x0 + self.w
        y1 = y0 + self.h
        return x0, y0, x1, y1

    def checkCollision(self, other):
        x0, y0, x1, y1 = self.getBounds()
        if other.x >= x0 - other.w/4 and other.x <= x1 + other.w/4 and other.y >= y0 and other.y <= y1 + other.h/4:
            self.collided = True
            self.collisionV0, self.collisionV1 = self.moveBack(other)
            self.impactAngle = self.getImpactAngle(other)
            self.objectBelow = []
            other.collided = True
            other.image = other.collideImage
            self.checkFall(other)
            return True
        return False 
    
    def solveQuadraticEquation(self, a, b, c):
        x0 = (-b + (b**2 - 4*a*c)**0.5)/(2*a)
        x1 = (-b - (b**2 - 4*a*c)**0.5)/(2*a)
        return (x0, x1)
    
    def quadraticABC(self, otherMass, horizKE, vertKE, horizMomentum, vertMomentum):
        aX = (self.mass**2) + (self.mass)*(otherMass)
        bX = (-1)*(self.mass**2)*horizMomentum
        cX = (horizMomentum**2) - otherMass*horizKE

        aY = (self.mass**2) + (self.mass)*(otherMass)
        bY = (-1)*(self.mass*2)*vertMomentum
        cY = (vertMomentum**2) - otherMass*vertKE
        return (aX, bX, cX, aY, bY, cY)
        
    def moveBack(self, other):
        horizKE, vertKE = other.getKineticEnergy(other.x)
        vertKE *= 2
        horizKE *= 2
        horizMomentum, vertMomentum = other.getMomentum(other.x)
        a, b, c, a1, b1, c1 = self.quadraticABC(other.mass,  horizKE, vertKE, horizMomentum, vertMomentum)
        (myV0, myV1) = self.solveQuadraticEquation(a, b, c)
        (myV3, myV4) = self.solveQuadraticEquation(a1, b1, c1)
        if myV0 == 0:
            myV0 = myV1
        if myV3 == 0:
            myV3 = myV4
        return (myV0, myV3)
    
    def getImpactAngle(self, other):
        adj = other.getCurrVertVelocity()
        opp = other.getHorizVelocity()
        return math.atan(opp/adj)
    
    def fallDown(self):
        if self.fall:
            if self.y <= self.mode.height - self.mode.marginY - self.h//2:
                dist = (1/2)*self.gravity*((self.timer/10)**2)
                self.y += dist
                if self.img != self.fallImg:
                    self.img = self.fallImg
                    temp = self.w
                    self.w = self.h
                    self.h = temp
        elif self.fallTier:
            dist = (1/2)*self.gravity*((self.timer/10)**2)
            self.y += dist
            if self.img != self.fallImg:
                self.img = self.fallImg
                temp = self.w
                self.w = self.h
                self.h = temp
    
    def timerFired(self):
        self.collidedMove(self.woodFriction)
        if self.fall == True or self.fallTier:
            self.timer += 1
            self.fallDown()
        else:
            for wood in self.objectBelow:
                if (wood not in self.mode.wood):
                    self.fall = True
                elif wood.fall or wood.collided:
                    self.fall = True
                if wood.y - self.y > wood.h/2 + self.h/2:
                    self.fall = True
                elif abs(wood.x - self.x) > self.h/2:
                    self.fall = True
            self.timer = 0

    def checkFall(self, other):
        impactForce = other.mass*other.gravity
        impactForce = math.sin(math.pi/4 - self.impactAngle)*impactForce
        normalForce = self.mass*self.gravity
        if impactForce > normalForce:
            self.fall = True
        if self.tier > 1:
            self.fallTier = True
        self.health -= impactForce
    
    def collidedMove(self, friction):
        if self.collided:
            self.timer += 1
            self.x += self.collisionV0/10
            normalForce = self.mass*self.gravity
            frictionForce = friction*normalForce
            accel = frictionForce/2
            self.collisionV0 += accel*(-1)
            if self.collisionV0 < 0:
                self.collisionV0 = 0
                self.collided = False

class Metal(Obstacle):
    def __init__(self, mode, x0, y0, tier, imageUrl, objectBelow = None):
        super().__init__(mode, x0, y0, imageUrl, tier, objectBelow)
        self.mass = 10
        self.health = 10
        self.fallImg = self.mode.loadImage("../images/flat metal.png")
        
    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.img))
    
    def __repr__(self):
        return f"Metal : x = {self.x}, y = {self.y}"
    
    def __eq__(self, other):
        return type(other) == Metal and self.health == other.health and self.mass == other.mass and self.x == other.x and self.y == other.y

class flatMetal(Metal):
    def __eq__(self, other):
        return type(other) == flatMetal and self.health == other.health and self.mass == other.mass and self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"Flat Metal: x = {self.x}, y = {self.y}"

    def timerFired(self):
        self.collidedMove(self.woodFriction)
        if self.fall == True or self.fallTier:
            self.timer += 1
            self.fallDown()
        else:
            for wood in self.objectBelow:
                if (wood not in self.mode.wood):
                    self.fall = True
                elif wood.fall == True:
                    self.fall = True
                elif wood.y - self.y > wood.h/2 + self.h/2:
                    self.fall = True
                elif abs(wood.x - self.x) > self.w/2:
                    self.fall = True
            self.timer = 0
    
    def fallDown(self):
        if self.y <= self.mode.height - self.mode.marginY - self.h/2:
            dist = (1/2)*self.gravity*((self.timer/10)**2)
            self.y += dist

class Wood(Obstacle):
    def __init__(self, mode, x0, y0, tier, imageUrl, objectBelow = None):
        super().__init__(mode, x0, y0, imageUrl, tier, objectBelow)
        self.mass = 7
        self.health = 5
        self.fallImg = self.mode.loadImage("../images/flat wood.png")
        
    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.img))
    
    def __repr__(self):
        return f"Wood : x = {self.x}, y = {self.y}"
    
    def __eq__(self, other):
        return type(other) == Wood and self.health == other.health and self.mass == other.mass and self.x == other.x and self.y == other.y

class flatWood(Wood):
    def __eq__(self, other):
        return type(other) == flatWood and self.health == other.health and self.mass == other.mass and self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"Flat Wood: x = {self.x}, y = {self.y}"

    def timerFired(self):
        self.collidedMove(self.woodFriction)
        if self.fall == True:
            self.timer += 1
            self.fallDown()
        else:
            for wood in self.objectBelow:
                if (wood not in self.mode.wood):
                    self.fall = True
                elif wood.fall == True:
                    self.fall = True
                elif wood.y - self.y > wood.h/2 + self.h/2:
                    self.fall = True
                elif abs(wood.x - self.x) > self.w/2:
                    self.fall = True
            self.timer = 0
    
    def fallDown(self):
        if self.y <= self.mode.height - self.mode.marginY - self.h/2:
            dist = (1/2)*self.gravity*((self.timer/10)**2)
            self.y += dist

class Pig(Obstacle):
    def __init__(self, mode, x, y, tier, imageUrl, objectBelow = None):
        super().__init__(mode, x, y, imageUrl, tier, objectBelow)
        self.img = self.mode.scaleImage(self.img, 1/2)
        self.w, self.h = self.img.size
        self.health = 50
        self.mass = 3

    def timerFired(self):
        self.collidedMove(self.woodFriction)
        if self.fall == True:
            self.timer += 1
            self.fallDown()
        else:
            wood = self.objectBelow
            if (wood not in self.mode.wood) or wood.y - wood.h/2 - self.y > self.h/2 or abs(wood.x - self.x) > wood.w/2:
                self.fall = True
            self.timer = 0
    
    def fallDown(self):
        if self.y <= self.mode.height - self.mode.marginY - self.h//2:
            dist = (1/2)*self.gravity*((self.timer/10)**2)
            self.y += dist
        else:
            self.fall = False
            self.health -= self.mass*self.gravity/10
    
    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.img))
