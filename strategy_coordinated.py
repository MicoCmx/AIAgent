import random
import math
from core_components import Dirt

class CoordinatedBrain:
    def __init__(self, bot, shared_map):
        self.bot = bot
        self.shared_map = shared_map
        self.steps = 0
        self.currentlyTurning = False
        self.movingCount = random.randint(40, 80)
        self.turningCount = 0

    def is_near_wall(self, obj, margin=40):
        x, y = obj.getLocation()
        return x < margin or x > 990 - margin or y < margin or y > 990 - margin

    def thinkAndAct(self, x, y, sl, sr, count, agents):
        self.steps += 1

        grid_x = int(self.bot.x // 10)
        grid_y = int(self.bot.y // 10)
        if 0 <= grid_x < 100 and 0 <= grid_y < 100:
            self.shared_map[grid_y, grid_x] = 1

        avoid_result = self.bot.avoidOthers(agents)
        if avoid_result:
            return avoid_result

        reachable_dirt = [obj for obj in self.bot.passiveObjects
                          if isinstance(obj, Dirt) and not self.is_near_wall(obj)]
        closest = None
        min_dist = float('inf')
        for obj in reachable_dirt:
            dist = self.bot.distanceTo(obj)
            if dist < min_dist:
                min_dist = dist
                closest = obj

        if closest:
            tx, ty = closest.getLocation()
            angle = math.atan2(ty - self.bot.y, tx - self.bot.x)
            self.bot.theta = angle + random.uniform(-0.1, 0.1)

        if self.currentlyTurning:
            speedLeft = -2.0
            speedRight = 2.0
            self.turningCount -= 1
        else:
            speedLeft = 5.0
            speedRight = 5.0
            self.movingCount -= 1

        if self.movingCount <= 0 and not self.currentlyTurning:
            self.turningCount = random.randint(20, 40)
            self.currentlyTurning = True
        if self.turningCount <= 0 and self.currentlyTurning:
            self.movingCount = random.randint(50, 100)
            self.currentlyTurning = False

        return speedLeft, speedRight, None, None
