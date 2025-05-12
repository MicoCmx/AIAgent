import tkinter as tk
import random
import math

class Dirt:
    def __init__(self, name, x, y):
        self.centreX = x
        self.centreY = y
        self.name = name
        self.radius = 36

    def draw(self, canvas):
        canvas.create_oval(self.centreX - 1, self.centreY - 1,
                           self.centreX + 1, self.centreY + 1,
                           fill="grey", tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY

class Bot:
    def __init__(self, name, passiveObjects, counter, color="blue"):
        self.name = name
        self.x = random.randint(100, 900)
        self.y = random.randint(100, 900)
        self.theta = random.uniform(0, 2 * math.pi)
        self.ll = 60
        self.sl = 0.0
        self.sr = 0.0
        self.passiveObjects = passiveObjects
        self.counter = counter
        self.color = color
        self.sensorPositions = [0] * 16  # 8 sensors: 4 corners + 4 edges (relative)
        self.setBrain(None)
        self.cooldown = 0
        self.radius = 36

    def setBrain(self, brain):
        self.brain = brain

    def thinkAndAct(self, agents, passiveObjects):
        self.sl, self.sr, xx, yy = self.brain.thinkAndAct(
            self.x, self.y, self.sl, self.sr, self.counter.total_cleaned, agents)
        if xx is not None:
            self.x = xx
        if yy is not None:
            self.y = yy

    def update(self, canvas, passiveObjects, dt):
        self.move(canvas, dt)

    def move(self, canvas, dt):
        self.x += self.sl * math.cos(self.theta) * dt
        self.y += self.sl * math.sin(self.theta) * dt

        # Boundary checking and bouncing (considering square size)
        margin = 45
        bounced = False
        if self.x < margin:
            self.x = margin
            self.theta = math.pi - self.theta
            bounced = True
        elif self.x > 990 - margin:
            self.x = 990 - margin
            self.theta = math.pi - self.theta
            bounced = True
        if self.y < margin:
            self.y = margin
            self.theta = -self.theta
            bounced = True
        elif self.y > 990 - margin:
            self.y = 990 - margin
            self.theta = -self.theta
            bounced = True
        if bounced:
            self.theta += random.uniform(-0.2, 0.2)

        canvas.delete(self.name)
        self.draw(canvas)

    def getLocation(self):
        return self.x, self.y

    def overlapsWith(self, other, size=70):
        return (
            abs(self.x - other.x) < size and
            abs(self.y - other.y) < size
        )

    def draw(self, canvas):
        # Main body outline (keep original style)
        points = [(self.x + 30 * math.sin(self.theta)) - 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y - 30 * math.cos(self.theta)) - 30 * math.cos((math.pi / 2.0) - self.theta),
                  (self.x - 30 * math.sin(self.theta)) - 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y + 30 * math.cos(self.theta)) - 30 * math.cos((math.pi / 2.0) - self.theta),
                  (self.x - 30 * math.sin(self.theta)) + 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y + 30 * math.cos(self.theta)) + 30 * math.cos((math.pi / 2.0) - self.theta),
                  (self.x + 30 * math.sin(self.theta)) + 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y - 30 * math.cos(self.theta)) + 30 * math.cos((math.pi / 2.0) - self.theta)]
        canvas.create_polygon(points, fill=self.color, tags=self.name)

        # Center circle and wheels
        canvas.create_oval(self.x - 16, self.y - 16, self.x + 16, self.y + 16, fill="gold", tags=self.name)
        canvas.create_oval(self.x - 30 * math.sin(self.theta) - 3, self.y + 30 * math.cos(self.theta) - 3,
                           self.x - 30 * math.sin(self.theta) + 3, self.y + 30 * math.cos(self.theta) + 3,
                           fill="red", tags=self.name)
        canvas.create_oval(self.x + 30 * math.sin(self.theta) - 3, self.y - 30 * math.cos(self.theta) - 3,
                           self.x + 30 * math.sin(self.theta) + 3, self.y - 30 * math.cos(self.theta) + 3,
                           fill="green", tags=self.name)

        # 8 sensor points, fixed relative to robot orientation
        d = 30
        # Midpoints of four edges
        front = (self.x + d * math.cos(self.theta), self.y + d * math.sin(self.theta))
        back = (self.x - d * math.cos(self.theta), self.y - d * math.sin(self.theta))
        left = (self.x - d * math.sin(self.theta), self.y + d * math.cos(self.theta))
        right = (self.x + d * math.sin(self.theta), self.y - d * math.cos(self.theta))
        # Four corner points
        dx = d * math.cos(self.theta)
        dy = d * math.sin(self.theta)
        lx = d * math.sin(self.theta)
        ly = -d * math.cos(self.theta)
        fl = (self.x + dx + lx, self.y + dy + ly)
        fr = (self.x + dx - lx, self.y + dy - ly)
        bl = (self.x - dx + lx, self.y - dy + ly)
        br = (self.x - dx - lx, self.y - dy - ly)

        self.sensorPositions = [*fl, *fr, *bl, *br, *front, *back, *left, *right]

        for i in range(0, len(self.sensorPositions), 2):
            canvas.create_oval(self.sensorPositions[i] - 2, self.sensorPositions[i+1] - 2,
                               self.sensorPositions[i] + 2, self.sensorPositions[i+1] + 2,
                               fill="yellow", tags=self.name)

    def distanceTo(self,obj):
        xx,yy = obj.getLocation()
        return math.sqrt( math.pow(self.x-xx,2) + math.pow(self.y-yy,2) )

    def distanceToSensor(self, idx, lx, ly):
        return math.sqrt((lx - self.sensorPositions[idx])**2 + (ly - self.sensorPositions[idx+1])**2)


    def avoidOthers(self, agents):
        # Prioritize finding the nearest other robot
        nearest = None
        min_dist = float('inf')
        for other in agents:
            if other.name != self.name:
                dist = self.distanceTo(other)
                if dist < min_dist:
                    min_dist = dist
                    nearest = other

        # Smart avoidance: move away from the nearest bot
        if nearest and min_dist < 140:
            dx = self.x - nearest.x
            dy = self.y - nearest.y
            escape_angle = math.atan2(dy, dx) + random.uniform(-0.3, 0.3)
            self.theta = escape_angle
            return 5.0, 5.0, None, None

        return None

    def collectDirt(self, canvas, passiveObjects, count):
        toDelete = []
        for idx, rr in enumerate(passiveObjects):
            if isinstance(rr, Dirt):
                if self.distanceTo(rr) < 30:
                    canvas.delete(rr.name)
                    toDelete.append(idx)
                    count.itemCollected(canvas, self.name)
        for ii in sorted(toDelete, reverse=True):
            del passiveObjects[ii]
        return passiveObjects

def initialise(window):
    window.title("Multi-Agent Vacuum Cleaner")
    window.resizable(False, False)
    canvas = tk.Canvas(window, width=990, height=990, bg="white")
    canvas.pack()
    return canvas
