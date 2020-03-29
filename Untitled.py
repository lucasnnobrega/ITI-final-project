
# coding: utf-8

# In[55]:


encoder_commands = [{"cmd":"python3 main.py encoder smallCorpus.txt {}".format(byte_len)} for byte_len in range(9,17)]


# In[56]:


encoder_commands


# In[57]:


decoder_commands = [{"cmd":"python3 main.py decoder smallCorpus_bl{}.lzw {}".format(byte_len, byte_len)} for byte_len in range(9,17)]


# In[58]:


decoder_commands


# In[29]:


import subprocess
import time
import shlex
import os
import pandas as pd
from datetime import datetime
from copy import deepcopy
from constantes import *


# In[30]:


cut_param = [0, 1, 2, 3, 4, 5, 9]

file = "smallCorpus.lzw"

corte_array = [("corte " + str(i)) for i in cut_param]

corte_array[0] = "sem"
corte_array[4] = "conjectura"
corte_array[-1] = "todos"
'''
commands_per_file = [{
    "file": file,
    "cortes": ["../CPP/main -v aa -c {} -t 1 -i ../CPP/instances/{}".format(c, file) for c in cut_param]
} for file in os.listdir("../CPP/instances")]
'''

commands_per_file = [{
    "file": file,
    "cortes": ["../CPP/main -v aa -c {} -t 1 -i ../CPP/instances/{}".format(c, file) for c in cut_param]
}]



# Necessario para ordenar as instancias pelo tamanho delas
commands_per_file = sorted(commands_per_file, key=lambda k: k['file'])

timeout=3600  # Em segundos => 1 hora tem 60 minutos que por sua vez tem 60 segundos

folder_name=str(time.ctime())


# In[44]:


def execute(command_line, timeout):

    args=shlex.split(command_line)
    print(args)

    start=time.time()
    try:
        p=subprocess.Popen(args )#, stdout=subprocess.DEVNULL)
        # p = subprocess.Popen(args)
        p.wait(timeout)
        delta=time.time() - start
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


# In[45]:


def mainLoop(timeout):

    # Create the directory with all benchmarks
    os.mkdir(f"./Data/{folder_name}")

    # Create a resume file with resume of the benchmark
    with open(f"./Data/{folder_name}/Resume.txt", "w+") as file:
        file.write("Resume\n\n")
        file.write(f"The benckmark started day {folder_name}.\n")
        file.write(f"Time to live of {timeout} seconds.\n")
        file.write(f"Cut parameters {cut_param}.\n")

    data=deepcopy(commands_per_file)
    for i in range(0, len(commands_per_file)):

        data[i]["cortes"]=[executeCpp(cmd, timeout)
                             for cmd in data[i]["cortes"]]

        data[i]["cortes"]=[task for task in data[i]["cortes"]]

        df=pd.DataFrame(data)
        # print(df.head(6))
        df2=pd.DataFrame(df)
        df2[corte_array]=pd.DataFrame(
            df2.cortes.values.tolist(), index=df2.index)
        # print(df2.head(6))
        df2.drop(columns="cortes", inplace=True)
        # print(df2.head(6))
        df2.to_csv("./Data/" + folder_name + "/" +
                   str(i+1) + " " + str(time.ctime()) + ".csv")

        # print(f"./Data/{folder_name}/{i+1} {time.ctime()}.csv")
    return data


# In[46]:


# Driver function
if __name__ == "__main__":

    '''
    print("This code executed in:", executeCpp(
        "../CPP/main -v aa -c 6 -t 1 -i ../CPP/instances/ins_05_20_4.txt", 120), "seconds.")
    '''

    try:
        data=mainLoop(timeout)
        df=pd.DataFrame(data)
        print(df.head(6))
        df2=pd.DataFrame(df)
        df2[corte_array]=pd.DataFrame(
            df2.cortes.values.tolist(), index=df2.index)
        print(df2.head(6))
        df2.drop(columns="cortes", inplace=True)
        print(df2.head(6))
        df2.to_csv(f"./Data/{folder_name}/FINAL.csv")
    finally:
        print(GREEN, '\nCode Finished\n', RESET)
        with open(f"./Data/{folder_name}/Resume.txt", "a") as file:
            file.write(f"The benckmark ended day {time.ctime()}\n")
            with open(f"./main.py", 'r') as code:
                space='#'*50
                file.write(f"\n{space}\nCODE\n{space}\n{code.read()}")
    # '''


# In[47]:


executeCpp(encoder_commands[0], timeout)


# In[48]:


executeCpp(decoder_commands[0], timeout)


# # Benchmark configuration

# In[53]:


folder_name=str(time.ctime())
# Create the directory with all benchmarks
os.mkdir(f"./Data/{folder_name}")

# Create a resume file with resume of the benchmark
with open(f"./Data/{folder_name}/Resume.txt", "w+") as file:
    file.write("Resume\n\n")
    file.write(f"The benckmark started day {folder_name}.\n")
    file.write(f"Time to live of {timeout} seconds.\n")


# In[67]:


encoder_commands[1]["cmd"]


# In[87]:


data = deepcopy(encoder_commands)
lista = []
for i in range(0, len(encoder_commands)):
    data[i]["time"] = execute(data[i]["cmd"], timeout)


# In[91]:


data


# In[97]:


df=pd.DataFrame(data)


# In[98]:


df


# In[111]:


df["k"] = df["cmd"].str.replace("python3 main.py encoder smallCorpus.txt", "")


# In[114]:


df.to_csv("./Data/" + folder_name + "/" +
           str(i+1) + " encoder " + str(time.ctime()) + ".csv")


# In[115]:


data = deepcopy(decoder_commands)
lista = []
for i in range(0, len(decoder_commands)):
    data[i]["time"] = execute(data[i]["cmd"], timeout)


# In[116]:


data


# In[121]:


df=pd.DataFrame(data)


# In[122]:


df


# In[153]:


df["k"] = list(range(9,17))


# In[154]:


df


# In[155]:


df.to_csv("./Data/" + folder_name + "/" +
           str(i+1) + " decoder " + str(time.ctime()) + ".csv")

