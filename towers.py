class Archer:
    def __init__(self):
        self.damage = 20
        self.speed = 30
    def shoot(self,enemyxy,enemyspeed,enemyvector):
        target = (enemyxy[0] + enemyspeed * self.speed * enemyvector[0], enemyxy[1] + enemyspeed * self.speed * enemyvector[1])
class Mage:
    def __init__(self):
        self.damage = 20
        self.speed = 30