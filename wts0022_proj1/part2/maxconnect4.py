import sys
from MaxConnect4Game import maxConnect4Game
import time
def interactiveGame(currentGame, next):
    currentGame.countScore()
    print("User is Player A" if (next == "human-first" or next == "human-next") else "User is Player B")
    
    while currentGame.getPieceCount() != 42:
        if next == 'human-first' or next == 'human-next':
            print("User's turn.")
            try:
                userMove = int(input("Enter column number (1 - 7): "))
            except ValueError:
                print("Invalid input!")
                continue
            if userMove < 1 or userMove > 7:
                print("Invalid input!")
                continue
            if not currentGame.playPiece(userMove - 1):
                print("Column is full!")
                continue
            currentGame.printGameBoard()
            with open("human.txt", "w") as f:
                currentGame.gameFile = f
                currentGame.printGameBoardToFile()
                #gameboard.gameFile.close()
            if currentGame.getPieceCount() == 42:
                print("Game board is full!")
                currentGame.countScore()
                print('Score: Player A = %d, Player B = %d\n' % (currentGame.player1Score, currentGame.player2Score))
                break
            next = "computer-next"
            currentGame.nextTurn()
        else:
            currentGame.aiPlay()
            print("Computer's turn")
            with open("human.txt", "w") as f:
                currentGame.gameFile = f
                currentGame.printGameBoardToFile()
            #gameboard.gameFile.close()
            currentGame.printGameBoard()
            currentGame.countScore()
            print('Score: Player A = %d, Player B = %d\n' % (currentGame.player1Score, currentGame.player2Score))
            next = "human-next"

    if currentGame.getPieceCount() == 42:
        if currentGame.player1Score > currentGame.player2Score:
            print("Player A won")
        if currentGame.player1Score == currentGame.player2Score:
            print("Tie, no winners")
        if currentGame.player1Score < currentGame.player2Score:
            print("Player B won")

def oneMoveGame(currentGame):
    if currentGame.getPieceCount() == 42:
        if currentGame.player1Score > currentGame.player2Score:
            print("Player A won")
        if currentGame.player1Score == currentGame.player2Score:
            print("Tie, no winners")
        if currentGame.player1Score < currentGame.player2Score:
            print("Player B won")
    if currentGame.piece_count >= 42:
        print("Game board is full!")
        sys.exit(0)
    currentGame.aiPlay()
    print ('Current game state:')
    currentGame.printGameBoard()
    currentGame.countScore()
    print('Score: Player A = %d, Player B = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()
    

def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print('Four command-line arguments are needed:')
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)
    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)
    currentGame = maxConnect4Game() # Create a game
    
    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")
    currentGame.depth = argv[-1]
    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    try:
        currentGame.currentTurn = int(file_lines[-1][0])
    except:
        sys.exit("\nError reading file input.\nCheck if file input is formated correctly.\n")
    currentGame.gameFile.close()
    print ('\nMaxConnect-4 game\n')
    print ('Game state before move:')
    currentGame.printGameBoard()
    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player A = %d, Player B = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    if game_mode == 'interactive':
        interactiveGame(currentGame, argv[3]) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)