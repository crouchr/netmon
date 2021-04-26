# run a command in shell
import subprocess

# ping returned in stdout
# fping returns in stderr
def run_sh_cmd(cmd_str):
    """
    Run a shell command
    :param cmd_str:
    :return:
    """
    # print(cmd_str)
    cmd_str = cmd_str.split(' ')
    p = subprocess.Popen(cmd_str,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout_, stderr_ = p.communicate()
    p.wait()

    stdout_ = stdout_.decode('ASCII')
    stderr_ = stderr_.decode('ASCII')
    if len(stdout_) > 0:
        console_output = stdout_.rstrip('\n')
    else:
        console_output = stderr_.rstrip('\n')

    #console_output = stderr_.decode().rstrip('\n')
    # console_error = stderr_.decode()
    # print(console_output)
    # print(console_error)

    return console_output
