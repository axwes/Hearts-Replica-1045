from __future__ import annotations
from random import shuffle
import random
from cards import Card, Rank, Suit
from basic_ai import BasicAIPlayer
from round import Round
from human import HumanPlayer
from better_ai import BetterAIPlayer
from player import Player


class Hearts:
    '''
    Class heart which run the game until one of the
    player reaches the target score. Prompt user for input
    for number of players between 3-5.
    '''

    players = []
    decksize = 0
    Round = 1
    highestscore = 0
    draw = 0
    topass = 0

    def __init__(self) -> None:
        targetscore = 0
        numofplayers = 0
        self.hand = []
        self.deck = []
        self.playing = True

        while True:  # loop will repeat until user enter a valid targetscore which is an integer larger than 0
            try:
                targetscore = int(input("Please enter a target score to end the game: "))
                if targetscore == 0:
                    raise ValueError
            except ValueError:
                continue
            else:
                break

        while numofplayers not in range(3,6):  # loop will repeat until user enter an int in range of 3, 6 not included
            try:
                numofplayers = int(input("Please enter the number of players (3-5): "))
                if numofplayers not in range(3, 6):
                    raise ValueError
            except ValueError:
                continue
            else:
                break

        print("Welcome to ♥ HEARTS ♥")
        Player.start = "  "
        print(Player.start)
        self.round_start(numofplayers)

        # if highest player score is less than or equal to target score (100)
        # or if the game is a draw, this loop will not end
        # this loop executes a round.
        while self.highestscore <= targetscore or self.draw > 1:
            print(f"========= Starting round {self.Round} =========")
            numofplayers = len(self.players)
            self.shufflecard(numofplayers)
            self.dealcard(numofplayers)
            self.checker(numofplayers)
            self.gettopass()
            self.choosing(targetscore)
            self.passnow()
            self.startgame(targetscore)
            self.endgame(targetscore)

    def round_start(self, numofplayers):
        '''
        A method to set player name, get player name, and set the AI as bot players.

        Arguments:
        - self (to access variables that belong to that class)
        - numofplayers (an integer inputted by users)

        Returns updated list of players.
        '''

        player1 = HumanPlayer()  # setting and getting player name
        player1.set_name()
        player1.get_name()
        self.players = [player1]

        player2 = BetterAIPlayer("Player 2")
        player3 = BasicAIPlayer("Player 3")

        self.players = [player1, player2, player3]

        if numofplayers == 3: #if numofplayers is 3, return self.players list
            return self.players

        while True:  # loop will repeat until user enter a valid typeofplayer
            try:
                if numofplayers == 4: #if num of players is 4 then ask user for type of player for player 4
                    for player in range(4, numofplayers + 1):
                        print("Type of player:\n1. BasicAiPlayer\n2. BetterAiPlayer")
                        typeofplayer = int(input(f"Please enter type of player {player}: "))
                        if typeofplayer == 1:
                            self.players.append(BasicAIPlayer("Player " + str(player)))
                        elif typeofplayer == 2:
                            self.players.append(BetterAIPlayer("Player " + str(player)))
                        else:
                            raise ValueError

                if numofplayers == 5: #if num of players is 5 then ask user for type of player for player 4 and player 5
                    for player in range(4, numofplayers + 1):
                        print("Type of player:\n1. BasicAiPlayer\n2. BetterAiPlayer")
                        typeofplayer = int(input(f"Please enter type of player{player}: "))
                        if typeofplayer == 1:
                            self.players.append(BasicAIPlayer("Player " + str(player)))
                        elif typeofplayer == 2:
                            self.players.append(BetterAIPlayer("Player " + str(player)))
                        else:
                            raise ValueError
            except ValueError:
                continue
            else:
                break

        return self.players

    def shufflecard(self, numofplayers):
        '''
        A method to shuffle all the card.

        Arguements:
        - self (to access variables that belong to that class)
        - numofplayers (an integer inputted by users)

        Does not return anything.
        '''

        self.deck = []  # creates an empty list
        for rank in Rank:
            for suit in Suit:
                card = Card(rank, suit)
                self.deck.append(card)  # append every card to self.deck
        if numofplayers == 3:
            self.deck.remove(Card(rank.Two, suit.Diamonds))  # remove Two of Diamonds if numofplayers is 3
        elif numofplayers == 5:
            self.deck.remove(
                Card(rank.Two, suit.Diamonds))  # remove Two of Diamonds and Two of Spades if numofplayers is 5
            self.deck.remove(Card(rank.Two, suit.Spades))
        random.shuffle(self.deck)  # shuffle the deck

    def dealcard(self, numofplayers):
        '''
        A method to deal shuffled card to every players equally.

        Arguements:
        - self (to access variables that belong to that class)
        - numofplayers (an integer inputted by users)
        '''

        handart = []
        dealt_list = []  # create an empty list
        self.divide_by = int(len(self.deck) / numofplayers)  # find the number of cards each dealt hand needs to have

        for i in range(0, len(self.deck), self.divide_by):
            dealt_list.append(self.deck[
                              i:i + self.divide_by])  # the initial deck is equally divided to chunks and each chunk is appended to dealt_list
        for i in range(len(self.players)):
            self.players[i].hand = dealt_list[i]  # a chunk is assigned to each player as their hand
            self.players[i].hand.sort(key=lambda x: (x.suit, x.rank))  # sorting by suit and rank in ascending order

    def checker(self, numofplayers):
        '''
        Check if every player has at least one card that isnt from
        the Queen of Spades or from Hearts.

        Arguments:
        - self (to access variables that belong to that class)
        - numofplayers (an integer inputted by users)

        Returns list of players.
        '''

        for player in range(len(self.players)):
            for hands in self.players[player].hand:
                if hands.suit == Suit.Hearts:
                    self.players[player].counter += 1
                if hands.rank == Rank.Queen and hands.suit == Suit.Spades:
                    self.players[player].counter += 1
                # if player hand contains card from Hearts or Queen of Spades, counter will += 1

        for player in self.players:
            while player.counter == self.decksize:
                self.shufflecard(numofplayers)
                self.dealcard(numofplayers)
        # if player hand contains all hearts or Queen of Spades, it will shuffle the card and deal again

        return self.players

    def choosing(self, targetscore):
        '''
        A method to pass away 3 cards

        Arguments:
        - self (to access variables that belong to that class)
        - targetscore (an integer inputted by users)

        '''

        # if numofplayer is 3 and Round is multiple of 3 then do not pass any Card
        # the same concep goes for numofplayer is 5 and Round is multiple of 5
        # otherwise, players have to pass cards
        for player in range(len(self.players)):

            if len(self.players) == 3 and self.Round % 3 == 0:
                pass
            elif len(self.players) == 5 and self.Round % 5 == 0:
                pass
            elif player == 0:
                self.players[0].passing = self.players[0].pass_cards(self.players[self.topass])
            elif player != 0:
                self.players[player].passing = self.players[player].pass_cards()

    def gettopass(self):
        """
        A method to allow the player to pass card to the correct
        player every round. E.G Round 1 passes to the left. Round 2 passes to the front
        and Round 3 passes to the right.

        Arguments:
        - self (to access variables that belong to that class)

        Returns index in which direction to pass the cards.
        """

        passindex = [1, 2, -1]  # left, infront, right
        if self.Round > len(passindex):
            tempround = self.Round % len(passindex)
            passto = passindex[tempround - 1]
        else:
            passto = passindex[self.Round - 1]
        # get the passto index for players to pass to the appropriate corresponding player

        for player in range(len(self.players)):

            if len(self.players) == 3 and self.Round % 3 == 0:
                pass
            elif len(self.players) == 5 and self.Round % 5 == 0:
                pass
            # if self.players == 3 and round is multiple of 3, player will not pass its card
            # same goes for self.players == 5 and round is multiple of 5

            else:
                self.topass = player + passto  # get the index for the player that need to be passed to

                if self.topass >= len(self.players):
                    self.topass = self.topass % len(self.players)
                    return (self.players[self.topass])
                else:
                    return (self.players[self.topass])

                # other than those condition, player will return the appropriate player that they need to

    def passnow(self):
        '''
        A method to pass the chosen 3 cards to the appropriate
        corresponding player.

        Arguments:
        - self (to access variables that belong to that class)
        '''

        passindex = [1, 2, -1]  # left, infront, right
        if self.Round > len(passindex):
            tempround = self.Round % len(passindex)
            passto = passindex[tempround - 1]
        else:
            passto = passindex[self.Round - 1]
        # get the passto index for players to pass to the appropriate corresponding player

        for player in range(len(self.players)):

            if len(self.players) == 3 and self.Round % 3 == 0:
                pass

            elif len(self.players) == 5 and self.Round % 5 == 0:
                pass
            # if self.players == 3 and round is multiple of 3, player will not pass its card
            # same goes for self.players == 5 and round is multiple of 5

            else:
                passer = player + passto  # get the index for the player that need to be passed to

                if passer >= len(self.players):
                    passer = passer % len(self.players)
                    self.players[passer].hand += self.players[player].passing
                else:
                    self.players[passer].hand += self.players[player].passing

                # other than those condition, player will pass the card they've chosen to the
                # appropriate corresponding player using the topass index

    def startgame(self, targetscore):
        '''
        A method to start the round, get player total score and
        check if they have shot the moon a score of 26 and check for the highestscore
        to compare with targetscore

        Arguments:
        - self (to access variables that belong to that class)
        - targetscore (an integer inputted by users) E.G Bob input target score of 100
          game will ends at 100.
        '''
        counter = 0
        shotthemoon = 0
        Round(self.players)
        print(f"========= End of round {self.Round} =========")
        for player in range(len(self.players)):
            self.players[player].total_score += self.players[player].round_score
            print(f"{self.players[player]}'s total score: {self.players[player].total_score}")
            self.players[player].round_score = 0

            if self.players[player].round_score == 26:
                print(f"{self.players[player]} has shot the moon! Everyone else receives 26 points")
                self.players[player].round_score = 0
                shotthemoon = player
                if self.players[player] != self.players[shotthemoon]:
                    self.players[player].round_score += 26

            if self.players[player].total_score > self.highestscore:
                self.highestscore = self.players[player].total_score

        self.Round += 1

    def endgame(self, targetscore):
        '''
        A method to check which player is the winner and to check
        if there is a draw.

        Arguments:
        - self (to access variables that belong to that class)
        - targetscore (an integer inputted by users)
        '''
        counter = 0
        lowestscore = self.players[0].total_score
        winner = self.players[0]

        # if highestscore is bigger or equal to targetscore then it will iterate through
        # player list  to check for the player with lowest score to be declared as the winner
        if self.highestscore >= targetscore:
            for player in range(len(self.players)):
                if self.players[player].total_score < lowestscore:
                    lowestscore = self.players[player].total_score
                    winner = self.players[player]

        for player in range(len(self.players)):
            if self.players[player].total_score == lowestscore:  # if there's more than one player who have the lowestscore, then there is a draw
                counter += 1  # assigned to counter
        for player in range(len(self.players)): #if player score is the lowestscore and game has ended and there is no draw
            if self.players[player].total_score == lowestscore and self.highestscore >= targetscore and counter == 1:

                print(f"{winner} is the winner!")

        self.draw = counter







if __name__ == "__main__":
    Hearts()