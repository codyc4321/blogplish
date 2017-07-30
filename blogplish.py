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
    """ returns a commits_array like:

        [
            {'commit_id': '23hj3sz...', 'message': 'cleanup cruft'},
            {'commit_id': 'df8dje...', 'message': 'Changed paypal api setting to...'},
            ...
        ]
    """
    commit_start_rgx = r"^commit (?P<commit_id>\w{40})"
    lines = text_output.split('\n')
    commits_array = []
    current_commit_id = None
    current_commit_message_string = ""

    for line in lines:
        match = re.match(commit_start_rgx, line)
        if match:
            # this if block fails only once, on the first pass through
            if current_commit_id:
                commits_array.append({'commit_id': current_commit_id, 'message': current_commit_message_string.strip()})
            current_commit_id = match.group('commit_id')
            current_commit_message_string = ""
        else:
            if not line.startswith('Author: ') and not line.startswith('Date: '):
                current_commit_message_string += line

    return commits_array


def get_files_that_were_changed_in_commit(commit_id):
    # "get files that were changed in a commit": https://stackoverflow.com/questions/424071/how-to-list-all-the-files-in-a-commit
    output, error = call_sp('git diff-tree --no-commit-id --name-only -r %s' % commit_id)
    if error:
        raise Exception("Error in get_files_that_were_changed_in_commit():\n\n" + error)
    changed_files_intermediary = output.split('\n')
    # at first got a result like ['blogplish.py', '']
    changed_files = [this_file for this_file in changed_files_intermediary if this_file]
    return changed_files


output, error = call_sp('git log')

parsed_commits = parse_git_log_info(output)

first_commit = parsed_commits[0]
first_commit_id = first_commit['commit_id']

changed_files = get_files_that_were_changed_in_commit(first_commit_id)
print(changed_files)
