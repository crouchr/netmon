# run a command in shell
import subprocess


def run_sh_cmd(cmd_str):
    # print(cmd_str)
    cmd_str = cmd_str.split(' ')
    p = subprocess.Popen(cmd_str,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout_, stderr_ = p.communicate()
    p.wait()

    console_output = stdout_.decode()
    console_error = stderr_.decode()
    # print(console_output)
    # print(console_error)

    return console_output
