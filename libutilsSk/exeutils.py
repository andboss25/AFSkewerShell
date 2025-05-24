
# TODO:
# Okay because last implementation was shit i must make a simple implementation and build on it (goal is to get everyhting down to a single respone)
# Make a basic Variable Replacer that will be used for variables and the pipeliner
# Make a basic Evaluator that will evaluate all expressions
# Add functions to it like "echo" that will be interpreted as keywords and evaluated
# Add keywords statements like variables
# Add keywords statements like "if"
# Add Api to run commands from its own folder that will get detected as keywords (with command line arguments)
# Make a Api to add plugins and shit

class Token:
    def __init__(self,type,value):
        self.type = type
        self.value = value
    def __repr__(self):
        return "| type: " + self.type + " value: " + str(self.value)
    def __eq__(self, other):
        return isinstance(other, Token) and self.type == other.type and self.value == other.value

def TokenizeString(typeline:str):
    typeline = typeline.split(" ")
    buffer = []

    in_quotes = False
    string_buffer = []
    
    for val in typeline:
        if "'" in val:
            if not in_quotes:
                in_quotes = True
                string_buffer.append(val.lstrip("'"))
            else:
                string_buffer.append(val.rstrip("'"))
                buffer.append(Token("string"," ".join(string_buffer)))
                string_buffer = []
                in_quotes = False
        elif in_quotes:
            string_buffer.append(val)
        
        elif val.isdigit():
            buffer.append(Token("int",int(val)))
        
        elif val.replace('.', '', 1).isdigit():
            buffer.append(Token("float", float(val)))
        
        elif val.startswith("-"):
            if val.lstrip("-").isdigit():
                buffer.append(Token("neg_int",int(val)))
            elif val.lstrip("-").replace('.', '', 1).isdigit():
                buffer.append(Token("neg_float", float(val)))
            else:
                buffer.append(Token("keyword",val))
        
        elif val == "+" or val == "-" or val == "*" or val == "/" or val == "**":
            buffer.append(Token("ar_op",val))
        
        elif val == "(" or val == ")":
            buffer.append(Token("pedmas_op",val))
        else:
            buffer.append(Token("keyword",val))

    return buffer

def InterpretTokens(tokens:list[Token]):
    v = 0
    while len(tokens) > v:

        if tokens[v].value == "echo":
            print(tokens[v + 1].value)
        
        v = v + 1

def ArithmeticOperationEvaluator(tokens: list[Token]):
    try:
        while True:
            open_idx = None
            close_idx = None
            for i, t in enumerate(tokens):
                if t.type == "pedmas_op" and t.value == "(":
                    open_idx = i
                elif t.type == "pedmas_op" and t.value == ")":
                    if open_idx is None:
                        raise Exception("Mismatched parentheses")
                    close_idx = i
                    break

            if open_idx is not None and close_idx is not None:
                inner_tokens = tokens[open_idx + 1: close_idx]

                evaluated_tokens = ArithmeticOperationEvaluator(inner_tokens)
                if len(evaluated_tokens) != 1:
                    raise Exception("Invalid expression inside parentheses")

                tokens = tokens[:open_idx] + evaluated_tokens + tokens[close_idx + 1:]
            else:
                break

        precedence_groups = [
            ["**"],
            ["*", "/"],
            ["+", "-"]
        ]

        for ops in precedence_groups:
            v = 0
            while v < len(tokens):
                if tokens[v].type == "ar_op" and tokens[v].value in ops:
                    left = tokens[v - 1].value
                    right = tokens[v + 1].value
                    op = tokens[v].value

                    if op == "+":
                        result = left + right
                    elif op == "-":
                        result = left - right
                    elif op == "*":
                        result = left * right
                    elif op == "/":
                        if right == 0:
                            raise ZeroDivisionError
                        result = left / right
                    elif op == "**":
                        result = left ** right
                    else:
                        raise Exception("Unknown operator")

                    tokens[v] = Token("expression_eval", result)
                    tokens.pop(v + 1)
                    tokens.pop(v - 1)
                    v = 0
                else:
                    v += 1

        return tokens

    except ZeroDivisionError:
        raise Exception("SkArithmeticError: Division by zero")
    except Exception as e:
        raise Exception(f"SkArithmeticError: Invalid expression syntax ({e})")

InterpretTokens(ArithmeticOperationEvaluator(TokenizeString("echo 4 ** -0.5 ")))