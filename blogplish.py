
from subprocess import Popen, PIPE



"""
Write function to call Bash command from Python

Get all commit info

For each commit in the commit info:
    Add commit message to a final string
    Add changes to final string
    Add entire files that were changed to final string
"""

ydef call_sp(command, *args, **kwargs):
    """ you can run command from any directory you want by passing in a kwarg of 'cwd' (current working directory):

        call_sp('ls', '-a', cwd='/home/username/projects/awesomeproject')
    """
    if args:
        command = command.format(*args)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
    output, err = p.communicate()
    return output, err


output, error = call_sp('ls')
print(output)
x
