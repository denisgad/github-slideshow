import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return(f'{self.rank} of {self.suit}')

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        card_str = ''
        for single_card in self.deck:
            card_str += '\n' + single_card.__str__()
        return card_str

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self,if_player):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.if_player = if_player

    def add_card(self,card): #add card method split into player version and dealer version
        
        self.cards.append(card)
        
        if card.rank == "Ace" and self.if_player == True: #player's add card with prompt for ace 
            
            loop_control = True
            
            while loop_control:
            
                a = int(input('What value does this ace have? 1 or 11 \nType 1 or 11 respectively: '))

                if a == 11:
                    self.value += 11
                    loop_control = False
                    
                elif a == 1:
                    self.value += 1
                    loop_control = False
                
                else:
                    continue
                    
        
        elif card.rank == "Ace" and self.if_player == False: #dealer's add card with logic for ace
            if self.value + 11 <= 17:
                self.value += 11
                loop_control = False
            
            else:
                self.value += 1
                loop_control = False 
            
        else:
            self.value += values[card.rank]
        
class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("What is your bet?: "))
            
        except ValueError:
            print('Not a number!!!\n')
            continue
        
        else:
            if chips.bet > chips.total:
                print('Not enough money!!!\n')
                continue
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())

def hit_or_stand(deck,hand):
    global playing # to control an upcoming while loop
    
    if hand.if_player == True:
        
        while True:
            a = input('\nWhat do you want to do? Hit or stand? \nType "h" or "s" respectively: ')

            if a[0].lower() == "h":
                hit(deck,hand)
                break

            elif a.lower() == "s":
                playing = False
                break

            else:
                continue
                
    else:
        while hand.value < 17:
            hit(deck,hand)

def show_some(player,dealer):
    
    print("\nPlayer's hand: ",*player.cards,sep="\n")
    print(f"The value of player's cards: {player.value}")
    
    temp = dealer.cards.copy()
    temp[0] = "Hidden Card"
    print("\nDealer's hand: ",*temp,sep="\n")

def show_all(player,dealer):
    
    print("\nPlayer's hand: ",*player.cards,sep="\n")
    print(f"The value of player's cards: {player.value}")
    
    print("\nDealer's hand: ",*dealer.cards,sep="\n")
    print(f"The value of dealer's cards: {dealer.value}")

def player_busts(chips):
    chips.lose_bet()
    print("\nPlayer busts! Dealer wins!")
    
def player_wins(chips):
    chips.win_bet()
    print("\nPlayer wins!")

def dealer_busts(chips):
    chips.win_bet()
    print("\nDealer busts! Player wins!")
    
def dealer_wins(chips):
    chips.lose_bet()
    print("\nDealer wins!")
    
def push():
    print("\nPush! It's a draw!")

game_on = True

print('Hello! Welcome to a game of Black Gad!\n')# Print an opening statement

players_chips = Chips() # Set up the Player's chips

while game_on:
    
    playing = True #this is here not to rerun the top cell
    
    the_deck = Deck()# Create & shuffle the deck, deal two cards to each player
    the_deck.shuffle()
    
    players_hand = Hand(True)
    dealers_hand = Hand(False)
          
    for a in [0,1]:
        players_hand.add_card(the_deck.deal())
        dealers_hand.add_card(the_deck.deal())
    
    take_bet(players_chips) # Prompt the Player for their bet

    show_some(players_hand,dealers_hand) # Show cards (but keep one dealer card hidden)

    while playing:  # recall this variable from our hit_or_stand function
        
        hit_or_stand(the_deck,players_hand) # Prompt for Player to Hit or Stand
        
        show_some(players_hand,dealers_hand) # Show cards (but keep one dealer card hidden)
 
        if players_hand.value > 21: # If player's hand exceeds 21, run player_busts() and break out of loop
            
            player_busts(players_chips) 
            
            break

    if players_hand.value <= 21: # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        
        print("\nDealer's turn!")
        
        show_all(players_hand,dealers_hand)
        
        hit_or_stand(the_deck,dealers_hand)
        
        print("\nDealer is finished")
        
        show_all(players_hand,dealers_hand) # Show all cards
    
        
        if dealers_hand.value <= 21: # Run different winning scenarios
            if dealers_hand.value == players_hand.value:
                push()
            
            elif dealers_hand.value > players_hand.value:
                dealer_wins(players_chips)
            
            else:
                player_wins(players_chips)
        
        else:
            dealer_busts(players_chips)
           
    print(f"\nPlayer's chips: {players_chips.total}") # Inform Player of their chips total 
    
    if players_chips.total != 0:
    
        play_again = input("\nDo you want to play again? Type Y or N respectively: ") # Ask to play again

        if play_again == "Y": 
            players_hand.cards = []
            dealers_hand.cards = []

            players_hand.value = 0
            dealers_hand.value = 0

            players_chips.bet = 0

            print('Hands reset!')

        else:
            game_on = False
            
    else:
        print("The player has no money! Game over!")
        game_on = False