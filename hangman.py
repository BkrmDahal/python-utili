import random                       # To generate random number to choose from list

cont = ""                             # variable, if programmer want to exit or play new game

while(cont!="end"):                   # If user input is 'end', END game
    print('''Hang man               
    Rule:
    1. You have six guess to make.
    2. Only wrong guess will be counted against you
    3. Always enter single letter and only letter from atoz.
    4. To exit game, during anytime type "end" ''')     #Rules
    print("\n")

    list_for_hangman = ['hello', 'world', 'king', 'queen', 'zebra', 
                            'python', 'anaconda']            #list of word to choose from 
    word_for_hangman = list_for_hangman[random.randint(0,6)] # randomly select word for game
    word_to_guess = ["_"] * len(word_for_hangman)            # shows word as '_', masking
    allowed_guess =6                                         # No of guess allowed
    guess = []                                               # Variable to store all guess of player
    valid_letters = "abcdefghijklmnopqrustuwxyz"             # Validation for user input(only allow test char as input)
    user_input = ""                                          # variable to store user_input

    print ("The word you're looking for is "+ str(word_to_guess)) 
    while (user_input!="end" and allowed_guess!=0) :            # until user_input is 'end' or no_guess not 0 
        user_input = input("Enter your guess letter: ")         # user input
        #clean the input 
        user_input = str(user_input)                            
        user_input.strip()                                      
        user_input = user_input.lower()    
        
        # check if letter is valid input and no of char is 1
        if user_input in valid_letters and len(user_input)==1:  
            
            #check if letter is in game word
            if user_input in word_for_hangman:  
                ''' if word is present than replace '_' with letter but some time same chr may be mutiple place
                than replace all '_' with letter, like for 'queen' if input is 'e' output will be '_ _ e e _ ' '''
                place_of_word = 0                               
                start = 0
                while place_of_word !=-1:                      
                    place_of_word = word_for_hangman.find(user_input, start)
                    #if position of user_input is not -1 ie  letter is still present in word, replace the '_' with letter
                    if place_of_word !=-1:
                        word_to_guess[place_of_word] = user_input
                        print("Success!!! Still more to go. The word you are looking for is:"+ str(word_to_guess))
                        start = place_of_word+1             # increased the index of letter
                        
                # if '_' is still present word is not complete so continue
                if '_' in word_to_guess:
                    guess.append(user_input)
                    print("Letter you have already guessed :" + str(''.join(guess)))
                    print("NO OF GUESS REMAINING:"+ str(allowed_guess))
                # if '_' is not present, word is complete type 'you won' and exit game
                else:
                    print("YOU WON")
                    break
            # If wrong guess decrease allowed_guess and continous
            else:
                print("WRONG LETTER!!! CAREFUL, You only have "+ str(allowed_guess-1), " guess left.")
                guess.append(user_input)
                print("Letter you have already guessed :" + str(''.join(guess)))
                allowed_guess = allowed_guess-1
                
        # if user_input multiple char
        elif len(user_input)!=1:
            print("Enter SINGLE LETTER.")
            print("NO OF GUESS REMAINING:"+ str(allowed_guess))
            print("Letter you have already guessed :" + str(''.join(guess)))

        #if user_input is not valid char
        elif user_input not in valid_letters:
            print("Please LETTER ONLY")
            print("NO OF GUESS REMAINING:"+ str(allowed_guess))
            print("Letter you have already guessed :" + str(''.join(guess)))
            
    # if allowed guess is zero or user type end , you loose
    if (allowed_guess == 0 or user_input=="end"):
        print("YOU LOSE!!!")
        print("Word you are looking for was "+ word_for_hangman.upper())
        
    #ask user if they want new game or want to exit
    cont = input("To play again click any key, to exit game type 'end':")
