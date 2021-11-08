from collections import defaultdict
from typing import List, Tuple, Dict
from enum import Enum

# UTILITY ENUMERATIONS  
"""
Enumeration to represent the numerical
equivalents for upper value cards
"""
class UpperValues(Enum):
    T = 10
    J = 11
    Q = 12
    K = 13
    A = 14

"""
Enumeration to represent the numerical 
values of the different rankings. 
(Where higher value represents higher rank)
"""
class PokerRanks(Enum):
    HIGHCARD = 1
    ONEPAIR = 2
    TWOPAIRS = 3
    THREEOFAKIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULLHOUSE = 7
    FOUROFAKIND = 8 
    STRAIGHTFLUSH = 9
    ROYALFLUSH = 10 

# UTILITY FUNCTIONS
"""
A function to convert string represented 
card values (T, J, Q, K, A) to numerical 
values
"""
def cardValueToNumericalRank(value:str) -> int:
    if value.isalpha():
        return UpperValues[value].value
    else: 
        return int(value)

"""
Returns the unique value counts for a valSuitPairs
"""
def getValCounts(valSuitPairs: List[Tuple[int, int]]) -> Dict[int, int]: 
    valCounts = defaultdict(lambda:0)
    for v,_ in valSuitPairs:
        valCounts[v]+=1
    return valCounts

"""
Returns unique suit counts for a valSuitPairs
"""
def getSuitCounts(valSuitPairs: List[Tuple[int, int]]) -> Dict[str, int]:
    suitCounts = defaultdict(lambda:0)
    for _,x in valSuitPairs:
        suitCounts[x]+=1
    return suitCounts

"""
Checks if the values for the given
set valSuitPairs are consecutive values 

ASSUMPTION: passed valSuitPairs are sorted by value 
(ascending)
"""            
def isIncreasingBy1(valSuitPairs: List[Tuple[int, int]]):
    lastVal = -1 
    for i, pair in enumerate(valSuitPairs):
        value = pair[0]
        if (i == 0):
            lastVal = value
        else:
            if (value - lastVal == 1):
                lastVal = value
            else:
                return False     
    return True

# POKER RANK CHECKING FUNCTIONS 
"""
Checks if the given set of 
valSuitPairs has a royal flush
"""
def checkRoyalFlush(valSuitPairs: List[Tuple[int, int]], suitCount: Dict[str, int]):
    hasFlush = checkFlush(valSuitPairs, suitCount)
    hasStraight = checkStraight(valSuitPairs)
    if (hasFlush and hasStraight and hasStraight[1] == 14):
        return (PokerRanks.ROYALFLUSH, 14)

"""
Checks if the given set of 
valSuitPairs has a straight flush
"""
def checkStraightFlush(valSuitPairs: List[Tuple[int, int]], suitCount:  Dict[str, int]):
    hasStraight = checkStraight(valSuitPairs)
    hasFlush = checkFlush(valSuitPairs, suitCount)
    if (hasStraight and hasFlush):
        return (PokerRanks.STRAIGHTFLUSH, hasStraight[1])

"""
Checks if the given set of 
valSuitPairs has four of a kind
"""
def checkFourOfAKind(valCounts: Dict[int, int]):
    for key, value in valCounts.items():
        if (value == 4):
            return (PokerRanks.FOUROFAKIND, key)
    return False

"""
Checks if the given set of 
valSuitPairs has a full house
"""
def checkFullHouse(valCounts:  Dict[int, int]):
    hasThreeOfKind = checkThreeOfAKind(valCounts)
    hasPair = checkOnePair(valCounts)
    if ( hasThreeOfKind and hasPair):
        return (PokerRanks.FULLHOUSE, hasThreeOfKind[1]) 

"""
Checks if the given set of 
valSuitPairs has a flush
"""
def checkFlush(valSuitPairs: List[Tuple[int, int]], suitCount: Dict[str, int]):
    if (5 in suitCount):
        return (PokerRanks.FLUSH, valSuitPairs[-1])
    return False

"""
Checks if the given set of 
valSuitPairs has a straight
"""
def checkStraight(valSuitPairs: List[Tuple[int, int]]):
    if (isIncreasingBy1(valSuitPairs)):
        return (PokerRanks.STRAIGHT, valSuitPairs[-1])
    return False


"""
Checks if the given valSuitPairs 
contain a three of a kind
"""
def checkThreeOfAKind(valCounts: Dict[int, int]):
    for key, value in valCounts.items():
        if (value == 3):
            return (PokerRanks.THREEOFAKIND, key)
    return False

"""
Checks if the the given valSuitPairs contain two pairs
"""
def checkTwoPairs(valCounts: Dict[int, int]):
    pairs = []
    for key, value in valCounts.items():
        if (value == 2):
            pairs.append(key)
    if (len(pairs) == 2):
        return (PokerRanks.TWOPAIRS, max(pairs))
    else:
        return False

"""
Checks if the given set of valSuitPairs contain a single pair
"""
def checkOnePair(valCounts: Dict[int, int]):
    for key, value in valCounts.items():
        if (value == 2):
            return (PokerRanks.ONEPAIR, [key])
    return False

"""
Returns the highest card in the given valSuitPairs
"""
def highCard(valSuitPairs: List[Tuple[PokerRanks, int]]): 
    return (PokerRanks.HIGHCARD, valSuitPairs[-1:])


# COMPARISON LOGIC 
"""
Finds the best hand in this valSuitPair

Takes advantage of the fact that Tuple[PokerRanks, int] is a truthy
value. Once one of the return values from one of the funcCheck functions 
returns Tuple[PokerRanks, int] instead of false the conditional on line 205
evaluates to true
"""
def findBestHand(valSuitPair: List[Tuple[PokerRanks, int]]):
    bestHand = False
    # Functions that need suit counts of a hand for their check 
    needSuitCounts = { checkFlush, checkStraightFlush, checkRoyalFlush}
    # Functions that need value counts of a hand for their check 
    needValCounts = { checkOnePair, checkTwoPairs, checkThreeOfAKind, checkFullHouse, checkFourOfAKind}
    # Order in which checks are done 
    orderOfChecks = [checkRoyalFlush, checkStraightFlush, checkFourOfAKind, checkFullHouse, checkFlush, checkStraight, checkThreeOfAKind, checkTwoPairs, checkOnePair, highCard]
    for funcCheck in orderOfChecks:
        suitCounts = getSuitCounts(valSuitPair)
        valCounts = getValCounts(valSuitPair)
        if (funcCheck in needValCounts):
            bestHand = funcCheck(valCounts)
        elif (funcCheck in needSuitCounts):
            bestHand = funcCheck(valSuitPair, suitCounts)
        else:
            bestHand = funcCheck(valSuitPair)
        if (bestHand):
            return bestHand

"""
Parses hand strings into values and suits. 
Finds the best hand in the parsed list 
"""
def evaluateHand(hand: List[str]) -> Tuple[PokerRanks, int]:
    valSuitPair = []
    # key to choose which value to sort valSuit pair on (@line 224)
    def comparePairsByValue(item1):
        return item1[0]
    for strVal in hand:
        value = strVal[0]
        suit = strVal[1]
        valSuitPair.append((cardValueToNumericalRank(value), suit))
    valSuitPair.sort(key=comparePairsByValue)
    return findBestHand(valSuitPair)

"""
Compares the player scores on the basis of 
PokerRanks and highest value 
"""
def compareScores(p1Score: Tuple[PokerRanks, int], p2Score: Tuple[PokerRanks, int]) -> Tuple[int, int]:
    (p1Rank, p1HighVal) = p1Score
    (p2Rank, p2HighVal) = p2Score
    p1RankVal = p1Rank.value
    p2RankVal = p2Rank.value
    if ( abs(p1RankVal - p2RankVal) > 0):
        return (1, 0) if p1RankVal > p2RankVal else (0, 1)
    else: 
        return (1, 0) if p1HighVal > p2HighVal else (0, 1)

"""
Calculates the number of wins by both player1 and player2
from poker.txt. Prints number of counts associated with 
player1
"""
def calculateP1WinCount():
    p1Wins = 0
    p2Wins = 0
    with open("poker.txt", "r") as pokerGames:
        for line in pokerGames:
            cards = line.rstrip().split(" ")
            player1Hand = cards[:5]
            player2Hand = cards[5:]
            player1bestHand = evaluateHand(player1Hand)
            player2bestHand = evaluateHand(player2Hand)
            (p1Point, p2Point) = compareScores(player1bestHand, player2bestHand)
            p1Wins += p1Point
            p2Wins += p2Point
    print(p1Wins)

        
