import tkinter as tk
import colors as c
import random as rand

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")

        self.main_grid = tk.Frame(
            self, bg=c.GRIDCOLOR, bd=3, width=600, height=600
        )
        self.main_grid.grid(pady=(100,0))
        self.makeGUI()
        self.start_game()
        self.master.bind("<Left>",self.left)
        self.master.bind("<Right>",self.right)
        self.master.bind("<Up>",self.up)
        self.master.bind("<Down>",self.down)
        self.mainloop()
        
    def makeGUI(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg = c.EMPTYCOLOR,
                    width = 150,
                    height = 150
                )
                cell_frame.grid(row=i,column=j,padx=5,pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTYCOLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5,y=45,anchor="center")
        tk.Label(
            score_frame,
            text="Score",
            font=c.SCORE_LABEL_FONT
        ).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    def start_game(self):
        self.matrix = [[0] * 4 for _ in range(4)]

        row = rand.randint(0,3) 
        col = rand.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg = c.CELLCOLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELLCOLORS[2],
            fg=c.NUMBERCOLORS[2],
            font=c.CELLFONTS[2],
            text="2"
        )
        while(self.matrix[row][col] != 0):
            row = rand.randint(0,3)
            col = rand.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg = c.CELLCOLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELLCOLORS[2],
            fg=c.NUMBERCOLORS[2],
            font=c.CELLFONTS[2],
            text="2"
        )

        self.score = 0

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix
    
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score += self.matrix[i][j]
            
    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
        self.matrix = new_matrix
    
    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix
        
    def add_new_tile(self):
        row = rand.randint(0,3) 
        col = rand.randint(0,3)
        while(self.matrix[row][col] != 0):
            row = rand.randint(0,3)
            col = rand.randint(0,3)
        self.matrix[row][col] = rand.choice([2,4])

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTYCOLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTYCOLOR,text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELLCOLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELLCOLORS[cell_value],
                        fg=c.NUMBERCOLORS[cell_value],
                        font=c.CELLFONTS[cell_value],
                        text=str(cell_value)
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False
    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False
        
    def left(self,event):
        if self.check("Left"):
            self.stack()
            self.combine()
            self.stack()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()

    def right(self,event):
        if self.check("Right"):
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()

    def up(self,event):
        if self.check("Up"):
            self.transpose()
            self.stack()
            self.combine()
            self.stack()
            self.transpose()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()

    def down(self,event):
        if self.check("Down"):
            self.transpose()
            self.reverse()
            self.stack()
            self.combine()
            self.reverse()
            self.transpose()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()
            
    def check(self, dir):
        if dir == "Right":
            self.reverse()
        elif dir == "Up":
            self.transpose()
        elif dir == "Down":
            self.transpose()
            self.reverse()
        cont = [True, True, True, True]
        for i in range(4):
            x = [self.matrix[i][0], self.matrix[i][1], self.matrix[i][2], self.matrix[i][3]]
            if x.count(0) == 4:
                cont[i] = False
            elif x.count(0) == 3 and x[0] != 0:
                cont[i] = False
            elif x.count(0) == 2 and x[1] != 0 and x[0] != 0 and x[1] != x[0]:
                cont[i] = False
            elif x.count(0) == 1 and x[2] != 0 and x[1] != 0 and x[0] != 0 and x[2] != x[1] and x[1] != x[0]:
                cont[i] = False
            elif x[3] != x[2] and x[2] != x[1] and x[1] != x[0] and x.count(0) == 0:
                cont[i] = False
        if dir == "Right" or dir == "Down":
            self.reverse()
        if dir == "Up" or dir == "Down":
            self.transpose()
        return cont.count(True) > 0
        
    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5,rely=0.5,anchor="center")
            tk.Label(
                game_over_frame,
                text="You win!",
                bg=c.WINNERCOLOR,
                fg=c.GAME_OVER_FONTCOLOR,
                font=c.GAME_OVER_FONT
            ).pack()
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5,rely=0.5,anchor="center")
            tk.Label(
                game_over_frame,
                text="Game Over",
                bg=c.LOSERCOLOR,
                fg=c.GAME_OVER_FONTCOLOR,
                font=c.GAME_OVER_FONT
            ).pack()
    
def main():
    Game()

if __name__ == "__main__":
    main()
