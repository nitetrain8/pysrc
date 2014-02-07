# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

from random import randint

_num_to_name = {
            0 : 'rock',
            1 : 'spock',
            2 : 'paper',
            3 : 'lizard', 
            4 : 'scissors'
}

_name_to_num = {
                'rock' : 0,
                'spock' : 1,
                'paper' : 2,
                'lizard' : 3,
                'scissors' : 4
                
}

def number_to_name(number):
    return _num_to_name[number]

    
def name_to_number(name):
    
    try:
        mynum = _name_to_num[name.lower()]
        
    except KeyError:
        print("You suck! Name not in RSPLS. You get Scissors.")
        mynum = _name_to_num['scissors']
        
    return mynum


def rpsls(name): 
    p_choice = name_to_number(name)
    c_choice = 4


    if (0 < c_choice - p_choice <= 2) or (p_choice - c_choice >= 3):
        winner = 'Computer'
    elif (c_choice == p_choice):
        winner = 'Tie! nobody'
    else:
        winner = 'Player'
        
    print("\nPlayer chooses %s!" % number_to_name(p_choice))
    print("Computer chooses %s!" % number_to_name(c_choice))
    
    print("%s wins!" % winner)
        
def main():
    
    playing = 1
    
    while playing:
        print("\nRock, paper, Spock, lizard, scissors! Make a choice or Q to quit")
        p_input = input('> ')
        
        if p_input in "qQ":
            playing = 0
        
        else: 
            rpsls(p_input)
            
        
    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric
if __name__ == "__main__":
    main()
