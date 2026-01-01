import random

def guessDice(count, side, ownDice, players, diceRemaining, playerNum):
    dice = []

    diceRemaining[playerNum] = 0

    for carrier in range(players):
        diceGen = []
        for carrier2 in range(diceRemaining[carrier]):
            diceGen.append(random.randint(1, 6))
        if len(diceGen) > 0:    
            dice.append(diceGen)

    dice.append(ownDice)

    for hand in dice:
        for d in hand:
            if d == side:
                count -= 1

    if count <= 0:
        return True
    else:
        return False


#if guessDice(6,1,[2,3,4,6,6],4,[3,4,5,4],1) == True: print("BLUFF")