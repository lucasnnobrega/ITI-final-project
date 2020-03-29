import subprocess
import time
import shlex
import os
import pandas as pd
from datetime import datetime
from copy import deepcopy
from constantes import *

# Em segundos => 1 hora tem 60 minutos que por sua vez tem 60 segundos
TIMEOUT = 3600

#filename = "mapa.mp4"
#filename = "corpus16MB.txt"
filename = "smallCorpus.txt"

folder_name = str(time.ctime())

small_filename = "smallCorpus.txt"

encoder_commands = [{"cmd": "python3 main2.py encoder {} {}".format(
    filename, byte_len)} for byte_len in range(9, 17)]

# Mudar parametro
if filename.find(".txt") > -1:
    decoder_commands = [{"cmd": "python3 main2.py decoder {} {}".format(
        filename.replace(".txt", ""), byte_len)} for byte_len in range(9, 17)]
elif filename.find(".mp4") > -1:
    decoder_commands = [{"cmd": "python3 main2.py decoder {} {}".format(
        filename.replace(".mp4", ""), byte_len)} for byte_len in range(9, 17)]


def execute(command_line, timeout):

    args = shlex.split(command_line)
    print(args)

    start = time.time()
    try:
        #p = subprocess.Popen(args, stdout=subprocess.DEVNULL)
        p = subprocess.Popen(args)
        print("PID:", p.pid)

        p.wait(timeout)
        delta = time.time() - start
        print("")
        return delta
    except subprocess.TimeoutExpired:
        # Terminate the process with SIGTERM
        p.terminate()

        # Terminate the process with SIGKILL
        # p.kill()
        print(RED, command_line, "process was terminated with ",
              RESET, "\n")
        return "ttl"


def main_Loop():
    folder_name = str(time.ctime())
    # Create the directory with all benchmarks
    os.mkdir(f"./Data/{folder_name}")
    # Create a resume file with resume of the benchmark
    with open(f"./Data/{folder_name}/Resume.txt", "w+") as file:
        file.write("Resume\n\n")
        file.write(f"The benckmark started day {folder_name}.\n")
        file.write(f"Time to live of {TIMEOUT} seconds.\n")
        file.write(f"Compressing and decompressing of the file: {filename}.\n")

    # Encoding
    encoder_commands[1]["cmd"]
    data = deepcopy(encoder_commands)
    lista = []
    for i in range(0, len(encoder_commands)):
        data[i]["time"] = execute(data[i]["cmd"], TIMEOUT)
    df = pd.DataFrame(data)
    df["k"] = list(range(9, 17))
    df.to_csv("./Data/" + folder_name + "/" +
              str(i+1) + " encoder " + str(time.ctime()) + ".csv")

    # Decoding
    data = deepcopy(decoder_commands)
    lista = []
    for i in range(0, len(decoder_commands)):
        data[i]["time"] = execute(data[i]["cmd"], TIMEOUT)

    df = pd.DataFrame(data)
    df["k"] = list(range(9, 17))
    df.to_csv("./Data/" + folder_name + "/" +
              str(i+1) + " decoder " + str(time.ctime()) + ".csv")


# Driver function
if __name__ == "__main__":
    try:
        main_Loop()
    finally:
        print(GREEN, '\nCode Finished\n', RESET)
        with open(f"./Data/{folder_name}/Resume.txt", "a") as file:
            file.write(f"The benckmark ended day {time.ctime()}\n")
            with open(f"./main2.py", 'r') as code:
                space = '#'*50
                file.write(f"\n{space}\nCODE\n{space}\n{code.read()}")
    # '''
