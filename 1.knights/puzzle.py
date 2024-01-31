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
    # game conditions:
    # A must be either knigth or knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # statements:
    Biconditional(And(AKnight, AKnave), AKnight)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # game conditions:
    # A must be either knigth or knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B must be either knigth or knave
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # statements:
    Biconditional(And(AKnave, BKnave), AKnight) #if statement is true a is knigth, if false a is knave
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # game conditions:
    # A must be either knigth or knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B must be either knigth or knave
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A statement
    Biconditional(Or(And(AKnave, BKnave), And(AKnight, BKnight)), AKnight),
    # B statement
    Biconditional(Or(And(AKnave, BKnight), And(AKnight, BKnave)), BKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # game conditions:
    # A must be either knigth or knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B must be either knigth or knave
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # C must be either knigth or knave
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A statement
    Or(
        And(AKnave, AKnight), # A said "aknave" and it is true,
        And(Not(AKnave), AKnave), # A said "aknave" and it is false,
        And(AKnight, AKnight), # A said "aknight" and it is true,
        And(Not(AKnight), AKnave), # A said "aknight" and it is false,
    ),

    # B statements 
    Biconditional(Or(
            And(AKnave, AKnight), # A said aknave and it is true
            And(Not(AKnave), AKnave) # A said aknave and it is false
        ), BKnight),

    Biconditional(CKnave, BKnight),

    # C statements
    Biconditional(AKnight, CKnight) 
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
