import random
import os
import sys
import argparse
os.system('stty cols 1000 rows 400')
os.system('cls||clear')

class Wordle:
    def __init__(self):
        self.bonsai = False
        parser = argparse.ArgumentParser(description='Wordle CLI game with bonsai')
        parser.add_argument('--bonsai', action='store_true', help='Show Bonsai ASCII art') #if args.bonsai: args bonsai lines 27, end: line index 4, start: line index 1
        args = parser.parse_args()
        if args.bonsai:
            self.bonsai = True
        self.guess = str()
        self.not_used = set()
        self.usable = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.d = open("words_ta.txt").read().splitlines()
        lines = open('words_la.txt').read().splitlines()
        self.ascii_lines = open("ascii2.txt").read().splitlines()
        #a b c d e f g h i j k l m n o p q r s t u v w x y z
        self.dict_ranges = {'a': 7, 'b': 14, 'c': 21, 'd': 28, 'e': 35, 'f': 42, 'g': 49, 'h': 56, 'i': 63, 'j': 70, 'k': 77, 'l': 84, 'm': 91, 'n': 98, 'o': 105, 'p': 112, 'q': 119, 'r': 126, 's': 133, 't': 140, 'u': 147, 'v': 154, 'w': 161, 'x': 168, 'y': 175, 'z': 182, '_': 189}
        self.word_of_day = random.choice(lines)
        self.word_of_day_list = list(self.word_of_day)
        self.fields = [
            ["_", "_", "_", "_", "_"], 
            ["_", "_", "_", "_", "_"], 
            ["_", "_", "_", "_", "_"], 
            ["_", "_", "_", "_", "_"], 
            ["_", "_", "_", "_", "_"], 
            ["_", "_", "_", "_", "_"]
        ]
        self.guess_count = 0
        #print(self.word_of_day_list)  # You can remove this line if you want to keep it hidden
        
        self.main()

    def main(self):
        for i in range(7):
            print("\033[1m" + self.ascii_lines[i] + "\033[0m")
        #print("    \033[1mWordle!\033[0m")  # Bold text
        for index, line in enumerate(self.fields):
            line_print = self.print_letter(line, index)
            for line2 in line_print:
                print(line2)
            #line_print = str()
            #for letter in line:
                #line_print += " " + "\033[4m" + letter + "\033[0m" + " "  # Underlined text
            #print(line_print)

        if self.guess == self.word_of_day_list:
            print("\n  you win!")
            sys.exit()
        elif self.guess_count == 6:
            print("\n  you lose, the correct word was " + self.word_of_day)
            sys.exit()
        else:
            if self.guess_count < 6:
                self.user_input()
                self.guess_count += 1
                self.main()

    def user_input(self):
        rights = {}
        self.guess = None
        while self.guess not in self.d:
            try:
                self.guess = input("\n  Guess: ").lower()
            except KeyboardInterrupt:
                sys.exit()
        
        
        #if self.guess not in self.d:
            #print(f"{self.guess} is not a valid word! Try again.")
            #self.user_input()
        
        self.guess = list(self.guess)
        for right in self.word_of_day_list:
            rights[right] = self.word_of_day_list.count(right)
        
        for i in range(5):
            
            if self.guess[i] == self.word_of_day_list[i]:
                # green
                rights[self.guess[i]] -= 1
                self.fields[self.guess_count][i] = ("\033[32m", self.guess[i])
        for i in range(5):
            if self.fields[self.guess_count][i] != "_":
                pass
            elif self.guess[i] in self.word_of_day_list:
                # yellow
                if rights[self.guess[i]] > 0:
                    rights[self.guess[i]] -= 1
                    self.fields[self.guess_count][i] = ("\033[33m", self.guess[i])
                    
                else:
                    self.fields[self.guess_count][i] = self.guess[i]
            else:
                # normal
                try:
                    self.usable.remove(self.guess[i])
                except ValueError:
                    pass
                self.fields[self.guess_count][i] = self.guess[i]
                self.not_used.add(self.guess[i])
        
       
        os.system('cls||clear')  # This works for Windows/Linux, may need different handling for macOS
        

    def print_letter(self, line, index):
        #base len needed: 12
        line_prints = ["  ", "  ", "  ", "  ", "  ", "  ", "  "]
        for letter in line: # "a" "b" "c" "d" "e"
            if len(letter) > 1:
                letterx = letter[1]
                letter_range = self.dict_ranges[letterx]
                for i in range(letter_range, letter_range+7):
                    remaining_width = 12 - len(self.ascii_lines[i])
                    line_prints[i-letter_range] += "" + letter[0] + self.ascii_lines[i] + "\033[0m"
            else:
                
                letter_range = self.dict_ranges[letter]
                for i in range(letter_range, letter_range+7):
                    remaining_width = 12 - len(self.ascii_lines[i])
                    line_prints[i-letter_range] += "" + self.ascii_lines[i] + ""
        if self.bonsai:
            if index == 1:
                line_prints[0] += "            " + self.ascii_lines[196]
                line_prints[1] += "            " + self.ascii_lines[197]
                line_prints[2] += "            " + self.ascii_lines[198]
                line_prints[3] += "            " + self.ascii_lines[199]
                line_prints[4] += "            " + self.ascii_lines[200]
                line_prints[5] += "            " + self.ascii_lines[201]
                line_prints[6] += "            " + self.ascii_lines[202]
            elif index == 2:
                line_prints[0] += "            " + self.ascii_lines[203]
                line_prints[1] += "            " + self.ascii_lines[204]
                line_prints[2] += "            " + self.ascii_lines[205]
                line_prints[3] += "            " + self.ascii_lines[206]
                line_prints[4] += "            " + self.ascii_lines[207]
                line_prints[5] += "            " + self.ascii_lines[208]
                line_prints[6] += "            " + self.ascii_lines[209]
            elif index == 3:
                line_prints[0] += "            " + self.ascii_lines[210]
                line_prints[1] += "            " + self.ascii_lines[211]
                line_prints[2] += "            " + self.ascii_lines[212]
                line_prints[3] += "            " + self.ascii_lines[213]
                line_prints[4] += "            " + self.ascii_lines[214]
                line_prints[5] += "            " + self.ascii_lines[215]
                line_prints[6] += "            " + self.ascii_lines[216]
            elif index == 4:
                line_prints[0] += "            " + self.ascii_lines[217]
                line_prints[1] += "            " + self.ascii_lines[218]
                line_prints[2] += "            " + self.ascii_lines[219]
                line_prints[3] += "            " + self.ascii_lines[220]
                line_prints[4] += "            " + self.ascii_lines[221]
                line_prints[5] += "            " + self.ascii_lines[222]
        if index == 5:
            row1 = ""
            row2 = ""
            for index1, usable in enumerate(self.usable):
                if index1 <= 12:
                    row1 += usable + "  "
                else:
                    row2 += usable + "  "
            line_prints[2] += "            letters:"
            line_prints[3] += "            " + row1
            line_prints[4] += "            " + row2
        return line_prints
if __name__ == "__main__":
    Wordle()
    
    
