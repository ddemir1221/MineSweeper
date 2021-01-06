from cmath import rect
from random import randint
from tkinter import *


class Square:
    has_mine = bool(False)
    surrounding_mines = 0
    is_pressed = bool(False)
    visited = bool(False)
    rect
    r = 0
    c = 0
    x = 0
    y = 0

    def __init__(self, has_mine, surrounding_mines, r, c, x, y):
        self.has_mine = has_mine
        self.surrounding_mines = surrounding_mines
        self.r = r
        self.c = c
        self.x = x
        self.y = y


arr = [[Square(bool(False), 0, 0, 0, 0, 0) for i in range(30)] for j in range(16)]


window = Tk()
window.title("MineSweeper")
window.geometry("1050x560+300+150")
window.resizable(False, False)

my_canvas = Canvas(window, width=1050, height=560, bg="white")
my_canvas.pack(padx=0, pady=0)

square_count = 0


def add_square():
    global square_count
    square_count += 1
    if square_count == 381:
        win()
    print(square_count)


def win():
    global win_window
    win_window = Toplevel(window)
    win_window.title("You Win")
    win_window.geometry("300x150+675+250")
    win_window.resizable(False, False)
    lbl = Label(win_window, text="Game Over")
    lbl.pack

    play_again_button = Button(win_window, text="Play Again", command=lambda: [win_window.destroy(), restart()])
    play_again_button.pack()


def lose():
    for r in range(16):
        for c in range(30):
            if arr[r][c].has_mine == bool(True):
                my_canvas.itemconfig(arr[r][c].rect, fill='red')
                my_canvas.create_text(arr[r][c].x + 18, arr[r][c].y + 18, fill="black", font="Arial 20 bold", text="M")
            else:
                my_canvas.itemconfig(arr[r][c].rect, fill='yellow')
                my_canvas.create_text(arr[r][c].x + 18, arr[r][c].y + 18, fill="black", font="Arial 20 bold",
                                      text=arr[r][c].surrounding_mines)
    global lose_window
    lose_window = Toplevel(window)
    lose_window.title("Game Over")
    lose_window.geometry("300x150+675+250")
    lose_window.resizable(False, False)
    lbl = Label(lose_window, text="Game Over")
    lbl.pack

    try_again_button = Button(lose_window, text="Try Again", command=lambda:[lose_window.destroy(), restart()])
    try_again_button.pack()


def restart():
    for i in range(30):
        for j in range(16):
            arr[j][i] = Square(bool(False), 0, 0, 0, 0, 0)
    global square_count
    square_count = 0
    main()


def empty_square_recursion(sq, row, col):
    if sq.visited == bool(True):
        return
    add_square()

    my_canvas.itemconfig(arr[row][col].rect, fill='yellow')
    my_canvas.create_text(sq.x + 18, sq.y + 18, fill="black", font="Arial 20 bold", text=sq.surrounding_mines)

    if sq.surrounding_mines != 0:
        return

    sq.visited = bool(True)



    if row != 15:
        empty_square_recursion(arr[row + 1][col], row + 1, col)  # r+ c
        if col != 29:
            empty_square_recursion(arr[row + 1][col + 1], row + 1, col + 1)  # r+ c+
        if col != 0:
            empty_square_recursion(arr[row + 1][col - 1], row + 1, col - 1)  # r+ c-
    if row != 0:
        empty_square_recursion(arr[row - 1][col], row - 1, col)  # r- c
        if col != 29:
            empty_square_recursion(arr[row - 1][col + 1], row - 1, col + 1)  # r- c+
        if col != 0:
            empty_square_recursion(arr[row - 1][col - 1], row - 1, col - 1)  # r- c-
    if col != 0:
        empty_square_recursion(arr[row][col - 1], row, col - 1)  # r c-
    if col != 29:
        empty_square_recursion(arr[row][col + 1], row, col + 1)  # r c+




def on_click(event):
    col = event.x // 35
    row = event.y // 35

    s = arr[row][col]

    if s.has_mine == bool(True):
        lose()
    else:
        if s.surrounding_mines == 0:
            empty_square_recursion(s, row, col)
        else:
            my_canvas.itemconfig(arr[row][col].rect, fill='yellow')
            my_canvas.create_text(s.x + 18, s.y + 18, fill="black", font="Arial 20 bold", text=s.surrounding_mines)
            add_square()



def on_right_click(event):
    col = event.x // 35
    row = event.y // 35

    s = arr[row][col]
    # my_canvas.itemconfig(rect_list[row][col], fill='yellow')
    my_canvas.create_text(s.x + 18, s.y + 18, fill="black", font="Arial 20 bold", text="F")

    win()


my_canvas.bind('<Button-1>', on_click)
my_canvas.bind('<Button-3>', on_right_click)


def plant_mines():
    mine_count = 0
    while mine_count < 99:
        rand_r = randint(0, 15)
        rand_c = randint(0, 29)
        if arr[rand_r][rand_c].has_mine == bool(False):
            arr[rand_r][rand_c].has_mine = bool(True)
            mine_count += 1

            if rand_c == 0:
                if rand_r == 0:
                    arr[rand_r][rand_c + 1].surrounding_mines += 1
                    arr[rand_r + 1][rand_c].surrounding_mines += 1
                    arr[rand_r + 1][rand_c + 1].surrounding_mines += 1
                if rand_r == 15:
                    arr[rand_r][rand_c + 1].surrounding_mines += 1
                    arr[rand_r - 1][rand_c].surrounding_mines += 1
                    arr[rand_r - 1][rand_c + 1].surrounding_mines += 1
                else:
                    arr[rand_r - 1][rand_c].surrounding_mines += 1
                    arr[rand_r][rand_c + 1].surrounding_mines += 1
                    arr[rand_r + 1][rand_c].surrounding_mines += 1
                    arr[rand_r + 1][rand_c + 1].surrounding_mines += 1
            if rand_c == 29:
                if rand_r == 0:
                    arr[rand_r][rand_c - 1].surrounding_mines += 1
                    arr[rand_r + 1][rand_c].surrounding_mines += 1
                    arr[rand_r + 1][rand_c - 1].surrounding_mines += 1
                if rand_r == 15:
                    arr[rand_r][rand_c - 1].surrounding_mines += 1
                    arr[rand_r - 1][rand_c].surrounding_mines += 1
                    arr[rand_r - 1][rand_c - 1].surrounding_mines += 1
                else:
                    arr[rand_r - 1][rand_c].surrounding_mines += 1
                    arr[rand_r - 1][rand_c - 1].surrounding_mines += 1
                    arr[rand_r][rand_c - 1].surrounding_mines += 1
                    arr[rand_r + 1][rand_c].surrounding_mines += 1
                    arr[rand_r + 1][rand_c - 1].surrounding_mines += 1
            if rand_r == 0:
                if not (rand_c == 0 or rand_c == 29):
                    arr[rand_r][rand_c - 1].surrounding_mines += 1
                    arr[rand_r + 1][rand_c - 1].surrounding_mines += 1
                    arr[rand_r + 1][rand_c].surrounding_mines += 1
                    arr[rand_r + 1][rand_c + 1].surrounding_mines += 1
                    arr[rand_r][rand_c + 1].surrounding_mines += 1
            if rand_r == 15:
                if not (rand_c == 0 or rand_c == 29):
                    arr[rand_r][rand_c - 1].surrounding_mines += 1
                    arr[rand_r - 1][rand_c - 1].surrounding_mines += 1
                    arr[rand_r - 1][rand_c].surrounding_mines += 1
                    arr[rand_r - 1][rand_c + 1].surrounding_mines += 1
                    arr[rand_r][rand_c + 1].surrounding_mines += 1
            if not rand_r == 0 and not rand_r == 15 and not rand_c == 0 and not rand_c == 29:
                arr[rand_r - 1][rand_c - 1].surrounding_mines += 1
                arr[rand_r - 1][rand_c].surrounding_mines += 1
                arr[rand_r - 1][rand_c + 1].surrounding_mines += 1
                arr[rand_r][rand_c - 1].surrounding_mines += 1
                arr[rand_r][rand_c + 1].surrounding_mines += 1
                arr[rand_r + 1][rand_c - 1].surrounding_mines += 1
                arr[rand_r + 1][rand_c].surrounding_mines += 1
                arr[rand_r + 1][rand_c + 1].surrounding_mines += 1


def create_squares():

    size = 35
    for r in range(16):
        for c in range(30):
            x = c * 35
            y = r * 35
            mine = bool(False)
            num = 0
            color = "white"
            if arr[r][c].has_mine == bool(True):
                mine = bool(True)
            if arr[r][c].surrounding_mines == 0 and arr[r][c].has_mine == bool(False):
                color = "blue"

            arr[r][c].x = x
            arr[r][c].y = y
            arr[r][c].r = r
            arr[r][c].c = c

            new_rect = my_canvas.create_rectangle(x, y, x + size, y + size, fill=color)
            arr[r][c].rect = new_rect


def main():

    plant_mines()
    create_squares()
    window.mainloop()


main()
