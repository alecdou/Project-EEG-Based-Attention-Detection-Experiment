import display
import logs
import tasks
import random

DATABASE = {
    "FT": {"description": "flanker task",
           "label": 1,
           "instruction": "You will need the left and the right arrow keys on the keyboard for this task\n"
                          "5 arrows will be displayed on the screen, "
                          "and you need to press the one that is different from the majority\n"
                          "Try to react as FAST as possible and REDUCE your body movement as MUCH as possible\n\n"
                          "Press blank space to start"},
    "FDA": {"description": "follow dot attention",
            "label": 2,
            "instruction": "There will be a moving white dot being displayed on the screen\n"
                           "Try to follow its path\n"
                           "Try to REDUCE your body movement and eye blinking as much as possible\n\n"
                           "Press blank space to start"},
    "FDD": {"description": "follow dot distraction",
            "label": 3,
            "instruction": "Move your eyes the same way as you did when you saw the white dot\n"
                           "That is, to move your eyes around the screen\n"
                           "Try to REDUCE your body movement and eye blinking as much as possible\n\n"
                           "Press blank space to start"},
    "ST": {"description": "stroop task",
           "label": 4,
           "instruction": "You will need the keyboard for this task\n"
                          "There will be a COLORED word being displayed on the screen\n"
                          "Try to identify its COLOR (not the word) as quickly as possible\n"
                          "Left arrow and right arrow represent two colors, which will be display on the screen\n"
                          "Press the corresponding arrow key on the keyboard\n\n"
                          "Press blank space to start"},
    "PVT": {"description": "pvt",
            "label": 5,
            "instruction": "You will need the blank space on keyboard for this task\n"
                           "Press the blank space when the number starts to change\n"
                           "Focus your attention on the screen and try to react as quickly as possible\n\n"
                           "Press blank space to start"},
    "EC": {"description": "eyes closed",
           "label": 6,
           "instruction": "Close your eyes and rest for 30 seconds until you hear a beep sound\n\n"
                          "Press blank space to start"},
    "EO": {"description": "eyes open",
           "label": 7,
           "instruction": "Open your eyes and rest for 30 seconds until you hear a beep sound\n\n"
                          "Press blank space to start"},
    "R": {"description": "rest",
          "label": -1,
          "instruction": "Take a short break for 30 seconds until you hear a beep sound\n\n"
                         "Press blank space to start"}
}

DURATION = 30
REST_TIME = 30
EYE_CO = ['EO', 'EC']
FLANKER = ['FT', 'FDD', 'FT', 'FDA', 'FT', 'FDD']
STROOP = ['ST', 'FDA', 'ST', 'FDD', 'ST', 'FDA']
PVT = ['PVT', 'FDD', 'PVT', 'FDA', 'PVT', 'FDD']
REST = ['R']
BLOCK_CHOICES = [FLANKER, STROOP, PVT, FLANKER, STROOP, PVT, FLANKER, STROOP, PVT]

TASK_LIST0 = ['EO', 'EC', 'FT', 'FDA', 'FDD', 'R', 'PVT', 'FDD', 'FDA', 'R', 'ST']


def get_task_list():
    random.shuffle(BLOCK_CHOICES)
    task_list = EYE_CO
    while len(BLOCK_CHOICES) > 0:
        task_list += BLOCK_CHOICES.pop()
        if len(BLOCK_CHOICES) != 0:
            task_list += REST
    return task_list


def get_instruction(task):
    return DATABASE[task]['instruction']


def get_label(task):
    return DATABASE[task]['label']


def run_tasks(task_list):
    for i in range(len(task_list)):
        task = task_list[i]
        instruction = get_instruction(task=task)
        label = get_label(task=task)
        if task == 'R':
            tasks.rest(instruction=instruction, label=label, duration=REST_TIME)
        elif task == 'FT':
            tasks.flanker_task(instruction=instruction, label=label, duration=DURATION)
        elif task == 'PVT':
            tasks.pvt(instruction=instruction, label=label, duration=DURATION)
        elif task == 'ST':
            tasks.stroop_task(instruction=instruction, label=label, duration=DURATION)
        elif task == 'FDA':
            tasks.follow_dots_attention(instruction=instruction, label=label, duration=DURATION)
        elif task == 'FDD':
            tasks.follow_dots_distraction(instruction=instruction, label=label, duration=DURATION)
        elif task == 'EC':
            tasks.eye_close(instruction=instruction, label=label, duration=DURATION)
        elif task == 'EO':
            tasks.eye_open(instruction=instruction, label=label, duration=DURATION)


def main():
    task_list = get_task_list()
    is_trial = input("Do you want to run the trial round? (Y/N)\t")

    if is_trial == 'Y':
        # trial round
        logs.experiment_log(database=DATABASE, task_list=TASK_LIST0)
        display.welcome_message()
        run_tasks(task_list=TASK_LIST0)
    else:
        # official round
        logs.experiment_log(database=DATABASE, task_list=task_list)
        display.welcome_message()
        run_tasks(task_list=task_list)
    display.ending_message()


if __name__ == '__main__':
    main()
