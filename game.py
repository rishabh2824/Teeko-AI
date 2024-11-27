import logging
import random
import copy
import numpy as np


class TeekoPlayer:
    pieces = ['b', 'r']

    # Teeko player object
    def __init__(self, ai_first=True):
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.my_piece = 'b' if ai_first else 'r'
        self.opp = 'r' if ai_first else 'b'
        self.move_count = 0  # Initialize the move counter

    def opponent_move(self, move):
        logging.debug(f"Processing opponent move: {move}")

        # Check if it's a move phase (not drop phase)
        if len(move) > 1:
            source_row, source_col = move[1]  # Source cell
            dest_row, dest_col = move[0]  # Destination cell

            # Validate the source cell
            if source_row is not None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")

            # Validate adjacency
            if abs(source_row - dest_row) > 1 or abs(source_col - dest_col) > 1:
                raise Exception('Illegal move: Can only move to an adjacent space')

        # Validate destination cell
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")

        # Make the move
        self.place_piece(move, self.opp)


    # Identify the position of all the pieces
    @staticmethod
    def piecesPosition(state):
        b, r = [], []
        # Loop through all the positions and add the filled positions to b, r as a tuple
        for row in range(5):
            for col in range(5):
                if state[row][col] == 'b': b.append((row, col))

                elif state[row][col] == 'r': r.append((row, col))
        return b, r

    # Returns a heuristic evaluation of the current board. The heuristic is the difference between my current longest
    # contiguous sequence and the opponents. The value is normalized for easier comparison
    @staticmethod
    def getHeuristic(state, piece):
        # Assign b, r to my piece and opponent's piece
        if piece == 'b': myPiece, oppPiece = 'b', 'r'

        else: myPiece, oppPiece = 'r', 'b'

        # Max connection counters for both players
        maxMine, maxOpp = 0, 0

        # Check horizontal and vertical connections - only where a sequence of 4 can fit
        for i in range(5):
            for j in range(2):
                # Check horizontal sequences for my pieces
                count = 0
                for k in range(4):
                    if state[i][j + k] == myPiece: count += 1

                maxMine = max(maxMine, count)

                # Check horizontal sequences for opponent's pieces
                count = 0
                for k in range(4):
                    if state[i][j + k] == oppPiece: count += 1

                maxOpp = max(maxOpp, count)

                # Check vertical sequences for my pieces
                count = 0
                for k in range(4):
                    if state[j + k][i] == myPiece: count += 1

                maxMine = max(maxMine, count)

                # Check vertical sequences for opponent's pieces
                count = 0
                for k in range(4):
                    if state[j + k][i] == oppPiece: count += 1

                maxOpp = max(maxOpp, count)

        # Check diagonal connections - (\)
        for i in range(2):
            for j in range(2):
                count = 0
                for k in range(4):
                    if state[i + k][j + k] == myPiece: count += 1

                maxMine = max(maxMine, count)

                count = 0
                for k in range(4):
                    if state[i + k][j + k] == oppPiece: count += 1

                maxOpp = max(maxOpp, count)


        # Check diagonal connections - (/)
        for i in range(2):
            for j in range(3, 5):
                count = 0
                for k in range(4):
                    if state[i + k][j - k] == myPiece: count += 1

                maxMine = max(maxMine, count)

                count = 0
                for k in range(4):
                    if state[i + k][j - k] == oppPiece: count += 1

                maxOpp = max(maxOpp, count)


        # Check 2x2 box connections
        for i in range(4):
            for j in range(4):
                count = 0
                for dx in [0, 1]:
                    for dy in [0, 1]:
                        if state[i + dx][j + dy] == myPiece: count += 1

                maxMine = max(maxMine, count)

                count = 0
                for dx in [0, 1]:
                    for dy in [0, 1]:
                        if state[i + dx][j + dy] == oppPiece: count += 1

                maxOpp = max(maxOpp, count)

        # Return the heuristic after normalizing
        return (maxMine - maxOpp) / 6, state

    # Returns the drop phase by checking for less than 8 pieces
    @staticmethod
    def getDropPhase(state):
        totalPieces = 0
        for row in state:
            totalPieces += row.count('b')
            totalPieces += row.count('r')

        return totalPieces < 8

    # Make the best move using minimax algo
    def make_move(self, state):
        # Check drop phase
        drop_phase = self.getDropPhase(state)

        # Find the best state starting with depth 0 and alpha beta initialized
        _, bestState = self.max_value(state, 0, float('-inf'), float('inf'))

        # Find the differences in current state and best state
        diff = np.array(state) != np.array(bestState)

        # Row and Col indices of differing cells
        indices = np.where(diff)

        # Find source and destination cells
        changedPositions = []
        for i in range(len(indices[0])):
            position = (indices[0][i], indices[1][i])
            changedPositions.append(position)

        if drop_phase:
            # Drop phase: Only one cell changes
            dst = changedPositions[0]
            return [dst]
        else:
            # Move phase: Two cells change
            src, dst = None, None
            for pos in changedPositions:
                if state[pos[0]][pos[1]] == self.my_piece: src = pos

                elif state[pos[0]][pos[1]] == ' ': dst = pos

                # Break if both src and dst are found
                if src and dst: break

            return [dst, src]


    # Min max algo
    def max_value(self, state, depth, alpha, beta):
        # Check if game has ended and return the result
        if self.game_value(state) != 0: return self.game_value(state), state

        # Check if max depth is reached and return the heuristic value of current state
        if depth >= 3: return self.getHeuristic(state, self.my_piece)

        # Initialize max value to -infinity
        value = float('-inf')

        # Set current state as best state
        bestState = state

        # Generate successors for my pieces
        for s in self.generateSuccessors(state, self.my_piece):
            # Get the successors value by exploring opponent's min layer
            sValue, _ = self.min_value(s, depth + 1, alpha, beta)

            # Check if the value is higher and update best value and state
            if sValue > value: value, bestState = sValue, s

            # Pruning
            if value >= beta: break
            alpha = max(alpha, value)

        return value, bestState

    def min_value(self, state, depth, alpha, beta):
        if self.game_value(state) != 0: return self.game_value(state), state
        if depth >= 3: return self.getHeuristic(state, self.opp)
        value, bestState = float('inf'), state
        for s in self.generateSuccessors(state, self.opp):
            sValue, _ = self.max_value(s, depth + 1, alpha, beta)
            if sValue < value: value, bestState = sValue, s
            if value <= alpha: break
            beta = min(beta, value)
        return value, bestState

    def generateSuccessors(self, state, piece):
        drop_phase = self.getDropPhase(state)
        successors = []
        if drop_phase:
            # Loop through all rows and cols
            for row in range(5):
                for col in range(5):
                    # Check if current position is empty
                    if state[row][col] == ' ':
                        # Create new state by placing a piece in the empty cell
                        newState = copy.deepcopy(state)
                        newState[row][col] = piece
                        successors.append(newState)
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == piece:
                        # Check all possible directions
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                            # Calculate the new row and col
                            nr, nc = row + dr, col + dc

                            # Check if it is empty and within bounds
                            if 0 <= nr < 5 and 0 <= nc < 5 and state[nr][nc] == ' ':
                                newState = copy.deepcopy(state)
                                newState[nr][nc], newState[row][col] = piece, ' '
                                successors.append(newState)
        return successors

    # Update the board after a move
    def place_piece(self, move, piece):
        if len(move) > 1: self.board[move[1][0]][move[1][1]] = ' '

        self.board[move[0][0]][move[0][1]] = piece
        self.move_count += 1  # Increment the move counter

    # Check game status
    def game_value(self, state):
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # Check diagonal wins (\ direction)
        for i in range(2):
            for j in range(2):
                diag1 = [state[i + k][j + k] for k in range(4)]

                if len(set(diag1)) == 1 and diag1[0] != ' ':
                    return 1 if diag1[0] == self.my_piece else -1

        # Check diagonal wins (/ direction)
        for i in range(2):
            for j in range(2):
                diag2 = [state[4 - i - k][j + k] for k in range(4)]

                if len(set(diag2)) == 1 and diag2[0] != ' ':
                    return 1 if diag2[0] == self.my_piece else -1

        # Check 2x2 box wins
        for i in range(4):
            for j in range(4):
                box = [state[i][j], state[i][j + 1], state[i + 1][j], state[i + 1][j + 1]]

                if len(set(box)) == 1 and box[0] != ' ':
                    return 1 if box[0] == self.my_piece else -1

        # No winner yet
        return 0