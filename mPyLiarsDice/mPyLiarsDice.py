import random, time
from neopixel import Neopixel
#import math #removed due to not being used at all in game (basic operations for maths needed so far)
global pixel#call the global version of pixel in use here
pixel = Neopixel(1,0,23,"GRB")#Neopixel object 'pixel'
pixel.brightness(127)#max brightness
global runtimeLEDState
runtimeLEDState = 0


#LD.txt is used to track state of LED
def createFile(name=str(None)):
    if name == None:
        name = str(random.randint(0,10000000))
    createdFile = open(name+".txt","a").close()


def reloadFile(name=str(None)):
    if name == None:
        name = str(random.randint(0,10000000))
    readingFile = open(name+".txt","r")
    data = readingFile.readline()
    readingFile.close()
    updateLED(data)
    return data


def writeFile(name=str(None),data=str(None)):
    if name == None:
        name = str(random.randint(0,10000000))
    if data == None:
        data = str(random.randint(0,10000000))
    writtenFile = open(name+".txt","w")
    writtenFile.write(data)
    writtenFile.flush()
    writtenFile.close()
    #update LED state to match data saved in file
    updateLED(data)


def reloadLED(r,g,b):
    global pixel
    pixel.set_pixel(0,(r,g,b))
    pixel.show()


def updateLED(data=str(None)):
    if data == "2":#win number
        reloadLED(0,255,0)
    if data == "1":#lose cond
        reloadLED(255,0,0)
    if data == "0":#quitter/in-progress
        reloadLED(255,255,0)


def blinkLED(r,g,b):
    global runtimeLEDState
    for carrier in range(15):
        reloadLED(r,g,b)
        time.sleep(0.1)
        reloadLED(0,0,0)
        time.sleep(0.1)
    updateLED(runtimeLEDState)


def setup():
    dieInHands = []
    allPlayerHands = []
    cpuMode = False

    
    try:
        players = int(input("How many players?"))
        if players <= 1:
            players = 2
            cpuMode = True
            easyChance, medChance, hardChance = difficultySelect()
            easyChance, medChance, hardChance = normaliseChanceValues(easyChance, medChance, hardChance)
        else:
            easyChance, medChance, hardChance = 1,0,0

        for placeholder in range(players):
            dieInHands.append(5)

        tempIndex = 0
        for dieCount in dieInHands:
            allPlayerHands.append([0])
            blankArray = []
            for placeholder in range(dieCount):
                blankArray.append(0)
            allPlayerHands[tempIndex] = blankArray
            tempIndex = tempIndex + 1

        currentAction = 0
        nextAction = currentAction + 1

        if cpuMode:
            cpugame(allPlayerHands, dieInHands, players, currentAction, nextAction, cpuMode, easyChance, medChance, hardChance)  # give initial conditions to gameloop
        else:
            game(allPlayerHands, dieInHands, players, currentAction, nextAction,
                 cpuMode)  # give initial conditions to gameloop
        playAgain = input("Play again? (y/n)")
        if playAgain == "y" or playAgain == "yes":
            return 1
        else:
            return 0
    except ValueError:
        setup()


def game(allPlayerHands, dieInHands, players, currentAction, nextAction, cpuMode):
    validGame = True
    lastBet = 10
    lastFace = 0
    lastCount = 0
    lastEject = "none"
    # when we start the game set this to true, so we can get new hands, it will reset to false anyway as actionTaken tells the code to gen new hands
    actionTaken = True  # records any action taken against any other player, resets when new hands are generated, which will be due to flag being true
    names = takenames(players,
                      cpuMode)  # Get player names (avoid use of magic number type of condition (pirate software XD))
    while validGame:  # main game while loop

        # crown winner
        if players <= 1:
            validGame = False
            print("Game Over")
        else:
            currentAction, nextAction = selectPlayers(players, currentAction, nextAction,
                                                      lastEject)  # select new numbers for actions

            if actionTaken:
                allPlayerHands = generateHands(dieInHands)
                lastBet = 10#reset here for centralised resetting
                lastFace = 1
                lastCount = 0
                actionTaken = False
            else:
                if (lastFace == 6 and lastCount >= totalDiceCount):
                    lastBet = 10
                    lastFace = 1
                    lastCount = 0
                    print("Maximum bet reached, resetting bet...")
                    time.sleep(1)
                else:
                    lastBet = currentBet
                    lastFace = diceFace
                    lastCount = minCount
                actionTaken = False  # reset flag for next round(not needed)

              # Clear the console for a fresh view
            print("Player " + names[currentAction] + "'s turn")
            print("Your dice:", allPlayerHands[currentAction])
            dieCountFormatted = "\n"
            for carrier in range(players):
                dieCountFormatted = dieCountFormatted + "Player " + names[carrier] + ":" + str(
                    dieInHands[carrier]) + "\n"
            print("\nPlayer Dice Count:" + dieCountFormatted)

            while True:
                try:
                    diceFace = int(input("Which face?"))
                    minCount = int(input("How much?"))
                    currentBet = int(str(diceFace) + str(minCount))

                    totalDiceCount = sum(dieInHands)
                    if (diceFace > lastFace or (diceFace == lastFace and minCount > lastCount)) and (minCount <= totalDiceCount and minCount >= 1 and diceFace <= 6 and diceFace >= 1):
                        break
                    else:
                        if diceFace > 6 or diceFace < 1:
                            print("Face chosen is not 1 to 6")
                        if minCount <= lastCount:
                            print("Minimum count is smaller than last count")
                        if minCount > totalDiceCount:
                            print("Minimum count is greater than total dice count. Nice one, mate.")
                        time.sleep(2)
                except ValueError:
                    print("Invalid input. Integers only for face and count.")

            
            print("Player " + names[nextAction] + "'s turn")
            print("Your dice:", allPlayerHands[nextAction])

            print("\nPlayer " + names[currentAction] + "'s bet:\n")
            print(dicegraphics(diceFace, minCount))

            bluffCall = input("(b)bluff\n(s)spot on\n(c)continue\nWhat do you want to call, Player " + names[nextAction] + "?(b/s/c):")
            if bluffCall.lower() == "y" or bluffCall.lower() == "b":

                actionTaken = True

                actualcount = 0
                validBet = False
                for hand in allPlayerHands:
                    for dice in hand:
                        if dice == diceFace:
                            actualcount = actualcount + 1
                if actualcount >= minCount:
                    validBet = True

                if validBet:
                    print("Valid bet from Player", names[currentAction], "so Player", names[nextAction],
                          "loses a dice for an incorrect bluff call")
                    dieInHands[nextAction] = dieInHands[nextAction] - 1
                    if dieInHands[nextAction] == 0:
                        lastEject = "next"
                        allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names, nextAction)
                        players -= 1

                    print(allPlayerHands)
                    print(dieInHands)
                else:
                    print("Invalid bet from Player", names[currentAction], "so Player", names[nextAction],
                          "wins a dice for a correct bluff call")
                    dieInHands[currentAction] = dieInHands[currentAction] - 1
                    if dieInHands[currentAction] == 0:
                        lastEject = "current"
                        allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,
                                                                         currentAction)
                        players -= 1

                    print(allPlayerHands)
                    print(dieInHands)
            elif bluffCall.lower() == "s":

                actionTaken = True

                actualcount = 0
                validBet = False
                for hand in allPlayerHands:
                    for dice in hand:
                        if dice == diceFace:
                            actualcount = actualcount + 1
                if actualcount == minCount:
                    validBet = False

                if validBet:
                    print("Bet from Player", names[currentAction], "was not exact, so Player", names[nextAction],
                          "loses a dice for an incorrect spot on call")
                    dieInHands[nextAction] = dieInHands[nextAction] - 1
                    if dieInHands[nextAction] == 0:
                        lastEject = "next"
                        allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names, nextAction)
                        players -= 1

                    print(allPlayerHands)
                    print(dieInHands)
                else:
                    print("Bet from Player", names[currentAction], "was exact, so Player", names[nextAction],
                          "wins a dice for a correct spot on call")
                    dieInHands[currentAction] = dieInHands[currentAction] - 1
                    if dieInHands[currentAction] == 0:
                        lastEject = "current"
                        allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,
                                                                         currentAction)
                        players -= 1

                    print(allPlayerHands)
                    print(dieInHands)


            else:
                print("No action taken, Player " + names[nextAction] + " continues")
                time.sleep(1)
                print("Last Bet was " + str(diceFace) + "x" + str(minCount) + ". You must bet higher than this next round, by frequency or face or both")
                time.sleep(1)


        input("Press Enter to continue...")


def cpugame(allPlayerHands, dieInHands, players, currentAction, nextAction, cpuMode, easyChance, medChance, hardChance):
    validGame = True
    lastBet = 10
    lastFace = 0
    lastCount = 0
    actionTaken = True  # records any action taken against any other player
    lastEject = "none"  # not used in 1v1 (only 2 players so once the first eject happens, it's the last eject for that game as well, right?)
    currentAction = random.randint(0, 1)
    nextAction = 1 - currentAction
    names = takenames(players, cpuMode)

    # easyChance, medChance, hardChance were here

    while validGame:  # main game while loop
        writeFile("ledState","0")

        # if only 1 player remains... CROWN HIM WINNER!!!
        if players <= 1:
            validGame = False
            print("Game Over")
            print("Player " + names[0] + " wins!")
            if names[0] == "T-800":
                writeFile("ledState","2")
            else:
                writeFile("ledState","1")
            
        else:  # else, we should start by generating the action numbers
            temp = currentAction
            currentAction = nextAction
            nextAction = temp

            if actionTaken:
                allPlayerHands = generateHands(dieInHands)
                lastBet = 10#reset here for centralised resetting
                lastFace = 1
                lastCount = 0
                actionTaken = False
            else:
                if (lastFace == 6 and lastCount >= totalDiceCount):
                    lastBet = 10
                    lastFace = 1
                    lastCount = 0
                    print("Maximum bet reached, resetting bet...")
                    time.sleep(1)
                else:
                    lastBet = currentBet
                    lastFace = diceFace
                    lastCount = minCount
                actionTaken = False  # reset flag for next round(not needed)

              # Clear the console for a fresh view
            # print(currentAction)debug due to old actioning code left in and causing bad behaviour (fixed)
            print("Player " + names[currentAction] + "'s turn")
            print("Your dice:", allPlayerHands[currentAction])
            dieCountFormatted = "\n"
            for carrier in range(players):
                dieCountFormatted = dieCountFormatted + "Player " + names[carrier] + ":" + str(
                    dieInHands[carrier]) + "\n"
            print("\nPlayer Dice Count:" + dieCountFormatted)
            totalDiceCount = sum(dieInHands)

            while True:
                if currentAction == 0:  # Player's turn
                    try:
                        diceFace = int(input("Which face?"))
                        minCount = int(input("How much?"))
                        currentBet = int(str(diceFace) + str(minCount))

                        if (diceFace > lastFace or (diceFace == lastFace and minCount > lastCount)) and (minCount <= totalDiceCount and minCount >= 1 and diceFace <= 6 and diceFace >= 1):
                            break
                        else:
                            if diceFace > 6 or diceFace < 1:
                                print("Face chosen is not 1 to 6")
                            if minCount <= lastCount:
                                print("Minimum count is smaller than last count")
                            if minCount > totalDiceCount:
                                print("Minimum count is greater than total dice count. Really proving that man is greater than machine here.")
                            time.sleep(2)
                    except ValueError:
                        print("Invalid input. Integers only for face and count.")
                else:  # cpu's turn
                    # needed to be returned
                    diceFace = 0
                    minCount = 0
                    currentBet = 0

                    currentBet, diceFace, minCount = cpuBet(allPlayerHands, currentAction, lastBet, lastFace, lastCount, currentBet, diceFace, minCount, easyChance, medChance, hardChance)

                    #game checking if bet is valid - it is NOT part of the CPU's betting system (FINAL CHECK, similar to player betting)
                    if (diceFace > lastFace or (diceFace == lastFace and minCount > lastCount)) and (minCount <= totalDiceCount and minCount >= 1 and diceFace <= 6 and diceFace >= 1):
                        print("Robot has done an invalid bet. Please wait...")
                        print("REPORT THIS IF YOU NOTICE WITH SCREENSHOT")
                        time.sleep(2)
                    else:
                        break

            
            if nextAction == 0:  # Player's turn
                print("Player " + names[nextAction] + "'s turn")
                print("Your dice:", allPlayerHands[nextAction])

                print("\nPlayer " + names[currentAction] + "'s bet:\n")
                print(dicegraphics(diceFace, minCount))

                bluffCall = input("(b)bluff\n(s)spot on\n(c)continue\n What do you want to do, Player " + names[nextAction] + "?(b/s/c):")
                if bluffCall.lower() == "y" or bluffCall.lower() == "b":

                    actionTaken = True

                    actualcount = 0
                    validBet = False
                    for hand in allPlayerHands:
                        for dice in hand:
                            if dice == diceFace:
                                actualcount = actualcount + 1
                    if actualcount >= minCount:
                        validBet = True

                    if validBet:
                        print("Valid bet from Player", names[currentAction], "so Player", names[nextAction],
                              "loses a dice for an incorrect bluff call")
                        dieInHands[nextAction] = dieInHands[nextAction] - 1
                        if dieInHands[nextAction] == 0:
                            lastEject = "next"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names, nextAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                        blinkLED(255,0,0)
                    else:
                        print("Invalid bet from Player", names[currentAction], "so Player", names[nextAction],
                              "wins a dice for a correct bluff call")
                        dieInHands[currentAction] = dieInHands[currentAction] - 1
                        if dieInHands[currentAction] == 0:
                            lastEject = "current"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names, currentAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                        blinkLED(0,255,0)
                elif bluffCall.lower() == "s":
                    print("Player", names[nextAction], "calls spot on, on Player", names[currentAction])
                    time.sleep(1)
                    actionTaken = True

                    actualcount = 0
                    validBet = False
                    for hand in allPlayerHands:
                        for dice in hand:
                            if dice == diceFace:
                                actualcount = actualcount + 1
                    if actualcount == minCount:
                        validBet = False

                    if validBet:
                        print("Bet from Player", names[currentAction], "was not exact, so Player", names[nextAction],
                              "loses a dice for an incorrect spot on call")
                        dieInHands[nextAction] = dieInHands[nextAction] - 1
                        if dieInHands[nextAction] == 0:
                            lastEject = "next"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names, nextAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                        blinkLED(255,0,0)
                    else:
                        print("Bet from Player", names[currentAction], "was exact, so Player", names[nextAction],
                              "wins a dice for a correct spot on call")
                        dieInHands[currentAction] = dieInHands[currentAction] - 1
                        if dieInHands[currentAction] == 0:
                            lastEject = "current"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names, currentAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                        blinkLED(0,255,0)


                else:
                    print("No action taken, Player ", names[nextAction], " continues")
                    time.sleep(1)
                    print("Last Bet was " + str(
                        currentBet) + ". You must bet higher than this next round, by frequency or face or both")
                    blinkLED(255,255,255)
            else:  # CPU's turn
                bluffCall = ""

                fakePlayerHands = []
                faceFrequency = [[],[],[],[],[],[]]
                for carrier in range(allPlayerHands[currentAction]-1):
                    face = random.randint(1,6)
                    fakePlayerHands.append(face)
                    faceFrequency[face - 1] = faceFrequency[face - 1] + 1
                fakePlayerHands.append(diceFace)

                for carrier in allPlayerHands[nextAction]:
                    faceFrequency[carrier-1] = faceFrequency[carrier-1] + 1

                if faceFrequency[diceFace] > minCount:
                    bluffCall = "b"
                elif faceFrequency[diceFace] < minCount:
                    bluffCall = "c"
                else:
                    bluffCall = "s"



                if bluffCall.lower() == "y" or bluffCall.lower() == "b":
                    print("Player", names[nextAction], " calls bluff on Player ", names[currentAction])
                    time.sleep(1)
                    actionTaken = True

                    actualcount = 0
                    validBet = False
                    for hand in allPlayerHands:
                        for dice in hand:
                            if dice == diceFace:
                                actualcount = actualcount + 1
                    if actualcount >= minCount:
                        validBet = True

                    if validBet:
                        print("Valid bet from Player", names[currentAction], "so Player", names[nextAction],
                              "loses a dice for an incorrect bluff call")
                        dieInHands[nextAction] = dieInHands[nextAction] - 1
                        if dieInHands[nextAction] == 0:
                            lastEject = "next"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,
                                                                             nextAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                        blinkLED(0,255,0)
                    else:
                        print("Invalid bet from Player", names[currentAction], "so Player", names[nextAction],
                              "wins a dice for a correct bluff call")
                        dieInHands[currentAction] = dieInHands[currentAction] - 1
                        if dieInHands[currentAction] == 0:
                            lastEject = "current"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,
                                                                             currentAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                        blinkLED(255,0,0)
                elif bluffCall.lower() == "s":
                    print("Player", names[nextAction], "calls spot on, on Player", names[currentAction])
                    time.sleep(1)
                    actionTaken = True

                    actualcount = 0
                    validBet = False
                    for hand in allPlayerHands:
                        for dice in hand:
                            if dice == diceFace:
                                actualcount = actualcount + 1
                    if actualcount == minCount:
                        validBet = False

                    if validBet:
                        print("Bet from Player", names[currentAction], "was not exact, so Player", names[nextAction],
                              "loses a dice for an incorrect spot on call")
                        dieInHands[nextAction] = dieInHands[nextAction] - 1
                        if dieInHands[nextAction] == 0:
                            lastEject = "next"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,
                                                                             nextAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                        blinkLED(0,255,0)
                    else:
                        print("Bet from Player", names[currentAction], "was exact, so Player", names[nextAction],
                              "wins a dice for a correct spot on call")
                        dieInHands[currentAction] = dieInHands[currentAction] - 1
                        if dieInHands[currentAction] == 0:
                            lastEject = "current"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,
                                                                             currentAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                        blinkLED(255,0,0)


                else:
                    print("No action taken, Player ", names[nextAction], " continues")
                    time.sleep(1)
                    print("Last Bet was " + str(diceFace) + "x" + str(minCount) + ". You must bet higher than this next round, by frequency or face or both")
                    blinkLED(255,255,255)

            input("Press Enter to continue...")


def generateHands(dieinhands):  # playercount not needed as len(dieInHands) represents info good enough
    player = 0
    allplayerhands = []
    tempArray = []
    for diecount in dieinhands:
        for dice in range(diecount):
            tempArray.append(0)
        allplayerhands.append(tempArray)
        tempArray = []
        for dice in range(diecount):
            allplayerhands[player][dice] = random.randint(1, 6)
        player = player + 1
    return allplayerhands


def removePlayer(hands, diecounts, givennames, index):
    if len(hands) != len(diecounts):  # user has given incorrect lengths of lists
        raise ValueError("Hands and die counts must be of the same length.")
    if index > len(hands):
        raise IndexError("Index out of range (too large i). Cannot remove player at index " + str(index) + ".")
    else:
        new_list1 = []
        new_list2 = []
        new_list3 = []
        for carrier in range(len(hands)):
            if carrier == index:
                pass
            else:
                new_list1.append(hands[carrier])
                new_list2.append(diecounts[carrier])
                new_list3.append(givennames[carrier])
        return new_list1, new_list2, new_list3


def dicegraphics(number, frequency):
    if number != int:
        try:
            number = int(number)
        except ValueError:
            return "Invalid input for dice graphics. Please enter an integer between 1 and 6."

    graphics = ""
    if number == 1:
        graphics += (" ---------") + "\n"
        graphics += ("|         |") + "\n"
        graphics += ("|    *    |   x     " + str(frequency)) + "\n"
        graphics += ("|         |") + "\n"
        graphics += (" ---------") + "\n"
    elif number == 2:
        graphics += (" ---------") + "\n"
        graphics += ("| *       |") + "\n"
        graphics += ("|         |   x     " + str(frequency)) + "\n"
        graphics += ("|       * |") + "\n"
        graphics += (" ---------") + "\n"
    elif number == 3:
        graphics += (" ---------") + "\n"
        graphics += ("| *       |") + "\n"
        graphics += ("|    *    |   x     " + str(frequency)) + "\n"
        graphics += ("|       * |") + "\n"
        graphics += (" ---------") + "\n"
    elif number == 4:
        graphics += (" ---------") + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += ("|         |   x     " + str(frequency)) + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += (" ---------") + "\n"
    elif number == 5:
        graphics += (" ---------") + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += ("|    *    |   x     " + str(frequency)) + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += (" ---------") + "\n"
    elif number == 6:
        graphics += (" ---------") + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += ("| *     * |   x     " + str(frequency)) + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += (" ---------") + "\n"
    else:
        graphics = ("""unknownNumber""")
    return graphics


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


def takenames(no_of_players, cpuMode):
    localnames = []
    if not cpuMode:
        for i in range(no_of_players):
            while True:
                name = input("Enter name for Player " + str(i) + ": ")
                if name.strip() == "":
                    print("Name cannot be empty. Please enter a valid name.")
                elif name in localnames:
                    print("Name already taken. Please choose a different name.")
                else:
                    localnames.append(name)
                    break
    else:
        player1name = ""
        cpuName = "T-800"
        while player1name.strip() == "" or player1name in localnames or player1name.lower() == cpuName:
            player1name = input("Enter name: ")
        localnames.append(player1name)
        localnames.append(cpuName)

    return localnames


def selectPlayers(players, current, nextaction, lasteject):
    maxIndex = players - 1
    if lasteject == "current":
        if current < maxIndex:  # has to be second to last or less, so next does not get assigned out of bounds
            pass
        elif current == maxIndex:
            nextaction = 0
        elif current > maxIndex:
            current = 0
            nextaction = current + 1
        else:
            pass
    elif lasteject == "next":
        if nextaction >= maxIndex:
            current = maxIndex
            nextaction = 0
        elif nextaction < maxIndex:
            current += 1
            nextaction = current + 1
        else:
            print("selectPlayers('next',...) failed cond check")
    elif lasteject == "none":
        if current >= maxIndex:  # should never execute, realistically
            current = 0
            nextaction = current + 1
        elif current == maxIndex - 1:
            current = maxIndex
            nextaction = 0
        elif current < maxIndex - 1:
            current = current + 1
            nextaction = current + 1
        else:
            print("selectPlayers('none',...) failed cond check")

    return current, nextaction


def cpuBet(allPlayerHands, currentAction, lastBet, lastFace, lastCount, currentBet, diceFace, minCount, easyChance, medChance, hardChance):
    #added hardening/checks against some errors (which technically should never occur, as the values are normalised before the game loop runs. They are never modified within game loop)
    if (easyChance + medChance + hardChance) != 1:
        easyChance, medChance, hardChance = normaliseChanceValues(easyChance, medChance, hardChance)
    else:
        pass

    # used in processing only
    facesPresent = []
    countOfFaces = [0, 0, 0, 0, 0, 0]

    # all faces present
    for carrier in allPlayerHands[currentAction]:
        if not carrier in facesPresent:
            facesPresent.append(carrier)
            countOfFaces[carrier - 1] = (
                allPlayerHands[currentAction].count(carrier))  # and count for all faces present

    easyMedHard = random.random()
    if easyMedHard <= easyChance:  # strat 1: bet the highest face held and pick and
        for carrier in facesPresent:
            if carrier >= lastFace:
                diceFace = carrier
                minCount = countOfFaces[carrier - 1]
                if minCount <= lastCount:
                    minCount = lastCount + 1  # easiest way to meet threshold (this is easymode betting after all)
                break  # to make it easy, just break now

        if diceFace < lastFace:#if no suitable face was found
            diceFace = facesPresent[random.randint(0, len(facesPresent) - 1)]
            minCount = countOfFaces[diceFace]
            if minCount <= lastCount:
                minCount = lastCount + 1  # just bluff away, don't bother rerolling

    elif easyMedHard <= easyChance + medChance:  # strat 2: checks if it can raise current face bet, otherwise try go to face with the highest face that beats count and if that fails, pick random face
        if lastFace in facesPresent and countOfFaces[lastFace - 1] > lastCount:
            diceFace = lastFace
            minCount = countOfFaces[lastFace - 1]
        else:
            for carrier in facesPresent:
                if carrier > lastFace or (carrier == lastFace and countOfFaces[carrier - 1] > lastCount):
                    diceFace = carrier
                    minCount = countOfFaces[carrier - 1]
            if diceFace <= lastFace:
                if lastCount + 1 > len(allPlayerHands[currentAction]):
                    diceFace = lastFace + 1
                    minCount = 1
                else:
                    diceFace = lastFace
                    minCount = lastCount + 1

    else:  # strat 3: goes to max straight away (best strat)
        diceFace = max(facesPresent)
        if lastFace > diceFace:
            diceFace = lastFace
            minCount = lastCount + 1
        else:
            minCount = countOfFaces[diceFace - 1] + random.randint(0, 2)
            if minCount <= lastCount:
                minCount = lastCount + 1#bluff as bet is too high for us to accurately call so just add one onto the bet



    # bet builder and final checks
    if diceFace > 6 or diceFace < 1:
        diceFace = 6
        minCount = countOfFaces[diceFace - 1]
    if minCount <= lastCount:
        minCount = lastCount + 1

    currentBet = int(str(diceFace) + str(minCount))
    totalDiceCount = len(allPlayerHands)

    if (diceFace > lastFace or (diceFace == lastFace and minCount > lastCount)) and (minCount <= totalDiceCount and minCount >= 1 and diceFace <= 6 and diceFace >= 1):
        currentBet = lastBet + random.randint(1, 2)
    else:# bet is valid
        pass

    return currentBet, diceFace, minCount


def difficultySelect():
    answer = 0#default answer to difficulty (was string but microcontrollers don't like this (was running in pico for fun))
    try:
        answer = int(input(
            "CPU Difficulty?\n(0) Crybaby Mode :,-(  (Easy Mode)\n(1) What's the controls again? |:-/  (Normal Mode)\n(2) Bring it on! >:-D  (Hard Mode)"))
    except:
        difficultySelect()

    if answer > 2 or answer < 0:
        print("Seeing as you find it difficult to differentiate 3 numbers, I'll go easy on you - CPU")
        answer = 0

    if answer == 0:
        easyChance = 1.0
        medChance = 0
        hardChance = 0
    elif answer == 1:
        easyChance = 0.5
        medChance = 0.5
        hardChance = 0
    elif answer == 2:
        easyChance = 0.2
        medChance = 0.2
        hardChance = 0.6
    else:
        print(
            "Answer out of choice and validation + correction for answer has failed. Fix logic. TEMPORARY MEDIUM DIFFICULTY GIVEN")
        easyChance = 1.0
        medChance = 0
        hardChance = 0
    return easyChance, medChance, hardChance


def normaliseChanceValues(easyChance, medChance, hardChance):  # in case new changes to the chances occurs
    totalChance = easyChance + medChance + hardChance
    if totalChance != 1.0:  # normalise by dividing by itself (n/n = 1 therefore dividing each constituent by n will yield normalised chance values NOTE: random.random() can only work within 0 to 1)
        easyChance = easyChance / totalChance
        medChance = medChance / totalChance
        hardChance = hardChance / totalChance

    return easyChance, medChance, hardChance


#this is done so we can call it from outside when imported into another script instead of relying on dunder for execution of main
def run():
    reloadFile("ledState")
    setupReturn = 1
    while setupReturn == 1:#ignore running in CI/CD
        #note: (CD mainly, as CI will just import necessary methods and operate on them with input data and valid output checking)
        setupReturn = setup()


#main
if __name__ == "__main__":
    run()
    print("GOODBYE")

