from __future__ import annotations  # for type hints of a class in itself
from enum import Enum



class Rank(Enum):
    """ Rank class for representing the range of ranks within a suit. """
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

    def __init__(self, Rank):
        self.Rank = Rank

    def __lt__(self, other: Rank) -> bool:
        """ Compares rank on hand with other ranks, and returns a boolean if rank on hand is less than other rank """

        return self.Rank < other.Rank



class Suit(Enum):
    """ Suit class for representing range of suits within a deck of cards. """

    Clubs = 1
    Diamonds = 2
    Spades = 3
    Hearts = 4

    def __init__(self, Suit):
        self.Suit = Suit

    def __lt__(self, other: Suit) -> bool:
        """ Compares card suit with other card suit, and returns a boolean if suit of card is less than other suit """

        return self.Suit < other.Suit



class Card:
    """ Card class for representing an object represents a combination of Rank and Suit. """

    pretty_print = True

    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        """ to be able to print __str__ """

        return self.__str__()

    def __str__(self) -> str:
        """ to return the card art such as Two of Diamonds etc """

        if self.pretty_print == True:

            # turn the symbol of the cards into their own symbols respectively
            if self.suit == Suit.Clubs:
                symbol = '♣'
            elif self.suit == Suit.Spades:
                symbol = '♠'
            elif self.suit == Suit.Hearts:
                symbol = '♥'
            elif self.suit == Suit.Diamonds:
                symbol = '♦'

            # dictionary to store the values of each rank with their formatted symbol
            card_art = {
                Rank.Two: ["┌─────┐", "│2    │", "│  {}  │".format(symbol), "│    2│", "└─────┘"],
                Rank.Three: ["┌─────┐", "│3    │", "│  {}  │".format(symbol), "│    3│", "└─────┘"],
                Rank.Four: ["┌─────┐", "│4    │", "│  {}  │".format(symbol), "│    4│", "└─────┘"],
                Rank.Five: ["┌─────┐", "│5    │", "│  {}  │".format(symbol), "│    5│", "└─────┘"],
                Rank.Six: ["┌─────┐", "│6    │", "│  {}  │".format(symbol), "│    6│", "└─────┘"],
                Rank.Seven: ["┌─────┐", "│7    │", "│  {}  │".format(symbol), "│    7│", "└─────┘"],
                Rank.Eight: ["┌─────┐", "│8    │", "│  {}  │".format(symbol), "│    8│", "└─────┘"],
                Rank.Nine: ["┌─────┐", "│9    │", "│  {}  │".format(symbol), "│    9│", "└─────┘"],
                Rank.Ten: ["┌─────┐", "│10   │", "│  {}  │".format(symbol), "│   10│", "└─────┘"],
                Rank.Jack: ["┌─────┐", "│J    │", "│  {}  │".format(symbol), "│    J│", "└─────┘"],
                Rank.Queen: ["┌─────┐", "│Q    │", "│  {}  │".format(symbol), "│    Q│", "└─────┘"],
                Rank.King: ["┌─────┐", "│K    │", "│  {}  │".format(symbol), "│    K│", "└─────┘"],
                Rank.Ace: ["┌─────┐", "│A    │", "│  {}  │".format(symbol), "│    A│", "└─────┘"],
            }

            # prints out the card art based on the card rank
            card_art_str = "\n"
            for k in range(5):
                card_art_str += card_art[self.rank][k] + "\n"

            # to format the symbol with the suit of the card
            output = card_art_str.format(symbol)
            return(output)

        else:
            return f'{self.rank.name} of {self.suit.name}'

    def __eq__(self, other: Card) -> bool:
        """ compares rank and suit to determine if a card is equal to each other, and returns booleans """

        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other: Card) -> bool:
        """ compares suit first then rank to determine if a card is less than the other and returns booleans """

        return (self.rank < other.rank or (self.rank == other.rank and self.suit < other.suit))