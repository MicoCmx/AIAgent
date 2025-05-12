import random

class IndependentBrain:
    def __init__(self, bot):
        self.bot = bot
        self.turningCount = 0
        self.movingCount = random.randint(50, 100)
        self.currentlyTurning = False
        self.steps = 0

    def thinkAndAct(self, x, y, sl, sr, count, agents):
        self.steps += 1

        avoid_result = self.bot.avoidOthers(agents)
        if avoid_result:
            return avoid_result

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
