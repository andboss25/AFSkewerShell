
import tkinter as tk
import re
from tkinter.scrolledtext import ScrolledText

# Executable utils that manage everything related to how the command line/functions are interprted

# Will take in a typeline stream and give arguments for the shell
# First it must add the basic start arguments
# Then it checks if it says exit or quit
# Then it must check for a expression in its native language like "1+1" , "1+1 -> 5*%pipe%"
def ExecuteCMD(typeline:str) -> list[str]:
    buffer = []

    buffer.append("SkStart")

    buffer.append("SkStdout")
    buffer.append(f"Usr >> '{typeline}' ")

    if typeline == "exit" or typeline == "quit":
        buffer.append("SkExit")
        return buffer
    
    try:
        ans = NativeExpression(typeline)
        buffer.append("SkStdout")
        buffer.append(f"AFSkewerShell '{typeline}' > " + str(ans))
        return buffer
    except:
        pass

    buffer.append("SkFailure")
    buffer.append("No such command or progam found")
    return buffer

# Find native expression from typeline and execute its
# Check if it has extra pipeline operators
# Loop over to find pipelining "->" then separate expressions in a pipebuffer
def NativeExpression(expression: str):
    pipebuffer = expression.split("->")
    pipebuffer = [expr.strip() for expr in pipebuffer]

    result = ArithmeticOp(pipebuffer[0])
    if result is None:
        return None

    for expr in pipebuffer[1:]:
        expr = expr.replace("%pipeline%", str(result))
        result = ArithmeticOp(expr)
        if result is None:
            return None

    return result


# Will evaluate a arithmetic statement
def ArithmeticOp(expression: str):
    expression = expression.replace(" ", "")

    def tokenize(expr):
        token_pattern = r'(\d+\.\d+|\d+|[+\-*/^()])'
        tokens = re.findall(token_pattern, expr)

        processed = []
        i = 0
        while i < len(tokens):
            if tokens[i] == '-' and (i == 0 or tokens[i - 1] in "+-*/^("):
                processed.append(tokens[i] + tokens[i + 1])
                i += 2
            else:
                processed.append(tokens[i])
                i += 1
        return processed

    def precedence(op):
        return {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}.get(op, 0)

    def apply_operator(op, b, a):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/':
            if a == 0 and b == 0:
                return None
            return a / b
        if op == '^': return a ** b

    def evaluate(tokens):
        values = []
        ops = []

        def compute():
            if len(values) < 2 or not ops:
                raise Exception
            op = ops.pop()
            b = values.pop()
            a = values.pop()
            result = apply_operator(op, b, a)
            if result is None:
                raise ZeroDivisionError
            values.append(result)

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if re.fullmatch(r'-?\d+(\.\d+)?', token):
                values.append(float(token))
            elif token == '(':
                ops.append(token)
            elif token == ')':
                while ops and ops[-1] != '(':
                    compute()
                ops.pop()
            else:
                while ops and precedence(ops[-1]) >= precedence(token):
                    compute()
                ops.append(token)
            i += 1

        while ops:
            compute()

        return values[0]

    try:
        tokens = tokenize(expression)
        return evaluate(tokens)
    except ZeroDivisionError:
        return None
    except:
        return None

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
