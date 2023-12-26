import chess
import chess.polyglot
import time

piece_values_midgame = {
        chess.PAWN: 82,
        chess.KNIGHT: 337,
        chess.BISHOP: 365,
        chess.ROOK: 477,
        chess.QUEEN: 1025,
        chess.KING: 0
    }

piece_values_endgame = {
        chess.PAWN: 94,
        chess.KNIGHT: 281,
        chess.BISHOP: 297,
        chess.ROOK: 512,
        chess.QUEEN: 936,
        chess.KING: 0
    }

piece_square_tables_midgame = {
    chess.PAWN:
    [
0,  0,  0,  0,  0,  0,  0,  0,
-11,  34,  126,  68,  95,  61,  134,  98,
-20,  25,  56,  65,  31,  26,  7,  -6,
-23,  17,  12,  23,  21,  6,  13,  -14,
-25,  10,  6,  17,  12,  -5,  -2,  -27,
-12,  33,  3,  3,  -10,  -4,  -4,  -26,
-22,  38,  24,  -15,  -23,  -20,  -1,  -35,
0,  0,  0,  0,  0,  0,  0,  0
    ],

    chess.KNIGHT:
    [
-107,  -15,  -97,  61,  -49,  -34,  -89,  -167,
-17,  7,  62,  23,  36,  72,  -41,  -73,
44,  73,  129,  84,  65,  37,  60,  -47,
22,  18,  69,  37,  53,  19,  17,  -9,
-8,  21,  19,  28,  13,  16,  4,  -13,
-16,  25,  17,  19,  10,  12,  -9,  -23,
-19,  -14,  18,  -1,  -3,  -12,  -53,  -29,
-23,  -19,  -28,  -17,  -33,  -58,  -21,  -105,
    ],

    chess.BISHOP:
    [
-8,  7,  -42,  -25,  -37,  -82,  4,  -29,
-47,  18,  59,  30,  -13,  -18,  16,  -26,
-2,  37,  50,  35,  40,  43,  37,  -16,
-2,  7,  37,  37,  50,  19,  5,  -4,
4,  10,  12,  34,  26,  13,  13,  -6,
10,  18,  27,  14,  15,  15,  15,  0,
1,  33,  21,  7,  0,  16,  15,  4,
-21,  -39,  -12,  -13,  -21,  -14,  -3,  -33,
    ],

    chess.ROOK:
    [
43,  31,  9,  63,  51,  32,  42,  32,
44,  26,  67,  80,  62,  58,  32,  27,
16,  61,  45,  17,  36,  26,  19,  -5,
-20,  -8,  35,  24,  26,  7,  -11,  -24,
-23,  6,  -7,  9,  -1,  -12,  -26,  -36,
-33,  -5,  0,  3,  -17,  -16,  -25,  -45,
-71,  -6,  11,  -1,  -9,  -20,  -16,  -44,
-26,  -37,  7,  16,  17,  1,  -13,  -19,
    ],

    chess.QUEEN:
    [
45,  43,  44,  59,  12,  29,  0,  -28,
54,  28,  57,  -16,  1,  -5,  -39,  -24,
57,  47,  56,  29,  8,  7,  -17,  -13,
1,  -2,  17,  -1,  -16,  -16,  -27,  -27,
-3,  3,  -4,  -2,  -10,  -9,  -26,  -9,
5,  14,  2,  -5,  -2,  -11,  2,  -14,
1,  -3,  15,  8,  2,  11,  -8,  -35,
-50,  -31,  -25,  -15,  10,  -9,  -18,  -1,
    ],

    chess.KING:
    [
13,  2,  -34,  -56,  -15,  16,  23,  -65,
-29,  -38,  -4,  -8,  -7,  -20,  -1,  29,
-22,  22,  6,  -20,  -16,  2,  24,  -9,
-36,  -14,  -25,  -30,  -27,  -12,  -20,  -17,
-51,  -33,  -44,  -46,  -39,  -27,  -1,  -49,
-27,  -15,  -30,  -44,  -46,  -22,  -14,  -14,
8,  9,  -16,  -43,  -64,  -8,  7,  1,
14,  24,  -28,  -44,  -54,  12,  36,  -15,
    ],

}

piece_square_tables_endgame = {
    chess.PAWN:
    [
0,  0,  0,  0,  0,  0,  0,  0,
187,  165,  132,  147,  134,  158,  173,  178,
84,  82,  53,  56,  67,  85,  100,  94,
17,  17,  4,  -2,  5,  13,  24,  32,
-1,  3,  -8,  -7,  -7,  -3,  9,  13,
-8,  -1,  -5,  0,  1,  -6,  7,  4,
-7,  2,  0,  13,  10,  8,  8,  13,
0,  0,  0,  0,  0,  0,  0,  0,
    ],

    chess.KNIGHT:
    [
-99,  -63,  -27,  -31,  -28,  -13,  -38,  -58,
-52,  -24,  -25,  -9,  -2,  -25,  -8,  -25,
-41,  -19,  -9,  -1,  9,  10,  -20,  -24,
-18,  8,  11,  22,  22,  22,  3,  -17,
-18,  4,  17,  16,  25,  16,  -6,  -18,
-22,  -20,  -3,  10,  15,  -1,  -3,  -23,
-44,  -23,  -20,  -2,  -5,  -10,  -20,  -42,
-64,  -50,  -18,  -22,  -15,  -23,  -51,  -29,
    ],

    chess.BISHOP:
    [
-24,  -17,  -9,  -7,  -8,  -11,  -21,  -14,
-14,  -4,  -13,  -3,  -12,  7,  -4,  -8,
4,  0,  6,  -2,  -1,  0,  -8,  2,
2,  3,  10,  14,  9,  12,  9,  -3,
-9,  -3,  10,  7,  19,  13,  3,  -6,
-15,  -7,  3,  13,  10,  8,  -3,  -12,
-27,  -15,  -9,  4,  -1,  -7,  -18,  -14,
-17,  -5,  -16,  -9,  -5,  -23,  -9,  -23,
    ],

    chess.ROOK:
    [
5,  8,  12,  12,  15,  18,  10,  13,
3,  8,  3,  -3,  11,  13,  13,  11,
-3,  -5,  -3,  4,  5,  7,  7,  7,
2,  -1,  1,  2,  1,  13,  3,  4,
-11,  -8,  -6,  -5,  4,  8,  5,  3,
-16,  -8,  -12,  -7,  -1,  -5,  0,  -4,
-3,  -11,  -9,  -9,  2,  0,  -6,  -6,
-20,  4,  -13,  -5,  -1,  3,  2,  -9,
    ],

    chess.QUEEN:
    [
20,  10,  19,  27,  27,  22,  22,  -9,
0,  30,  25,  58,  41,  32,  20,  -17,
9,  19,  35,  47,  49,  9,  6,  -20,
36,  57,  40,  57,  45,  24,  22,  3,
23,  39,  34,  31,  47,  19,  28,  -18,
5,  10,  17,  9,  6,  15,  -27,  -16,
-32,  -36,  -23,  -16,  -16,  -30,  -23,  -22,
-41,  -20,  -32,  -5,  -43,  -22,  -28,  -33,
    ],

    chess.KING:
    [
-17,  4,  15,  -11,  -18,  -18,  -35,  -74,
11,  23,  38,  17,  17,  14,  17,  -12,
13,  44,  45,  20,  15,  23,  17,  10,
3,  26,  33,  26,  27,  24,  22,  -8,
-11,  9,  23,  27,  24,  21,  -4,  -18,
-9,  7,  16,  23,  21,  11,  -3,  -19,
-17,  -5,  4,  14,  13,  4,  -11,  -27,
-43,  -24,  -14,  -28,  -11,  -21,  -34,  -53,
    ],

}

def evaluate_board(board):
    midgame = not is_endgame(board)

    if midgame:
        piece_values = piece_values_midgame
        piece_square_tables = piece_square_tables_midgame
    else:
        piece_values = piece_values_endgame
        piece_square_tables = piece_square_tables_endgame

    evaluation = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            sign = 1 if piece.color == chess.WHITE else -1
            piece_type = piece.piece_type

            color = piece.color

            if color == chess.WHITE:
                # Get the piece square value based on midgame or endgame
                square_value = piece_square_tables[piece_type][63 - square]
            else:
                # Get the piece square value based on midgame or endgame
                square_value = piece_square_tables[piece_type][square]

            evaluation += sign * (piece_values[piece_type] + square_value)

    return evaluation


def is_endgame(board):
  # Check if there are no major pieces
  no_major_pieces = (
      sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 0
      and sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 0
      and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 0
      and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 0)
  if no_major_pieces:
    return True

  # Check for two rooks and no queen
  if (sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) == 0
      and sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) <= 1
      and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) == 0
      and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) <= 1):
    return True

  # Check for two queens or less, kings, and no other pieces except pawns
  if (sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) <= 1
      and sum(1 for _ in board.pieces(chess.KNIGHT, chess.WHITE)) == 0
      and sum(1 for _ in board.pieces(chess.BISHOP, chess.WHITE)) == 0
      and sum(1 for _ in board.pieces(chess.ROOK, chess.WHITE)) == 0
      and sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK)) <= 1
      and sum(1 for _ in board.pieces(chess.KNIGHT, chess.BLACK)) == 0
      and sum(1 for _ in board.pieces(chess.BISHOP, chess.BLACK)) == 0
      and sum(1 for _ in board.pieces(chess.ROOK, chess.BLACK)) == 0):
    return True

  # If none of the above conditions are met, return False
  return False

def quiescence_search(board, color, alpha, beta, ply):

    if board.can_claim_draw() or board.is_stalemate() or board.is_insufficient_material():
            return 0

    if board.is_checkmate():
            return -10000+ply
    
    stand_pat = color * evaluate_board(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    # Sort capture moves using MVV-LVA ordering
    capture_moves = [move for move in board.legal_moves if board.is_capture(move)]
    ordered_moves = sorted(capture_moves, key=lambda move: mvv_lva(board, move), reverse=True)

    for move in ordered_moves:
        board.push(move)
        score = -quiescence_search(board, -color, -beta, -alpha, ply+1)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha

def mvv_lva(board, move):

    if board.can_claim_draw() or board.is_stalemate() or board.is_insufficient_material():
            return 0

    if board.is_checkmate():
            return -10000+ply
    
    # Get the piece at the destination square, or None if the square is empty
    to_piece = board.piece_at(move.to_square)

    # Get the piece at the source square, or None if the square is empty
    from_piece = board.piece_at(move.from_square)

    # Calculate MVV-LVA score for a move
    if to_piece is not None and from_piece is not None:
        return piece_values_midgame[to_piece.piece_type] - piece_values_midgame[from_piece.piece_type]
    else:
        # If either square is empty, return a low score
        return -1  # You can adjust this value based on your preferences


def negamax(board, depth, color, alpha, beta, ply, nodes):
    if board.can_claim_draw() or board.is_stalemate() or board.is_insufficient_material():
            return 0, nodes

    if board.is_checkmate():
            return -10000+ply, nodes
        
    if depth == 0 or board.is_game_over():
        return quiescence_search(board, color, alpha, beta, ply+1), nodes

    # Sort legal moves using MVV-LVA ordering
    ordered_moves = sorted(board.legal_moves, key=lambda move: mvv_lva(board, move), reverse=True)

    for move in ordered_moves:
        board.push(move)
        nodes += 1
        value, nodes = negamax(board, depth - 1, -color, -beta, -alpha, ply+1, nodes)
        value = -value
        board.pop()

        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return alpha, nodes


def best_move(board, start_time, max_time, depth):
    if board.turn == chess.WHITE:
        color = 1
    else: 
        color = -1

    alpha = float('-inf')
    beta = float('inf')
    ply = 0
    nodes = 0

    opening_book_path = 'book/komodo.bin'  # Use the .bin file for polyglot
    # Try moves from the opening book first
    with chess.polyglot.open_reader(opening_book_path) as reader:
        for entry in reader.find_all(board):
            move = entry.move
            if move in board.legal_moves:
                return move  # Return a move from the opening book

    best_mv = None

    for current_depth in range(1, depth + 1):
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_time:
            return best_mv  # Exit the function immediately if max_time is reached
        ordered_moves = sorted(
            board.legal_moves,
            key=lambda move: (
                -piece_values_midgame[board.piece_at(move.to_square).piece_type]
                if board.piece_at(move.to_square) is not None else 0,
                -piece_values_midgame[board.piece_at(move.from_square).piece_type]
                if board.piece_at(move.from_square) is not None else 0
            )
        )

        for move in ordered_moves:
            board.push(move)
            nodes += 1
            if board.is_checkmate():
                return move
            eval, nodes = negamax(board, current_depth - 1, -color, -beta, -alpha, ply+1, nodes)
            eval = -eval
            board.pop()

            if eval > alpha:
                alpha = eval
                best_mv = move

        print(f"info depth {current_depth} score cp {alpha} nps {int(nodes/max(0.01, elapsed_time))} time {int(elapsed_time*100)} pv {best_mv.uci()}")

    return best_mv


def calculateMaxTime(remaining_time):
    return remaining_time / 60

DEFAULT_WTIME = 1000000
DEFAULT_BTIME = 1000000

def parse_parameters(line):
    parameters = line.split()[1:]
    wtime, btime = DEFAULT_WTIME, DEFAULT_BTIME

    for i in range(len(parameters)):
        if parameters[i] == "wtime" and i + 1 < len(parameters):
            wtime = float(parameters[i + 1])
        elif parameters[i] == "btime" and i + 1 < len(parameters):
            btime = float(parameters[i + 1])

    return wtime, btime

def play_chess():
    board = chess.Board()
    remaining_time = 1000000

    while True:
        line = input()
        if line == "uci":
            print("id name PyGo")
            print("id author Chess123easy")
            print("uciok")
        elif line == "isready":
            print("readyok")
        elif line.startswith("position startpos"):
            board = chess.Board()
            if "moves" in line:
                _, moves_part = line.split("moves")
                moves = moves_part.strip().split()
                for move in moves:
                    board.push_uci(move)
        elif line.startswith("position fen"):
            _, fen = line.split("fen", 1)
            board.set_fen(fen.strip())
        elif line.startswith("go"):
            wtime, btime = parse_parameters(line)
            remaining_time = wtime / 1000 if board.turn == chess.WHITE else btime / 1000

            start_time = time.time()
            max_time = calculateMaxTime(remaining_time)
            move = best_move(board, start_time, max_time, depth=3).uci()
            print(f"bestmove {move}")
        elif line == "quit":
            break

if __name__ == "__main__":
    play_chess()
