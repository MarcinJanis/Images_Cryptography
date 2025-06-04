import cv2
import os

class ImageStorage:  
    instances = []  # List of all existing instances

    def __init__(self, img, name, img_type):  
        self.img = img
        self.name = name#os.path.basename(name)  
        self.size = img.shape
        self.type = img_type
        ImageStorage.instances.append(self)  #Add to instances list
        print(f'ImageStorage:: {self.name} added.')

    def __del__(self):
        print(f'ImageStorage:: {self.name} deleted.')

    def delete(self):  
        # Delete instance from list and memory
        if self in ImageStorage.instances:
            ImageStorage.instances.remove(self)
        del self  # Delete from memory

    @classmethod
    def imgList(cls):  
        #Reurn list of all existing instances
        return cls.instances
