def handle_number(self):
    number = []
    decimal = False
    
    while self.index < len(self.curent_line_string) and self.curent_line_string[self.index].isdigit():
        self.index += 1

    print(number)         
    if decimal:
        number_str = "".join(number)
        handled_number = self.handle_extrazero(number) 
        handle_extrazero = "".join(handled_number)
        return f'NUMBER {number_str} {handle_extrazero}'
    else:
        number_str = "".join(number)
        return f'NUMBER {number_str} {number_str}.0'


def handle_extrazero(number):
    for i in range(len(number) - 1, -1, -1):
        if number[i-1] != "." and number[i] == "0":
            if number[i] == "0":
                number.pop(i)
            else:
                break
        else:
            break
    return number