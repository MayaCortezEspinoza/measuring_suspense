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
The data is saved as a .csv file. As soon as there is a file with the results-file name in the directory ("results.csv"), new data will be appended (i.e. the data of all participants will be saved in the same file.)

These are the columns in which the data is saved: 
1. Index (of word rated for suspense)
2. **text** of word rated for suspense
3. number of word (same as index +1)
4. position_x and cumulative x: data about where the word was displayed on the screen
5. screen number: in which section was this word shown
6. paragraph: original paragraph index from the narrative that was rated
7. mean_value: most important column: what was the mean suspense rating for this word? (as the software is able to capture even more fine grained data, this one-value-per-word data is already an averaged value)
8. mean_screen_value: suspense value averaged over the whole 10 line section
9. : in milliseconds: how long did the participant take to rate this section for suspense (from the moment they started drawing)
10. screen starting time: as unix time stamp 
11. screen drawing time, time until next screen, mean screen time, max and min screen time additional properties calculated from the data (adjust to need)
12. all further columns: data from the questionnaires (first two: participant index and participant age)

Please contact me at maya.cortez-espinoza@uni-graz.at in case you encounter issues with the code or if you want to develop further versions with me. 

## Here are some improvement ideas for further versions:
- move up and down additionally or instead of zooming
- implementing a joystick for easier handling in experiments with kids
