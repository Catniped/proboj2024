import easygame,numpy
class Archer:
    def __init__(self):
        self.damage = 20
        self.speed = 30
    def shoot(self,enemyxy,enemyspeed,enemyvector):
        target = (enemyxy[0] + enemyspeed * self.speed * enemyvector[0], enemyxy[1] + enemyspeed * self.speed * enemyvector[1])
        vector = easygame.rotate(vector,easygame.degrees(6))/numpy.linalg.norm(vector)
        return vector
    def projectile(position):
        vector = easygame.rotate(vector,easygame.degrees(6))/numpy.linalg.norm(vector)
        position += vector
        return position
class Mage:
    def __init__(self):
        self.damage = 20
        self.speed = 30
        self.placement = 0,0
    def shoot(self,enemyxy):
        self.placement += enemyxy[0] - self.placement[0],enemyxy[1] - self.placement[1]