import subprocess

gitRepositoryPath = "E:/j6/fresh/resource/"

startCommitSign = "931d78f7ed1372aa5c598b20f35180f19089b04c"

endCommitSign = "0cd9b397c63c6999932418008bfe68d19b6df8d5"

#[(A|C|D|M|R|T|U|X|B)…
def gitStatus(startCommit, endCommit, repoDir):
    cmd = 'git diff --name-only --diff-filter=ACMR %s %s %s'%(endCommit,startCommit,repoDir)
    pipe = subprocess.Popen(cmd, shell=True, cwd=repoDir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
    (out, error) = pipe.communicate()
    print out,error
    #k = out.split("\n")
    #print(k[0])
    pipe.wait()
    return

gitStatus(startCommitSign,endCommitSign, gitRepositoryPath)