import cmd
from os import system
import random
import colorama
from colorama import Fore

class OX_cmd(cmd.Cmd):
    print(f"{Fore.WHITE}Choose:\nnew : New Game\nload : Load Game\nquit : Quit\n")
    def do_new(self,arg):
        board=[" "," "," "," "," "," "," "," "," "]
        name=input(f"{Fore.WHITE}Enter your name : ")
        diff=2
        try:
            diff=int(input("Enter Difficulty(1 2 or 3) Difficulty will be set to 2 for invald inputs : "))
        except:
            print(f"{Fore.RED}Invalid input. Taking difficulty level 2 by default")
        turn=random.randint(0,1)
        turn =0
        t=0
        if turn:
            print(f"{Fore.YELLOW}You win the toss")
        else:
            print(f"{Fore.YELLOW}Computer wins the toss")
        printBoard(board)
        Playgame(board,turn,name,t,diff)

    def do_load(self,arg):
        board=[" "," "," "," "," "," "," "," "," "]
        try:
            ptr=open("SaveGame.txt",'r')
        except:
            print(f"{Fore.RED}Error!!!No previously saved file present.")
            print(f"{Fore.WHITE}")
            exit()
        arr=ptr.read()
        if arr=="":
            print(f"{Fore.RED}Error!!! SaveGame.txt might have been modified. Please delete that file and restart again to create a new file")
            print(f"{Fore.WHITE}")
            exit()
        for i in range (0,9):
            board[i]=arr[i]
        print(f"{Fore.GREEN}Loading Details :-")
        turn=arr[9]
        diff=arr[11]
        name=arr[12:]
        print(f"{Fore.WHITE}Name : %s"%(name))
        print(f"{Fore.WHITE}Difficulty : %s"%(diff))
        t=arr[10]
        printBoard(board)
        if turn:
            print(f"{Fore.WHITE}It was your turn to move")
        Playgame(board,turn,name,(int)(t),(int)(diff))

    def do_quit(self,arg):
        print(f"{Fore.WHITE}Thanks for playing")
        raise SystemExit
    
def printBoard(board):  #print tic tac toe board
    display = '''
    1 | 2 | 3     {} | {} | {}
    ---------    ------------
    4 | 5 | 6     {} | {} | {}
    ---------    ------------
    7 | 8 | 9     {} | {} | {}'''

    print(f"{Fore.WHITE}")
    print(display.format(*board),"\n")

def SaveGame(board,turn,name,t,diff):    #save your game
    ptr=open("SaveGame.txt",'w')
    for i in range (0,9):
        ptr.write("%s"%(board[i]))
    ptr.write("%d%s%d%s"%(int(turn),t,diff,name))

def UserMove(board,turn,name,t,diff):    #Take input from user
    while True:
        n=-1
        try:
            n=input(f"{Fore.WHITE}Enter where u want to move (Enter save to save the game and quit to exit): ")
            if n=="save":
                SaveGame(board,turn,name,t,diff)
                print(f"{Fore.GREEN}Game Saved")
                continue
            if n=="quit":
                w=input(f"{Fore.YELLOW}Are you sure you want to quit?You will lose your data if not saved the game.\nEnter y for yes and anything else for no : ")
                if w.lower()=="y":
                    raise SystemExit
                else:
                    continue
            n=(int)(n)
        except:
            if n=="quit":
                raise SystemExit
            print(f"{Fore.RED}Invalid input")
            continue
        if(n<1 or n>9):
            print("Invalid move")
            continue
        if n>=0 and board[n-1]==" ":
            board[n-1]="X"
        else:
            print(f"{Fore.RED}Position Occupied Already")
            continue
        break

def Case1(board):   #special case to assist compMove method
    count=0
    flag=1
    for i in range (0,9):
        if board[i]=="X":
            count+=1
    if count<=1:
        return True

def CompMove(board,diff):    #logic for computer to move
    if diff==1:
        while True:
            x=random.randint(0,8)
            if(board[x]==" "):
                board[x]="O"
                return
            continue
        
    if Case1(board) and diff==2:
        pos=random.randint(0,8)
        if(board[pos]==" "):
            board[pos]="O"
            return

    if Case1(board) and diff==3:
        h=0
        while h<9:
            if(board[h]==" "):
                board[h]="O"
                return
            h+=2
        for pos in range(0,8):
            if(board[pos]==" "):
                board[pos]="O"
                return

    wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8),(0, 3, 6), (1, 4, 7), (2, 5, 8),(0, 4, 8), (2, 4, 6))
    for i in wins:
        chars = board[i[0]] + board[i[1]] + board[i[2]]
        if chars==" OO":
            board[i[0]]="O"
            return
        if chars=="O O":
            board[i[1]]="O" 
            return
        if chars=="OO ":
            board[i[2]]="O"
            return
    for i in wins:
        chars = board[i[0]] + board[i[1]] + board[i[2]]
        if chars==" XX":
            board[i[0]]="O"
            return
        if chars=="X X":
            board[i[1]]="O" 
            return
        if chars=="XX ":
            board[i[2]]="O"
            return

    for i in range (0,9):
        if board[i]==" ":
            board[i]="O"
            return

def WinMove(board):      #check if someone wins
    wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8),(0, 3, 6), (1, 4, 7), (2, 5, 8),(0, 4, 8), (2, 4, 6))
    for i in wins:
        chars = board[i[0]] + board[i[1]] + board[i[2]]
        if chars == "XXX" or chars == "OOO":
            return True
    return False

def BoardFull(board):   #check if board full
    for i in range (0,9):
        if board[i]==" ":
            return False
    print(f"{Fore.WHITE}It's a tie")
    return True

def Playgame(board,turn,name,t,diff):    #Main logic to play the game
    
    while(t<9):
        if turn:
            UserMove(board,turn,name,t,diff)
            printBoard(board)
            if WinMove(board):
                print(f"{Fore.GREEN}%s Wins"%(name))
                main()
        else:
            print(f"{Fore.CYAN}Computer is moving......")
            CompMove(board,diff)
            printBoard(board)
            if WinMove(board):
                print(f"{Fore.GREEN}Computer Wins")
                main()
        t+=1
        turn= not turn
        BoardFull(board)
def main():
    game=OX_cmd().cmdloop()

main()