In this post, we will look at how blogplish (blog autopublish) was written. This script this post describes wrote itself. It sounds confusing...let's just write it again.

Make a new git repo. Make a file called `blogplish.py`, using `touch blogplish.py`.

Add only the code `print("The script is working.")` in this script.

You can run this file using the `python` command in your terminal:

```$ python blogplish.py\nThe script is working.```



`blogplish.py`

```

print("The script is working.")
```


When you're working on a task you've never done before, most of your time is usually spent figuring out what it is you need to do.        In this case, we found ourselves stuck planning out how to write the script (Do we use regular Bash, or the Github API?, Do we get all commits at once, or go backwards using the HEAD~1 style syntax until there's no commits left?, and so on).    When you get that stuck, it's best to start out writing pseudocode and describe what you think you need to do overall:



`blogplish.py`

```

print("The script is working.")

"""
Write function to call Bash command from Python

Get all commit info

For each commit in the commit info:
    Add commit message to a final string
    Add changes to final string
    Add entire files that were changed to final string
"""
```


As far as the first step "Write function to call Bash command from Python" goes, in theory, I already had a sturdy function to flexibly run linux commands in a python script:



`blogplish.py`

```
from subprocess import Popen, PIPE


"""
Write function to call Bash command from Python

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


output, error = call_sp('ls')
print(output)
```



Run 'ls' in your terminal, and see it outputs only `blogplish.py`, the only file in our project (besides hidden .git files).        In the python script, it also runs `ls`, in the `call_sp('ls')` portion. The output here should match:



`blogplish.py`

```
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
```



Run 'ls' in your terminal, and see it outputs only `blogplish.py`, the only file in our project (besides hidden .git files).        In the python script, it also runs `ls`, in the `call_sp('ls')` portion. The output here should match:        cchilders:~/blogplish (master)    $ python blogplish.py    blogplish.py        cchilders:~/blogplish (master)    $ ls    blogplish.py



`blogplish.py`

```
from subprocess import Popen, PIPE



"""
Write function to call Bash command from Python

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


output, error = call_sp('ls')
print(output)
```



Update our pseudocode:



`blogplish.py`

```
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


output, error = call_sp('ls')
print(output)
```



** ERROR: call_sp('ls', '-a', ...) doesn't work; *args is only used to substitute into the command string like 'ls %s' etc. Fix this before publish **        As for `Get all commit info`, we can use `git log` for that. Update `call_sp`:



`blogplish.py`

```
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


output, error = call_sp('git log')
print(output)
```



Now run our script again. You can compare the output with `git log` in your terminal. You should see a summary of your commit history like:        ```    cchilders:~/blogplish (master)    $ python blogplish.py    commit ea270e9a879b385580a855f1f83736ccce345de3    Author: Cody Childers <email@example.com>    Date:   Sun Jul 30 00:06:03 2017 -0500            ** ERROR: call_sp('ls', '-a', ...) doesn't work; *args is only used to substitute into the command string like 'ls %s' etc. Fix this before publish **            As for `Get all commit info`, we can use `git log` for that. Update `call_sp`:        commit bb19fca5f6461fbf8ca6e1870964021f818ba063    Author: Cody Childers <email@example.com>    Date:   Sun Jul 30 00:00:11 2017 -0500            Update our pseudocode:        ...etc...    ```



`blogplish.py`

```
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


output, error = call_sp('git log')
print(output)
```


Next, we need to parse the output of `git log`. Look at what it outputs and take a few minutes to think about how you'd parse it to get the commit ID and message for each commit.        Start a function to do the parsing:


`blogplish.py`

```
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
    pass


output, error = call_sp('git log')
print(output)
```


At first we tried this:


`blogplish.py`

```import re
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
    # https://stackoverflow.com/questions/10974932/split-string-based-on-a-regular-expression
    commits_array = re.split("commit \w{40}", text_output)
    print(commits_array)


output, error = call_sp('git log')
print(output)

parse_git_log_info(output)
```


But the problem was, it was cutting off the commit id;        ['', "\nAuthor: Cody Childers <email@example.com>\nDate:   Sun Jul 30 00:15:39 2017 -0500\n\n    Next, we need to parse the output of `git log`. Look at what it outputs and take a few minutes to think about how you'd parse it to get the commit ID and message for each commit.\n    \n    Start a function to do the parsing:\n\n", '\nAuthor: ...]


`blogplish.py`

```import re
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
    # https://stackoverflow.com/questions/10974932/split-string-based-on-a-regular-expression
    commits_array = re.split("commit \w{40}", text_output)
    print(commits_array)


output, error = call_sp('git log')
print(output)

parse_git_log_info(output)
x
```


We were able to split the `git log` output by using `re.findall`. The `re` package is a python pattern matcher, that allows you to find text of interest.    The easiest way to write regexes is to go to [pythex.org](https://www.pythex.org "Pythex - Python regex checker").

The `time` module introduces a pause as we looked for a list of approximately 10-15 commits:


`blogplish.py`

```import re
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
```


This seemed like a great start, but we soon noticed that the commit messages where we had copypasted the output of `git log` broke our `parse_git_log_info` function, because they also matched `commit \w{40}`:        

```    
...        
commit 3e4aca9f102229c890ef73967f4a4c1c61a51a73    Author: Cody Childers <email@example.com>    Date:   Sun Jul 30 00:08:46 2017 -0500            Now run our script again. You can compare the output with `git log` in your terminal. You should see a summary of your commit history like:            ```        cchilders:~/blogplish (master)        $ python blogplish.py        commit ea270e9a879b385580a855f1f83736ccce345de3        Author: Cody Childers <email@example.com>        Date:   Sun Jul 30 00:06:03 2017 -0500                ** ERROR: call_sp('ls', '-a', ...) doesn't work; *args is only used to substitute into the command string like 'ls %s' etc. Fix this before publish **                As for `Get all commit info`, we can use `git log` for that. Update `call_sp`:            commit bb19fca5f6461fbf8ca6e1870964021f818ba063        Author: Cody Childers <email@example.com>        Date:   Sun Jul 30 00:00:11 2017 -0500        ...    ```        

This threw a wrench in our plan of 1 distinct function to split the commits into an array, and another function to parse each singular commit one by one. Instead, we ended up with a rambling parser that parsed the entire output line by line. Hideous, but works:


`blogplish.py`

```import re
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
```


This parser goes line by line, checking if the line starts a new commit block or not `match = re.match(commit_start_rgx, line)`.    If not, the parser adds the line to the commit message if applicable (if it doesn't start with 'commit', 'Author: ', or 'Date: ').    If the line does match `"^commit (?P<commit_id>\w{40})"`, it will add the data to the final results if the data is ready (except on the first go around, where we have `current_commit_id` initialized to `None`).        While it isn't as clean looking as smaller parsers, I always find this line-by-line style to be less error prone for tricky text parsing.


`blogplish.py`

```import re
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


output, error = call_sp('git log')

print(parse_git_log_info(output))
```


Now, let's work on the `Add entire files that were changed to final string` part. To do this, we want to first find the files that were changed in each commit:


`blogplish.py`

```import re
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
    return output.split('\n')


output, error = call_sp('git log')

parsed_commits = parse_git_log_info(output)

first_commit = parsed_commits[0]
first_commit_id = first_commit['commit_id']

changed_files = get_files_that_were_changed_in_commit(first_commit_id)
print(changed_files)
```


We have a small issue however, as the output is `['blogplish.py', '']`. We can prune empty lines out of our result using a list comprehension:


`blogplish.py`

```import re
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
```



Now that we know which files were changed in any commit, we need to get the contents of the file at that point in time:



`blogplish.py`

```import re
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


def get_contents_of_certain_file_in_certain_commit(commit_id, filename):
    # "get contents of a certain file in a commit": https://stackoverflow.com/questions/2497051/how-can-i-show-the-contents-of-a-file-at-a-specific-state-of-a-git-repo
    output, error = call_sp('git show %s:%s' % (commit_id, filename))
    if error:
        raise Exception("Error in get_contents_of_certain_file_in_certain_commit():\n\n" + error)
    return output


output, error = call_sp('git log')

parsed_commits = parse_git_log_info(output)

first_commit = parsed_commits[0]
first_commit_id = first_commit['commit_id']

changed_files = get_files_that_were_changed_in_commit(first_commit_id)

for changed_file in changed_files:
    contents = get_contents_of_certain_file_in_certain_commit(first_commit_id, changed_file)
    print(contents)
```



To double-check this, we used the first commit of the blogplish project and got:        ```    cchilders:~/blogplish (master)    $ python blogplish.py        print("The script is working.")    ```        It's working.



`blogplish.py`

```import re
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


def get_contents_of_certain_file_in_certain_commit(commit_id, filename):
    # "get contents of a certain file in a commit": https://stackoverflow.com/questions/2497051/how-can-i-show-the-contents-of-a-file-at-a-specific-state-of-a-git-repo
    output, error = call_sp('git show %s:%s' % (commit_id, filename))
    if error:
        raise Exception("Error in get_contents_of_certain_file_in_certain_commit():\n\n" + error)
    return output


output, error = call_sp('git log')

parsed_commits = parse_git_log_info(output)

first_commit = parsed_commits[0]
first_commit_id = first_commit['commit_id']

changed_files = get_files_that_were_changed_in_commit(first_commit_id)

# for changed_file in changed_files:
#     contents = get_contents_of_certain_file_in_certain_commit(first_commit_id, changed_file)
#     print(contents)

print(get_contents_of_certain_file_in_certain_commit('b37ae0371d1', 'blogplish.py'))
```



To get the diff of a file at a certain point in time, we use `git diff {older_commit_id}..{newer_commit_id} {filename}` syntax.        My output for the diff of the most recent commit looked like:        ```    cchilders:~/blogplish (master)    $ python blogplish.py    diff --git a/blogplish.py b/blogplish.py    index 0285d88..7be3810 100644    --- a/blogplish.py    +++ b/blogplish.py    @@ -82,6 +82,8 @@ first_commit_id = first_commit['commit_id']         changed_files = get_files_that_were_changed_in_commit(first_commit_id)        -for changed_file in changed_files:    -    contents = get_contents_of_certain_file_in_certain_commit(first_commit_id, changed_file)    -    print(contents)    +# for changed_file in changed_files:    +#     contents = get_contents_of_certain_file_in_certain_commit(first_commit_id, changed_file)    +#     print(contents)    +    +print(get_contents_of_certain_file_in_certain_commit('b37ae0371d1', 'blogplish.py'))    ```



`blogplish.py`

```import re
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


output, error = call_sp('git log')

parsed_commits = parse_git_log_info(output)

first_commit = parsed_commits[0]
first_commit_id = first_commit['commit_id']

changed_files = get_files_that_were_changed_in_commit(first_commit_id)

# for changed_file in changed_files:
#     contents = get_contents_of_certain_file_in_certain_commit(first_commit_id, changed_file)
#     print(contents)

# print(get_contents_of_certain_file_in_certain_commit('b37ae0371d1', 'blogplish.py'))

a_diff_2_commits_back = get_diff_of_certain_file_in_certain_commit('c4b7c7cabccc350eef5ef80344f', 'f66b7bfd0f82d5b987d9f71f', THIS_SCRIPT_NAME)
print(a_diff_2_commits_back)
```



We're finally ready to combine these 3 functions into an autogenerated markdown file for our blogpost. We started with this func and reviewed the commits data we first got:



`blogplish.py`

```import re
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
    print(parsed_commits)

    # first_commit = parsed_commits[0]
    # first_commit_id = first_commit['commit_id']
    #
    # changed_files = get_files_that_were_changed_in_commit(first_commit_id)
    #
    # # for changed_file in changed_files:
    # #     contents = get_contents_of_certain_file_in_certain_commit(first_commit_id, changed_file)
    # #     print(contents)
    #
    # # print(get_contents_of_certain_file_in_certain_commit('b37ae0371d1', 'blogplish.py'))
    #
    # a_diff_2_commits_back = get_diff_of_certain_file_in_certain_commit('c4b7c7cabccc350eef5ef80344f', 'f66b7bfd0f82d5b987d9f71f', THIS_SCRIPT_NAME)
    # print(a_diff_2_commits_back)


auto_blogplish_blog()
```



While the commits come back in order, we write tutorials from start to finish, so the order is backwards. Reversing a list in python is very easy:



`blogplish.py`

```import re
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
    print(parsed_commits)

    # first_commit = parsed_commits[0]
    # first_commit_id = first_commit['commit_id']
    #
    # changed_files = get_files_that_were_changed_in_commit(first_commit_id)
    #
    # # for changed_file in changed_files:
    # #     contents = get_contents_of_certain_file_in_certain_commit(first_commit_id, changed_file)
    # #     print(contents)
    #
    # # print(get_contents_of_certain_file_in_certain_commit('b37ae0371d1', 'blogplish.py'))
    #
    # a_diff_2_commits_back = get_diff_of_certain_file_in_certain_commit('c4b7c7cabccc350eef5ef80344f', 'f66b7bfd0f82d5b987d9f71f', THIS_SCRIPT_NAME)
    # print(a_diff_2_commits_back)


auto_blogplish_blog()
```



Now we want to start iterating over the commit data, generating the text. The order will go    1. commit message    2. the diff of each file that was changed    3. the total contents of each file that was changed        First, get the commit messages added in the correct order:



`blogplish.py`

```import re
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
```



I did step 3, add the total contents, second:



`blogplish.py`

```import re
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

    for index, commit_data in enumerate(parsed_commits):
        blog_post += commit_data['message']
        blog_post += '\n\n\n\n'
        commit_id = commit_data['commit_id']

        changed_files = get_files_that_were_changed_in_commit(commit_id)
        if changed_files:
            blog_post += '$$$ Entire contents of changed files: $$$\n\n'
        for changed_file in changed_files:
            contents = get_contents_of_certain_file_in_certain_commit(commit_id, changed_file)
            blog_post += '## ' + changed_file + ': ##\n\n'
            blog_post += contents
            blog_post += '\n\n\n\n'

    # print(get_contents_of_certain_file_in_certain_commit('b37ae0371d1', 'blogplish.py'))

    # a_diff_2_commits_back = get_diff_of_certain_file_in_certain_commit('c4b7c7cabccc350eef5ef80344f', 'f66b7bfd0f82d5b987d9f71f', THIS_SCRIPT_NAME)
    # print(a_diff_2_commits_back)

    return blog_post


blog_text = auto_blogplish_blog()
print(blog_text)
```



Now step 2, adding the diff of each file that was changed:



`blogplish.py`

```import re
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

    for index, commit_data in enumerate(parsed_commits):
        blog_post += commit_data['message']
        blog_post += '\n\n\n\n'
        this_commit_id = commit_data['commit_id']

        changed_files = get_files_that_were_changed_in_commit(this_commit_id)

        if changed_files:
            if index > 0:
                blog_post += '$$$ Diffs of changed files: $$$\n\n'
                for changed_file in changed_files:
                    older_commit_id = parsed_commits[index - 1]['commit_id']
                    this_diff = get_diff_of_certain_file_in_certain_commit(older_commit_id, this_commit_id, changed_file)
                    blog_post += '## ' + changed_file + ': ##\n\n'
                    blog_post += this_diff
                    blog_post += '\n\n\n\n'

            blog_post += '$$$ Entire contents of changed files: $$$\n\n'
            for changed_file in changed_files:
                contents = get_contents_of_certain_file_in_certain_commit(this_commit_id, changed_file)
                blog_post += '## ' + changed_file + ': ##\n\n'
                blog_post += contents
                blog_post += '\n\n\n\n'

    return blog_post


blog_text = auto_blogplish_blog()
print(blog_text)
```



The output is still rough, and the diffs printed out are hard to read. It can use a CLI to take you through each commit, each file, and let the author pick how to show the changes in the blog. A javascript UI might be much easier than using a CLI, as you can click what to keep and edit text in place much easier. Overall, in 1 day, after work, with no beer or caffiene in the house, I'd say Servando and I did pretty good.



`blogplish.py`

```import re
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

    for index, commit_data in enumerate(parsed_commits):
        blog_post += commit_data['message']
        blog_post += '\n\n\n\n'
        this_commit_id = commit_data['commit_id']

        changed_files = get_files_that_were_changed_in_commit(this_commit_id)

        if changed_files:
            if index > 0:
                blog_post += '$$$ Diffs of changed files: $$$\n\n'
                for changed_file in changed_files:
                    older_commit_id = parsed_commits[index - 1]['commit_id']
                    this_diff = get_diff_of_certain_file_in_certain_commit(older_commit_id, this_commit_id, changed_file)
                    blog_post += '## ' + changed_file + ': ##\n\n'
                    blog_post += this_diff
                    blog_post += '\n\n\n\n'

            blog_post += '$$$ Entire contents of changed files: $$$\n\n'
            for changed_file in changed_files:
                contents = get_contents_of_certain_file_in_certain_commit(this_commit_id, changed_file)
                blog_post += '## ' + changed_file + ': ##\n\n'
                blog_post += contents
                blog_post += '\n\n\n\n'

    return blog_post


blog_text = auto_blogplish_blog()
print(blog_text)
x
```



Before the blog you're reading was autogenerated for publishing, I commented out the lines that show the diffs. It also lacked some autoformatting, such as code blocks in ```, and filenames printed pretty:



`blogplish.py`

```import re
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

    for index, commit_data in enumerate(parsed_commits):
        blog_post += commit_data['message']
        blog_post += '\n\n\n\n'
        this_commit_id = commit_data['commit_id']

        changed_files = get_files_that_were_changed_in_commit(this_commit_id)

        if changed_files:
            # if index > 0:
            #     blog_post += '$$$ Diffs of changed files: $$$\n\n'
            #     for changed_file in changed_files:
            #         older_commit_id = parsed_commits[index - 1]['commit_id']
            #         this_diff = get_diff_of_certain_file_in_certain_commit(older_commit_id, this_commit_id, changed_file)
            #         blog_post += '## ' + changed_file + ': ##\n\n'
            #         blog_post += this_diff
            #         blog_post += '\n\n\n\n'

            # blog_post += '$$$ Entire contents of changed files: $$$\n\n'
            for changed_file in changed_files:
                contents = get_contents_of_certain_file_in_certain_commit(this_commit_id, changed_file)
                # blog_post += '## ' + changed_file + ': ##\n\n'
                blog_post += '`' + changed_file + '`\n\n'
                blog_post += "```" + contents + "```"
                blog_post += '\n\n\n\n'

    return blog_post


blog_text = auto_blogplish_blog()
print(blog_text)
```
