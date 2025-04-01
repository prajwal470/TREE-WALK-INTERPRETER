import sys
# from error import lex_error  # Import the lex_error module

class lex_error():

    def lerror(self ,token , file):
        line_number = file.count("\n", 0, file.find(token)) + 1
        # print(f"Error: Unexpected token {token}")
        return ("[line %s] Error: Unexpected character: %s" % (line_number, token))
   

class Scanner(lex_error):
    def __init__(self , source):
        self.source = source
        # self.current = 0
        self.error = False
        self.index = 0

    def scan_token(self):  
        # self.index = 0  
        while self.index < len(self.source):
            token = self.source[self.index]
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
                if not self.handle_slash():
                    print("SLASH / null")
            elif token == "=":
                if self.match("="):
                    print("EQUAL_EQUAL == null")
                else:
                    print("EQUAL = null")
            elif token == "<":
                if self.match("="):
                    print("LESS_EQUAL <= null")
                else:
                    print("LESS < null")
            elif token == ">":
                if self.match("="):
                    print("GREATER_EQUAL >= null")
                else:
                    print("GREATER > null")
            elif token == "!":
                if self.match("="):
                    print("BANG_EQUAL != null")
                else:
                    print("BANG ! null")
            else:
                error_response = self.lerror(token , self.source)
                print(error_response,file=sys.stderr,)
                self.error = True
            self.index += 1

    def match(self, expected):
        if self.index + 1 < len(self.source) and self.source[self.index + 1] == expected:
            self.index += 1
            return True
        return False
    
    def handle_slash(self):
        if self.match("/"):
            while self.index < len(self.source) and self.source[self.index] != "\n":
                self.index += 1
        else:
            return False
        return True

    def is_at_end(self):
        return self.index >= len(self.source)
    
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
    scan = Scanner(file_contents)
    scan.scan_token()
   
    # index = 0
    # while index < len(file_contents):
    #     token = file_contents[index]
    #     if token == "(":
    #         print("LEFT_PAREN ( null")
    #     elif token == ")":
    #         print("RIGHT_PAREN ) null")
    #     elif token == "{":
    #         print("LEFT_BRACE { null")
    #     elif token == "}":
    #         print("RIGHT_BRACE } null")
    #     elif token == "[":
    #         print("LEFT_BRACKET [ null")
    #     elif token == "]":
    #         print("RIGHT_BRACKET ] null")
    #     elif token == ";":
    #         print("SEMICOLON ; null")
    #     elif token == ",":
    #         print("COMMA , null")
    #     elif token == ".":
    #         print("DOT . null")
    #     elif token == "+":
    #         print("PLUS + null")
    #     elif token == "-":
    #         print("MINUS - null")
    #     elif token == "*":
    #         print("STAR * null")
    #     elif token == "/":
    #         print("SLASH / null")
    #     elif token == "!":
    #         print("BANG_EQUAL = BANG")
    #     elif token == "=":
    #         if index + 1 < len(file_contents) and file_contents[index + 1] == "=":
    #             print("EQUAL_EQUAL == null")  
    #             # Skip the next characte
    #             index += 1
    #         else:
    #             print("EQUAL = null")
    #     else:
    #         error = True
    #         line_number = file_contents.count("\n", 0, file_contents.find(token)) + 1
    #         print(
    #             "[line %s] Error: Unexpected character: %s" % (line_number, token),
    #             file=sys.stderr,
    #         )
    #     index += 1
    



    print("EOF  null")

    if scan.error:
        exit(65)
    else:
        exit(0)

    print("EOF  null") 


if __name__ == "__main__":
    main()
