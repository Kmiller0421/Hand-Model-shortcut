import math

class distance:
    def __init__(self) -> None:
        pass

    def point_distance(self, point_1, point_2):

        dis_formula = math.sqrt((point_2.x - point_1.x) ** 2 + (point_2.y - point_1.y) ** 2
                      + (point_2.z - point_1.z) ** 2)
        
        return dis_formula