import time
import math
import random
from aqt import mw, gui_hooks
from anki.collection import Card


# Setup Hooks
#########################################################################

MIN_SPACING = 60
MAX_SPACING = 90
ONE_MINUTE = 60  # in seconds


@gui_hooks.reviewer_did_show_question.append
def handleReviewer(card: Card) -> None:
    now = math.floor(time.time())  # in seconds since epoch
    totalRandomness = 0

    # if the current card is a 'red' card
    cardIds = mw.col.findCards("is:due is:learn")
    if card.id in cardIds:
        cards = list(map(lambda id: mw.col.getCard(id), cardIds))
        overdueCards = list(
            filter(lambda c: c.due <= now + ONE_MINUTE and c.id != card.id, cards)
        )

        # Shuffle all cards that are comming up soon.
        random.shuffle(overdueCards)
        for card in overdueCards:
            # Properly Space the review cards that are in this time range
            # Show the first card right away
            randomness = random.randint(MIN_SPACING, MAX_SPACING)
            card.due = now + totalRandomness + randomness
            card.flush()
            totalRandomness += randomness
