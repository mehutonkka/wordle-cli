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
        print("    \033[1mWordle!\033[0m")  # Bold text
        for line in self.fields:
            line_print = str()
            for letter in line:
                line_print += " " + "\033[4m" + letter + "\033[0m" + " "  # Underlined text
            print(line_print)

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
        
        try:
            self.guess = input("Guess: ").lower()
        except KeyboardInterrupt:
            sys.exit()
        
        
        if self.guess not in self.d:
            print(f"{self.guess} is not a valid word! Try again.")
            self.user_input()
        
        self.guess = list(self.guess)
        for right in self.word_of_day_list:
            rights[right] = self.word_of_day_list.count(right)
        
        for i in range(5):
            if self.guess[i] == self.word_of_day_list[i]:
                # green
                rights[self.guess[i]] -= 1
                self.fields[self.guess_count][i] = "\033[32m" + self.guess[i] + "\033[0m"
        for i in range(5):
            if self.fields[self.guess_count][i] != "_":
                pass
            elif self.guess[i] in self.word_of_day_list:
                # yellow
                if rights[self.guess[i]] > 0:
                    rights[self.guess[i]] -= 1
                    self.fields[self.guess_count][i] = "\033[33m" + self.guess[i] + "\033[0m"
                    
                else:
                    self.fields[self.guess_count][i] = self.guess[i]
            else:
                # normal
                self.fields[self.guess_count][i] = self.guess[i]
                self.not_used.add(self.guess[i])
        
       
        os.system('cls||clear')  # This works for Windows/Linux, may need different handling for macOS
        


if __name__ == "__main__":
    Wordle()
