from controller import Controller
from repository import repository
from userinterface import UI


def main():
    repo = repository()
    ctrl = Controller(repo)
    console = UI(ctrl)
    console.run()


main()