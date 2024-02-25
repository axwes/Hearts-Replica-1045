from __future__ import annotations
from cards import Card, Rank, Suit
from player import Player


class HumanPlayer(Player):
    """ HumanPlayer class that inherits base player and asks the user to input a name when initialising itself. """

    def __init__(self) -> None:
        self.name = ""
        self.hand = []
        self.round_score = 0
        self.total_score = 0

    def set_name(self):
        """
        A method to set the name of the player.

        Arguments:
        - self (to access variables that belong to that class)

        Does not return anything.
        """

        # prompts user to enter name and stores it in self.name
        entername = input("Enter your name: ")
        self.name = entername

    def get_name(self):
        """
        A method to get the name of the player.

        Arguments:
        - self (to access variables that belong to that class)

        Returns the name of the player.
        """

        return self.name

    def printcard(self, cardlist):
        """
        		A method used to return the art and the index for each card in a list
        		Arguments:
        		- self (to access variables that belong to that class)
        		- cardlist (a list containing cards; either a player's hand or the trick of a round)


        		Returns the art format of cards in a list alongside their index
        		"""

        # variable that will contain the art is created with spacing
        cards_art = [""] * 6

        # the index, rank and suit of each card is retrieved
        for card in cardlist:
            index = str(cardlist.index(card))
        for i in range(len(cardlist)):
            card_rank = cardlist[i].rank
            card_suit = cardlist[i].suit

            # the spacing of when the index is determined based on if the index is one digit or two digits
            if i < 10:
                card_index = "   " + str(i) + "   "
            else:
                card_index = "  " + str(i) + "   "

            # the symbol of the suit is determined
            if card_suit == Suit.Clubs:
                symbol = '♣'
            elif card_suit == Suit.Spades:
                symbol = '♠'
            elif card_suit == Suit.Hearts:
                symbol = '♥'
            elif card_suit == Suit.Diamonds:
                symbol = '♦'

            # dictionary for each card and its index is created according to Rank
            # the suit symbol is formatted accordingly
            card_art = {
                Rank.Two: ["┌─────┐", "│2    │", "│  {}  │".format(symbol), "│    2│", "└─────┘",
                           "{}".format(card_index)],
                Rank.Three: ["┌─────┐", "│3    │", "│  {}  │".format(symbol), "│    3│", "└─────┘",
                             "{}".format(card_index)],
                Rank.Four: ["┌─────┐", "│4    │", "│  {}  │".format(symbol), "│    4│", "└─────┘",
                            "{}".format(card_index)],
                Rank.Five: ["┌─────┐", "│5    │", "│  {}  │".format(symbol), "│    5│", "└─────┘",
                            "{}".format(card_index)],
                Rank.Six: ["┌─────┐", "│6    │", "│  {}  │".format(symbol), "│    6│", "└─────┘",
                           "{}".format(card_index)],
                Rank.Seven: ["┌─────┐", "│7    │", "│  {}  │".format(symbol), "│    7│", "└─────┘",
                             "{}".format(card_index)],
                Rank.Eight: ["┌─────┐", "│8    │", "│  {}  │".format(symbol), "│    8│", "└─────┘",
                             "{}".format(card_index)],
                Rank.Nine: ["┌─────┐", "│9    │", "│  {}  │".format(symbol), "│    9│", "└─────┘",
                            "{}".format(card_index)],
                Rank.Ten: ["┌─────┐", "│10   │", "│  {}  │".format(symbol), "│   10│", "└─────┘",
                           "{}".format(card_index)],
                Rank.Jack: ["┌─────┐", "│J    │", "│  {}  │".format(symbol), "│    J│", "└─────┘",
                            "{}".format(card_index)],
                Rank.Queen: ["┌─────┐", "│Q    │", "│  {}  │".format(symbol), "│    Q│", "└─────┘",
                             "{}".format(card_index)],
                Rank.King: ["┌─────┐", "│K    │", "│  {}  │".format(symbol), "│    K│", "└─────┘",
                            "{}".format(card_index)],
                Rank.Ace: ["┌─────┐", "│A    │", "│  {}  │".format(symbol), "│    A│", "└─────┘",
                           "{}".format(card_index)]
            }
            # the loop iterates 6 times (for the 6 elements in each rank) and it is added as a string to 'cards_art'
            for j in range(6):
                cards_art[j] += card_art[card_rank][j]

        # the diagram takes all the elements of cards_art, returns a new line between them
        # and joins them into a single string
        diagram = "\n".join(cards_art)
        return (diagram)

    def play_card(self, trick, broken_hearts):
        """
        A method to return a valid card of the player's choice, removing it from self.hand before returning.

        Arguments:
        - self (to access variables that belong to that class)
        - trick (to check current trick)
        - broken_hearts (to check if hearts has been broken)

        Returns the player's choice of card.
        """

        # initialises the arguments
        self.trick = trick
        self.broken_hearts = broken_hearts

        # sorts the hand from lowest to highest ranking.
        self.hand.sort(key=lambda x: (x.suit, x.rank))

        # prints the current trick and current hand
        print("Current trick: ", "\n" + self.printcard(self.trick))
        print("Your current hand: ", "\n" + self.printcard(self.hand))

        # a continuous loop that will only accept valid inputs
        while True:

            try:
                # asks user for index of card to play
                card_to_play = int(input("Please enter the index of the card to play: "))

                # if card index entered not in range of hand, error is raised
                if card_to_play not in range(len(self.hand)):
                    raise ValueError

                # a loop that obtains the index of each card, and executes the following conditions
                for cards in range(len(self.hand)):

                    # if card to play is valid, then remove card from hand and return card
                    if self.check_valid_play(self.hand[card_to_play], self.trick, self.broken_hearts)[0] == True:
                        card = self.hand[card_to_play]
                        self.hand.remove(self.card)
                        return (card)

                    # if card to be played is not valid, checks if card suit is heart and if hearts been broken
                    elif self.hand[card_to_play].suit == Suit.Hearts and self.broken_hearts == False:
                        print(False, ', Hearts is not broken ')
                        raise ValueError

                    # if both condition not met, means player still has cards from the suit of the current trick
                    else:
                        print(False, ',player still has cards from the suit of the current trick')
                        raise ValueError

            except ValueError:
                continue
            else:
                break

    def pass_cards(self, passing_to):
        """
        A method that prints the current hand before asking the user which cards they wish to pass.

        Arguments:
        - self (to access variables that belong to that class)
        - passing_to (method from Hearts that returns the player to which the cards are passed to)

        Returns 3 cards of the player's choice to be passed.
        """

        # initialising variables
        passlist = []
        passingcard = []

        # prints the hand
        print("Your current hand: ", "\n" + self.printcard(self.hand))

        # a while loop that will keep running until 3 valid cards are passed
        while True:
            try:

                # card to pass seperated by comma to allow splitting with comma
                card_to_pass = input(
                    f"Please enter the index of the card to pass to {passing_to} (Separated by comma): ")
                index = card_to_pass.split(",")
                index_list = []

                # if 3 cards are not entered, raise error
                if (len(index)) != 3:
                    raise ValueError

                # checks if there are duplicates in the list
                if (len(set(index)) != len(index)):
                    raise ValueError

                # append card_to_pass to index_list
                for i in index:
                    index_list.append(int(i))

                # if index of cards to be passed is not in hand, raise error
                for i in index_list:
                    if i not in range(len(self.hand)):
                        passingcard = []
                        raise ValueError
                    passingcard.append(self.hand[i])

                # removes cards from hand
                for passs in range(len(passingcard)):
                    if passingcard[passs] in self.hand:
                        self.hand.remove(passingcard[passs])
                return (passingcard)

            # if error is raised then will restart the loop
            except ValueError:
                continue

            # break loop if 3 valid card are passed.
            else:
                break


