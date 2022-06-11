# import java.awt.*;

#
# Created by Robert on 5/13/2014.
#

from card import Card
from cardpile import CardPile


# There is a bug that sometimes it will not move cards to the right
# Exclude checking its own column

# Enhancement: Let the deckpile repeat

class TablePile(CardPile):
    def __init__(self, x, y, c, main, canvas):
        super().__init__(x, y, canvas)
        self.c = c
        self.canvas = canvas
        self.main = main
        print("In TablePile, c is: ", c)
        for i in range(c):  # this needs to be c after testing
            temp_card = self.main.deckPile.pop()  # type needs to be Card
            self.add_card(temp_card)

        # flip topmost card face up
        self.top().flip()

    def includes(self, tx, ty):
        # don't test bottom of card
        return self.x <= tx <= (self.x + Card.width) and self.y <= ty

    def can_take(self, a_card):
        # print("In tablepile can take: ", a_card.rank() + 1, a_card.suit())
        if len(self.thePile) == 0:
            return a_card.rank() == 12

        top_card = self.top()

        return (a_card.color() != top_card.color()) and (a_card.rank() == top_card.rank() - 1)

    # break up into smaller funcs
    def get_pile_stats(self):
        print("\nIn TablePile get_pile_stats -")
        num_cards = len(self.thePile)
        print("The number of cards in this pile is: ", num_cards)
        tmp_cards = []
        bmfc = None
        num_fu = 0
        num_fd = 0
        for card in self.thePile:
            # build tmp_cards which are the faceup cards in the pile,
            # starting with the bottom most faceup card and remaining
            # face up cards.  All the cards above the bmfc will be faceup.
            # All the cards below the bmfc will be face down.
            print("Checking card: ", card.rank() + 1, card.suit())
            if card.faceUp():
                if num_fu == 0:
                    bmfc = card
                    print(bmfc.rank() + 1, bmfc.suit(), "card is bottom most faceup card")
                tmp_cards.append(card)
                # self.pop()
                print(card.rank() + 1, card.suit(), "card is face up")

                print("len of tmp_cards is: ", len(tmp_cards))
                num_fu += 1
            else:
                print(card.rank() + 1, card.suit(), "card is face down")
                num_fd += 1

        print("The number of faceup cards in the pile is: ", num_fu)
        print("The number of facedown cards in the pile is: ", num_fd)
        for c in range(num_fd, num_cards):
            card_popped = self.pop()
            print("card popped is: ", card_popped.rank() + 1, card_popped.suit())

        return num_cards, num_fu, num_fd, bmfc, tmp_cards

    # break up into smaller funcs
    def select(self):
        # if column empty ...
        if self.is_empty():
            print("This pile is empty")
            return

        # make sure top card is faceup in a non-empty colunmn...
        top_card = self.top()
        if not top_card.faceUp():
            top_card.flip()
            return

        # See if any suit pile can take top card
        top_card = self.pop()
        for sp in self.main.suitPile:
            if sp.can_take(top_card):
                sp.add_card(top_card)
                return

        # if suit pile cannot take top card, return top card to pile
        self.add_card(top_card)
        # still a minor bug here
        # get the numner of cards in the pile, number faceup, number facedown,
        # the bottom most faceup card, and the temp pile of cards to possibly move...
        num_cards, num_fu, num_fd, bmfc, tmp_cards = self.get_pile_stats()
        # What column am I in?  Exclude that column from check.
        for i, tb in enumerate(self.main.tableau):
            # check to see if tb can take bmfc
            # loop through the (other) tableau files,
            # and see if the bmfc can be moved to that pile.
            # If som move to the first one it finds.
            # Don't check the current pile to see if it can
            # be moved to itself.
            if self.c != i+1:
                if tb.can_take(tmp_cards[0]):
                    print("Column: ", i, "can take bmfc")
                    print("Moving tmp_cards to new column.")
                    for card in tmp_cards:
                        tb.add_card(card)
                    return

        # else put it back on our pile
        # be able to put all the faceup cards back in the pile
        for c in range(num_fu):
            self.add_card(tmp_cards[c])

    def display(self):
        local_y = self.y
        for aCard in self.thePile:
            aCard.draw(self.x, local_y, self.canvas)
            local_y += 35
