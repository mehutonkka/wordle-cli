import random
import os
import sys
import argparse
import time
if os.name == 'nt':
    import msvcrt
    os.system('mode con: cols=140 lines=53')
else:
    import termios
    import tty
    os.system('stty cols 150 rows 53')



os.system('cls||clear')

class Wordle:
    def __init__(self):
        # Argument and bonsai stuff
        self.bonsai = False
        parser = argparse.ArgumentParser(description='Wordle CLI game with bonsai')
        parser.add_argument('-bonsai', action='store_true', help='Show Bonsai ASCII art') # Show bonsai
        parser.add_argument('-letters', action='store_true', help='Show actual letters next to ASCII art letters')
        args = parser.parse_args()
        if args.bonsai:
            self.bonsai = True
            self.bonsai_lines = open("bonsai.txt").read().splitlines()
        if args.letters:
            self.ascii_lines = open("ascii3.txt").read().splitlines()
        else:
            self.ascii_lines = open("ascii2.txt").read().splitlines()
        
        
        
        
        
        
        # Open files and other variable/info
        self.guess = str()
        self.guess_count = 0
        self.alpha = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
        self.usable = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.d = open("words_ta.txt").read().splitlines()
        lines = open('words_la.txt').read().splitlines()
        
        
        
        # Letter ASCII stuff
        #a b c d e f g h i j k l m n o p q r s t u v w x y z _ -
        self.dict_ranges = {'a': 7, 'b': 14, 'c': 21, 'd': 28, 'e': 35, 'f': 42, 'g': 49, 'h': 56, 'i': 63, 'j': 70, 'k': 77, 'l': 84, 'm': 91, 'n': 98, 'o': 105, 'p': 112, 'q': 119, 'r': 126, 's': 133, 't': 140, 'u': 147, 'v': 154, 'w': 161, 'x': 168, 'y': 175, 'z': 182, '_': 189, '-': 196}
        self.bg = 0
        self.letters_ascii = dict()
        self.header_ascii = []

        # Get random word
        self.word_of_day = random.choice(lines)
        self.word_of_day_list = list(self.word_of_day)
        self.bg_list = self.word_of_day_list.copy()
        
        # Gameboard fields
        self.fields = [
            ["-", "_", "_", "_", "_"], 
            ["_", "_", "_", "_", "_"], 
            ["_", "_", "_", "_", "_"], 
            ["_", "_", "_", "_", "_"], 
            ["_", "_", "_", "_", "_"], 
            ["_", "_", "_", "_", "_"]
        ]
        
        
        # Initialise ascii and then start the program
        self.initialise_ascii()

        while True:
            self.main()

    def initialise_ascii(self):
        for line_num in range(7):
            self.header_ascii.append("\033[1m" + self.ascii_lines[line_num] + "\033[0m")

        for letter in self.dict_ranges.keys():
            self.letters_ascii[letter] = []
            letter_range = self.dict_ranges[letter]
            for line_num in range(letter_range, letter_range+7):
                self.letters_ascii[letter].append(self.ascii_lines[line_num])


    def main(self):
        self.print_all()
        #print(self.word_of_day_list)  # You can remove this line if you want to keep it hidden
        
        
        if self.guess == self.word_of_day_list:
            print("\n\033[32m   you win!\033[0m")
            sys.exit()
        elif self.guess_count == 6:
            print("\n\033[31m   you lose, the correct word was " + self.word_of_day + "\033[0m")
            sys.exit()
    
        if self.guess_count < 6:
            self.user_input()
            self.guess_count += 1
            

    def user_input(self):
        rights = {}
        self.input_loop()
        
        self.guess = list(self.guess)
        for right in self.word_of_day_list:
            rights[right] = self.word_of_day_list.count(right)
        
        # Go through correct letters first
        for i in range(5):
            if self.guess[i] == self.word_of_day_list[i]:
                # green
                if self.guess[i] in self.bg_list:
                    self.bg += 27
                    self.bg_list.remove(self.guess[i])
                rights[self.guess[i]] -= 1
                self.fields[self.guess_count][i] = ("\033[32m", self.guess[i])

        # Then possible "yellow" letters
        for i in range(5):
            if len(self.fields[self.guess_count][i]) == 2:
                pass
            elif self.guess[i] in self.word_of_day_list:
                # yellow
                if rights[self.guess[i]] > 0:
                    rights[self.guess[i]] -= 1
                    self.fields[self.guess_count][i] = ("\033[33m", self.guess[i])
                    
            else:
                # normal
                if self.guess[i] in self.usable:
                    self.usable.remove(self.guess[i])
                
                
        
        #os.system('cls||clear')  # This works for Windows/Linux, may need different handling for macOS

    def input_loop(self):
        self.guess = ""
        #word = ["_", "_", "_", "_", "_"]
        word_index = -1
        
        while True:
            letter = self.get_input()
            
            if letter == "ESC":
                print("\n\033[31m   manual end with ESC\033[0m")
                sys.exit()
            elif letter == "ENTER" and self.guess in self.d:
                if self.guess_count < 5:
                    self.fields[self.guess_count+1][0] = "-"
                break
            elif letter == "BACKSPACE" and word_index != -1 and word_index >= 0:
                word_index -= 1
                self.fields[self.guess_count][word_index+1] = "-"
                if word_index < 3:
                    self.fields[self.guess_count][word_index+2] = "_"
                self.guess = self.guess[:-1]
                
            elif len(self.guess) < 5 and len(letter) <= 1 and letter in self.alpha and word_index < 5: 
                if word_index < 3:
                    self.fields[self.guess_count][word_index+2] = "-"
                word_index += 1
                self.fields[self.guess_count][word_index] = letter
                self.guess += letter
            
            self.print_all()
 
    def get_input(self):
        def decode_key( key ):
            if key in KEY_MAPPING:
                key = KEY_MAPPING[ key ]

            return key

        if os.name == 'nt':
            KEY_MAPPING = {'\r': 'ENTER','\t': 'TAB', '\x08': 'BACKSPACE', '\x1b': 'ESC'}
            while True:
                if msvcrt.kbhit(): #key is pressed
                    key = msvcrt.getwch() #decode
                    key = decode_key(key)
                    
                    return key
                
        else:
            #KEY_MAPPING = {'\n': 'ENTER', '\t': 'TAB', '\x7f': 'BACKSPACE', '\x1b': 'ESC'}
            filedescriptors = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin)
            key = sys.stdin.read(1)[0]
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN,filedescriptors) 
            key = decode_key(key)
            return key         
    
    def print_all(self):
        os.system('cls||clear')  # This works for Windows/Linux, may need different handling for macOS
        # WORDLE header
        for line_h in self.header_ascii:
            print(line_h)

        # Gameboard
        for index, line in enumerate(self.fields):
            line_prints = ["  ", "  ", "  ", "  ", "  ", "  ", "  "]
            
            for letter in line: # "a" "b" "c" "d" "e"
                color_code = ""
                if len(letter) > 1: # if colors
                    color_code = letter[0]
                    letter = letter[1]

                for line_num in range(7):
                    line_prints[line_num] += color_code + self.letters_ascii[letter][line_num]+ "\033[0m"

            # Bonsai
            if self.bonsai:
                if 1 <= index <= 4:
                    for line_num in range(7):
                        line_prints[line_num] += "            " + self.bonsai_lines[line_num+((index-1)*7) + self.bg].encode().decode("unicode_escape")

            # Available letters
            if index == 5:
                row1 = "  ".join(self.usable[:13])
                row2 = "  ".join(self.usable[13:])
                
                line_prints[2] += "          usable letters:"
                line_prints[3] += "          " + row1
                line_prints[4] += "          " + row2

            for line_to_print in line_prints:
                print(line_to_print)
        
if __name__ == "__main__":
    Wordle()
    
    
