import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import libutilsSk.exeutils as SkExe

# Run a command
def Execute():
    typeline = entry.get()
    entry.delete(0, 'end')
    # TODO: Completly rethink this

root = tk.Tk()
root.title("AFSkewerShell")

text_area = ScrolledText(root, width=80, height=20)
text_area.tag_config("blue", foreground="blue")
text_area.tag_config("green", foreground="green")
text_area.tag_config("red", foreground="red")
text_area.tag_config("black", foreground="black")
text_area.tag_config("white", foreground="white")
text_area.pack()
text_area.config(state=tk.DISABLED,bg="black")
text_area.config(font=("Arial", 15))

entry = tk.Entry(root, width=80)
entry.pack()
entry.config(bg="black",foreground="white")
entry.config(font=("Arial", 10))
entry.bind("<Return>", lambda event: Execute())

root.resizable(False, False)
root.mainloop()