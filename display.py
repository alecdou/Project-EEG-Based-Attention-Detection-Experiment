import random
import time

from psychopy import visual, core, sound, event


DEFAULT_WINDOW = visual.Window([1366, 768], fullscr=False, viewScale=[768/1366, 1])
win = DEFAULT_WINDOW


def welcome_message():
    simple_message("Thanks for your participation")
    core.wait(3)
    simple_message("Please remain calm")
    core.wait(3)
    simple_message("Try to diminish body movement\nincluding hand and head movement")
    core.wait(3)
    simple_message("Try to reduce eye blinks during experiment tasks")
    core.wait(3)
    simple_message("We are about to start\nFocus on the screen")
    core.wait(3)


def ending_message():
    simple_message("The experiment has ended")
    core.wait(2)
    simple_message("Thanks again for your participation")
    core.wait(10)


def simple_message(text, height=0.1, color="White"):
    visual.TextStim(win, text=text, height=height, color=color, wrapWidth=2).draw()
    win.flip()


def count_down(start, end=0, interval=1, pos=(0, 0)):
    """Documentation here."""
    counting = visual.TextStim(win, text='', height=0.15, color="Green")
    for i in range(start, end, -1):
        counting.text = i
        counting.pos = pos
        counting.draw()
        win.flip()
        core.wait(interval)


def fixture():
    line1 = visual.ShapeStim(win, lineWidth=5, lineColor='White', vertices=((-0.2, 0), (0.2, 0), (-0.2, 0), (0.2, 0)))
    line2 = visual.ShapeStim(win, lineWidth=5, lineColor='White', vertices=((0, 0.2), (0, -0.2), (0, 0.2), (0, -0.2)))
    line1.draw()
    line2.draw()
    win.flip()


def instruction(text, color=(1, 1, 1), height=0.1):
    visual.TextStim(win, text=text, height=height, colorSpace='rgb', color=color).draw()
    win.flip()


def stroop_task(color_list):
    stimulus = visual.TextStim(win, text="", height=0.2)
    left_option = visual.TextStim(win, text="", height=0.1, pos=(-0.4, 0))
    right_option = visual.TextStim(win, text="", height=0.1, pos=(0.4, 0))

    # stimulus color & text
    random.shuffle(color_list)
    stimulus_color = color_list.pop()
    stimulus_text = color_list.pop()
    stimulus.text = stimulus_text
    stimulus.color = stimulus_color

    # left & right options
    selected_color = [stimulus_color, stimulus_text]
    random.shuffle(selected_color)
    left_option_text = selected_color.pop()
    left_option.text = left_option_text
    right_option_text = selected_color.pop()
    right_option.text = right_option_text

    stimulus.draw()
    left_option.draw()
    right_option.draw()
    win.flip()
    return stimulus_text, stimulus_color, left_option_text, right_option_text, time.time()


def play_alarm():
    alarm = sound.backend_sounddevice.SoundDeviceSound(value=1200, secs=0.1, name='s')
    alarm.play()


def flanker_task():
    orientation = [0, 180]
    position = [(-0.4, 0), (-0.2, 0), (0, 0), (0.2, 0), (0.4, 0)]
    shape_list = []  # generate 5 stimulus
    for i in range(5):  # generate 5 arrows
        shape = visual.ShapeStim(
            win, fillColor='White',
            vertices=([-2, 0.5], [0.5, 0.5], [0.5, 1.5], [2, 0], [0.5, -1.5], [0.5, -0.5], [-2, -0.5])
        )
        shape_list.append(shape)

    random.shuffle(orientation)
    ori_side = orientation.pop()
    ori_middle = orientation.pop()
    for i in range(len(shape_list)):  # draw all 5 stimulus on the screen
        shape_list[i].size = 0.03
        shape_list[i].pos = position[i]
        if i == 2:
            shape_list[i].ori = ori_middle
        else:
            shape_list[i].ori = ori_side
        shape_list[i].draw()
    win.flip()
    return ori_middle, time.time()


def dot(start_time, duration):
    x_range = 1.7
    y_range = 0.9
    x = -x_range
    y = -y_range
    up = False
    down = False
    right = False
    left = False

    while time.time() - start_time < duration:
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

        shape = visual.GratingStim(win, tex=None, mask='circle')  # circular grating
        shape.size = 0.1
        shape.pos = [x, y]
        speed = 0.0001
        shape.draw()
        win.flip()
        core.wait(speed)


def rest(start_time, duration):
    text = "Now you have " + str(duration) + " seconds to rest\nOr press any key to skip rest."
    text = visual.TextStim(win, text=text, height=0.1, color='White')
    text.autoDraw = True
    text.draw()
    win.flip()

    counting = visual.TextStim(win, text='', height=0.1, color='Green')
    counting.pos = [0, -0.2]
    i = duration
    while time.time() - start_time <= duration:
        counting.text = i
        i -= 1
        counting.draw()
        win.flip()
        key = event.waitKeys(maxWait=1)
        if key is not None:
            break
    text.autoDraw = False
    win.flip()


def eye_close(duration):
    text = visual.TextStim(win, text='', height=0.1, color='White')
    text.autoDraw = True
    text.text = 'Eye Closed'
    win.flip()

    count_down(duration, 0, 1, (0, -0.2))
    text.autoDraw = False
    win.flip()


def eye_open(duration):
    text = visual.TextStim(win, text='', height=0.1, color='White')
    text.autoDraw = True
    text.text = 'Eye Open'
    win.flip()

    count_down(duration, 0, 1, (0, -0.2))
    text.autoDraw = False
    win.flip()
