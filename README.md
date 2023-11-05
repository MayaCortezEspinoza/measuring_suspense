# measuring_suspense
This repository contains the software code developed by Edgar Onea and me and used in an experiment that measured narrative suspense in the Project "The erotetic and the aesthetic." in the University of Göttingen.
The main purpose of this program is to enable reading a narrative text while simultaneously drawing a suspense arc for the respective text. 
Therefore, its main functions are
- drawing with the mouse
- navigating through the text (in sections of 10 lines)

please be aware that this version is a prototype and the full potential of the design is far from exhausted. New versions will come. (right now, I am developing a more flexible and modular version that will be easier to use without figuring out the code as a whole 😎)

The programm is written with [python 3.10](https://www.python.org/downloads/release/python-3100/) and [pygame 2.5.2](https://www.pygame.org/news). and consists of three scripts: the experiment itself (which should be run as main) and two modules: auxiliaries.py and units.py. The question_window.py mudule builds a window with the Tkinter package that can be altered in case questionnaires should attached to the experiment.
There are questionnaires attached to the experiment right now, but they are in German (As you will not have the same questions as we did, I did not bother translating them.)

Right now, there is a training section attached to the front - it explains how the software works. Some screens in the training do not allow the drawing function and some do. 
Additionally,

## The data saved
The data is saved as a csv file

Please contact me at maya.cortez-espinoza@uni-graz.at in case you encounter issues with the code or if you want to develop further versions with me. 

## Here are some improvement ideas for further versions:
- move up and down additionally or instead of zooming
- implementing a joystick for easier handling in experiments with kids
