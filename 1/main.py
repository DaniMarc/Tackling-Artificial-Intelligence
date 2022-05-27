# import the pygame module, so you can use it
from multiprocessing.spawn import import_main_path
from pygame.locals import *
from random import randint

from Model.DMap import DMap
from Controller.Drone import Drone
from Model.Environment import Environment
from View.ViewClass import View

     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    v = View()
    v.start()