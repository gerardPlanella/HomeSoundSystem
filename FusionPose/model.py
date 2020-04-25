from tf_pose.estimator import BodyPart
from enum import Enum
class Model():
    def __init__(self, skeleton_points, name):
        self.skeleton_points = skeleton_points
        self.name = name
    
    
    def __str__(self):
        return 'Model: %s skeleton is [%s]' % (self.name,', '.join(map(str, self.skeleton_points)))

    def __repr__(self):
        return self.__str__()

    def checkSkeleton(self, newSkeleton):
        for point in self.skeleton_points:
            if point not in newSkeleton:
                #The skeleton provided dont have all the parts required.
                #print("Returing FALSE! Loooks like the point " + str(point) + " not in skeleton!") 
                return False
        return True     

    def isPointInsideModel(self,point):   
        return (point in self.skeleton_points)

    #Gets an BODY25 dictionary and translates it to a COCO one with BodyParts.
    @staticmethod
    def fromBodyToCoco(skeleton, img_w, img_h):
        result = {}
        i = 0
        for point in skeleton:
            if i == 8:
                i=i+1
                continue
            if i >= 19:
                break

            if point[2] != 0:
                if i > 8:
                    obj = BodyPart(0,i-1,point[0]/img_w,point[1]/img_h,point[2])
                    result.update({i-1:obj})
                else:
                    obj = BodyPart(0,i,point[0]/img_w,point[1]/img_h,point[2])
                    result.update({i:obj})
            i=i+1
        return result

    @staticmethod
    def skeletonFitsAModel(skeleton):
        return (Model.FULL_BODY().checkSkeleton(skeleton) or
            Model.FULL_BODY_NO_EARS().checkSkeleton(skeleton) or
            Model.LEFT_SIDE().checkSkeleton(skeleton) or 
            Model.RIGHT_SIDE().checkSkeleton(skeleton) or 
            Model.TORSO().checkSkeleton(skeleton) or
            Model.FULL_TORSO_LEGS().checkSkeleton(skeleton) or
            Model.LEFT_TORSO_LEGS().checkSkeleton(skeleton) or
            Model.RIGHT_TORSO_LEGS().checkSkeleton(skeleton))

    @staticmethod
    def isScoreAcceptable(skeleton,acceptanceValue):
        dataOk = True
        for bodyPart in skeleton.values():
            dataOk = dataOk and (bodyPart.score > acceptanceValue)
        return dataOk

    #Factory of dataset skeletons.
    @classmethod
    def FULL_BODY(cls):
        return cls([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], "FULL_BODY")    

    @classmethod
    def FULL_BODY_NO_EARS(cls):
        return cls([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], "FULL_BODY_NO_EARS")    

    @classmethod
    def LEFT_SIDE(cls):
        return cls([0, 1, 2, 3, 4, 8, 9, 10, 14, 16], "LEFT_SIDE")    

    @classmethod
    def RIGHT_SIDE(cls):
        return cls([0, 1, 5, 6, 7, 11, 12, 13, 15, 17], "RIGHT_SIDE")    

    @classmethod
    def TORSO(cls):
        return cls([0, 1, 8, 11], "TORSO")    

    @classmethod
    def FULL_TORSO_LEGS(cls):
        return cls([0, 1, 8, 9, 10, 11, 12, 13], "FULL_TORSO_LEGS")    

    @classmethod
    def LEFT_TORSO_LEGS(cls):
        return cls([0, 1, 8, 9, 10], "LEFT_TORSO_LEGS")    

    @classmethod
    def RIGHT_TORSO_LEGS(cls):
        return cls([0, 1, 11, 12, 13], "RIGHT_TORSO_LEGS")

    @classmethod
    def TEST_ADRIA(cls):
        return cls([0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15], "TEST_ADRIA")

class ModelEnum(Enum):
    FULL_BODY = 0
    FULL_BODY_NO_EARS = 1
    LEFT_SIDE = 2
    RIGHT_SIDE = 3
    TORSO = 4
    FULL_TORSO_LEGS = 5
    LEFT_TORSO_LEGS = 6
    RIGHT_TORSO_LEGS = 7
    TEST_ADRIA = 8

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(s):
        try:
            return ModelEnum[s]
        except KeyError:
            print("Key was " + str(s))
            raise ValueError()