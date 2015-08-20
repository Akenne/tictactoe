#!/bin/python
import random

def available_moves(board):
    zz = 0
    moves = []
    for v in (board):
        if v == "_":
            moves.append(zz)
        zz+=1    
    return moves
    
def get_squares(board, player):
    zz = 0
    moves = []
    for v in (board):
        if v == player:
            moves.append(zz)
        zz+=1    
    return moves
    
def make_move(board, position, player):
    board[position] = player
    
def get_enemy(player):
    if player == 'X':
        return 'O'
    return 'X'

def X_won(board):
    return winner(board) == 'X'

def O_won(board):
    return winner(board) == 'O'

def winner(board):
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])
    for player in ('X', 'O'):
        positions = get_squares(board, player)
        for combo in winning_combos:
            win = True
            for pos in combo:
                if pos not in positions:
                    win = False
            if win:
                return player
    return None

def complete(board):
        if "_" not in board:
            return True
        if winner(board) != None:
            return True
        return False
    
def determine(board, player):
    if get_bot_move(board, player):
        return get_bot_move(board, player)-1
    if len(available_moves(board)) == 7 and len(get_squares(board, get_enemy(player))) == 1 and board[4] == player:
        aaz = get_squares(board, get_enemy(player))
        if 2 in aaz:
            return 0
        else:
            return 2
        
    a = 2 if player == "X" else -2
    choices = []
    if len(available_moves(board)) == 9:
        return 4
    for move in available_moves(board):
        make_move(board, move, player)
        val = alphabeta(board, get_enemy(player), -2, 2)
        make_move(board, move, "_")
        winners = ('X-win', 'Draw', 'O-win')
        if (val < a) and (player == "X") or (val > a) and (player == "O"):
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)
    
def alphabeta(node, player, alpha, beta):
        if complete(node):
            if X_won(node):
                return -1
            elif tied(node):
                return 0
            elif O_won(node):
                return 1
        for move in available_moves(node):
            make_move(node, move, player)
            val = alphabeta(node, get_enemy(player), alpha, beta)
            make_move(node, move, "_")
            if player == 'O':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'O':
            return alpha
        else:
            return beta

def is_winner(board, marker):
    winning_combos = ([6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6])
    for combo in winning_combos:
        if (board[combo[0]] == board[combo[1]] == board[combo[2]] == marker):
            return True
    return False

def empty(board):
    for i in range(0,len(board)):
        if i != "_":
            return False
    return True

def tied(board):
    return complete(board) == True and winner(board) is None

def win(board):
    for i in range(0,len(board)):
        board_copy = board[:]
        board_copy2 = board[:]
        if is_space_free(board_copy, i):
            make_move(board_copy,i,"O")
            if is_winner(board_copy, "O"):
                return True
            make_move(board_copy2,i,"X")
            if is_winner(board_copy2, "X"):
                return True
    return False

def get_bot_move(board, mark):
    if mark == "X":
        umark = "X"
        omark = "O"
    else:
        umark = "O"
        omark = "X"
    for i in range(0,len(board)):
        board_copy = board[:]
        if is_space_free(board_copy, i):
            make_move(board_copy,i,umark)
            if is_winner(board_copy, umark):
                return i+1
            
    for i in range(0,len(board)):
        board_copy = board[:]
        if is_space_free(board_copy, i):
            make_move(board_copy,i,omark)
            if is_winner(board_copy, omark):
                return i+1

def is_space_free(board, index):
    return board[index] == '_'

def make_move(board,index,move):
    board[index] =  move

def cal_first_bids_num(first_player_bids, second_player_bids):
    bids_num = 4;
    same_num = 0;
    for i in range(len(first_player_bids)):
        if(first_player_bids[i] < second_player_bids[i]):
            bids_num += second_player_bids[i]
        elif (first_player_bids[i] > second_player_bids[i]):
            bids_num -= first_player_bids[i]
        else:
            same_num+=1
            if (same_num % 2 == 0):
                bids_num += first_player_bids[i]
            else:
                bids_num -= first_player_bids[i]
    return bids_num

def next_move(player, first_player_bids, second_player_bids, board, move):
    player_num = 0;
    player_num = (cal_first_bids_num(first_player_bids, second_player_bids))  if (player == 'X') else (8 - cal_first_bids_num(first_player_bids, second_player_bids));
    rival_num = 8 - player_num;
    same = 0
    for i in range(len(first_player_bids)):
        if(first_player_bids[i] == second_player_bids[i]):
            same+=1
    tsp = 0 if (player == "X" and same%2==0) or (player== "O" and same%2==1) else 1
    nboard = []
    for i in board:
        for j in i:
            nboard.append(j)
    if move == "PLAY":
        num = determine(nboard, player)
        if num <3:
            print 0, num
        elif num < 6:
            print 1, num-3
        else:
            print 2, num-6
    else:
        if len(first_player_bids) == 2 and nboard[4] == get_enemy(move):
            print 1 + tsp
            return
        if len(first_player_bids) == 0 and player == "O":
            print 2
            return
        if win(nboard):
            print min(player_num, max(rival_num+tsp,1))
        elif player_num > 6:
            print max(rival_num +tsp, 1)
        else:
            print min(1,player_num)
        
        
#gets the id of the player
player = raw_input()

move = raw_input()         #current position of the scotch

first_player_bids = [int(i) for i in raw_input().split()]
second_player_bids = [int(i) for i in raw_input().split()]
board = []

for i in xrange(0, 3):
    board.append(raw_input())

next_move(player, first_player_bids, second_player_bids, board, move)