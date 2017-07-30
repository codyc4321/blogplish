import re
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
    commit_count = 0
    commit_start_rgx = r"^commit \w{40}"
    lines = text_output.split('\n')
    # commits_array = []
    current_commit_string = ""
    for line in lines:
        match = re.match(commit_start_rgx, line)
        if match:
            commit_count += 1
            print(line + " matched the start of a commit")
    print("\n")
    print(commit_count)
    # return commits_array


output, error = call_sp('git log')

parse_git_log_info(output)
