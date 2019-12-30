from psychopy import core, event
import random
import logs
import time
import display


def session_starter(instruction, label):
    display.instruction(instruction)
    event.waitKeys()  # click to continue
    display.count_down(3)
    session_start = time.time()
    logs.session_log(session_start, label, "starts")
    return session_start


def rest_session_starter(instruction, label):
    display.instruction(instruction)
    display.count_down(3)
    session_start = time.time()
    logs.session_log(session_start, label, "starts")
    return session_start


def stroop_task(instruction, label, duration):
    """Function for displaying Stroop Task.
    Args:
        instruction (str): instruction displayed on the screen;
        label (int): label of stroop_task;
        duration (float): set the duration of stroop task (each trial is pre-set to 4 seconds)
    """
    session_start = session_starter(instruction, label)

    trial_count = 1
    while time.time() < session_start + duration:
        trial_start = time.time()  # the starting time of the trial
        logs.trial_log(trial_start, label, trial_count, "starts")
        # todo fixture time position
        # display fixture for 0.5 second
        display.play_alarm()
        display.fixture()
        # todo wait for a variable duration
        variable_duration_list = [0.3, 0.6, 0.9, 1.2]
        core.wait(random.choice(variable_duration_list))
        fixture_time = time.time()  # the time when the fixture is displayed
        logs.trial_log(fixture_time, label, trial_count, "fixture_displayed")

        # display options
        color_list = ['Red', 'Yellow', 'Blue', 'Green']
        text, color, left, right, stimulus_time = display.stroop_task(color_list)
        logs.trial_log(stimulus_time, label, trial_count, 'stimulus_displayed_'+text+"_text "+color+"_color")

        # fixed time out
        keyboard = event.waitKeys(maxWait=2)
        press_time = time.time()  # the time when user press the keyboard
        display.clear()
        answer = "wrong"
        try:
            user_response = keyboard[0]
            if user_response == 'left' and left == color:
                answer = "correct"
            elif user_response == 'right' and right == color:
                answer = "correct"
            logs.trial_log(press_time, label, trial_count, answer)
        except:
            answer = "np_press"

        event.clearEvents()
        reaction_time = press_time - stimulus_time
        logs.user_reaction_log(label, trial_count, reaction_time, answer)
        logs.trial_log(trial_start, label, trial_count, "ends")
        trial_count += 1
        core.wait(1)  # 4 seconds each trial

    session_end = time.time()
    logs.session_log(session_end, label, "ends")


def pvt(instruction, label, duration):
    session_start = session_starter(instruction, label)

    variable_duration_list = [0.3, 0.6, 0.9, 1.2]
    trial_count = 1
    while time.time() < session_start + duration:
        trial_start = time.time()  # the starting time of the trial
        logs.trial_log(trial_start, label, trial_count, "starts")
        display.simple_message('')
        core.wait(0.5)
        display.simple_message(0, 0.5)
        core.wait(random.choice(variable_duration_list))
        stimulus_time = time.time()
        display.play_alarm()
        logs.trial_log(stimulus_time, label, trial_count, "stimulus_displayed")

        timeout = 2
        number = 1
        event.clearEvents()
        while time.time() - stimulus_time < timeout:
            keys_pressed = event.getKeys()
            display.simple_message(number, 0.5)
            if len(keys_pressed) > 0:
                press_time = time.time()
                logs.trial_log(press_time, label, trial_count, "user_press")
                answer = "pressed"
                break
            number += 1
        # todo optimize key press capture
        if len(keys_pressed) == 0:
            press_time = time.time()
            logs.trial_log(press_time, label, trial_count, "no_press")
            answer = "no_press"
        reaction_time = press_time - stimulus_time
        logs.user_reaction_log(label, trial_count, reaction_time, answer)
        logs.trial_log(trial_start, label, trial_count, "ends")
        trial_count += 1
        core.wait(1)
        event.clearEvents()

    session_end = time.time()
    logs.session_log(session_end, label, "ends")


def flanker_task(instruction, label, duration):
    """Function for displaying Flanker Task.
        Args:
            instruction (str): instruction to be displayed on the screen
            label (int): label of Flanker Task
            duration (float): set the duration of Flanker Task session
    """
    session_start = session_starter(instruction, label)

    event.clearEvents()

    trial_count = 1
    while time.time() < session_start + duration:
        trial_start = time.time()  # the starting time of the trial
        logs.trial_log(trial_start, label, trial_count, "starts")

        display.play_alarm()
        display.fixture()
        variable_duration_list = [0.3, 0.6, 0.9, 1.2]
        core.wait(random.choice(variable_duration_list))
        fixture_time = time.time()  # the time when the fixture is displayed
        logs.trial_log(fixture_time, label, trial_count, "fixture_displayed")

        event.clearEvents()
        ori, stimulus_time = display.flanker_task()
        keyboard = event.waitKeys(maxWait=2)
        press_time = time.time()  # the time when user responds
        logs.trial_log(stimulus_time, label, trial_count, 'ori='+str(ori))
        display.clear()

        if ori == 0:
            correct_key = 'right'
        else:
            correct_key = 'left'

        try:
            if keyboard.pop() == correct_key:
                answer = "correct"
            else:
                answer = "wrong"
        except:
            answer = "no_press"

        logs.trial_log(press_time, label, trial_count, answer)
        reaction_time = press_time - stimulus_time
        logs.user_reaction_log(label, trial_count, reaction_time, answer)
        logs.trial_log(trial_start, label, trial_count, "ends")
        trial_count += 1
        core.wait(1)

    session_end = time.time()
    logs.session_log(session_end, label, "ends")


def follow_dots_attention(instruction, label, duration):
    session_start = session_starter(instruction, label)
    trial_start = session_start
    logs.trial_log(trial_start, label, 1, "starts")

    display.dot(session_start, duration)
    display.play_alarm()

    session_end = time.time()
    trial_end = session_end
    logs.session_log(session_end, label, "ends")
    logs.trial_log(trial_end, label, 1, "ends")


def follow_dots_distraction(instruction, label, duration):
    session_start = session_starter(instruction, label)
    trial_start = session_start
    logs.trial_log(trial_start, label, 1, "starts")

    while time.time() - session_start < duration:
        display.simple_message('')
    display.play_alarm()

    session_end = time.time()
    trial_end = session_end
    logs.session_log(session_end, label, "ends")
    logs.trial_log(trial_end, label, 1, "ends")


def eye_close(instruction, label, duration):
    session_start = session_starter(instruction, label)
    trial_start = session_start
    logs.trial_log(trial_start, label, 1, "starts")

    display.eye_close(duration)
    display.play_alarm()

    core.wait(1)
    session_end = time.time()
    trial_end= session_end
    logs.session_log(session_end, label, "ends")
    logs.trial_log(trial_end, label, 1, "ends")


def eye_open(instruction, label, duration):
    session_start = session_starter(instruction, label)
    trial_start = session_start
    logs.trial_log(trial_start, label, 1, "starts")

    display.eye_open(duration)
    display.play_alarm()

    core.wait(1)
    session_end = time.time()
    trial_end = session_end
    logs.session_log(session_end, label, "ends")
    logs.trial_log(trial_end, label, 1, "ends")


def rest(instruction, label, duration):
    session_start = rest_session_starter(instruction, label)
    display.rest(session_start, duration)
    session_end = time.time()
    logs.session_log(session_end, label, "ends")


