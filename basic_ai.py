from __future__ import annotations
from cards import Card, Rank, Suit
from player import Player
import time

class BasicAIPlayer(Player):
	""" Class BasicAIPlayer for tracking attributes such as a player's hand of cards and deciding what card to play on a given trick."""
	counter = 0
	passing = []

	def play_card(self, trick, broken_hearts):
		"""
		A method to return the lowest ranking card from the player's hand that constitutes a valid play, removing it from self.hand before returning.

		Arguments:
		- self (to access variables that belong to that class)
		- trick (to check current trick)
		- broken_hearts (to check if hearts has been broken)

		Returns the lowest ranking car.
		"""

		# initialises the arguments
		self.trick = trick
		self.broken_hearts = broken_hearts
		self.hand.sort()
		Player.start = "time.sleep"
		if Player.start == "  ":
			time.sleep(5)
		# checks if Two of Clubs is in hand, if it is, remove the card from hand and returns it
		for cards in range(len(self.hand)):
			if Card(Rank.Two, Suit.Clubs) in self.hand:
				self.card = Card(Rank.Two, Suit.Clubs)
				self.hand.remove(self.card)
				return self.card

			# if card played is a valid play, then will remove the card from hand and return it
			if self.check_valid_play(self.hand[cards], self.trick, self.broken_hearts)[0] == True:
				self.card = self.hand[cards]
				self.hand.remove(self.card)
				return self.card

		return self.hand[0]

	def pass_cards(self):
		"""
		A method to return a list of three cards from hte player's hands to pass off, and removing them from self.hand before returning.

		Arguments:
		- self (to access variables that belong to that class)

		Returns 3 cards to be passed.
		"""

		# sorts the cards in hand by suit first, then rank, in decending order, then adding the 3 highest ranking cards to a variable
		self.hand.sort(key=lambda x: (x.suit, x.rank), reverse=True)
		passing_card = [self.hand[0], self.hand[1], self.hand[2]]

		# if passed card in hand, removes it from hand
		for passs in range(len(passing_card)):
			if passing_card[passs] in self.hand:
				self.hand.remove(passing_card[passs])
		return passing_card


