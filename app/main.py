import sys
# from error import lex_error  # Import the lex_error module
 # Import Enum for defining TokenType

class lex_error():

    def lerror(self ,token , line_number):
        line_number = line_number
        # print(f"Error: Unexpected token {token}")
        return ("[line %s] Error: Unexpected character: %s" % (line_number, token))

    def string_error(self, line_number):
        return ("[line %s] Error: Unterminated string." % (line_number))



class Token:
    def __init__(self, type: TOKEN_TYPE, name: str, value):
        self.type = type
        self.name = name
        self.value = value
    def __str__(self):
        return f"{str(self.type)} {self.name} {self.value}"
    def __repr__(self):
        return str(self)


class Scanner(lex_error):

    keywords = {
        "and": "AND",
        "class": "CLASS",
        "else": "ELSE",
        "false": "FALSE",
        "for": "FOR",
        "fun": "FUN",
        "if": "IF",
        "nil": "NIL",
        "or": "OR",
        "print": "PRINT",
        "return": "RETURN",
        "super": "SUPER",
        "this": "THIS",
        "true": "TRUE",
        "var": "VAR",
        "while": "WHILE",
    }
    



    def __init__(self , source):
        self.source = source
        # self.line_number = 0
        self.error = False
        self.index = 0
        self.line_string = ""
        self.start = 0



    def scan_token(self):  
        # elf.index = 0  
        
        for line_number, string in enumerate(self.source.split("\n")):
            self.index = 0
            self.curent_line_string = string
            
            while self.index < len(string):
                token = string[self.index]
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
                elif token in [" ", "\t","\r","\n"]:
                    pass
                elif token == '"':
                    value = self.handle_string(line_number)
                    if self.error:
                        print(value,file=sys.stderr,)
                    else:
                        print(value)   
                elif token.isdigit():
                    value = self.handle_number(line_number)
                    print(value)

                elif token.isalpha() or token == "_":
                    value = self.identifier()
                    print(value)
                else:
                    error_response = self.lerror(token ,line_number+1)
                    print(error_response,file=sys.stderr,)
                    self.error = True        
                self.index += 1

    def is_at_end(self):
        return self.index >= len(self.source)

    def is_digit(self, char):
        return char >= "0" and char <= "9"
    
    def is_number(self, character: str):
        return character.isnumeric()
    
    def is_alpha(self, character: str):
        return character.isalpha() or character == "_"
    
    def is_alpha_or_number(self, character: str):
        return self.is_number(character) or self.is_alpha(character)
    
    def peek(self):
        return "\0" if self.is_at_end() else self.curent_line_string[self.index]
    
    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.curent_line_string[self.index + 1]

    def identifier(self):
        value = []
        while self.index < len(self.curent_line_string) and self.is_alpha_or_number(self.curent_line_string[self.index]):
            self.index += 1
            value.append(self.curent_line_string[self.index-1])
        

        value = "".join(value)
        self.index -= 1

        if value in self.keywords:
            key = self.keywords[value]

            return f"{key} {key.lower()} null"
        else:
            return f"IDENTIFIER {value} null"   


    def handle_number(self, line_number):
        number = []
        decimal = False



        while self.index < len(self.curent_line_string) and self.is_digit(self.curent_line_string[self.index]):

            number.append(self.curent_line_string[self.index])
            self.index += 1

        if self.index < len(self.curent_line_string) and self.curent_line_string[self.index] == ".":
            decimal = True
            number.append(".")
            self.index += 1

        while self.index < len(self.curent_line_string) and self.is_digit(self.curent_line_string[self.index]):
            number.append(self.curent_line_string[self.index])
            self.index += 1
                
        if decimal:
            number_str = "".join(number)
            handled_number = self.handle_extrazero(number) 
            handle_extrazero = "".join(handled_number)
            self.index -= 1
            return f'NUMBER {number_str} {handle_extrazero}'
        else:
            number_str = "".join(number)
            self.index -= 1
            return f'NUMBER {number_str} {number_str}.0'

 


    def handle_extrazero(self, number):
        
        for i in range(len(number) - 1, -1, -1):
            if number[i-1] != "." and number[i] == "0":
                if number[i] == "0":
                    number.pop(i)
                else:
                    break
            else:
                break
        return number
    

    def handle_string(self,line_number):
        
        temp_string = []
        
        self.index += 1
        while self.index < len(self.curent_line_string) and self.curent_line_string[self.index] != '"':
            temp_string.append(self.curent_line_string[self.index])
            self.index += 1

        if self.index == len(self.curent_line_string):
            self.error = True
            error_response = self.string_error(line_number+1)
            return error_response
        else:
            string = "".join(temp_string)
            return f'STRING "{string}" {string}'



            
    def match(self, expected):
        if self.index + 1 < len(self.curent_line_string) and self.curent_line_string[self.index + 1] == expected:
            self.index += 1
            return True
        return False
    
    def handle_slash(self):
        if self.match("/"):
            while self.index < len(self.curent_line_string) and self.curent_line_string[self.index] != "\n":
                self.index += 1
        else:
            return False
        return True
    


    class Praser():
        pass









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

    scan = Scanner(file_contents)
    scan.scan_token()
   
    print("EOF  null")

    if scan.error:
        exit(65)
    else:
        exit(0)

    


if __name__ == "__main__":
    main()
