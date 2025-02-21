import random
import os
import sys
os.system('cls||clear')

class Wordle:
    def __init__(self):
        self.guess = str()
        self.not_used = set()
        self.d = open("words_ta.txt").read().splitlines()
        lines = open('words_la.txt').read().splitlines()
        self.ascii_lines = open("ascii.txt").read().splitlines()
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
        for line in self.fields:
            line_print = self.print_letter(line)
            for line2 in line_print:
                print(line2)
            #line_print = str()
            #for letter in line:
                #line_print += " " + "\033[4m" + letter + "\033[0m" + " "  # Underlined text
            #print(line_print)

        if self.guess == self.word_of_day_list:
            print("you win!")
            sys.exit()
        elif self.guess_count == 6:
            print("you lose, the correct word was " + self.word_of_day)
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
                self.guess = input("Guess: ").lower()
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
                self.fields[self.guess_count][i] = self.guess[i]
                self.not_used.add(self.guess[i])
        
       
        os.system('cls||clear')  # This works for Windows/Linux, may need different handling for macOS
        

    def print_letter(self, line):
        #base len needed: 12
        line_prints = ["", "", "", "", "", "", ""]
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
       
        return line_prints
if __name__ == "__main__":
    Wordle()
    
    
