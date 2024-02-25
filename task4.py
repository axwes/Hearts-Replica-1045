from __future__ import annotations
from random import shuffle
import random
from cards import Card, Rank, Suit
from basic_ai import BasicAIPlayer
from round import Round


class Hearts:
    '''
	Class heart which run the game until one of the
	player reaches the target score. Prompt user for input
	for number of players between 3-5.
	'''
    players = []
    Round = 1
    highestscore = 0
    draw = 0
    Card.pretty_print = False

    def __init__(self) -> None:
        targetscore = 0
        numofplayers = 0
        self.deck = []

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

        self.round_start(numofplayers)  # call for function roundstart to append player to players list

        while self.highestscore <= targetscore or self.draw >= 2:  # loop will continue until highestscore is bigger or equal to targetscore OR if there's a draw
            print(f"========= Starting round {self.Round} =========")
            self.shufflecard(numofplayers)
            self.dealcard(numofplayers)
            self.checker(numofplayers)
            self.cardpasser()
            self.passnow()
            self.startgame(targetscore)
            self.endgame(targetscore)

    def round_start(self, numofplayers):
        '''
		A method to append player to players list according to the numofplayer
		user inputted.

		Arguments:
		- self (to access variables that belong to that class)
		- numofplayers (an integer inputted by users)
		'''

        for player in range(1, numofplayers + 1):
            self.players.append(BasicAIPlayer("Player " + str(player)))

    # append each player according to the numofplayers inputted by the user

    def shufflecard(self, numofplayers):
        '''
		A method to shuffle all the card.

		Arguements:
		- self (to access variables that belong to that class)
		- numofplayers (an integer inputted by users)
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

        dealt_list = []  # creates an aempty list
        self.divide_by = int(len(self.deck) / numofplayers)  # find the number of cards each dealt hand need to have

        for i in range(0, len(self.deck), self.divide_by):
            dealt_list.append(self.deck[
                              i:i + self.divide_by])  # the initial deck is equally divided to chunks and each chunk is appended to dealt_list
        for i in range(len(self.players)):
            self.players[i].hand = dealt_list[i]  # a chunk is assigned to each player as their hand
        for player in self.players:
            print(f"{player} was dealt {player.hand}")  # prints the output of the above

    def checker(self, numofplayers):
        '''
		Check if every player has at least one card that isnt from
		the Queen of Spades or from Hearts.

		Arguements:
		- self (to access variables that belong to that class)
		- numofplayers (an integer inputted by users)

		'''

        for player in range(len(self.players)):
            for hands in self.players[player].hand:
                if hands.suit == Suit.Hearts:  # Check if player hand contain hearts
                    self.players[player].counter += 1  # Add one to player counter
                if hands.rank == Rank.Queen and hands.suit == Suit.Spades:  # Check if player hand contain Queen of Spades
                    self.players[player].counter += 1  # Add one to player counter

        for player in self.players:
            if player.counter == self.divide_by:  # if player is same as total number of card in each dealt hand
                self.shufflecard(numofplayers)  # shuffle and deal card again
                self.dealcard(numofplayers)

    def cardpasser(self):
        '''
		A method to get 3 cards that player has chosen to pass.

		Arguements:
		- self (to access variables that belong to that class)
		'''

        for player in range(len(self.players)):

            if len(self.players) == 3 and self.Round % 3 == 0:
                pass
            elif len(self.players) == 5 and self.Round % 5 == 0:
                pass
            else:
                self.players[player].passing = self.players[player].pass_cards()

    # if players = 3 and round is multiple of 3, player will not pass any card
    # the same goes to if players = 4 and round is multiple of 5
    # other than those condition, player will choose 3 largest card from their hand to pass

    def passnow(self):
        '''
		A method to pass the chosen 3 cards to the appropriate
		corresponding player.

		Arguements:
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
                topass = player + passto  # get the index for the player that need to be passed to

                if topass >= len(self.players):
                    topass = topass % len(self.players)
                    self.players[topass].hand += self.players[player].passing
                else:
                    self.players[topass].hand += self.players[player].passing
                # other than those condition, player will pass the card they've chosen to the
                # appropriate corresponding player using the topass index

                print(f"{self.players[player]} passed {self.players[player].passing} to {self.players[topass]}")

    def startgame(self, targetscore):
        '''
		A method to start the round, get player total score and
		check if they have shot the moon and check for the highestscore
		to compare with targetscore

		Arguements:
		- self (to access variables that belong to that class)
		- targetscore (an integer inputted by users)
		'''
        counter = 0
        shotthemoon = 0
        Round(self.players)
        print(f"========= End of round {self.Round} =========")
        for player in range(len(self.players)):
            self.players[player].total_score += self.players[player].round_score
            print(f"{self.players[player]}'s total score: {self.players[player].total_score}")
            self.players[player].round_score = 0
            # tally each player total score and print it out

            if self.players[player].round_score == 26:
                print(f"{self.players[player]} has shot the moon! Everyone else receives 26 points")
                self.players[player].round_score = 0
                shotthemoon = player
                if self.players[player] != self.players[shotthemoon]:
                    self.players[player].round_score += 26
            # check if player shot the moon and print out if it does, assign player to have 0 points
            # and add 26 points to other players

            if self.players[player].total_score > self.highestscore:
                self.highestscore = self.players[player].total_score

        # iterate through player list to find the highest score among all players

        self.Round += 1

    # add 1 round

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
            if self.players[
                player].total_score == lowestscore:  # if there's more than one player who have the lowestscore, then there is a draw
                counter += 1  # assigned to counter
        for player in range(
                len(self.players)):  # if player score is the lowestscore and game has ended and there is no draw
            if self.players[player].total_score == lowestscore and self.highestscore >= targetscore and counter == 1:
                print(f"{winner} is the winner!")

        self.draw = counter


if __name__ == "__main__":
    Hearts()