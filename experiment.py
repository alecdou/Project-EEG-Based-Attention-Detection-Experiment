import psychopy
from psychopy import visual, core, sound, event
import time
import logging
from experimentTask import Tasks

dataBase = {
    "JC": {"description": "jaw clenching", "label": 0,
           "instruction": "You will need to clench your jaw once when we count down to 1\n"
                          "Please finish clenching your jaw in 1 second\n"
                          "Try to REDUCE your body movement and CONTROL eye blinking when performing the task\n\n"
                          "Press any key to start"},
    "JM": {"description": "jaw moving", "label": 1,
           "instruction": "You will need to move your jaw once when we count down to 1\n"
                          "Please finish moving your jaw in 1 second\n"
                          "Try to REDUCE your body movement and CONTROL eye blinking when performing the task\n\n"
                          "Press any key to start"},
    "EB": {"description": "eye blinking", "label": 2,
           "instruction": "You will need to blink your eyes once when we count down to 1\n"
                          "Please finish blinking in 1 second\n"
                          "Try to REDUCE your body movement when performing the task\n\n"
                          "Press any key to start"},
    "EL": {"description": "eye left", "label": 3,
           "instruction": "You will need to look to your left once when we count down to 1\n"
                          "Look at the center of the screen once finished\n"
                          "Please finish this task in 1 second\n"
                          "Try to REDUCE your body movement when performing the task\n\n"
                          "Press any key to start"},
    "ER": {"description": "eye right", "label": 4,
           "instruction": "You will need to look to your right once when we count down to 1\n"
                          "Look at the center of the screen once finished\n"
                          "Please finish this task in 1 second\n"
                          "Try to REDUCE your body movement when performing the task\n\n"
                          "Press any key to start"},
    "RH": {"description": "rotating head", "label": 5,
           "instruction": "You will need to rotate your head once when we count down to 1\n"
                          "Please finish this task in 1 second\n"
                          "Try to REDUCE your body movement except for head movement when performing the task\n"
                          "Also do NOT blink your eyes when performing this task\n\n"
                          "Press any key to start"},
    "NH": {"description": "nodding head", "label": 6,
           "instruction": "You will need to nod your head once when we count down to 1\n"
                          "Please finish nodding in 1 second\n"
                          "Try to REDUCE your body movement except for head movement when performing the task\n"
                          "Also do NOT blink your eyes when performing this task\n\n"
                          "Press any key to start"},
    "EU": {"description": "eye up", "label": 7,
           "instruction": "You will need to look up once when we count down to 1\n"
                          "Look at the center of the screen once finished\n"
                          "Please finish this task in 1 second\n"
                          "Try to REDUCE your body movement when performing the task\n\n"
                          "Press any key to start"},
    "ED": {"description": "eye right", "label": 8,
           "instruction": "You will need to look down once when we count down to 1\n"
                          "Look at the center of the screen once finished\n"
                          "Please finish this task in 1 second\n"
                          "Try to REDUCE your body movement when performing the task\n\n"
                          "Press any key to start"},

    "FT": {"description": "flanker task", "label": 9,
           "instruction": "You will need to use the left and right arrow keys on the keyboard for this task\n"
                          "5 arrows will be displayed on the screen, "
                          "and you need to press the one that is different from the majority using the keyboard\n"
                          "Try to react as FAST as possible and REDUCE your body movement as much as possible\n\n"
                          "Press any key to start"},
    "FDA": {"description": "follow dot (attention)", "label": 10,
            "instruction": "There will be a moving white dot being displayed on the screen\n"
                           "Try to look at it and follow its path\n"
                           "Try to REDUCE your body movement and eye blinking as much as possible\n"
                           "Ask the experimenter for help if there is anything unclear\n\n"
                           "Press any key to start"},
    "FDD": {"description": "follow dot (distraction)", "label": 11,
            "instruction": "Move your eyes the same way as you did when you see the white dot\n"
                           "That is, to move your eyes around the screen\n"
                           "Try to REDUCE your body movement and eye blinking as much as possible\n\n"
                           "Press any key to start"},
    "ST": {"description": "stroop task", "label": 12,
           "instruction": "You will need the keyboard for this task\n"
                          "There will be a COLORED word being displayed on the screen\n"
                          "Try to identify its COLOR (not the word) as quickly as possible\n"
                          "Left arrow and right arrow represent two colors, which will be display on the screen\n"
                          "Press the corresponding arrow key on the keyboard\n\n"
                          "Press any key to start"},
    "SART": {"description": "sart", "label": 13,
             "instruction": "You will need the blankspace key on keyboard for this task\n"
                            "Press the blank space when you hear a beep sound and the number starts to change\n"
                            "Focus your attention on the screen and try to react as quickly as possible\n\n"
                            "Press any key to start"},
    "EC": {"description": "eyes closed", "label": 14,
           "instruction": "Close your eyes and rest for 30 seconds until you hear a beep sound\n\n"
                          "Press any key to start"},
    "EO": {"description": "eyes open", "label": 15,
           "instruction": "Open your eyes and rest for 30 seconds until you hear a beep sound\n"
                          "Ask the experimenter for help if there is anything unclear\n\n"
                          "Press any key to start"},
    "R": {"description": "eyes open", "label": 16,
           "instruction": "Open your eyes and rest for 30 seconds until you hear a beep sound\n\n"
                          "Press any key to start"}
}
allTasks = []
for element in dataBase.keys():
    allTasks.append(element)

print("allTasks = ", allTasks)
artifactList = ['JC', 'JM', 'EB', 'EL', 'ER', 'RH', 'NH', 'EU', 'ED']
eyeCloseOpen = ['EO', 'EC']
flankerTaskSession = ['FT', 'FDD', 'FT', 'FDA', 'FT', 'FDD']
restSession = ['R']
stroopTaskSession = ['ST', 'FDA', 'ST', 'FDD', 'ST', 'FDA']
sartTaskSession = ['SART', 'SART', 'SART', 'SART', 'SART', 'SART', 'FDD', 'FDA']
# create a list of tasks
# otherTaskList = ['EC', 'EO', 'JC', 'JM', 'EB', 'EL', 'ER', 'RH', 'NH', 'EU', 'ED', 'R', 'FT', 'FDA', 'FT', 'FDA',
#            'FT', 'FDA', 'R', 'ST', 'FDD', 'ST', 'FDD', 'ST', 'FDD', 'R', 'SART']


taskList = eyeCloseOpen + flankerTaskSession + restSession + flankerTaskSession + restSession + \
           flankerTaskSession + restSession + stroopTaskSession + restSession + stroopTaskSession + restSession + \
           stroopTaskSession + restSession + sartTaskSession + sartTaskSession
# unique experiment name
path = 'experiment_test_1'

# set the screen size
win = visual.Window([1366, 768], fullscr=False, viewScale=[768/1366, 1])    # create a display window


logging.basicConfig(filename=path+'.log',
                    filemode='w',
                    level=logging.INFO,
                    format='%(message)s')

for element in dataBase.keys():
    logging.info('label: %d\ttask:%s\t%s', dataBase[element]['label'],
                 element, dataBase[element]['description'])

logging.basicConfig(filename=path+'.log',
                    filemode='a',
                    level=logging.INFO,
                    format='%(message)s')

logging.info('%.3f\t%d\t%s\n', time.time(), -1, path)


msg = visual.TextStim(win, text="Thanks for your participation", height=0.1)
msg.wrapWidth = 2   # display message in one line
msg.draw()
win.flip()
core.wait(3)

tasks = Tasks(win, path, taskList=allTasks)

"""
taskList = [element for element in dataBase.keys()]
for task in taskList:
    tasks.artifact_activity(dataBase[task]["instruction"], dataBase[task]['label'])
    breakAA
for i in range(1):
    tasks.flanker_task(dataBase["FT"]["instruction"], dataBase["FT"]["label"], 10)
    tasks.follow_dots(dataBase["FD"]["instruction"], dataBase["FD"]["label"], 10)
for i in range(1):
    tasks.sart(dataBase["SART"]['instruction'], dataBase["SART"]['label'], 10)
for i in range(1):
    tasks.stroop_task(dataBase["ST"]['instruction'], dataBase["ST"]['label'], 10)
"""


iteration = 2
duration = 3
restTime = 3

i = 0
while i < len(taskList):
    task = taskList[i]
    i += 1
    print(task)
    if task in artifactList:
        tasks.artifact_activity(dataBase[task]['instruction'], dataBase[task]['label'], iteration)
    elif task == 'R':
        tasks.rest(restTime)
    elif task == 'FT':
        tasks.flanker_task(dataBase[task]["instruction"], dataBase[task]["label"], duration)
    elif task == 'SART':
        tasks.sart(dataBase[task]["instruction"], dataBase[task]["label"], 60*5)
    elif task == 'ST':
        tasks.stroop_task(dataBase[task]["instruction"], dataBase[task]["label"], duration)
    elif task == 'FDA':
        tasks.follow_dots(dataBase[task]["instruction"], dataBase[task]["label"], duration, attention=True)
    elif task == 'FDD':
        tasks.follow_dots(dataBase[task]["instruction"], dataBase[task]["l"
                                                                        "abel"], duration, attention=False)
    elif task == 'EC':
        tasks.eyeClose(dataBase[task]['instruction'], dataBase[task]['label'], 30, close=True)
    elif task == 'EO':
        tasks.eyeClose(dataBase[task]['instruction'], dataBase[task]['label'], 30, close=False)