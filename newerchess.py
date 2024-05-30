import pygame
import os
import pyautogui

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def match(self,list_pos):
        pass
    def __str__(self):
        return (f'({self.row} ,{self.col})')
    def __eq__(self,other):
        if self.row == other.row and self.col == other.col:
            return True
        return False


class Piece:
    def __init__(self, color, board, position=None):
        self.color = color
        self.board = board
        self.has_moved = False 
        self.position = position
        # self.move_logs= False
    def possible_moves(self):
        pass
    def move(self,end_pos):
        moves = self.possible_moves()
        # print(*moves)
        for move in moves:
            if end_pos.row == move.row and end_pos.col == move.col:
                return True
        return False
    def __str__(self):
        pass
    
class King(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "king"
        
    def possible_moves(self):
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                   (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        # Castling
        if not self.board.board[self.position.row][self.position.col].has_moved:
            # Check kingside castling
            if self.board.board[self.position.row][7] and not self.board.board[self.position.row][7].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(self.position.col + 1, 7)):
                    moves.append(Position(self.position.row, self.position.col + 2))
            # Check queenside castling
            if  self.board.board[self.position.row][0] and not self.board.board[self.position.row][0].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(1, self.position.col)):
                    moves.append(Position(self.position.row, self.position.col - 2))
        return moves
    def __str__(self):
        if self.color == "White":
            return "K"
        return "k" 
class Bishop(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "bishop"
    def possible_moves(self):
        moves = []
        directions = [(1,1) , (-1 , -1) , (1,-1) , (-1,1)]
        for direction in directions:
            for i in range(1,8):
                new_pos = Position(self.position.row + direction[0]*i , self.position.col + direction[1]*i)
                if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                    moves.append(new_pos)
                if self.board.is_inside_board(new_pos) and not self.board.is_square_empty(new_pos):
                    break
        return moves
    def __str__(self):
        if self.color == "White":
            return "B"
        return "b" 

class Pawn(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "pawn"
        self.move_logs = []
        self.en_passan_direction = None
        # self.using_en_passan = False
        # self.on_steps = []
        # self.two_step_move = False
        # self.possibility_for_
    def possible_moves(self):
        moves = []
        offsets = []
        direction = 1 if self.color == "White" else -1
        start_row = 1 if self.color == "White" else 6
        if direction == 1:
            offsets = [(1,0)]
            if self.position.row==1:
                offsets.append((2,0))
        else:
            offsets = [(-1,0)]
            if self.position.row==6:
                offsets.append((-2,0))
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos)):
                moves.append(new_pos)
        # Capturing enemy
        enemy_capturing = ((1,1) ,(1,-1))
        if direction == 1:
            for dr, dc in enemy_capturing:
                new_pos = Position(self.position.row + dr, self.position.col + dc)
                if self.board.is_inside_board(new_pos) and not self.board.is_square_empty(new_pos):
                    if (self.board.is_enemy_piece(new_pos , self.color)):
                        moves.append(new_pos)
            if self.en_passan_direction == "right":
                moves.append(Position(self.position.row+1 ,self.position.col+1))
            elif self.en_passan_direction == "left":
                moves.append(Position(self.position.row+1 , self.position.col-1))
            elif self.en_passan_direction == "both":
                moves.append(Position(self.position.row+1 ,self.position.col+1))
                moves.append(Position(self.position.row+1 , self.position.col-1))
                
        # Capturing enemy            
        else:
            enemy_capturing = ((-1,1) , (-1,-1))
            for dr, dc in enemy_capturing:
                new_pos = Position(self.position.row + dr, self.position.col + dc)
                if self.board.is_inside_board(new_pos) and not self.board.is_square_empty(new_pos):
                    if (self.board.is_enemy_piece(new_pos , self.color)):
                        moves.append(new_pos)
            # possible moves for en passan
            if self.en_passan_direction == "right":
                moves.append(Position(self.position.row-1 ,self.position.col+1))
            elif self.en_passan_direction == "left":
                moves.append(Position(self.position.row-1 , self.position.col-1))
            elif self.en_passan_direction == "both":
                moves.append(Position(self.position.row-1 ,self.position.col+1))
                moves.append(Position(self.position.row-1 , self.position.col-1))
                
                        
            # print(self.en_passan_direction)
            # if self.en_passan_direction == "right":
            #     moves.append(Position(self.position.row-1 ,self.position.col+1))
            # elif self.en_passan_direction == "left":
            #     moves.append(Position(self.position.row-1 , self.position.col-1))
        return moves
    def __str__(self):
        if self.color == "White":
            return "P"
        return "p" 
class Rook(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "rook"
    def possible_moves(self):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for direction in directions:
            for i in range(1,8):
                new_pos = Position(self.position.row + direction[0]*i , self.position.col + direction[1]*i)
                if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                    moves.append(new_pos)
                if self.board.is_inside_board(new_pos) and not self.board.is_square_empty(new_pos):
                    break
        return moves
    def __str__(self):
        if self.color == "White":
            return "R"
        return "r" 

class Knight(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "knight"
    def possible_moves(self):
        offsets = [(-1,-2) , (-1,2) ,(1,2) , (1,-2) , (2,1) , (2,-1) , (-2 ,1) , (-2,-1)]
        moves = []
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            # print(self.board.is_inside_board(new_pos) ,self.board.is_square_empty(new_pos)  ,  self.board.is_enemy_piece(new_pos, self.color))
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        return moves
    def __str__(self):
        if self.color == "White":
            return "N"
        return "n" 
            
class Queen(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "queen"
    def possible_moves(self):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1) , (1,1) , (-1 , -1) , (1,-1) , (-1,1)]
        for direction in directions:
            for i in range(1,8):
                new_pos = Position(self.position.row + direction[0]*i , self.position.col + direction[1]*i)
                if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                    moves.append(new_pos)
                if self.board.is_inside_board(new_pos) and not self.board.is_square_empty(new_pos):
                    break
        return moves
    def __str__(self):
        if self.color == "White":
            return "Q"
        return "q" 



class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)] #initialize the board
        self.move_logs = []
        self.en_passan_movement = False
    def place_piece(self, piece, position):
        self.board[position.row][position.col] = piece
        piece.position = position

    def remove_piece(self, piece):
        self.board[piece.position.row][piece.position.col] = None

    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos.row][start_pos.col]
        # self.moves_log
        # print("here")
        # print(piece.position)
        # print(piece.en_passan_direction)
        
        
        
        if piece:
            if piece.move(end_pos):
                if type(piece)==Pawn:
                    # Updating move logs for pawn
                    if end_pos.row - start_pos.row == -1:
                        self.board[start_pos.row][start_pos.col].move_logs.append(1)
                    elif end_pos.row - start_pos.row == -2:
                        self.board[start_pos.row][start_pos.col].move_logs.append(2)
                        
                    else:
                        self.board[start_pos.row][start_pos.col].move_logs.append(end_pos.row - start_pos.row)
                        # print(*piece.possible_moves())
                
                
                # detecting en passan move
                    if (end_pos ==piece.possible_moves()[-1] or end_pos ==piece.possible_moves()[-2]) and piece.en_passan_direction != None:
                            print("enPassan")
                            if piece.en_passan_direction == "right":
                                if piece.color == "Black":
                                    self.remove_piece(self.board[start_pos.row][start_pos.col+1])
                                    # print(self.board[start_pos.row][start_pos.col+1])
                                else:
                                    self.remove_piece(self.board[start_pos.row][start_pos.col-1])
                                    # print(self.board[start_pos.row][start_pos.col-1])
                            else:
                                if piece.color == "Black":
                                    # print(self.board[start_pos.row][start_pos.col-1])
                                    self.remove_piece(self.board[start_pos.row][start_pos.col-1])
                                else:
                                    # print(self.board[start_pos.row][start_pos.col+1])
                                    self.remove_piece(self.board[start_pos.row][start_pos.col+1])
                                    
                            self.en_passan_movement = True
                             
                # piece.move_logs.append((start_pos , end_pos))
                # self.move_logs.append({"piece":piece , "from":start_pos , "to": end_pos})
                piece.has_moved = True
                # print("move was valid")
                self.remove_piece(self.board[start_pos.row][start_pos.col])
                
                # self.board[start_pos.row][start_pos.col] = "."
                self.board[end_pos.row][end_pos.col] = piece
                piece.position = end_pos
                # print(piece.position)
                return True
            # print("here")
        else:
            print("No piece at the starting position.")
            return False

    def is_square_empty(self, position):
        return self.board[position.row][position.col] is None

    def is_enemy_piece(self, position, color):
        if self.board[position.row][position.col]!= None and self.board[position.row][position.col]!= ".":
            if self.board[position.row][position.col].color !=color:
                return True
        return False

    def is_inside_board(self, position):
        if position.row <0 or position.row > 7 or position.col <0 or position.col > 7:
            return False
        return True
       
    # def checking_for_en_passant(self):
    def print_board(self):
        print(" | a b c d e f g h")
        print("------------------")
        for i, row in enumerate(self.board):
            row_str = str(i) + "| "
            for piece in row:
                if piece:
                    row_str += f"{piece} "
                else:
                    row_str += ". "
            print(row_str)
        print("\n")






class ChessSet:
    def __init__(self):
        self.board = Board()
        self.setup_board()

    def setup_board(self):
        # Place white pieces
        self.board.place_piece(Rook("White",self.board), Position(0, 0))
        self.board.place_piece(Rook("White",self.board), Position(0, 7))
        self.board.place_piece(Knight("White",self.board), Position(0, 1))
        self.board.place_piece(Knight("White",self.board), Position(0, 6))
        self.board.place_piece(Bishop("White",self.board), Position(0, 2))
        self.board.place_piece(Bishop("White",self.board), Position(0, 5))
        self.board.place_piece(Queen("White",self.board), Position(0, 4))
        self.board.place_piece(King("White",self.board), Position(0, 3))
        for i in range(8):
            self.board.place_piece(Pawn("White" , self.board) , Position(1,i))


        # Place black pieces
        self.board.place_piece(Rook("Black",self.board), Position(7, 0))
        self.board.place_piece(Rook("Black",self.board), Position(7, 7))
        self.board.place_piece(Knight("Black",self.board), Position(7, 1))
        self.board.place_piece(Knight("Black",self.board), Position(7, 6))
        self.board.place_piece(Bishop("Black",self.board), Position(7, 2))
        self.board.place_piece(Bishop("Black",self.board), Position(7, 5))
        self.board.place_piece(Queen("Black",self.board), Position(7, 4))
        self.board.place_piece(King("Black",self.board), Position(7, 3))
        for i in range(8):
            self.board.place_piece(Pawn("Black" , self.board) , Position(6,i))



    def print_board(self):
        self.board.print_board()






class Chess:
    def __init__(self):
        self.start_pos = None
        self.end_pos = None
        self.chess_set = ChessSet()
        self.pieces = [[None for _ in range(8)] for _ in range(8)]
        self.player_is_check  = 0
        self.playerismaking_promotion = 0
        # self.active = False
        # self.root = tk.Tk()

        
    def start_game(self):
        print("Welcome to Chess!\n")
        current_player = "White"
        self.settingUpGui()
        running  = True
        self.putting_pieces()
        while running:
            # checkig for checkmate
            if self.is_checkmate(current_player):
                print("Checkmate")
                if current_player == "Black":
                    pyautogui.alert("White won")
                    return
                    # print("White won")
                else:
                    pyautogui.alert("Black won")
                    return
                    # print("Black won")
            # checking for check
            if self.is_check(current_player):
                self.player_is_check+=1
                if self.player_is_check==1:
                    pyautogui.alert("You  are check")
            # finding possible en passan actions
            self.checkingForEnpassant(current_player)
            # checking for pawn promotion
            results  = self.checkingForPawnPromotion(current_player)
            # if self.checkingForPawnPromotion(current_player):
            if len(results)==2:
                self.playerismaking_promotion+=1
                pos = results[1]
                if self.playerismaking_promotion==1:
                    # asking player to select a piece for promoting pawn
                    pyautogui.alert('''
                    Please Press the number of  piece you want to change your pawn into it:
                        1.Queen
                        2.Rook
                        3.Bishop
                        4.Knight
                                    ''')        
                # self.player_is_check = True

                # self.menumanager.open_menu(InfoBox("message" , [[TextElement(f"{current_player} is check" , (400 , 400))]]))
                # print("Your king is check")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # continuing = False
            # while event.type != pygame.MOUSEBUTTONUP:
            #     if event.type == pygame.MOUSEBUTTONUP:
            #         break
                # detecting mouse click for moves
                if event.type == pygame.MOUSEBUTTONUP:
                    # print(pygame.mouse.get_pos()[1]//73)
                    pos = Position(pygame.mouse.get_pos()[1]//73 , pygame.mouse.get_pos()[0]//73 )
                    self.chekingFormoveInGui(pos , current_player)
                # getting user's choice for pawn promotion
                if event.type == pygame.KEYDOWN:
                    if self.playerismaking_promotion >=1:
                        self.playerismaking_promotion = 0
                        choice = 0         
                        if event.key == pygame.K_1:
                            print("Your choice is Queen")
                            choice = 1
                                
                        if event.key == pygame.K_2:
                            print("Your choice is Rook")
                            choice = 2
                        if event.key == pygame.K_3:
                            print("Your choice is Bishop")
                            choice = 3
                        if event.key == pygame.K_4:
                            print("Your choice is Knight")
                            choice = 4
                        i = pos.row
                        j = pos.col
                        self.chess_set.board.remove_piece(self.chess_set.board.board[pos.row][pos.col])
                        if choice ==1:
                            self.chess_set.board.place_piece(Queen(current_player,self.chess_set.board ), pos)
                            
                        elif choice == 2:
                            self.chess_set.board.place_piece(Rook(current_player,self.chess_set.board ),pos)
                        elif choice ==3:
                            self.chess_set.board.place_piece(Bishop(current_player,self.chess_set.board ), pos)
                        elif choice ==4:    
                            self.chess_set.board.place_piece(Knight(current_player,self.chess_set.board ), pos)
                        else:    
                            print("invalid choice")
                        img = pygame.image.load(f"{os.getcwd()}/oop/assets/{self.chess_set.board.board[i][j].color.lower()} {self.chess_set.board.board[i][j].piece_type.lower()}.png").convert()
                        # print(img.)
                        img = pygame.transform.scale(img , (45,45))
                        self.pieces[pos.row][pos.col]= image_piece(img ,Position(i , j) , self.chess_set.board.board[i][j].color )
                        pygame.display.flip()
            # while not self.start_pos or not self.end_pos:
            #     if self.start_pos and self.end_pos:
            #         break
            
            
                
                        # self.chess_set.board.board = Queen(current_player , self.chess_set.board)
                # if event.type == pygame.KEYDOWN:
                #     if self.checkingForPawnPromotion():
                #         text = ''
                #         if event.key == pygame.K_RETURN:
                #             print(text)
                #             text = ''
                #         elif event.key == pygame.K_BACKSPACE:
                #             text = text[:-1]
                #         else:
                #             text += event.unicode
            # moving pieces with clicking on staer and end positions
            if self.start_pos and self.end_pos:
                copy_piece = self.chess_set.board.board[self.start_pos.row][self.start_pos.col]
                if self.chess_set.board.move_piece(self.start_pos , self.end_pos):
                    # making move for en passan
                    if self.chess_set.board.en_passan_movement:
                        # print("here")
                        # print(copy_piece.en_passan_direction)
                        if copy_piece.en_passan_direction == "right" or copy_piece.en_passan_direction =="left":
                            self.updating_gui_for_en_passan(current_player , copy_piece.en_passan_direction)
                        # if there were both directions possibility in en passan
                        elif copy_piece.en_passan_direction == "both":
                            # print("update_gui for both")
                            if current_player == "Black":
                                if self.start_pos.col >self.end_pos.col:
                                    # print("here")
                                    # print("both right")
                                    self.updating_gui_for_en_passan(current_player ,  "right")
                                else:
                                    self.updating_gui_for_en_passan(current_player , "left")
                                    # print("both left")
                                    
                            else:
                                if self.start_pos.col >self.end_pos.col:
                                    self.updating_gui_for_en_passan(current_player ,  "left")
                                    # print("both right")
                                    
                                else:
                                    self.updating_gui_for_en_passan(current_player , "right")
                                    # print("both left")
                                    
                                
                        self.chess_set.board.en_passan_movement =  False
                    self.movePieceinGui()
                    # print(self.chess_set.board.en_passan_movement)
                    
                    
                    # upgrading pygame gui
                    pygame.display.flip()
                    self.start_pos = None
                    self.end_pos = None
                    # switching turns
                    if current_player =="White":
                        current_player = "Black"
                    else:
                        current_player = "White"
                    # removing check 
                    self.player_is_check=0
            # for item in self.chess_set.board.board[3] + self.chess_set.board.board[4]:
            #     if item:
            #         if item.piece_type == "pawn":
            #             item.en_passan_direction = None
            # upgrading gui
            self.putting_pieces()
            
            
                # print(pos[ , pos[1]//73)
            # self.placing_pieces_in_gui()
            # self.root.mainloop()
            # self.chess_set.print_board()
            # print(f"\n{current_player}'s turn:")
            # start_pos = input("Enter the position of the piece you want to move (e.g., 'a2'): ")
            # end_pos = input("Enter the position to move the piece to (e.g., 'a4'): ")
            # while not self.is_valid_input(start_pos, end_pos):
            #     start_pos = input("Enter the position of the piece you want to move (e.g., 'a2'): ")
            #     end_pos = input("Enter the position to move the piece to (e.g., 'a4'): ")
            # start_pos, end_pos = self.from_algebraic(start_pos) , self.from_algebraic(end_pos)

            # piece = self.chess_set.board.board[start_pos.row][start_pos.col]
            # while piece.color!= current_player or not end_pos in piece.possible_moves():
            #     start_pos = input("Enter the position of the piece you want to move (e.g., 'a2'): ")
            #     end_pos = input("Enter the position to move the piece to (e.g., 'a4'): ")
            #     start_pos, end_pos = self.from_algebraic(start_pos) , self.from_algebraic(end_pos)
            #     piece = self.chess_set.board.board[start_pos.row][start_pos.col]
            # while not self.chess_set.board.move_piece(start_pos, end_pos):
            #     start_pos = input("Enter the position of the piece you want to move (e.g., 'a2'): ")
            #     end_pos = input("Enter the position to move the piece to (e.g., 'a4'): ")
            #     start_pos, end_pos = self.from_algebraic(start_pos) , self.from_algebraic(end_pos)
            #TODO - print the board
            # self.chess_set.board.print_board()
            #self.end_pos.row*73     return
            #TODO - check if the king is in checkmate (much simpler than real-world chess)

            #TODO - check the king is in check
            
            # if current_player == "White":
            #     current_player = "Black"
            # else:
            #     current_player = "White"
            
            
        # quitting the game if exit button is pressed
        pygame.quit()
    # checking for valid mouse clicks
    def chekingFormoveInGui(self , position , currentPlayer):
        piece = self.chess_set.board.board[position.row][position.col]
        if piece and piece!= ".":
            if piece.color == currentPlayer:
                self.start_pos = position
            else:
                if isinstance(self.start_pos , Position):
                    self.end_pos = position
        else:
            if isinstance(self.start_pos , Position):
                self.end_pos = position
    # upgrading gui for moves
    def movePieceinGui(self):
        # # print(self.start_pos , self.end_pos)
        # last_piece = self.pieces[self.end_pos.row][self.end_pos.col]
        self.pieces[self.start_pos.row][self.start_pos.col].position = self.end_pos
        self.pieces[self.end_pos.row][self.end_pos.col] = self.pieces[self.start_pos.row][self.start_pos.col]
        self.pieces[self.start_pos.row][self.start_pos.col] = None
        
        # self.pieces[self.start_pos.row][self.start_pos.col].y = (self.end_pos.col)*73
        # print(self.pieces[self.start_pos.row][self.start_pos.col])
        if self.start_pos.row %2 == 0:
            if self.start_pos.col %2 == 0:
                pygame.draw.rect(self.screen , "black" , rect=(self.start_pos.col*70 , self.start_pos.row*70, 70 , 70 ))
            else:
                pygame.draw.rect(self.screen , "white" , rect=(self.start_pos.col*70 , self.start_pos.row*70, 70 , 70 ))
        else:
            if self.start_pos.col %2 == 0:
                pygame.draw.rect(self.screen , "white" , rect=(self.start_pos.col*70 , self.start_pos.row*70, 70 , 70 ))
            else:
                pygame.draw.rect(self.screen , "black" , rect=(self.start_pos.col*70 , self.start_pos.row*70, 70 , 70 ))
                # self.screen.draw.rect("black" , 
        pygame.display.flip()
        
            
    def is_valid_input(self, start_pos, end_pos):
        if len(start_pos)==2 and len(end_pos)==2 and start_pos[0].isalpha() and end_pos[0].isalpha() and start_pos[1].isdigit() and end_pos[1].isdigit():
            return True
        return False
        

    def is_check(self, current_player):
        flag =False
        pos = None
        # enemy_possible_moves = list()
        for i in range(8):
            for j in range(8):  
                if self.chess_set.board.board[i][j]!= "." and self.chess_set.board.board[i][j] != None:
                    if self.chess_set.board.board[i][j].piece_type == "king" and self.chess_set.board.board[i][j].color== current_player:
                        pos = self.chess_set.board.board[i][j].position
                        flag = True
                        break
            if flag:
                break
        # print(pos)

        for i in range(8):
            for j in range(8):
                # print(self.chess_set.board.board[i][j])
                if self.chess_set.board.board[i][j]!= "." and self.chess_set.board.board[i][j] != None:
                    if self.chess_set.board.board[i][j].color != current_player:
                        if self.chess_set.board.board[i][j].possible_moves()!= None:
                            for item in self.chess_set.board.board[i][j].possible_moves():
                                if item.row == pos.row and item.col == pos.col:
                                    # print(item , self.chess_set.board.board[i][j])
                                    # print("checkedddd")
                                    return True
        # print("not checked")
        return False
                        
        # for item in enemy_possible_moves:
        #     if item.row == pos.row and item.col == pos.col:
        #         return True
        # return False
            
                    

    # def is_checkmate(self, current_player):

    #     flag =False
    #     pos = None
    #     # enemy_possible_moves = list()
    #     for i in range(8):
    #         for j in range(8):  
    #             if self.chess_set.board.board[i][j]!= "." and self.chess_set.board.board[i][j] != None:
    #                 if self.chess_set.board.board[i][j].piece_type == "king" and self.chess_set.board.board[i][j].color== current_player:
    #                     pos = self.chess_set.board.board[i][j].position
    #                     flag = True
    #                     break
    #         if flag:
    #             break
    #     all_enemy_moves = list()
    #     checking= False
    #     for i in range(8):
    #         for j in range(8):
    #             if self.chess_set.board.board[i][j] and self.chess_set.board.board[i][j].color != current_player:
    #                 all_enemy_moves += self.chess_set.board.board[i][j].possible_moves()
    #     # all_enemy_moves = list(set(all_enemy_moves))
    #     # print(*all_enemy_moves)
    #     for item in self.chess_set.board.board[pos.row][pos.col].possible_moves():
    #         if not item in all_enemy_moves:
    #             checking= True
    #             break
    #     if not checking and self.is_check(current_player):
    #         return True
    #     return False
    def is_checkmate(self, current_player):
        # For simplicity, we consider losing the king as checkmate
        enemy = "Black" if current_player == "White" else "White"
        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j]
                if isinstance(piece  , Piece):
                    if piece.piece_type == "king" and piece.color == current_player:
                        return False
        return True
    def from_algebraic(self,algebraic_notation):
        col = ord(algebraic_notation[0]) - ord('a')
        row = int(algebraic_notation[1])
        return Position(row,col)
    # creating game's starting Gui
    def settingUpGui(self):
        pygame.init()
        # print(os.getcwd())
        # pygamepopup.init()
        pygame.display.set_caption('Chess')
        self.screen = pygame.display.set_mode([560, 560])
        # self.menumanager = MenuManager(self.screen)
        # self.screen.fill("red")
        for i in range(8):
            for j in range(8):
                if i%2==0:
                    if j%2 == 0 :
                        pygame.draw.rect(self.screen,"black" , pygame.Rect(70*j, 70*i, 70, 70))
                    else:
                        pygame.draw.rect(self.screen,"white" , pygame.Rect(70*j, 70*i, 70, 70))
                else:
                    if j%2 == 1 :
                        pygame.draw.rect(self.screen,"black" , pygame.Rect(70*j, 70*i, 70, 70))
                    else:
                        pygame.draw.rect(self.screen,"white" , pygame.Rect(70*j, 70*i, 70, 70))
                if isinstance(self.chess_set.board.board[i][j] , Piece):
                    img = pygame.image.load(f"{os.getcwd()}/assets/{self.chess_set.board.board[i][j].color.lower()} {self.chess_set.board.board[i][j].piece_type.lower()}.png").convert()
                    # print(img.)
                    img = pygame.transform.scale(img , (45,45))
                            # print(self.screen.get)
                    # self.pieces.append(image_piece(img ,73*j , 73*i ))
                    self.pieces[i][j]= image_piece(img ,Position(i , j) , self.chess_set.board.board[i][j].color )

                    # self.screen.blit(img ,(73*j , 73*i))
                # btn.configure(bg = "white")
        pygame.display.flip()
    # putting pieces in gui and updating it with our board object
    def putting_pieces(self):
        # x = 0
        # y = 0
        for i in range(8):
            for j in range(8):
                if self.pieces[i][j]:
                    self.screen.blit(self.pieces[i][j].image , (self.pieces[i][j].position.col*70+10 , self.pieces[i][j].position.row*70 + 10 ))
                    pygame.display.flip() # Updates Gui
    def checkingForPawnPromotion(self , currentplayer):
        if  currentplayer == "Black":
            for piece in self.chess_set.board.board[0]:
                if piece and piece.piece_type == "pawn" and piece.color == "Black"  :
                    return True , piece.position
        else:
            for piece in self.chess_set.board.board[-1]:
                if piece and piece.piece_type == "pawn" and piece.color == "White"  :
                    return [True, piece.position]
        return [False]

    def checkingForEnpassant(self , currentplayer):
        # my_piece_is_able = False
        # enemy_piece_is_able = False
        pos = None
        if currentplayer == "Black":
            for piece in self.chess_set.board.board[3]:
                if piece: 
                    if piece.piece_type == "pawn" and piece.en_passan_direction != None:
                        piece.en_passan_direction =None
                        break
                if piece and piece.piece_type == "pawn" and piece.color=="Black" and piece.move_logs[-1]==1 and piece.move_logs[-2]==1 and piece.move_logs[-3]==1 and piece.en_passan_direction == None:          
                    pos = piece.position
                    # print(pos)
                    # if self.chess_set.board.board[3][pos.col+1] and self.chess_set.board.board[3][pos.col-1]:
                    #     if self.chess_set.board.board[3][pos.col+1].piece_type == "pawn" and self.chess_set.board.board[3][pos.col+1].color == "White" and self.chess_set.board.board[3][pos.col+1].move_logs[-1]==2 and self.chess_set.board.board[3][pos.col-1].piece_type == "pawn" and self.chess_set.board.board[3][pos.col-1].color == "White" and self.chess_set.board.board[3][pos.col-1].move_logs[-1]==2:
                    #         piece.en_passan_direction = "Both"
                    if self.chess_set.board.board[3][pos.col+1] and self.chess_set.board.board[3][pos.col-1]:
                        if self.chess_set.board.board[3][pos.col+1].piece_type == "pawn" and self.chess_set.board.board[3][pos.col+1].color == "White" and self.chess_set.board.board[3][pos.col+1].move_logs[-1]==2 and self.chess_set.board.board[3][pos.col-1].piece_type == "pawn" and self.chess_set.board.board[3][pos.col-1].color == "White" and self.chess_set.board.board[3][pos.col-1].move_logs[-1]==2 and piece.en_passan_direction == None:
                            piece.en_passan_direction = "both"
                            # print("detects both")
                            return
                    elif self.chess_set.board.board[3][pos.col+1]:
                        if self.chess_set.board.board[3][pos.col+1].piece_type == "pawn" and self.chess_set.board.board[3][pos.col+1].color == "White" and self.chess_set.board.board[3][pos.col+1].move_logs[-1]==2 and piece.en_passan_direction == None:
                            piece.en_passan_direction = "right"
                            # print("detects right")
                            return
                            
                    elif self.chess_set.board.board[3][pos.col-1]:
                        if self.chess_set.board.board[3][pos.col-1].piece_type == "pawn" and self.chess_set.board.board[3][pos.col-1].color == "White" and self.chess_set.board.board[3][pos.col-1].move_logs[-1]==2 and piece.en_passan_direction == None:
                            piece.en_passan_direction = "left"
                            # print("detects left")
                            return
                            
                            
        else:
            for piece in self.chess_set.board.board[4]:
                if piece: 
                    if piece.piece_type == "pawn" and piece.en_passan_direction != None:
                        piece.en_passan_direction =None
                        break
                if piece and piece.piece_type == "pawn" and piece.color=="White" and piece.move_logs[-1]==1 and piece.move_logs[-2]==1 and piece.move_logs[-3]==1 and piece.en_passan_direction == None:          
                    pos = piece.position
                    # print("fine")
                    # if pos.col+1<8:
                    # if self.chess_set.board.board[4][pos.col+1] and self.chess_set.board.board[4][pos.col-1]:
                    #     if
                    if self.chess_set.board.board[4][pos.col+1] and self.chess_set.board.board[4][pos.col-1]:
                        if self.chess_set.board.board[4][pos.col+1].piece_type == "pawn" and self.chess_set.board.board[4][pos.col+1].color == "Black" and self.chess_set.board.board[4][pos.col+1].move_logs[-1]==2 and self.chess_set.board.board[4][pos.col-1].piece_type == "pawn" and self.chess_set.board.board[4][pos.col-1].color == "Black" and self.chess_set.board.board[4][pos.col-1].move_logs[-1]==2 and piece.en_passan_direction == None:
                            piece.en_passan_direction = "both"
                            # print("detects both")
                            return
                            
                            
                    if self.chess_set.board.board[4][pos.col+1]:
                            # print(self.chess_set.board.board[4][pos.col+1].piece_type , self.chess_set.board.board[4][pos.col+1].color , self.chess_set.board.board[4][pos.col+1].move_logs[-1] )
                        if self.chess_set.board.board[4][pos.col+1].piece_type == "pawn" and self.chess_set.board.board[4][pos.col+1].color == "Black" and self.chess_set.board.board[4][pos.col+1].move_logs[-1]==2 and piece.en_passan_direction == None:
                            piece.en_passan_direction = "right"
                            # print("detects right")
                            return
                            
                            
                    # if pos.col-1>=0:
                    if self.chess_set.board.board[4][pos.col-1]:
                        if self.chess_set.board.board[4][pos.col-1].piece_type == "pawn" and self.chess_set.board.board[4][pos.col-1].color == "Black" and self.chess_set.board.board[4][pos.col-1].move_logs[-1]==2 and piece.en_passan_direction == None:
                            piece.en_passan_direction = "left"
                            # print("detects left")
                            return
                  
                            
                            
            
    def updating_gui_for_en_passan(self , current_player , direction):
        j = 0
        i = self.start_pos.row 
        if current_player == "Black":
            if direction == "right":
                self.pieces[self.start_pos.row][self.start_pos.col+1] = None
                # self.chess_set.board.remove_piece(self.chess_set.board.board[self.start_pos.row][self.start_pos.col-1])
                j = self.start_pos.col+1
                
            else:
                self.pieces[self.start_pos.row][self.start_pos.col-1] = None
                # self.chess_set.board.remove_piece(self.chess_set.board.board[self.start_pos.row][self.start_pos.col+1])
                
                j = self.start_pos.col-1

        else:
            if direction == "right":
                j = self.start_pos.col-1
                # self.chess_set.board.remove_piece(self.chess_set.board.board[self.start_pos.row][self.start_pos.col+1])
                
                self.pieces[self.start_pos.row][self.start_pos.col+1] = None
                
            else:
                j = self.start_pos.col+1
                # self.chess_set.board.remove_piece(self.chess_set.board.board[self.start_pos.row][self.start_pos.col-1])
                
                self.pieces[self.start_pos.row][self.start_pos.col-1] = None
        # i+=1
        # j+=1
        # print(self.pieces[i][j])
        if i%2==0:
            if j%2 == 0 :
                pygame.draw.rect(self.screen , "black" , rect=(j*70 , i*70, 70 , 70 ))
                # print(self.pieces[i][j])
                
                # pygame.draw.rect(self.screen,"black" , pygame.Rect(70*i, 70*j, 70, 70))
            else:
                pygame.draw.rect(self.screen , "white" , rect=(j*70 , i*70, 70 , 70 ))
                # print("debugging black")
                
                
                # pygame.draw.rect(self.screen,"white" , pygame.Rect(70*i, 70*j, 70, 70))
        else:
            if j%2 == 1 :
                pygame.draw.rect(self.screen , "black" , rect=(j*70 , i*70, 70 , 70 ))
                # print(self.pieces[i][j])

                # pygame.draw.rect(self.screen,"black" , pygame.Rect(70*i, 70*j, 70, 70))
            else:
                pygame.draw.rect(self.screen , "white" , rect=(j*70 , i*70, 70 , 70 ))
                # print("debugging black"
                
                # pygame.draw.rect(self.screen,"white" , pygame.Rect(70*i, 70*j, 70, 70))
        # print(i,j)
        pygame.display.flip()
# this class returns object for gui which have position and image properties
class image_piece():
    def __init__(self , image ,position ,color) :
        self.image = image
        self.position = position
        self.color = color
    def __str__(self) -> str:
        return f"{self.image} , {self.position.row} , {self.position.col}"
if __name__ == "__main__":
    chess_game = Chess()
    chess_game.start_game()




