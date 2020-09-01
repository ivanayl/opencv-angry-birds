#manages the different modes of the game including the game modes
#the code for the opencv feature is included in this file

#Used graphics framework from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
#Used and edited image from https://fontmeme.com/images/Angry-Birds-Logo.jpg
#Used and edited image from https://i.pinimg.com/originals/92/7b/2c/927b2caca31fda5069f3116d424881c7.jpg
#Used and edited image from https://pbs.twimg.com/media/BFki7jaCcAIgTj3.png
#Used and edited image from https://www.angrybirdsnest.com/wp-content/uploads/2012/03/AngryBirdsNest-FAQ.jpg
#Used image from https://middle.pngfans.com/20190513/gx/angry-birds-slingshot-png-angry-birds-stella-clipa-9daf9b446dcfa636.jpg
#Used image from https://vignette.wikia.nocookie.net/angrybirds/images/d/d3/INGAME_BLOCKS_WOOD_1.png/revision/latest?cb=20110723175423
#Used image from https://vignette.wikia.nocookie.net/angrybirds/images/2/2b/INGAME_BLOCKS_STONE_1.png/revision/latest?cb=20110723175248
#Used image from https://www.spriters-resource.com/download/66439/

from cmu_112_graphics import *
from tkinter import *
from PIL import *
import random
import math
import cv2
import numpy as np
from Bird import RedBird, YellowBird
from Obstacles import Metal, Wood, flatMetal, flatWood, Pig

class Button(object):
    def __init__(self, mode, x, y, width, height, color, mouseOverColor, clickColor, text):
        self.x = x
        self.y = y
        self.mode = mode
        self.width = width
        self.height = height
        self.defaultColor = color
        self.color = color
        self.mouseOverColor = mouseOverColor
        self.text = text
        self.clickColor = clickColor
    
    def getBounds(self):
        x0 = self.x - self.width/2
        y0 = self.y - self.height/2
        x1 = x0 + self.width
        y1 = y0 + self.height
        return x0, y0, x1, y1
    
    def mouseInBounds(self, mX, mY):
        x0, y0, x1, y1 = self.getBounds()
        if mX >= x0 and mX <= x1 and mY >= y0 and mY <= y1:
            return True
    
    def go(self):
        if "One Tier" in self.text:
            self.mode.app.setActiveMode(self.mode.app.oneTier)
        elif "Two Tier" in self.text:
            self.mode.app.setActiveMode(self.mode.app.twoTier)
        else:
            self.mode.app.setActiveMode(self.mode.app.helpMode)

    def draw(self, canvas):
        x0, y0, x1, y1 = self.getBounds()
        canvas.create_rectangle(x0, y0, x1, y1, fill = self.color, width = 5)
        canvas.create_text(self.x, self.y, text = self.text)

class startScreenMode(Mode):
    def appStarted(mode):
        mode.bkgd = mode.loadImage("https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/20fa2328-7b87-4789-a45f-22a14b89394f/d63ystt-e22432f7-ee54-4906-b23c-f3f0de5775d7.png/v1/fill/w_1208,h_662,strp/_background_angry_birds_classic_title_screen_by_nikitabirds_d63ystt-pre.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9ODA2IiwicGF0aCI6IlwvZlwvMjBmYTIzMjgtN2I4Ny00Nzg5LWE0NWYtMjJhMTRiODkzOTRmXC9kNjN5c3R0LWUyMjQzMmY3LWVlNTQtNDkwNi1iMjNjLWYzZjBkZTU3NzVkNy5wbmciLCJ3aWR0aCI6Ijw9MTQ3MSJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.2C8CMO3XPKkavh-OTNKMt26uUyPGfGBS645VkD_2iUw")
        mode.bkgd = mode.bkgd.resize((mode.width, mode.height), Image.ANTIALIAS)
        clickColor = '#%02x%02x%02x' % (254, 200, 89)
        hoverColor = '#%02x%02x%02x' % (150, 206, 223)
        defaultColor = '#%02x%02x%02x' % (223, 239, 254)
        mode.oneTier = Button(mode, mode.width*3/8, mode.height*3/4, mode.width/10, mode.height/10, defaultColor, hoverColor, clickColor, "One Tier Mode")
        mode.twoTier = Button(mode, mode.width*5/8, mode.height*3/4, mode.width/10, mode.height/10, defaultColor, hoverColor, clickColor, "Two Tier Mode")
        mode.helpMode = Button(mode, mode.width*8/9, mode.height*7/8, mode.width/15, mode.height/20, hoverColor, clickColor, defaultColor, "Help")
        mode.title = mode.loadImage("../images/title.png")

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.bkgd))
        mode.oneTier.draw(canvas)
        mode.twoTier.draw(canvas)
        mode.helpMode.draw(canvas)
        canvas.create_image(mode.width/2, mode.height/4, image = ImageTk.PhotoImage(mode.title))

    def mousePressed(mode, event):
        if mode.oneTier.mouseInBounds(event.x, event.y):
            mode.oneTier.color = mode.oneTier.clickColor
            mode.oneTier.go()
        else:
            mode.oneTier.color = mode.oneTier.defaultColor
        if mode.twoTier.mouseInBounds(event.x, event.y):
            mode.twoTier.color = mode.twoTier.clickColor
            mode.twoTier.go()
        else:
            mode.twoTier.color = mode.twoTier.defaultColor
        if mode.helpMode.mouseInBounds(event.x, event.y):
            mode.helpMode.color = mode.helpMode.clickColor
            mode.helpMode.go()
        else:
            mode.helpMode.color = mode.helpMode.defaultColor
    
    def mouseMoved(mode, event):
        if mode.oneTier.mouseInBounds(event.x, event.y):
            mode.oneTier.color = mode.oneTier.mouseOverColor
        else:
            mode.oneTier.color = mode.oneTier.defaultColor
        if mode.twoTier.mouseInBounds(event.x, event.y):
            mode.twoTier.color = mode.twoTier.mouseOverColor
        else:
            mode.twoTier.color = mode.twoTier.defaultColor
        if mode.helpMode.mouseInBounds(event.x, event.y):
            mode.helpMode.color = mode.helpMode.mouseOverColor
        else:
            mode.helpMode.color = mode.helpMode.defaultColor
    
    def sizeChanged(mode):
        mode.bkgd = mode.bkgd.resize((mode.width, mode.height), Image.ANTIALIAS)
        mode.oneTier.x = mode.width*3/8
        mode.oneTier.y = mode.height*3/4
        mode.twoTier.x = mode.width*5/8
        mode.twoTier.y = mode.height*3/4
        mode.helpMode.x = mode.width*7/8
        mode.helpMode.y = mode.height*7/8

class HelpMode(Mode):
    def appStarted(mode):
        mode.bkgd = mode.loadImage("../images/help screen.jpg")
        mode.bkgd = mode.bkgd.resize((mode.width, mode.height), Image.ANTIALIAS)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.startScreenMode)

    def redrawAll(mode, canvas):
        font = "Courier 20"
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.bkgd))
    
    def sizeChanged(mode):
        mode.bkgd = mode.bkgd.resize((mode.width, mode.height), Image.ANTIALIAS)

class WinMode(Mode):
    def appStarted(mode):
        mode.bkgd = mode.loadImage("../images/win screen.png")
        mode.bkgd = mode.bkgd.resize((mode.width, mode.height), Image.ANTIALIAS)

    def keyPressed(mode, event):
        mode.app.oneTier = oneTierMode()
        mode.app.twoTier = twoTierMode()
        if mode.app.video:
            mode.app.capture = cv2.VideoCapture(0) 
        mode.app.setActiveMode(mode.app.startScreenMode)

    def redrawAll(mode, canvas):
        font = "Courier 20"
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.bkgd))
    
    def sizeChanged(mode):
        mode.bkgd = mode.bkgd.resize((mode.width, mode.height), Image.ANTIALIAS)

class LoseMode(Mode):
    def appStarted(mode):
        mode.bkgd = mode.loadImage("../images/lose screen.jpg")
        mode.bkgd = mode.bkgd.resize((mode.width, mode.height), Image.ANTIALIAS)

    def keyPressed(mode, event):
        mode.app.oneTier = oneTierMode()
        mode.app.twoTier = twoTierMode()
        if mode.app.video:
            mode.app.capture = cv2.VideoCapture(0) 
        mode.app.setActiveMode(mode.app.startScreenMode)

    def redrawAll(mode, canvas):
        font = "Courier 20"
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.bkgd))

class oneTierMode(Mode):
    def appStarted(mode):
        mode.bkgd = mode.loadImage("https://i.pinimg.com/564x/a5/29/f5/a529f594aab155e3de451e5c5b0f3e45.jpg")
        mode.bkgd = mode.bkgd.resize((mode.width, mode.height), Image.ANTIALIAS)
        mode.marginY = 90
        mode.marginX = 200
        mode.slingX = 175
        mode.slingY = 440
        mode.possiblePath = []
        mode.timer = 0
        mode.ball = False
        mode.ballx = None
        mode.bally = None
        mode.slingshot = mode.loadImage("../images/slingshot.png")
        mode.slingshot = mode.scaleImage(mode.slingshot, 1/2)
        mode.slingWidth, mode.slingHeight = mode.slingshot.size
        mode.bird = []
        redBird = RedBird(mode, mode.slingX, mode.slingY - mode.slingHeight/2)
        redBird.y += redBird.h/2
        mode.bird.append(redBird)
        mode.mouseX = mode.slingX
        mode.mouseY = mode.slingY - mode.slingHeight/2
        #wood and metal
        mode.woodSpacing = 84
        mode.woodShift = 23
        mode.wood = []
        startX = random.randint(mode.width/2, mode.width - mode.marginX)
        woodRange = (mode.width - startX)//mode.woodSpacing
        woodRange = random.randint(5, woodRange + 3)
        if woodRange%2 == 0:
            woodRange += 1
        for i in range(woodRange):
            yes = random.randint(0,1)
            if i%2 == 0:
                if yes == 0:
                    wood = Wood(mode, startX + mode.woodSpacing*(i/2), mode.height - mode.marginY - mode.woodShift*3/2, 1, "../images/small wood.png", [])
                    mode.wood.append(wood)
                else:
                    metal = Metal(mode, startX + mode.woodSpacing*(i/2), mode.height - mode.marginY - mode.woodShift*3/2, 1, "../images/metal block.png", [])
                    metal.h = mode.woodSpacing
                    metal.w = mode.woodShift
                    mode.wood.append(metal)
            elif i%2 != 0:
                if yes == 0:
                    flat = flatWood(mode, startX + mode.woodSpacing*(i/2), mode.height - mode.marginY - mode.woodSpacing, 1, "../images/flat wood.png", [])
                    mode.wood.append(flat)
                else:
                    metal = flatMetal(mode, startX + mode.woodSpacing*(i/2), mode.height - mode.marginY - mode.woodSpacing, 1, "../images/flat metal.png", [])
                    metal.w = mode.woodSpacing
                    metal.h = mode.woodShift
                    mode.wood.append(metal)
        
        for flat in mode.wood:
            if type(flat) == flatWood or type(flat) == flatMetal:
                for wood in mode.wood:
                    if type(wood) != flatWood and type(wood) != flatMetal:
                        if wood.x >= flat.x - flat.w/2 and wood.x <= flat.x + flat.w/2:
                            flat.objectBelow.append(wood)
        #pigs
        pigWidth = 50
        pigX = random.randint(mode.wood[0].x, mode.wood[0].x + pigWidth*3//4)
        mode.pigs = []
        numPigs = random.randint(1, woodRange - 3)
        numBirds = numPigs//2
        for j in range(numPigs):
            space = random.randint(pigWidth//2, pigWidth)
            pig = Pig(mode, pigX + space, mode.height - mode.marginY - mode.woodShift*3/2 - mode.woodSpacing, 1, "../images/piggy.png", [])
            for wood in mode.wood:
                if type(wood) == flatWood or type(wood) == flatMetal:
                    if pig.x >= wood.x - wood.w/2 and pig.x <= wood.x + wood.w/2:
                        pig.objectBelow = wood
            pigX += space
            mode.pigs.append(pig)
            if numBirds > 0:
                red = random.randint(0, 1)
                if red == 0:
                    bird = RedBird(mode, mode.slingX - 75 - 25*(numPigs - numBirds - 1), mode.slingY + mode.slingHeight/2)
                else:
                    bird = YellowBird(mode, mode.slingX - 75 - 25*(numPigs - numBirds - 1), mode.slingY + mode.slingHeight/2)
                numBirds -= 1
                bird.y -= bird.h/2
                mode.bird.append(bird)
                
    def mousePressed(mode, event):
        if mode.app.video == False:
            if mode.bird[0].launched == True:
                if type(mode.bird[0]) == YellowBird:
                    mode.bird[0].image = mode.bird[0].powerImage
                    mode.bird[0].accel = .3
                    mode.bird[0].mass *= 1.5
            if mode.bird[0].clickOnBird(event.x, event.y) == True and mode.bird[0].x == mode.slingX and mode.bird[0].y == mode.slingY - mode.slingHeight/2 + mode.bird[0].h/2:
                mode.bird[0].selected = True

    def dragged(mode, x, y):
        mode.bird[0].x = x
        mode.bird[0].y = y
        mode.possiblePath = []
        hypotenuse = mode.getHypotenuse(x, y)
        theta = mode.getTheta(x, y)
        for xPos in range(int(x), int(mode.bird[0].getHorizRange(hypotenuse/4, theta)) + int(x), 10):
            yPos = mode.bird[0].getYPosition(xPos, hypotenuse/4, theta)
            mode.possiblePath.append((xPos, yPos))
        mode.mouseX = x - mode.bird[0].w/2
        mode.mouseY = y + mode.bird[0].h

    def released(mode, x, y):
        if mode.bird[0].selected == True and mode.bird[0].launched == False:
            mode.bird[0].x = x
            mode.bird[0].y = y
            mode.bird[0].launched = True
            mode.bird[0].image = mode.bird[0].flyImage
            hypotenuse = mode.getHypotenuse(x, y)
            mode.bird[0].v0 = hypotenuse/5
            mode.bird[0].theta = mode.getTheta(x, y)
            mode.bird[0].timerFired()
        mode.possiblePath = []
        mode.mouseX = mode.slingX
        mode.mouseY = mode.slingY - mode.slingHeight/2

    def mouseDragged(mode, event):
        if mode.app.video == False:
            if mode.bird[0].selected == True and (abs(mode.slingX-event.x)<=150) and (abs(event.y - mode.slingY)<= 50):
                mode.dragged(event.x, event.y)

    def ballMoved(mode):
        frame1 = mode.app.capture.read()[1]
        frame2 = mode.app.capture.read()[1]
        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 164, 110])
        upper = np.array([255, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        mask2 = cv2.inRange(hsv2, lower, upper)
        res = cv2.bitwise_and(frame1, frame1, mask = mask)
        diff = cv2.absdiff(mask, mask2)
        blur = cv2.GaussianBlur(diff, (5, 5), 0)
        threshold = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)[1]
        dilated = cv2.dilate(threshold, None, iterations = 3)
        contours = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        for contour in contours:
            (x,y),radius = cv2.minEnclosingCircle(contour)
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(frame1,center,radius,(0,255,0),1)
            cv2.putText(frame1, str(int(x)) + ", " + str(int(y)), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(0,255,0),1)
            cv2.imwrite("../images/frame.jpg", frame1)
            return int(x), int(y)
        cv2.imwrite("../images/frame.jpg", frame1)
    
    def ballDragged(mode):
        if mode.ballx != None:
            x = (mode.ballx)//4
            y = (mode.bally)//4
            if mode.bird[0].selected == True:
                mode.dragged(mode.slingX - x, y + mode.slingY - mode.slingHeight//2)

    def ballReleased(mode):
        if mode.ball == False and mode.ballx != None:
            x = (mode.ballx)//4
            y = (mode.bally)//4
            mode.released(mode.slingX - x, y + mode.slingY - mode.slingHeight//2)

    def getHypotenuse(mode, x, y):
        return (((mode.slingX-x)**2 + (mode.slingY - mode.slingHeight/2 - y)**2)**0.5)

    def getTheta(mode, x, y):
        return math.asin(abs(mode.slingY - mode.slingHeight/2 - y)/(mode.getHypotenuse(x, y)*2))
    
    def mouseReleased(mode, event):
        if mode.app.video == False:
            mode.released(event.x, event.y)
    
    def drawDot(self, canvas, x, y):
        canvas.create_oval(x-5, y-5, x+5, y+5, fill = "white")

    def timerFired(mode):
        if len(mode.pigs) == 0:
            if mode.bird[0].launched == False:
                mode.timer += 1
                if mode.timer > 25:
                    if mode.app.video:
                        mode.app.capture.release()
                        cv2.destroyAllWindows()
                    mode.app.setActiveMode(mode.app.winMode)
            else:
                mode.bird[0].timerFired()
        elif len(mode.bird) > 0:
            if mode.bird[0].launched == False:
                if mode.app.video:
                    move = mode.ballMoved()
                    if move != None:
                        mode.ballx, mode.bally = move
                    if mode.ball:
                        mode.ballDragged()
                    else:
                        mode.ballReleased()
            mode.bird[0].timerFired()
            if mode.bird[0].imageChangeTimer > 20:
                mode.bird.pop(0)
                if len(mode.bird) > 0:
                    mode.bird[0].x = mode.slingX
                    mode.bird[0].y += mode.bird[0].h - mode.slingHeight
                    mode.bird[0].x0 = mode.slingX
                    mode.bird[0].y0 = mode.slingY - mode.slingHeight/2
                    mode.bird[0].imageChangeTimer = 0
        if len(mode.bird) == 0:
            mode.timer += 1
            if mode.timer > 20:
                if mode.app.video:
                    mode.app.capture.release()
                    cv2.destroyAllWindows()
                mode.app.setActiveMode(mode.app.loseMode)
        i = 0
        while i < len(mode.wood):
            wood = mode.wood[i]
            wood.timerFired()
            if len(mode.bird) > 0:
                wood.checkCollision(mode.bird[0])
            if wood.health < 0:
                mode.wood.pop(i)
            else:
                i+=1
        j = 0
        while j < len(mode.pigs):
            pig = mode.pigs[j]
            if pig.health < 0:
                mode.pigs.pop(j)
            else:
                if len(mode.bird) > 0 and pig.collided == False:
                    pig.checkCollision(mode.bird[0])
                pig.timerFired()
                j+=1

    def keyPressed(mode, event):
        if event.key == "r":
            mode.appStarted()
        elif event.key == "q":
            mode.app.setActiveMode(mode.app.startScreenMode)
        elif event.key == "Space":
            mode.ball = not mode.ball
            mode.bird[0].selected = True
        elif event.key == "Enter" and mode.app.video:
            if mode.bird[0].launched and type(mode.bird[0]) == YellowBird:
                mode.bird[0].image = mode.bird[0].powerImage
                mode.bird[0].accel = .5
                mode.bird[0].mass *= 1.5
        elif event.key == "q":
            mode.app.video = False
            mode.app.capture.release()
            cv2.destroyAllWindows()
        
    def redrawAll(mode, canvas):
        font = 'Arial 10 bold'
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.bkgd))
        for wood in mode.wood:
            wood.draw(canvas)
            if wood.collided:
                canvas.create_text(wood.x - wood.w, wood.y - wood.h, text = "HIT", font = font)
        for pig in mode.pigs:
            pig.draw(canvas)
            if pig.collided:
                canvas.create_text(pig.x - pig.w, pig.y - pig.h, text = "HIT", font = font)
        canvas.create_image(mode.slingX, mode.slingY, image = ImageTk.PhotoImage(mode.slingshot))
        for bird in mode.bird:
            bird.draw(canvas)
        for dot in mode.possiblePath:
            x, y = dot
            canvas.create_oval(x-1, y-1, x+1, y+1, fill = "white")
        canvas.create_line(mode.slingX, mode.slingY - mode.slingHeight/2, mode.mouseX, mode.mouseY, fill = "black", width = 20)
        if mode.app.video and mode.ball:
            frame = mode.loadImage("../images/frame.jpg")
            frame = frame.resize((400, 250), Image.ANTIALIAS)
            canvas.create_image(200, 125, image = ImageTk.PhotoImage(frame))
        
class twoTierMode(oneTierMode):
    def appStarted(mode):
        mode.bkgd = mode.loadImage("https://i.pinimg.com/564x/a5/29/f5/a529f594aab155e3de451e5c5b0f3e45.jpg")
        mode.bkgd = mode.bkgd.resize((mode.width, mode.height), Image.ANTIALIAS)
        mode.marginY = 90
        mode.marginX = 200
        mode.slingX = 175
        mode.slingY = 440
        mode.possiblePath = []
        mode.ball = False
        mode.ballx = None
        mode.bally = None
        mode.timer = 0
        mode.slingshot = mode.loadImage("../images/slingshot.png")
        mode.slingshot = mode.scaleImage(mode.slingshot, 1/2)
        mode.slingWidth, mode.slingHeight = mode.slingshot.size
        mode.bird = []
        redBird = RedBird(mode, mode.slingX, mode.slingY - mode.slingHeight/2)
        redBird.y += redBird.h/2
        mode.bird.append(redBird)
        mode.mouseX = mode.slingX
        mode.mouseY = mode.slingY - mode.slingHeight/2
        #wood and metal
        mode.woodSpacing = 84
        mode.woodShift = 23
        mode.wood = []
        mode.pigs = []
        startX = random.randint(mode.width/2, mode.width - mode.marginX)
        woodRange = (mode.width - startX)//mode.woodSpacing
        woodRange = random.randint(5, woodRange + 3)
        tierShift = 0
        numBirds = 0
        for tier in range(2):
            if woodRange%2 == 0:
                woodRange += 1
            for i in range(woodRange):
                yes = random.randint(0,1)
                if i%2 == 0:
                    if yes == 0:
                        wood = Wood(mode, startX + mode.woodSpacing*(i/2), mode.height - mode.marginY - mode.woodShift*3/2 - tierShift, tier + 1, "../images/small wood.png", [])
                        mode.wood.append(wood)
                    else:
                        metal = Metal(mode, startX + mode.woodSpacing*(i/2), mode.height - mode.marginY - mode.woodShift*3/2 - tierShift, tier + 1, "../images/metal block.png", [])
                        metal.h = mode.woodSpacing
                        metal.w = mode.woodShift
                        mode.wood.append(metal)
                elif i%2 != 0:
                    if yes == 0:
                        flat = flatWood(mode, startX + mode.woodSpacing*(i/2), mode.height - mode.marginY - mode.woodSpacing - tierShift, tier + 1, "../images/flat wood.png", [])
                        mode.wood.append(flat)
                    else:
                        metal = flatMetal(mode, startX + mode.woodSpacing*(i/2), mode.height - mode.marginY - mode.woodSpacing - tierShift, tier + 1, "../images/flat metal.png", [])
                        metal.w = mode.woodSpacing
                        metal.h = mode.woodShift
                        mode.wood.append(metal)
            #pigs
            pigWidth = 50
            pigX = random.randint(startX, startX + pigWidth*3//4)
            numPigs = random.randint(1 - tier, woodRange//2)
            numBirds += numPigs//2
            for j in range(numPigs):
                space = random.randint(pigWidth//2, pigWidth)
                pig = Pig(mode, pigX + space, mode.height - mode.marginY - mode.woodShift*3/2 - mode.woodSpacing - tierShift, tier + 1, "../images/piggy.png", [])
                for wood in mode.wood:
                    if type(wood) == flatWood or type(wood) == flatMetal:
                        if pig.x >= wood.x - wood.w/2 and pig.x <= wood.x + wood.w/2 and pig.y <= wood.y + wood.h/2:
                            pig.objectBelow = wood
                pigX += space
                mode.pigs.append(pig)
            if tier == 0:
                startX  = random.randint(startX, int(startX + (len(mode.wood)//2)*mode.woodSpacing//4))
                woodRange = random.randint(1, woodRange - 2)
                tierShift += mode.woodSpacing + mode.woodShift/2
                numBirds += woodRange//2
        i = numBirds
        while i > 0:
            red = random.randint(0, 1)
            if red == 0:
                bird = RedBird(mode, mode.slingX - 75 - 25*(numBirds - i), mode.slingY + mode.slingHeight/2)
                i-=1
            else:
                bird = YellowBird(mode, mode.slingX - 75 - 25*(numBirds - i), mode.slingY + mode.slingHeight/2)
                i -= 2
            bird.y -= bird.h/2
            mode.bird.append(bird)

        for flat in mode.wood:
            if type(flat) == flatWood or type(flat) == flatMetal:
                for wood in mode.wood:
                    if wood.tier == flat.tier:
                        if wood.x >= flat.x - flat.w/2 and wood.x <= flat.x + flat.w/2 and wood != flat and wood not in flat.objectBelow and wood.y - flat.y <= flat.h/2 + wood.h/2:
                            flat.objectBelow.append(wood)
            elif flat.tier > 1:
                for wood in mode.wood:
                    if wood.tier + 1 == flat.tier and (type(wood) == flatWood or type(wood) == flatMetal):
                        if flat.x >= wood.x - wood.w/2 and flat.x <= wood.x + wood.w/2 and wood != flat and wood not in flat.objectBelow:
                            flat.objectBelow.append(wood)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.startScreenMode = startScreenMode()
        app.oneTier = oneTierMode()
        app.twoTier = twoTierMode()
        app.helpMode = HelpMode()
        app.loseMode = LoseMode()
        app.winMode = WinMode()
        app.setActiveMode(app.startScreenMode)
        app.video = None
        while app.video == None or (app.video.lower() != "y" and app.video.lower() != "yes"
            and app.video.lower() != "n" and app.video.lower() != "no"):
            app.video = app.getUserInput('Do you want to use the camera as a controller? y/n')
        if app.video.lower() == "y" or app.video.lower() == 'yes':
            app.video = True
            app.capture = cv2.VideoCapture(0)   
        elif app.video.lower() == "n" or app.video.lower() == 'no':
            app.video = False
        app.timerDelay = 1
app = MyModalApp(width=1000, height=600)
