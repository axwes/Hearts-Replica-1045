from __future__ import annotations
from cards import Card, Rank, Suit
from basic_ai import BasicAIPlayer
from player import Player
import time


class BetterAIPlayer(Player):
    '''
    BetterAIPlayer that inherits the base player and functions the same as the basic AI player however it implement a more advanced strategy of play
    '''

    def play_card(self, trick, broken_hearts):
        '''
        A method to play a more strategic card

        Arguments:
        - self (to access variables that belong to that class)
        - trick (to check current trick)
        - broken_hearts (to check if hearts has been broken)

        return the most strategic card to play
        '''

        # initialises the arguments
        self.trick = trick
        self.broken_hearts = broken_hearts

        Player.start = "time.sleep"
        if Player.start == "  ":
            time.sleep(2)

        # if player is not leading the trick and broken heart is false then player should return the highest card in their hand
        if len(self.trick) != 0:
            for cards in range(len(self.hand)):
                for tricks in trick:
                    if self.broken_hearts == False:
                        self.hand.sort(key=lambda x: (x.rank), reverse=True)
                        if self.check_valid_play(self.hand[cards], self.trick, self.broken_hearts)[0] == True:
                            self.card = self.hand[cards]
                            self.hand.remove(self.card)
                            return self.card

                    # if player is not leading the trick check if broken hearts is true and Queen of spade not in trick
                    # then check if anyone played Hearts, if no one played Heart yet then player will return the highest card in their hand
                    if len(self.trick) > 2:
                        if broken_hearts == True and Card(Rank.Queen, Suit.Spades) not in self.trick:
                            if tricks.suit != Suit.Hearts:
                                self.hand.sort(key=lambda x: (x.rank), reverse=True)
                                if self.check_valid_play(self.hand[cards], self.trick, self.broken_hearts)[0] == True:
                                    self.card = self.hand[cards]
                                    self.hand.remove(self.card)
                                    return self.card

                        if self.hand[cards] == Card(Rank.Queen, Suit.Spades):
                            if tricks > Card(Rank.Queen, Suit.Spades):
                                if self.check_valid_play(self.hand[cards], self.trick, self.broken_hearts)[0] == True:
                                    self.card = self.hand[cards]
                                    self.hand.remove(self.card)
                                    return self.card

            # if all the condition doesnt meet, then just return the lowest card
            for cards in range(len(self.hand)):
                self.hand.sort(key=lambda x: (x.suit, x.rank), reverse=False)
                if self.check_valid_play(self.hand[cards], self.trick, self.broken_hearts)[0] != False:
                    self.card = self.hand[cards]
                    self.hand.remove(self.card)
                    return self.card


        else:
            for cards in range(len(self.hand)):
                #if Two of Clubs in hand, return the card
                if Card(Rank.Two, Suit.Clubs) in self.hand:
                    self.card = Card(Rank.Two, Suit.Clubs)
                    self.hand.remove(self.card)
                    return self.card
            # if player is leading the trick, if broken hearts is false, player will return the highest card in their hand
                if self.broken_hearts == False:
                    self.hand.sort(key=lambda x: (x.rank), reverse=True)
                    if self.check_valid_play(self.hand[cards], self.trick, self.broken_hearts)[0] == True:
                        self.card = self.hand[cards]
                        self.hand.remove(self.card)
                        return self.card
                # if not leading the trick, if broken hearts is True, player will return the lowest card in their hand
                elif self.broken_hearts == True:
                    self.hand.sort(key=lambda x: (x.suit, x.rank), reverse=False)
                    if self.check_valid_play(self.hand[cards], self.trick, self.broken_hearts)[0] == True:
                        self.card = self.hand[cards]
                        self.hand.remove(self.card)
                        return self.card

    def pass_cards(self) -> list[Card]:
        '''
         A method to return a list of three cards from the player's hands to pass off, and removing them from self.hand before returning.

         Arguements:
         - self (to access variables that belong to that class)

         Returns 3 cards to be passed.

        '''

        # initalise the variable
        passing_card = []
        dontremove = []
        self.hand.sort(key=lambda x: (x.rank), reverse=True)  # sort hand to highest rank

        # if Ace of Clubs, Spades with Rank higher than Seven, Hearts with rank higher than seven in self.hand, then append those cards to dontremove
        for cards in range(len(self.hand)):
            if self.hand[cards] == Card(Rank.Ace, Suit.Clubs):
                dontremove.append(self.hand[cards])
            if self.hand[cards].suit == Suit.Spades and self.hand[cards].rank < Rank.Seven:
                dontremove.append(self.hand[cards])
            if self.hand[cards].suit == Suit.Hearts and self.hand[cards].rank < Rank.Seven:
                dontremove.append(self.hand[cards])
        # remove all the cards in dontremove from self.hand
        for remove in dontremove:
            if remove in self.hand:
                self.hand.remove(remove)
        # add back all the cards in dontremove to self.hand so it's store from the last elements in the list
        self.hand += dontremove

        for cards in range(len(self.hand)):
            # if havent choose 3 cards to pass, check if Two of Clubs in hand, if it is then append it to passing card and add 2 more highest rank card to pass away
            if len(passing_card) != 3:
                if self.hand[cards] == Card(Rank.Two, Suit.Clubs):
                    passing_card.append(self.hand[cards])
                    self.hand.remove(self.hand[cards])
                    while len(passing_card) != 3:
                        passing_card.append(self.hand[0])
                        self.hand.remove(self.hand[0])
                # if havent choose 3 cards to pass, choose 3 highest rank card to pass away
                else:
                    passing_card = [self.hand[0], self.hand[1], self.hand[2]]

        # check if cards in passing card is still in self.hand then remove it if it is
        for passs in range(len(passing_card)):
            if passing_card[passs] in self.hand:
                self.hand.remove(passing_card[passs])

        return passing_card


