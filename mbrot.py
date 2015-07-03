import curses
import math
import cmath

maxy = 0


def iterator(fktr, cx, cy, max_square, max_iter):
    i = x = y = sqx = sqy = 0
    fktr *= 10

    while i <= max_iter and sqx+sqy <= max_square:
        y=(2*x*y)/fktr+cy
        x=(sqx-sqy)/fktr+cx

        sqx=x*x
        sqy=y*y
        i+=1

    return i


def app(scr):

    # set up colors
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(10, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)

    colormode = [
            curses.A_BOLD,
            curses.A_BOLD,
            0,
            0,
            0,
            curses.A_BOLD,
            0,
            0,
            0,
            0
    ]

    # set up some dimension variables
    dim = scr.getmaxyx()

    flx = int(math.floor(dim[1]/2))
    fly = int(math.floor(dim[0]/2))
    clx = int(math.ceil(dim[1]/2))

    # initial zoom factor (increases accuracy to some extent)
    factor = 100000
    
    # set the base parameters
    step=1*factor
    max_i=100
    cx= -1*factor#2.5-dim[1]/2*step
    cy = 0#-dim[0]/2*step

    while 1:
        scr.addstr(dim[0]-1,0,'                                                                               ')
        scr.addstr(dim[0]-1,0,'Pos {:0.4f} : {:0.4f}   step [{:0.5e}]    Move: h,j,k,l    Zoom: n,p'.format(cx/factor/10,cy/factor/10,step/factor,max_i))

        for x in range(-flx, clx):
            for y in range(-fly, fly):

                iters = iterator(factor, cx+x*step/2, cy+y*step, 4000*factor*factor, max_i)

                if iters >= max_i:
                    char=' '
                    color = 0
                else:
                    char = str(iters%10)
                    color = iters%10

                scr.addstr(y+fly, x+flx, char, curses.color_pair(color+1) | colormode[color])

        scr.refresh()

        # navigation key bindings
        c= scr.getch()
        if c == ord('q'):
            break
        elif c == curses.KEY_NPAGE or c in [ord(' '),ord('+'),ord('n')]:
            step *= 0.8
        elif c == curses.KEY_BACKSPACE or c== curses.KEY_PPAGE or c in [ord('-'),ord('p')]:
            step *= 1/0.8
        elif c == curses.KEY_LEFT or c == ord('h'):
            cx -= step
        elif c == curses.KEY_RIGHT or c == ord('l'):
            cx += step
        elif c == curses.KEY_UP or c == ord('k'):
            cy -= step
        elif c == curses.KEY_DOWN or c == ord('j'):
            cy += step

        # dynaically adapt iterations
        max_i=max(100,int(math.log(1.0/step,10)*50))

if __name__ == "__main__":
    curses.wrapper(app)

