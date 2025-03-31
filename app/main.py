import sys
# from error import lex_error  # Import the lex_error module

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage
    # if file_contents:
    #     raise NotImplementedError("Scanner not implemented")
    # else:
    #     print("EOF  null") # Placeholder, remove this line when implementing the scanner
    error = False
    for token in file_contents:
        if token == "(":
            print("LEFT_PAREN ( null")
        elif token == ")":
            print("RIGHT_PAREN ) null")
        elif token == "{":
            print("LEFT_BRACE { null")
        elif token == "}":
            print("RIGHT_BRACE } null")
        elif token == "[":
            print("LEFT_BRACKET [ null")
        elif token == "]":
            print("RIGHT_BRACKET ] null")
        elif token == ";":
            print("SEMICOLON ; null")
        elif token == ",":
            print("COMMA , null")
        elif token == ".":
            print("DOT . null")
        elif token == "+":
            print("PLUS + null")
        elif token == "-":
            print("MINUS - null")
        elif token == "*":
            print("STAR * null")
        elif token == "/":
            print("SLASH / null")
        elif token == "!":
            print("BANG_EQUAL = BANG")
        else:
            error = True
            line_number = file_contents.count("\n", 0, file_contents.find(token)) + 1
            print(
                "[line %s] Error: Unexpected character: %s" % (line_number, token),
                file=sys.stderr,
            )
    print("EOF  null")
    
    
    if error:
        exit(65)
    else:
        exit(0)

    print("EOF  null") 


if __name__ == "__main__":
    main()
