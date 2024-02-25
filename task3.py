from __future__ import annotations
from cards import Card, Rank, Suit


class Round:
    """ Class Round that takes a list of players and executes a round of the game."""

    trick = []
    startlist = []
    broken_hearts = False
    playing = True
    Card.pretty_print = False

    def __init__(self, players: list[Player]) -> None:
        self.players = players

        # while playing is True, this loop will keep running
        while self.playing == True:
            self.startplayer(players)
            self.playcard()
            self.winnercard()
            self.checkifendgame()

    def startplayer(self, players):
        """
        A method that starts the game by arranging the player list to play accordingly to who has the Two of Clubs.

        Arguments:
        - self (to access variables that belong to that class)
        - players (list of players)

        Returns updated player list.
        """

        self.players = players

        # checks for Two of Clubs in each player's hand, and will rearrange the list by slicing.
        for player in range(len(players)):
            if Card(Rank.Two, Suit.Clubs) in players[player].hand:
                self.startlist = self.players[player:]
                self.startlist += self.players[:player]

        # assign self.players to a copy of self.startlist
        self.players = self.startlist[:]

        return self.players

    def playcard(self):
        """
        A method to play the cards.

        Arguments:
        - self (to access variables that belong to that class)

        Does not return anything, but executes actions for AI.
        """
        self.trick = []

        # for each player, they'll play a card, and the card is appended to the trick.
        for player in range(len(self.players)):
            played_card = self.players[player].play_card(self.trick, self.broken_hearts)
            print(self.players[player], "plays", played_card)
            self.trick.append(played_card)

            # if the player played a card of heart suit, it'll change broken_hearts to True and notifies the players.
            if played_card.suit == played_card.suit.Hearts and self.broken_hearts == False:
                self.broken_hearts = True
                print("Hearts have been broken!")
                if played_card in self.players[player].hand:
                    self.players[player].hand.remove(played_card)

    def winnercard(self):
        """
        A method to determine who is the receiver for each trick, and count the penalty received.
        Also modifies the player list to start with the receiver.

        Arguments:
        - self (to access variables that belong to that class)

        Returns updated player list.
        """

        winnerindex = 0
        max_card = self.trick[0]
        penalty = 0
        taker = self.players[winnerindex]
        counter = 0
        index = 0

        # a loop that determines the taker
        for card in range(len(self.trick)):

            # for the 2nd card onwards, if it's not the same suit as the trick, it means the first player is the taker
            if self.trick[card].suit != self.trick[0].suit:
                counter += 1

                # if counter equals to length of players excluding the first player, then the taker will be the first player
                if counter == len(self.players) - 1:
                    taker = self.players[0]
                    index = 0

            # if a card is larger than the current max card, winner index will be from the current card
            # max card will be the current card, and the taker will be from the winner index.
            elif self.trick[card] > max_card:
                winnerindex = card
                max_card = self.trick[card]
                taker = self.players[winnerindex]
                index = winnerindex

        # checks for hearts and Queen of Spades in the trick to penalise accordingly
        for card in self.trick:
            if card.suit == Suit.Hearts:
                penalty += 1
            elif card.suit == Suit.Spades and card.rank == Rank.Queen:
                penalty += 13

        # if penalty is more than 1, the player's total score will be updated accordingly
        if penalty > 0:
            self.players[index].total_score += penalty

        print(f"{taker} takes the trick. Points received: {penalty}")

        # rearranges the player list according to the taker
        self.startlist = self.players[winnerindex:]
        self.startlist += self.players[:winnerindex]

        # assigning a copy of the start list to the player list
        self.players = self.startlist[:]

        return self.players

    def checkifendgame(self):
        """
        A method to check if the game has ended.

        Arguments:
        - self (to access variables that belong to that class)

        Does not return anything but will stop the loop in the constructor if each player has played all their cards.
        """

        counter = 0

        # a loop to check if each player has played all their cards.
        for player in self.players:
            if len(player.hand) == 0:
                counter += 1

        # if all player is done, end the loop in the constructor and calls for roundstats().
        if counter == len(self.players):
            self.playing = False


