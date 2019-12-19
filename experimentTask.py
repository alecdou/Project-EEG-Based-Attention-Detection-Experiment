import psychopy
from psychopy import visual, core, sound, event
import random
import logging
import time

class Tasks:
    """
    The Tasks object contains multiple tasks that might need to be performed during experiments.
    Args:
        win (object): display window created using psychopy
        path (str): the path to the logging file
        taskList (list): the list of tasks to be performed
    Attributes:
        win (object): display window created using psychopy
        path (str): the path to the logging file
        taskList (list): the list of tasks to be performed
    """

    def __init__(self, win, path, taskList):
        self.win = win
        self.path = path
        self.taskList = taskList

    def counting_down(self, start, interval):
        """Count down.
        Args:
            start (int): the starting number
        """
        countingMSG = visual.TextStim(self.win, height=0.3)
        for i in range(start, 0, -1):
            countingMSG.text = i
            countingMSG.color = (1, 1, 1)
            countingMSG.draw()
            self.win.flip()
            core.wait(interval)

    def fixture(self):
        line1 = visual.ShapeStim(self.win, units='', lineWidth=5, lineColor='white', lineColorSpace='rgb', fillColor=None,
                  fillColorSpace='rgb', vertices=((-0.2, 0), (0.2, 0), (-0.2, 0), (0.2, 0)))
        line2 = visual.ShapeStim(self.win, units='', lineWidth=5, lineColor='white', lineColorSpace='rgb', fillColor=None,
                  fillColorSpace='rgb', vertices=((0, 0.2), (0, -0.2), (0, 0.2), (0, -0.2)))
        line1.draw()
        line2.draw()
        self.win.flip()

    def artifact_activity(self, instruction, label, iteration):
        """Function for displaying artifact activities.
                Args:
                    instruction (str): instruction of a specific task
                    label (int): label of the corresponding task
                    iteration (int): the no. of iteration of a task
                Returns:
                    None
                """
        msg = visual.TextStim(self.win, text=instruction, height=0.1)  # display instructions
        msg.draw()
        self.win.flip()

        event.waitKeys()  # wait for user response to start the task
        logging.info("%.3f\t%d\t%s starts", time.time(), label, self.taskList[label])

        countingMSG = visual.TextStim(self.win, text="READY!", height=0.3, colorSpace='rgb', color=(1, 0, 0))

        # 3 seconds for each trial, each trial is repeated by "iteration" times
        # 1s of rest between each trial
        # at round 1.5s, the user performs the task
        # user has up to 1.5s to finish the task
        for count in range(1, iteration+1):
            countingMSG.text = "Round " + str(count)
            countingMSG.draw()
            self.win.flip()
            core.wait(1)

            logging.info('%.3f\t%d\t%d_starts', time.time(), label, count)
            self.counting_down(3, 0.5)
            alarm = sound.backend_sounddevice.SoundDeviceSound(value=1200, secs=0.1, name='s')
            alarm.play()

            core.wait(1.5)
            logging.info('%.3f\t%d\t%d_ends', time.time(), label, count)

        self.win.flip()
        logging.info("%.3f\t%d\t%s ends", time.time(), label, self.taskList[label])

    def stroop_task(self, instruction, label, duration):
        """Function for displaying Stroop Task.
        Args:
            instruction (str): instruction displayed on the screen;
            label (int): label of stroop_task;
            duration (float): set the duration of stroop task (each trial is pre-set to 4 seconds)
        """

        msg = visual.TextStim(self.win, text=instruction, height=0.1, colorSpace='rgb', color=(1, 1, 1))
        msg.draw()
        self.win.flip()
        event.waitKeys()    # click to continue

        self.counting_down(3, 0.5)
        logging.info("%.3f\t%d\t%s_starts", time.time(), label, self.taskList[label])  # log of the start of Stroop Task

        colorList = [('red', (1, 0, 0)), ('green', (0, 1, 0)), ('blue', (0, 0, 1)), ('yellow', (1, 1, 0))]
        textList = ["red", "green", "blue", "yellow"]
        startingTime = time.time()

        stim = visual.TextStim(self.win, text="", height=0.5, colorSpace='rgb', color=(1, 1, 1))
        optionLeft = visual.TextStim(self.win, text="", height=0.1, colorSpace='rgb', color=(1, 1, 1), pos=(-0.8, -0.8))
        optionRight = visual.TextStim(self.win, text="", height=0.1, colorSpace='rgb', color=(1, 1, 1), pos=(0.8, -0.8))

        trialCount = 0
        while time.time() <= startingTime + duration:
            trialStart = time.time()  # the starting time of the trial
            logging.info('%.3f\t%d\t%d_starts', trialStart, label, trialCount)
            # display fixture for 0.5 second
            self.fixture()
            alarm = sound.backend_sounddevice.SoundDeviceSound(value=1200, secs=0.1, name='s')
            alarm.play()
            core.wait(0.5)
            fixtureTime = time.time()  # the time when the fixture is displayed
            logging.info('%.3f\t%d\t%d_fixtureDisplayed', fixtureTime, label, trialCount)

            # display options
            choices = [0, 1, 2, 3]
            colorChoice = random.choice(choices)
            choices.remove(colorChoice)
            textChoice = random.choice(choices)
            colorDisplayed = colorList[colorChoice]
            textDispalyed = textList[textChoice]
            stim.text = textDispalyed
            stim.color = colorDisplayed[1]

            option = [textDispalyed, colorDisplayed[0]]
            leftText = random.choice(option)
            option.remove(leftText)
            optionLeft.text = leftText
            rightText = option[0]
            optionRight.text = rightText

            stim.draw()
            optionLeft.draw()
            optionRight.draw()
            self.win.flip()

            logging.info('\t\t\t\t\tdisplay:(%s, %s)\toption:(%s, %s)', colorDisplayed[0],
                         textDispalyed, leftText, rightText)

            keyboard = event.waitKeys(maxWait=2)
            pressTime = time.time()  # the time when user press the keyboard

            try:
                if keyboard[0] == 'left':
                    userResponse = leftText
                else:
                    userResponse = rightText

                logging.info("%.3f\t%d\tuserResponse = %s\t", pressTime, label,
                             userResponse)

                if userResponse == colorDisplayed[0]:
                    msg.text = "CORRECT!"
                    msg.color = (0, 1, 0)
                else:
                    msg.text = "WRONG!"
                    msg.color = (1, 0, 0)
            except:
                msg.text = "TOO SLOW!"
                msg.color = (1, 0, 0)
                logging.info("%.3f\t%d\tuserResponse = %s", pressTime, label, "None")

            msg.height = 0.2
            msg.draw()
            self.win.flip()
            logging.info("%.3f\t%d\t%s_ends", time.time(), label,
                         self.taskList[label])
            core.wait(1)  # 4 seconds each trial

    def sart(self, instruction, label, duration):
        msg = visual.TextStim(self.win, text=instruction, height=0.1, colorSpace='rgb', color=(1, 1, 1))
        msg.draw()
        self.win.flip()
        event.waitKeys()  # click to continue

        self.counting_down(3, 0.5)

        logging.info("%.3f\t%d\t%s_starts", time.time(), label, self.taskList[label])  # log of the start of SART

        stim = visual.TextStim(self.win, text="", height=0.5, colorSpace='rgb', color=(1, 1, 1))
        startingTime = time.time()

        randomTime = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
        trialCount = 0
        while time.time() < startingTime + duration:
            trialStart = time.time()
            logging.info("%.3f\t%d\t%d_start", trialStart, label, trialCount)

            stim.text = 0
            stim.draw()
            self.win.flip()
            core.wait(random.choice(randomTime))
            alarmTime = time.time()

            alarm = sound.backend_sounddevice.SoundDeviceSound(value=1200, secs=0.1, name='s')
            alarm.play()
            logging.info("%.3f\t%d\t%d_alarm", time.time(), label, trialCount)

            number = 1
            event.clearEvents()
            while time.time() - alarmTime < 2:
                keyPress = event.getKeys()
                stim.text = number
                stim.draw()
                self.win.flip()

                if len(keyPress) > 0:
                    pressTime = time.time()
                    logging.info("%.3f\t%d\tuserPress", pressTime, label)
                    break
                number += 1
            if len(keyPress) == 0:
                logging.info("%.3f\t%d\tnoPress", time.time(), label)
            core.wait(1)
            trialCount += 1
        event.clearEvents()
        logging.info("%.3f\t%d\t%s_ends", time.time(), label, self.taskList[label])

    def flanker_task(self, instruction, label, duration):
        """Function for displaying Flanker Task.
            Args:
                instruction (str): instruction to be displayed on the screen
                label (int): label of Flanker Task
                duration (float): set the duration of Flanker Task session
        """
        msg = visual.TextStim(self.win, text=instruction, height=0.1, colorSpace='rgb', color=(1, 1, 1))
        msg.draw()
        self.win.flip()
        event.waitKeys()  # click to continue
        self.counting_down(3, 0.5)  # count down from 3 to 1

        startTime = time.time()  # the starting time of the session
        logging.info('%.3f\t%d\t%s starts', time.time(), label, self.taskList[label])
        event.clearEvents()

        orientation = [0, 180]
        position = [(-0.4, 0), (-0.2, 0), (0, 0), (0.2, 0), (0.4, 0)]

        trialCount = 0
        while time.time() < startTime + duration:

            shapeList = []  # generate 5 stimulus
            for i in range(5):  # generate 5 arrows
                shape = visual.ShapeStim(
                    self.win,
                    fillColorSpace='rgb', fillColor=(1, 1, 1),
                    vertices=([-2, 0.5], [0.5, 0.5], [0.5, 1.5], [2, 0], [0.5, -1.5], [0.5, -0.5], [-2, -0.5])
                )
                shapeList.append(shape)

            trialStart = time.time()  # the starting time of the trial
            logging.info('%.3f\t%d\t%d_starts', trialStart, label, trialCount)

            # display fixture for 0.5 second
            self.fixture()
            alarm = sound.backend_sounddevice.SoundDeviceSound(value=1200, secs=0.1, name='s')
            alarm.play()
            core.wait(0.5)
            fixtureTime = time.time()  # the time when the fixture is displayed
            logging.info('%.3f\t%d\t%d_fixtureDisplayed', fixtureTime, label, trialCount)

            ori1 = random.choice(orientation)
            ori2 = random.choice(orientation)
            while ori2 == ori1:
                ori2 = random.choice(orientation)
            for i in range(len(shapeList)):  # draw all 5 stimulus on the screen
                shapeList[i].size = 0.03
                shapeList[i].pos = position[i]
                if i == 2:
                    shapeList[i].ori = ori2
                else:
                    shapeList[i].ori = ori1
                shapeList[i].draw()
            self.win.flip()

            keyboard = event.waitKeys(maxWait=2)
            pressTime = time.time()  # the time when user responds

            if ori2 == 0:
                correct_key = 'right'
            else:
                correct_key = 'left'

            try:
                if keyboard.pop() == correct_key:
                    shapeList[2].colorSpace = 'rgb'
                    shapeList[2].color = (0, 1, 0)
                    logging.info('%.3f\t%d\tcorrectPress', pressTime, label)
                else:

                    shapeList[2].color = (1, 0, 0)
                    logging.info('%.3f\t%d\tfalsePress', pressTime, label)
            except:
                shapeList[2].color = (1, 0, 0)
                logging.info('%.3f\t%d\tnoPress', pressTime, label)
            shapeList[2].draw()
            self.win.update()
            core.wait(1)
            trialCount += 1

        logging.info('%.3f\t%d\t%d_ends', time.time(), label, self.taskList[label])

    def follow_dots(self, instruction, label, duration, attention=True):
        msg = visual.TextStim(self.win, text=instruction, height=0.1, colorSpace='rgb', color=(1, 1, 1))
        msg.draw()
        self.win.flip()
        event.waitKeys()  # click to continue

        self.counting_down(3, 0.5)

        logging.info("%.3f\t%d\t%s_starts", time.time(), label, self.taskList[label])

        startTime = time.time()

        x_range = 1.7
        y_range = 0.9
        x = -x_range
        y = -y_range
        up = False
        down = False
        right = False
        left = False

        while True:
            if x <= -x_range and y <= -y_range:
                up = True
                down = False
                right = False
                left = False
            elif x <= -x_range and y >= y_range:
                up = False
                down = False
                right = True
                left = False
            elif x >= x_range and y >= y_range:
                up = False
                down = True
                right = False
                left = False
            elif x >= x_range and y <= -y_range:
                up = False
                down = False
                right = False
                left = True

            step = 0.05
            if up:
                y += step
            elif down:
                y -= step
            elif left:
                x -= step
            elif right:
                x += step

            # print(x, y)
            shape = visual.GratingStim(self.win, tex=None, mask='circle')  # circular grating
            shape.size = 0.1
            shape.pos = [x, y]

            if not attention:
                shape.color = (0, 0, 0)
            shape.draw()  # display the shape
            self.win.update()  # update the window

            speed = 0
            core.wait(speed)

            if (time.time() - startTime) >= duration:
                alarm = sound.backend_sounddevice.SoundDeviceSound(value=1200, secs=0.1, name='s')
                alarm.play()
                break

        logging.info("%.3f\t%d\t%s_ends", time.time(), label, self.taskList[label])

    def rest(self, duration):
        logging.info("%.3f\t%d\trest_starts", time.time(), -1)
        text = "Now you have " + str(duration) + " seconds to rest\nOr press any key to skip rest."
        msg = visual.TextStim(self.win, text=text, height=0.1, colorSpace='rgb', color=(1, 1, 1))
        msg.autoDraw = True
        msg.draw()
        self.win.flip()
        start_time = time.time()
        countingMSG = visual.TextStim(self.win, text=text, height=0.1, colorSpace='rgb', color=(1, 0, 0))
        countingMSG.pos = [0, -0.2]
        i = duration
        while time.time() - start_time <= duration:
            countingMSG.text = i
            i -= 1
            countingMSG.draw()
            self.win.flip()
            key = event.waitKeys(maxWait=1)
            if key is not None:
                break
        logging.info("%.3f\t%d\trest_ends", time.time(), -1)
        msg.autoDraw = False
        self.win.update()

    def eyeClose(self, instruction, label, duration, close=True):
        msg = visual.TextStim(self.win, text=instruction, height=0.1, colorSpace='rgb', color=(1, 1, 1))
        msg.draw()
        self.win.flip()
        event.waitKeys()  # click to continue

        start_time = time.time()

        self.counting_down(3, 0.5)
        logging.info("%.3f\t%d\t%s_starts", time.time(), label, self.taskList[label])
        if close:
            msg.text = 'Eye closed'
        else:
            msg.text = 'Eye Open'
        msg.autoDraw = True
        self.win.flip()
        countingMSG = visual.TextStim(self.win, text='', height=0.1, colorSpace='rgb', color=(1, 0, 0))
        countingMSG.pos = [0, -0.2]
        i = duration
        while time.time() - start_time <= duration+1:
            countingMSG.text = i
            i -= 1
            countingMSG.draw()
            self.win.flip()
            core.wait(1)
        msg.autoDraw = False
        self.win.flip()
        alarm = sound.backend_sounddevice.SoundDeviceSound(value=1200, secs=0.1, name='s')
        alarm.play()
        logging.info("%.3f\t%d\t%s_ends", time.time(), label, self.taskList[label])
        core.wait(1)