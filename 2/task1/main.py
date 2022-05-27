
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
from View.View import View
from Controller.Controller import Controller
from Model.Drone import Drone
from Model.Map import Map


if __name__=="__main__":
    # call the main function
    v = View()
    v.start()