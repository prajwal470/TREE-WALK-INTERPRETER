import sys

class lex_error():

    def error(token , file):
        
        
        line_number = file.count("\n", 0, file.find(token)) + 1
        # print(f"Error: Unexpected token {token}")
        return ("[line %s] Error: Unexpected character: %s" % (line_number, token))