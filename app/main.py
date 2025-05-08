import sys

from reslover import Resolver
from lox_scanner import Scanner 
from lox_parser import Parser
from lox_interpreter import Interpreter


def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    # expression = parser.parse()
    statements = parser.parse()
    
    for stmt in statements:
        print(stmt)

    interpreter = Interpreter()
    

    resolver = Resolver(interpreter)
    resolver.resolve(statements)
    
    
    interpreter.interpret(statements)
    

    # print(f"Result: {result}")

    # if expression is not None:
    #     print(AstPrinter().print(expression))

def run_file(path):
    with open(path, 'r') as file:
        run(file.read())

def run_prompt():
    while True:
        try:
            line = input("> ")
            if not line:
                continue
            run(line)
        except (EOFError, KeyboardInterrupt):
            break

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python main.py [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()