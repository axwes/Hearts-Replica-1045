from __future__ import annotations
from cards import Card, Rank, Suit


class Player:
    """ Class BasicAIPlayer for tracking attributes such as a player's hand of cards and deciding what card to play on a given trick."""

    counter = 0
    passing = []

    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.round_score = 0
        self.total_score = 0
        self.start = ""


    def __str__(self) -> str:
        """ to return card name """
        return f'{self.name}'

    def __repr__(self) -> str:
        """ to be able to print __str__ """
        return self.__str__()

    def check_valid_play(self, card: Card, trick: list[Card], broken_hearts: bool) -> (bool, str):
        """
        A method to check if a play is valid.

        Arguments:
        - self (to access variables that belong to that class)
        - trick (to check current trick)
        - broken_hearts (to check if hearts has been broken)

        Returns boolean True if it's a valid play, else False.
        """

        # initialises the argumments
        self.card = card
        self.trick = trick
        self.broken_hearts = broken_hearts

        # counter for checking if suit of card is different from suit of trick
        counter = 0

        for cards in range(len(self.hand)):

            # if the trick is empty, and if a card in the range of the player's hand is Two of Clubs, it'll return True, else False
            if len(self.trick) == 0:
                if self.hand[cards].suit == Suit.Clubs and self.hand[cards].rank == Rank.Two:
                    if self.card.rank == Rank.Two and self.card.suit == Suit.Clubs:
                        return (True,"")
                    return (False,"")
                if self.hand[cards].suit == Suit.Hearts and self.broken_hearts == False:
                    counter += 1

                # if suit of card is Hearts and hearts has not been broken, then it'll return False (can't be played), else True.
                elif self.broken_hearts == False and self.card.suit == Suit.Hearts:
                    return (False, 'Hearts has not been broken. Please play another card.')
                else:
                    return (True,"")

            # if the trick is not empty, and if the suit of the card played is not same as the first card of the trick, if card played is of same suit, then it'll move on
            # it'll check if for cards of same suit as trick in all cards in hand
            # if the card is of different suit from trick, counter will increase by 1.
            elif len(trick) > 0:
                if card.suit != self.trick[0].suit:
                    if self.hand[cards].suit != self.trick[0].suit:
                        counter += 1

                else:
                    return (True,"")

        # if counter is same as the number of cards in hand, means it's a valid play, else false.
        if counter == len(self.hand):
            return (True,"")
        else:
            return (False, 'Player still has cards from the suit of the current trick')


