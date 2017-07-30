import re
import time
from subprocess import Popen, PIPE



"""
Get all commit info

For each commit in the commit info:
    Add commit message to a final string
    Add changes to final string
    Add entire files that were changed to final string
"""

def call_sp(command, *args, **kwargs):
    """ you can run command from any directory you want by passing in a kwarg of 'cwd' (current working directory):

        call_sp('ls', '-a', cwd='/home/username/projects/awesomeproject')
    """
    if args:
        command = command.format(*args)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
    output, err = p.communicate()
    return output, err


def parse_git_log_info(text_output):
    # https://stackoverflow.com/questions/4697882/how-can-i-find-all-matches-to-a-regular-expression-in-python
    # https://stackoverflow.com/questions/1870954/python-regular-expression-across-multiple-lines
    rgx = re.compile(r"commit \w{40}.*?(?=commit)", re.DOTALL)
    commits_array = re.findall(rgx, text_output)
    print(len(commits_array))
    time.sleep(3)
    for item in commits_array:
        print(item)
        print('\n\n\n\n')


output, error = call_sp('git log')

parse_git_log_info(output)
