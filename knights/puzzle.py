from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a Knight or a Knave and not both, A said he is both a Knight and a Knave, so A is a Knight if and only if what he said is true
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)), Biconditional((And(AKnight, AKnave)), AKnight)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A is either a Knight or a Knave and not both, A said A and B are both Knaves, therefore A is a Knight if and only if what he said is true
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)), Biconditional((And(AKnave, BKnave)), AKnight),
    Or(BKnight, BKnave), Not(And(BKnight, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is either a Knight or a Knave and not both, A said A and B are both the same kind, therefore A is a Knight if and only if what he said is true
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)), Biconditional(Or(And(AKnight, BKnight), And(AKnave, BKnave)), AKnight),
    # B is either a Knight or a Knave and not both, B said A and B are different kinds, therefore B is a Knight if and only if what he said is true
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)), Biconditional(Or(And(AKnight, BKnave), And(AKnave, BKnight)), BKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A is either a Knight or a Knave and not both, A either said 'i am a knight' or 'i am a knave' but we don't know which, therefore A is a Knight if and only if what he said is true
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)), Biconditional(And(Or(AKnight, AKnave), Not(And(AKnave, AKnight))), AKnight),
    # B is either a Knight or a Knave and not both, B said A said he is a Knave, therefore the only way B is a Knight is if what he said is true
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)), Biconditional(AKnave, BKnight),
    # C is either a Knight or a Knave and not both, B said C is a knave, therefore for B to be a knight what he said must be true, likewise C said A is a knight and C has to be a knight for that to be true
    Or(CKnight, CKnave), Not(And(CKnight, CKnave)), Biconditional(CKnave, BKnight), Biconditional(AKnight, CKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
