import logging


def session_log(time, session_name, status, path):
    logging.basicConfig(filename='SESSION_'+path+'.log',
                        filemode='a',
                        level=logging.INFO,
                        format='%(message)s')
    message = "{:.3f}".format(time) + '\t' + session_name + '\t' + status
    logging.info(message)


def trial_log(time, session_name, trial_no, status, path):
    logging.basicConfig(filename='TRIAL_'+path+'.log',
                        filemode='a',
                        level=logging.INFO,
                        format='%(message)s')
    message = "{:.3f}".format(time) + '\t' + session_name + '\ttrial_' + trial_no + ' ' + status
    logging.info(message)


def user_reaction_log(session_name, trial_no, reaction_time, path, remark=""):
    logging.basicConfig(filename='REACTION_'+path+'.log',
                        filemode='a',
                        level=logging.INFO,
                        format='%(message)s')
    message = session_name + '\t' + trial_no + '\t' + "{:.3f}".format(reaction_time) + '\t' + remark
    logging.info(message)