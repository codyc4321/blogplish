import re
import sys
from subprocess import Popen, PIPE

THIS_SCRIPT_NAME = sys.argv[0]


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


def get_contents_of_certain_file_in_certain_commit(commit_id, filename):
    # "get contents of a certain file in a commit": https://stackoverflow.com/questions/2497051/how-can-i-show-the-contents-of-a-file-at-a-specific-state-of-a-git-repo
    output, error = call_sp('git show %s:%s' % (commit_id, filename))
    if error:
        raise Exception("Error in get_contents_of_certain_file_in_certain_commit():\n\n" + error)
    return output


def get_diff_of_certain_file_in_certain_commit(newer_commit_id, older_commit_id, filename):
    """
    head diff means how many commits back, as in

        HEAD~3

    means 3 commits back
    """
    # "get dif of a certain file in certain commit": https://stackoverflow.com/questions/42357521/generate-diff-file-of-a-specific-commit-in-git
    command = 'git diff {older_commit_id}..{newer_commit_id} {filename}'.format(older_commit_id=older_commit_id, newer_commit_id=newer_commit_id, filename=filename)
    raw_diff, error = call_sp(command)
    if error:
        raise Exception("Error in get_diff_of_certain_file_in_certain_commit():\n\n" + error)
    return raw_diff


def auto_blogplish_blog():
    blog_post = ""

    output, error = call_sp('git log')

    parsed_commits = parse_git_log_info(output)
    # "reverse a list python": https://stackoverflow.com/questions/3940128/how-can-i-reverse-a-list-in-python
    parsed_commits.reverse()

    first_commit = parsed_commits[0]
    first_commit_id = first_commit['commit_id']

    for index, commit_data in enumerate(parsed_commits):
        blog_post += commit_data['message']
        blog_post += '\n\n\n\n'

    # changed_files = get_files_that_were_changed_in_commit(first_commit_id)

    # for changed_file in changed_files:
    #     contents = get_contents_of_certain_file_in_certain_commit(first_commit_id, changed_file)
    #     print(contents)

    # print(get_contents_of_certain_file_in_certain_commit('b37ae0371d1', 'blogplish.py'))

    # a_diff_2_commits_back = get_diff_of_certain_file_in_certain_commit('c4b7c7cabccc350eef5ef80344f', 'f66b7bfd0f82d5b987d9f71f', THIS_SCRIPT_NAME)
    # print(a_diff_2_commits_back)

    return blog_post


blog_text = auto_blogplish_blog()
print(blog_text)
