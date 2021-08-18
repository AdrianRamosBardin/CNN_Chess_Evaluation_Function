import chess.svg
import numpy as np
import chess
import chess.pgn

#Este file contiene funciones del programa principal que se llama stockfish_data_evaluator

chess_dict = {
    'p' : [1,0,0,0,0,0],
    'P' : [-1,0,0,0,0,0],
    'n' : [0,1,0,0,0,0],
    'N' : [0,-1,0,0,0,0],
    'b' : [0,0,1,0,0,0],
    'B' : [0,0,-1,0,0,0],
    'r' : [0,0,0,1,0,0],
    'R' : [0,0,0,-1,0,0],
    'q' : [0,0,0,0,1,0],
    'Q' : [0,0,0,0,-1,0],
    'k' : [0,0,0,0,0,1],
    'K' : [0,0,0,0,0,-1],
    '.' : [0,0,0,0,0,0],
}

def make_matrix(board): 
    pgn = board.epd()
    foo = []  
    pieces = pgn.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        foo2 = []  
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('.')
            else:
                foo2.append(thing)
        foo.append(foo2)
    return foo

#---------------------------------------------------------------------------------------------------------------------------------------

def board2vec_flat(board):
    matrix_board = make_matrix(board)

    for row_num in range(8):
        for col_num in range(8):
            matrix_board[row_num][col_num] = chess_dict[matrix_board[row_num][col_num]]
    np_matrix_board = np.array(matrix_board)
    flat_matrix_board = np_matrix_board.flatten()
    return(flat_matrix_board)

def board2vec(board):
    matrix_board = make_matrix(board)

    for row_num in range(8):
        for col_num in range(8):
            matrix_board[row_num][col_num] = chess_dict[matrix_board[row_num][col_num]]
    return(matrix_board)    

#---------------------------------------------------------------------------------------------------------------------------------------

def san2list_flatvec(san):
    #Creo lista con todas las boards ordenadas de cada game
    game_boards = []

    board = chess.Board()
    splited_moves = san.split()
    i = 0
    for move in splited_moves:
        try:
            game_boards.append(board2vec_flat(board.copy()))
            board.push_san(move) 
            i = i+1
        except:
            #print(i)
            break
    #Saca una lista con la secuenciua de boards vectorizadas del "san" que tiene como input
    return(game_boards)

def san2list_vec(san):
    #Creo lista con todas las boards ordenadas de cada game
    game_boards = []

    board = chess.Board()
    splited_moves = san.split()
    i = 0
    for move in splited_moves:
        try:
            game_boards.append(board2vec(board.copy()))
            board.push_san(move) 
            i = i+1
        except:
            #print(i)
            break
    #Saca una lista con la secuenciua de boards vectorizadas del "san" que tiene como input
    return(game_boards)


def san2list(san):
    #Creo lista con todas las boards ordenadas de cada game
    game_boards = []

    board = chess.Board()
    splited_moves = san.split()
    i = 0
    for move in splited_moves:
        try:
            game_boards.append(board.copy())
            board.push_san(move)
            i = i+1
        except:
            #print(i)
            break
    #Saca una lista con la secuenciua de boards del "san" que tiene como input
    return(game_boards)
