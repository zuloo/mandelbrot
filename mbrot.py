import curses
import math
from time import sleep
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

    curses.init_pair(12, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(11, curses.COLOR_BLUE, curses.COLOR_BLACK)
    c_stat = curses.color_pair(12) | curses.A_BOLD | curses.A_REVERSE
    c_stat_div = curses.color_pair(11) | curses.A_BOLD | curses.A_REVERSE

    curses.curs_set(0)
    # set up some dimension variables
    dim = scr.getmaxyx()

    flx = int(math.floor(dim[1]/2))
    fly = int(math.floor(dim[0]/2))
    clx = int(math.ceil(dim[1]/2))
    cly = int(math.ceil(dim[0]/2))
    statscr=curses.newpad(1,dim[1])
    helpscr=curses.newpad(1,dim[1])


    # initial zoom factor (increases accuracy to some extent)
    factor = 100000
    
    # set the base parameters
    step = 1*factor*0.8
    max_i = 100
    cx = -1*factor
    cy = 0

    # set up stats pad
    show_bars = True
    y_range = y_off = None

    while 1:

        # draw the mandelbrot
        if show_bars:
            y_range = range(1-fly,cly)
            y_off = fly+1
        else:
            y_range = range(-fly,cly+1)

        for x in range(-flx, flx):
            for y in y_range:

                iters = iterator(factor, cx+x*step/2, cy+y*step, 4000*factor*factor, max_i)

                if iters >= max_i:
                    char=' '
                    color = 0
                else:
                    char = str(iters%10)
                    color = iters%10

                # mbscr.addstr(y+fly, x+flx, char, curses.color_pair(color+1) | colormode[color])
                if x+flx < dim[1]-1 and y+fly < dim[0]:
                    scr.addstr(fly+y, x+flx, char, curses.color_pair(color+1) | colormode[color])

        # update
        scr.refresh()


        if show_bars:
            # draw the stat
            for x in range(0,dim[1]-1):
                statscr.addstr(0,x,' ',c_stat_div)
                helpscr.addstr(0,x,' ',c_stat_div)
            statscr.addstr(0,0,' X',c_stat_div)
            statscr.addstr(' {:0.5f} '.format(cx/(factor*10)),c_stat)
            statscr.addstr('   Y',c_stat_div)
            statscr.addstr(' {:0.5f} '.format(cy/(factor*10)),c_stat)
            statscr.addstr('   Stepsize',c_stat_div)
            statscr.addstr(' {:0.5e} '.format(step/factor),c_stat)
            statscr.addstr('   Iterations',c_stat_div)
            statscr.addstr(' {} '.format(max_i),c_stat)
            statscr.refresh(0,0,0,0,1,dim[1])

            helpscr.addstr(0,0,' Move', c_stat_div)
            helpscr.addstr(' h,j,k,l ', c_stat)
            helpscr.addstr('[',c_stat_div)
            helpscr.addstr('Shift *10', c_stat)
            helpscr.addstr('] ',c_stat_div)
            helpscr.addstr('   Zoom', c_stat_div)
            helpscr.addstr(' n,p ', c_stat)
            helpscr.addstr('   Quit', c_stat_div)
            helpscr.addstr(' q ', c_stat)
            helpscr.addstr('   Show/Hide', c_stat_div)
            helpscr.addstr(' ?  ', c_stat)
            helpscr.addstr(0,dim[1]-19,' http://unix.porn ',c_stat_div)
            helpscr.refresh(0,0,dim[0]-1,0,dim[0],dim[1])

        # navigation key bindings
        c= scr.getch()
        if c == curses.KEY_RESIZE:
            dim = scr.getmaxyx()
            flx = int(math.floor(dim[1]/2))
            fly = int(math.floor(dim[0]/2))
            clx = int(math.ceil(dim[1]/2))
            cly = int(math.ceil(dim[0]/2))
            statscr=curses.newpad(1,dim[1])
            helpscr=curses.newpad(1,dim[1])
        elif c == ord('q'): break
        elif c == ord('n'): step *= 0.8
        elif c == ord('p'): step *= 1.25
        elif c == ord('h'): cx -= step
        elif c == ord('l'): cx += step
        elif c == ord('k'): cy -= step
        elif c == ord('j'): cy += step
        elif c == ord('H'): cx -= step*10
        elif c == ord('L'): cx += step*10
        elif c == ord('K'): cy -= step*10
        elif c == ord('J'): cy += step*10
        elif c == ord('?'): show_bars = not show_bars
        
        # dynaically adapt iterations
        max_i=max(100,int(math.log(1.0/step,10)*80))

if __name__ == "__main__":
    curses.wrapper(app)

