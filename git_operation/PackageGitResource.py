import os
import winreg

r = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
k = winreg.OpenKey(r, r'SOFTWARE\GitForWindows')
install_path = winreg.QueryValueEx(k, 'InstallPath')[0]
git_path = os.path.join(install_path, 'bin/git.exe')
assert os.path.exists(git_path), "Git path not found"
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = git_path


from git import Repo
#https://pypi.python.org/pypi/GitPython

import git
# rorepo is a Repo instance pointing to the git-python repository.
# For all you know, the first argument to Repo is a path to the repository
# you want to work with
repo = Repo("E:/flashWithJenkinsDemo")

old_head_sha = repo.git.rev_parse("HEAD")

repo.remotes.origin.pull()

new_head_sha = repo.git.rev_parse("HEAD")

#downcase means exclude types and uppercase mean include types

diff1 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="A")
diff2 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="D")
diff3 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="M")
diff4 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="AD")
diff5 = repo.git.diff(old_head_sha + ".." + new_head_sha,name_only=True,diff_filter="R")

#,
assert not repo.bare