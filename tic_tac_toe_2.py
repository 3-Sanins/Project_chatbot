from tkinter import *
from threading import *
from tkinter import messagebox

window=Tk()
window.config(bg='blue')

F=Frame(window,height=130,width=20,background='red')
F.config(bg='black')
F.place(relx=0.5,rely=0.5,anchor=CENTER)


board={1:' ',2:' ',3:' ',4:' ',5:' ',6:' ',7:' ',8:' ',9:' '}

def minimax(board,turn):
    if checkwin(u):
        return -10
    elif checkwin(c):
        return 10
    elif checkdraw():
        return 1
        
    if turn:
        score=-100
        for i in board.keys():
            if free(i):
                board[i]=c
                s=minimax(board,False)
                board[i]=' '
                #if s>=10:
#                    return score
                if s>score:
                    score=s
        return score
    
    else:
        score=100
        for i in board.keys():
            if free(i):
                board[i]=u
                s=minimax(board,True)
                board[i]=' '
                
                if s<score:
                    score=s
        return score
    
def g(i):
    return board[i]

def ground():
    print(f'{board[1]} | {board[2]} | {board[3]}')
    print('--+---+--')
    print(f'{board[4]} | {board[5]} | {board[6]}')
    print('--+---+--')
    print(f'{board[7]} | {board[8]} | {board[9]}')
    
def free(index):
    if board[index]==' ':
        return True
    else:
        return False

def insert(index,letter):
    Tkboard[index].config(text=letter)
    board[index]=letter
        
u='X'
c='O'

def uws(index):
    t1=Thread(target=user,args=(index,))
    for i in range(1,10):
        Tkboard[i]['state']=DISABLED
    t1.start()
    return

def us(index):
    
    if Tkboard[index]['text']=='  ':
        Tkboard[index]['text']='X'
        Tkboard[index]['state']=DISABLED
        insert(index,'X')
        fmove()
        
        if checkwin('O'):
            messagebox.showinfo('Game Ends','You LOSE')
            reset()
        if checkwin('X'):
            messagebox.showinfo('Game Ends','You WIN')
            reset()
            # 
        for i in Tkboard.keys():
            if Tkboard[i]['text']=='  ':
            
                
                return
        messagebox.showinfo('Game ends','Its a Draw')
        reset()
        # 
        
    for i in Tkboard.values():
        i.config(state=ACTIVE)

h=1
w=1

Tkboard={
1:Button(F,text='  ',command=lambda:us(1),height=h,width=w,
fg='red',bg='blue',activebackground='blue',font=('Arial',50,'bold'),highlightthickness=0),
2:Button(F,text='  ',command=lambda:us(2),height=h,width=w,
fg='red',bg='blue',activebackground='blue',font=('Arial',50,'bold'),
highlightthickness=0),
3:Button(F,text='  ',command=lambda:us(3),height=h,width=w,
fg='red',bg='blue',activebackground='blue',font=('Arial',50,'bold'),highlightthickness=0),
4:Button(F,text='  ',command=lambda:us(4),height=h,width=w,
fg='red',bg='blue',activebackground='blue',font=('Arial',50,'bold'),highlightthickness=0),
5:Button(F,text='  ',command=lambda:us(5),height=h,width=w,
fg='red',bg='blue',activebackground='blue',font=('Arial',50,'bold'),highlightthickness=0),
6:Button(F,text='  ',command=lambda:us(6),height=h,width=w,
fg='red',bg='blue',activebackground='blue',font=('Arial',50,'bold'),highlightthickness=0),
7:Button(F,text='  ',command=lambda:us(7),height=h,width=w,
fg='red',bg='blue',activebackground='blue',font=('Arial',50,'bold'),highlightthickness=0),
8:Button(F,text='  ',command=lambda:us(8),height=h,width=w,
fg='red',bg='blue',activebackground='blue',font=('Arial',50,'bold'),highlightthickness=0),
9:Button(F,text='  ',command=lambda:us(9),height=h,width=w,
fg='red',bg='blue',activebackground='blue',font=('Arial',50,'bold'),highlightthickness=0),
}



#Tkboard[1].place(x=150,y=290)
Tkboard[1].grid(row=4,column=4,padx=3,pady=5)
Tkboard[2].grid(row=4,column=5,padx=3,pady=5)
Tkboard[3].grid(row=4,column=6,padx=3,pady=5)
Tkboard[4].grid(row=5,column=4)
Tkboard[5].grid(row=5,column=5)
Tkboard[6].grid(row=5,column=6)
Tkboard[7].grid(row=6,column=4,padx=3,pady=5)
Tkboard[8].grid(row=6,column=5,padx=3,pady=5)
Tkboard[9].grid(row=6,column=6,padx=3,pady=5)




def reset():
    for i in range(1,10):
        Tkboard[i]['text']='  '
        board[i]=' '
        Tkboard[i].config(state=ACTIVE)


def move(board):
    best= 0
    score=-100
    for i in board.keys():
        if board[i]==' ':
            board[i]=c
            s=minimax(board,False)
            board[i]=' '
         #   if s>=0:
#                best=i
#                try:
#                    Tkboard[int(best)]['text']='O' 
#                    insert(best,'O')
#                    for i in Tkboard.values():
#                        if i['text']=='  ':
#                            i.config(state=ACTIVE)
#                    nnvbreturn
#                except:
#                    messagebox.showinfo('Game Ends','Its a DRAW')
#                    reset()
#                    break
            if s>score:
                best=i
                score=s
    try:
        Tkboard[int(best)]['text']='O' 
        insert(best,'O')
        for i in Tkboard.values():
            if i['text']=='  ':
                i.config(state=ACTIVE)
    except:
        messagebox.showinfo('Game Ends','Its a DRAW')
        reset()
         


def checkwin(letter):
    if g(1)==g(2)==g(3)==letter:
        return True
    elif g(4)==g(5)==g(6)==letter:
        return True
    elif g(7)==g(8)==g(9)==letter:
        return True
    elif g(1)==g(5)==g(9)==letter:
        return True
    elif g(7)==g(5)==g(3)==letter:
        return True
    elif g(4)==g(1)==g(7)==letter:
        
        return True
    elif g(2)==g(5)==g(8)==letter:
        
        return True
    elif g(3)==g(6)==g(9)==letter:
        
        return True
    else:
        return False

def one(board):
    v=0
    for i in board.values():
        if i=='X' or i=='O':
            v+=1
    if v==1:
        return True # if v==1

def fmove():
    if one(board):
        #sys.exit()
        for i in range(1,10):
            if Tkboard[i]['text']!='  ':
                if i==1 or i==3 or i==7:
                    insert(5,c)
                    return
                elif i==2 or i==4 or i==5 or i==9:
                    insert(1,c)
                    return
                elif i==6:
                    insert(3,c)
                    return
                elif i==8:
                    insert(2,c)
                    return
    else:
        move(board)                



def checkdraw():
    
    for i in board.keys():
        if board[i]==' ':
            return False
   
    return True



window.mainloop()



