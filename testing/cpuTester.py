import random,os

if os.environ.get('GITHUB_ACTIONS'):
    import sys
    sys.path.append('..')

from LiarsDice.LiarsDice.LiarsDice import cpuBet,dicegraphics
#package/repo name, folder name, filename/module/script name


threeTestUnit = ""

threeTestUnit += (" ---------") + "\n"
threeTestUnit += ("| *       |") + "\n"
threeTestUnit += ("|    *    |   x     " + str(9)) + "\n"
threeTestUnit += ("|       * |") + "\n"
threeTestUnit += (" ---------") + "\n"

def generateHandsForTests():
    allPlayerHands = [[], []]
    for carrier in range(2):
        for carrier2 in range(5):
            allPlayerHands[carrier].append(random.randint(1, 6))
    return allPlayerHands

def testBetting(allPlayerHands,lastFace,lastCount):
    lastBet = int(str(lastFace) + str(lastCount))
    currentBet, diceFace, minCount = cpuBet(allPlayerHands, 1, lastBet, lastFace, lastCount, 0, 5, 5, 1, 0, 0)
    assert (diceFace >= 0)
    assert (minCount > 0)
    assert (currentBet > lastBet)
    return currentBet

def testGraphics():
    assert dicegraphics(0,9) == "unknownNumber"
    assert dicegraphics(7,9) == "unknownNumber"
    assert dicegraphics(3,9) == threeTestUnit
    print("PASSED - GRAPHICS TESTING")

face = 3
count = 3
lastBet = int(str(face) + str(count))
print("Last Bet:", lastBet)
for carrier in range(10):
    print("Hand:",carrier+1)
    currentHands = generateHandsForTests()
    print("Current Hands:",currentHands)
    for carrier2 in range(10):#repeat n times and see how stable the cpuBetting is
        print("Iteration:",carrier2+1)
        cBet = testBetting(currentHands,face,count)
        print("Current Bet:",cBet)

testGraphics()