
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Executable utils that manage everything related to how the command line/functions are interprted

# Will take in a typeline stream and give arguments for the shell
def ExecuteCMD(typeline:str) -> list[str]:
    buffer = []

    buffer.append("SkStart")

    if typeline == "exit" or typeline == "quit":
        buffer.append("SkExit")
        return buffer
    
    try:
        ans = eval(typeline,{'__builtins__': {}})
        buffer.append("SkStdout")
        buffer.append(f"AFSkewerShell '{typeline}' > " + str(ans))
        return buffer
    except:
        pass

    buffer.append("SkFailure")
    buffer.append("No such command or progam found")
    return buffer

# Execute a argslist
def ReadArgs(arglist:list[str],text_area:ScrolledText):
    index = 0
    for arg in arglist:
        
        if arg == "SkExit":
           exit(0)
        elif arg == "SkFailure":
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END,"Error: " + arglist[index + 1] + "\n","red")
            text_area.config(state=tk.DISABLED)
        elif arg == "SkStdout":
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END,arglist[index + 1] + "\n","white")
            text_area.config(state=tk.DISABLED)

        index = index + 1
