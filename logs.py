import logging
import time


filename = str(time.ctime(time.time())).replace(" ", "_").replace(':', "-")
session_logger = logging.getLogger('session_' + filename)
handler = logging.FileHandler('./data/SESSION/' + filename + '.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
session_logger.addHandler(handler)
session_logger.setLevel(logging.INFO)

experiment_logger = logging.getLogger('experiment_' + filename)
handler = logging.FileHandler('./data/EXPERIMENT/' + filename + '.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
experiment_logger.addHandler(handler)
experiment_logger.setLevel(logging.INFO)

trial_logger = logging.getLogger('trial_' + filename)
handler = logging.FileHandler('./data/TRIAL/' + filename + '.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
trial_logger.addHandler(handler)
trial_logger.setLevel(logging.INFO)

reaction_logger = logging.getLogger('reaction_' + filename)
handler = logging.FileHandler('./data/REACTION/' + filename + '.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
reaction_logger.addHandler(handler)
reaction_logger.setLevel(logging.INFO)


def experiment_log(database, task_list):
    message = ""
    message += time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n\n"
    for task in database.keys():
        message += task + "\t" + str(database[task]['label']) + "\t" + database[task]['description'] + "\n"
    message += '\n\n'
    for task in task_list:
        message += task + ' '
    experiment_logger.info(message)


def session_log(timing, session_label, status):
    message = "{:.3f}".format(timing) + '\t' + str(session_label) + '\t' + status
    session_logger.info(message)


def trial_log(timing, session_label, trial_no, status):
    message = "{:.3f}".format(timing) + '\t' + str(session_label) + '\ttrial_' + str(trial_no) + ' ' + status
    trial_logger.info(message)


def user_reaction_log(session_label, trial_no, reaction_time, remark=""):
    message = str(session_label) + '\t' + str(trial_no) + '\t' + "{:.3f}".format(reaction_time) + '\t' + remark
    reaction_logger.info(message)
