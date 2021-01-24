# You have to run the following cmd in your terminal
# pip install windows-curses

import curses, random, time

# teris piece class
class piece:

    # initial piece paramers
    def __init__(self, shape, height, width, rotation):

        self.width = width
        self.height = height
        self.rotation = 0
        self.shape = shape
        self.cleft = 1
        self.cright = 1
        #self.falling = 1

    # draw shape charachter * on screen in set it in screen bits matrix
    def draw(self,py,px,screen,screen_bits):
        # left move
        self.cleft=1
        # right move
        self.cright=1
        # falling move
        self.falling=1

        for h in range(self.height):
            for w in range(self.width):
                # check for value 1 (means * there)
                if self.shape[h][w] == 1:
                    # if rotation is zeore just increase px and py
                    if self.rotation == 0:
                        yt = py + h
                        xt = px + w
                        # if rotation is 1 90 degree the increase y by width
                    elif self.rotation == 1:
                        yt = py + w
                        xt = px + ((self.height-1)-h)
                        # if rotation is 180 degree
                    elif self.rotation == 2:
                        yt = py + ((self.height-1)-h)
                        xt = px + ((self.width-1)-w)
                        # if rotation is 270 degree
                    elif self.rotation == 3:
                        yt = py + ((self.width-1)-w)
                        xt = px + h

                    # draw * for position
                    screen.addstr(yt,xt,"*")

                    if  (yt >= board_height - 1)  or screen_bits[yt][xt-4] == 1:
                        self.falling=0

                    # check if new x
                    elif xt-2 < 0:
                        self.cleft = 0

                    # check if that position is already set to 1
                    elif screen_bits[yt][xt-2]==1:
                        self.cleft = 0

                    # chceck if the piece hit the right side
                    if xt > (board_width - 2): # as there are extra 2 * as per task
                        self.cright = 0

                    # check if the new y TODO
                    elif screen_bits[yt][xt]==1:
                        self.cright = 0

    # update screen bits for the previous piece
    def update_screen_bits(self,py,px,screen_bits):
        for h in range(self.height):
            for w in range(self.width):
                # check if value = 1
                if self.shape[h][w] == 1:
                    # if there is no rotation
                    if self.rotation == 0:
                        try:

                            screen_bits[py+h][px+w] = 1
                        except:
                            tetris_screen.addstr(36,2, "Please enter a valid move")

                    # if it is rotated 90 degree
                    elif self.rotation == 1:
                        try:

                            screen_bits[py+w][px+((self.height-1)-h)]=1
                        except:
                            tetris_screen.addstr(36,2, "Please enter a valid move")

                    # if it rotated 180 degree
                    elif self.rotation == 2:

                        try:

                            screen_bits[py+((self.height-1)-h)][px+((self.width-1)-w)]=1
                        except:
                            tetris_screen.addstr(36,2, "Please enter a valid move")
                    # if it is rotated 270
                    elif self.rotation == 3:
                        try:
                            screen_bits[py+((self.width-1)-w)-1][px+h]=1
                        except:
                            tetris_screen.addstr(36,2, "Please enter a valid move")

        return screen_bits

    # turn peice clock wise
    def turn_c(self,screen_bits):
        overlap=0
        # do one rotation clockwise
        self.rotation = self.rotation + 1
        if self.rotation > 3:
            tetris_screen.addstr(39,0, "rotating counter clock wise")
            self.rotation = 0

        # check if there is overlap
        if self.overlap(screen_bits):
            # reset the ortation to original and ignore that rotation
            self.rotation = self.rotation - 1
            if self.rotation < 0:
                self.rotation=3
            # set valid move to false to let user know
            self.valid_move = False


    # turn piece aginast clockwise
    def turn_ac(self,screen_bits):
        # do one rotation against clock wise
        self.rotation = self.rotation - 1
        if self.rotation < 0:
            tetris_screen.addstr(39,0, "rotating - clock wise")
            self.rotation = 3

        # check overlap
        if self.overlap(screen_bits):
            tetris_screen.addstr(36,2, "Please enter a valid move")
            self.rotation = self.rotation - 1
            if self.rotation > 3:
                self.rotation = 0



    # checking overlap function
    def overlap(self,screen_bits):
        ovl=0
        for h in range(self.height):
            for w in range(self.width):
                if self.shape[h][w] == 1:
                    # if rortation is 0
                    if self.rotation == 0:
                        yt = py + h
                        xt = px + w
                    # check if rotation is 90 degree
                    elif self.rotation==1:
                        yt = py + w
                        xt = px + ((self.height-1)-h)
                    # check if rotation is 180 degree
                    elif self.rotation == 2:
                        yt = py + ((self.height-1)-h)
                        xt = px + ((self.width-1)-w)
                    # check if rotation is 270 degree
                    elif self.rotation == 3:
                        yt = py + ((self.width-1)-w)
                        xt = px + h
                    if xt-4 < 0:
                        ovl=1
                    # check if it overlab with tetris board lines
                    elif xt - 4 > board_width - 1:
                        ovl = 1
                    # check if it overlap with any prvious piece
                    elif screen_bits[yt][xt-4] == 1:
                        ovl = 1
        return ovl


#################### initialize 5 pieces ##########################

# list of 5 pieces
pieces = []

# piece 1 definition ( Shape, height of piece, width of piece, initial rotation/direction of piece)
piece_1 = piece([[1,1,1,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]],1,4,1)
pieces.append(piece_1)

# piece 1 definition
piece_2 = piece([[0,1,1,0],[1,1,0,0],[0,0,0,0],[0,0,0,0]],2,3,1)
pieces.append(piece_2)

# piece 1 definition
piece_3 = piece([[1,1,1,0],[0,0,1,0],[0,0,0,0],[0,0,0,0]],2,3,1)
pieces.append(piece_3)

# piece 1 definition
piece_4 = piece([[1,1,0,0],[1,1,0,0],[0,0,0,0],[0,0,0,0]],2,2,1)
pieces.append(piece_4)

# piece 1 definition
piece_5 = piece([[1,1,1,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]],2,3,1)
pieces.append(piece_5)

# board is 20 x 20
board_width = 20
board_height = 20

# put play margine from top = 3
playfield_y_margin = 0
playfield_x_margin = 0

# function to draw play field
def draw_playfield():
    str = ' ' * board_width
    str = "*" + str + "*"
    for n in range(playfield_y_margin , board_height):
        tetris_screen.addstr(n, playfield_x_margin ,str)
    str = "*" * (board_width + 2)  # gives 20 *
    tetris_screen.addstr(board_height, playfield_x_margin, str)

# initialize the curses screen
tetris_screen = curses.initscr()
curses.noecho()
curses.curs_set(0)

# initialize random piece
piece = random.choice(pieces)
# print(piece)
# flag to exit the Tetris game
exit=0

while exit != 1:
    # piece number
    n=0
    # position x of the piece in the grid, initially 8
    px = 10
    # position y of initially at the top
    py = 0
    # number of points collected
    points=0
    # bits representation of the play field
    screen_bits = [[0] * board_width for _ in range(board_height)]

    # set base line = *
    screen_bits[board_height-1] = [1] * board_width
    # cause certain 50ms delay
    curses.halfdelay(1)
    t = time.time()
    while 1:
        # request user input
        input = tetris_screen.getch()
        # user exit the game
        if input == ord('q'):
            break
        # use alter piece counter clock wise
        elif input == ord('w'):
            piece.turn_c(screen_bits)
            py = py + 1
        # user moved piece left
        elif input == ord('a'):
            # deduct 1 from x position
            px = px - piece.cleft
            py = py + 1
        # user moved right
        elif input == ord('d'):
            # increas position x by 1
            px = px + piece.cright
            py = py + 1
        elif input == ord('s'):
            piece.turn_ac(screen_bits)
            py = py + 1

        # draw the play field
        draw_playfield()

        # after that start drawing the piece shape in the play field
        try:
            piece.draw(py,px,tetris_screen,screen_bits)
        except:
            break
        #
        #
        for j in range(board_height):
            for i in range(board_width):
                if screen_bits[j][i] == 1:
                    tetris_screen.addstr(j,i,"*")

        if piece.falling==0:

            screen_bits = piece.update_screen_bits(py,px,screen_bits)
            # rest position of x & y for the new comoing piece
            px = 10
            py = 0

            # new random piece
            piece = random.choice(pieces)
            # check if there is overlap
            if piece.overlap(screen_bits):
                break
        # move piece down
        py = py + 0
        #fall_temp = not piece.falling

        # reset the play field
        for j in range(board_height):
            if screen_bits[j] == [1] * board_width:
                for k in range(j,0,-1):
                    screen_bits[k] = screen_bits[k-1]
                    screen_bits[0] = [0] * board_width

        tetris_screen.addstr(23, 0, "Please enter a valid move")
        tetris_screen.addstr(24, 0, "a (return): move piece left")
        tetris_screen.addstr(25, 0, "d (return): move piece right")
        tetris_screen.addstr(26, 0, "w (return): rotate piece counter clockwise")
        tetris_screen.addstr(27, 0, "s (return): rotate piece clockwise")

        tetris_screen.addstr(29, 0, "---- Log ---")


    while 1:
        input = tetris_screen.getch()
        if input == ord('q'):
            exit = 1
            break
        elif input == ord('p'):
            break
    tetris_screen.refresh()

curses.echo()
curses.endwin()
