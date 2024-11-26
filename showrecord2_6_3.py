from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql as mysql

cn=mysql.Connection(host="localhost",user="root",passwd="admin",database="cricket_project")

cur=cn.cursor()

q="set autocommit=1;"
cur.execute(q)

def show_hts(root,hg):
    hts=Toplevel(root)
    hts.title("Highlights")
    t1=ttk.Treeview(hts,height=18)
    t1["columns"]=("E","s")
    t1.column("#0",width=250,minwidth=150)
    t1.column("s",width=0,minwidth=0)
    t1.column("E",width=100,minwidth=100)

    t1.heading("#0",text="Event",anchor=W)
    t1.heading("s",text="",anchor=W)
    t1.heading("E",text="Ball",anchor=W)
    for i in range(1,len(hg)):
        #print(hg[i][1])
        t1.insert("",i-1,text=hg[i][1],values=(hg[i][0]))
    Label(hts,text="For team "+hg[0]).pack()
    t1.pack()


#root=Tk()
def show(root,scoreboard,balls,six,fours,fpl1,pl1,fpl2=-1,pl2=-1,total_ball=0,iscomputer=False):
    scorecard=Toplevel(root)
    scorecard.title("Score Board")
    if fpl2!=-1:
        if pl1>pl2:
            winner=fpl1
        else:
            winner=fpl2
        man_match=winner[0]
        for player in winner:
            if scoreboard[player]>scoreboard[man_match]:
                man_match=player
            if scoreboard[player]==scoreboard[man_match]:
                if balls[player]==0 or balls[man_match]==0:
                    pass
                elif round((scoreboard[player]/balls[player])*100,2)>(round((scoreboard[man_match]/balls[man_match])*100,2)):
                    man_match=player
        best_player=fpl1[0]
        for batter in scoreboard:
            if scoreboard[batter]>scoreboard[best_player]:
                best_player=batter
            if scoreboard[player]==scoreboard[best_player]:
                if balls[player]==0 or balls[best_player]==0:
                    pass
                elif round((scoreboard[player]/balls[player])*100,2)>(round((scoreboard[best_player]/balls[best_player])*100,2)):
                    best_player=player
        if pl1==pl2:
            man_match=best_player
        Best_player=best_player.partition("__")[0]
        Man_match=man_match.partition("__")[0]
        Label(scorecard,text="Best Player of the Match : "+Best_player,fg="red").pack(anchor="center",side="top")
        Label(scorecard,text="Man of the Match : "+Man_match,fg="blue").pack(anchor="center",side="top")

    
    t1=ttk.Treeview(scorecard,height=8)
    t1["columns"]=("R","SF","B","SR")
    t1.column("#0",width=150,minwidth=150)
    t1.column("R",width=100,minwidth=90)
    t1.column("SF",width=150,minwidth=150)
    t1.column("B",width=150,minwidth=150)
    t1.column("SR",width=150,minwidth=150)


    t1.heading("#0",text="Player name",anchor=W)
    t1.heading("R",text="Runs Scored",anchor=W)
    t1.heading("SF",text="4/6",anchor=W)
    t1.heading("B",text="Balls faced",anchor=W)
    t1.heading("SR",text="Strike Rate",anchor=W)

    s=0
    k=1
    for i in range(1,len(fpl1)+1):
        
        cursc=scoreboard[fpl1[i-1]]
        if cursc==-1:
            cursc=0
        s+=cursc
        if scoreboard[fpl1[i-1]]!=-1:
            #print(balls,balls[fpl1[i-1]])
            if balls[fpl1[i-1]]==0:
                balls[fpl1[i-1]]=1
            t1.insert("",k,text=fpl1[i-1].partition("__")[0],values=(cursc,str(fours[fpl1[i-1]])+"/"+str(six[fpl1[i-1]]),balls[fpl1[i-1]],round((cursc/balls[fpl1[i-1]])*100,2)))
            k+=1
    t1.insert("",k+1,text="-------------------",values=("-------------"))
    t1.insert("",k+2,text="Extras",values=(pl1-s,"",""))
    t1.insert("",k+3,text="Net Total",values=(pl1))

    Label(scorecard,text=fpl1[0]+"'s Team Scorecard").pack()
    t1.pack()

    if fpl2==-1:
        Button(scorecard,text="Proceed",command=scorecard.destroy).pack()
        return
    
    t2=ttk.Treeview(scorecard,height=8)
    t2["columns"]=("R","SF","B","SR")
    t2.column("#0",width=150,minwidth=150)
    t2.column("R",width=100,minwidth=90)
    t2.column("SF",width=150,minwidth=150)
    t2.column("B",width=150,minwidth=150)
    t2.column("SR",width=150,minwidth=150)

    t2.heading("#0",text="Player name",anchor=W)
    t2.heading("R",text="Runs Scored",anchor=W)
    t2.heading("SF",text="4/6",anchor=W)
    t2.heading("B",text="Balls faced",anchor=W)
    t2.heading("SR",text="Strike Rate",anchor=W)

    s=0
    k=1
    for i in range(1,len(fpl2)+1):
        cursc=scoreboard[fpl2[i-1]]
        if cursc==-1:
            cursc=0
        s+=cursc
        if scoreboard[fpl2[i-1]]!=-1:
            
            if balls[fpl2[i-1]]==0:
                balls[fpl2[i-1]]=1
            t2.insert("",k,text=fpl2[i-1].partition("__")[0],values=(cursc,str(fours[fpl2[i-1]])+"/"+str(six[fpl2[i-1]]),balls[fpl2[i-1]],round((cursc/balls[fpl2[i-1]])*100,2)))
            k+=1
    t2.insert("",k+1,text="-------------------",values=("-------------"))
    t2.insert("",k+2,text="Extras",values=(pl2-s,"",""))
    t2.insert("",k+3,text="Net Total",values=(pl2))

    Label(scorecard,text=fpl2[0]+"'s Team Scorecard").pack()
    t2.pack()

    Button(scorecard,text="Exit",command=root.destroy).pack(side="left")
    storedata(six,fours,balls,scoreboard,fpl1,fpl2,pl1,pl2,total_ball,iscomputer)
    if iscomputer:
        Button(scorecard,text="Records",command=lambda:show_records(root,fpl1,[])).pack(side="right")
    else:
        Button(scorecard,text="Records",command=lambda:show_records(root,fpl1,fpl2)).pack(side="right")


def show_records(root,t1=-1,t2=-1):
    record=Toplevel(root)
    history=ttk.Treeview(record,height=20)
    history["columns"]=("N","R","M","X")
    history.column("#0",width=150,minwidth=150)
    history.column("N",width=100,minwidth=90)
    history.column("R",width=150,minwidth=150)
    history.column("M",width=150,minwidth=150)
    history.column("X",width=150,minwidth=150)

    history.heading("#0",text="SR. no",anchor=W)
    history.heading("N",text="Name",anchor=W)
    history.heading("R",text="Runs Scored",anchor=W)
    history.heading("M",text="Matches Played",anchor=W)
    history.heading("X",text="Maximum Scores",anchor=W)

    k=0
    if t2==[]:
        teams=[t1]
    else:
        teams=[t1,t2]
    for t in teams:
        ld=t[0].split("_")[0]
        for i in range(0,len(t1)):
            
            player=t[i].split("_")[0]
            q="select * from {} where nm='{}';".format(ld,player)
            cur.execute(q)
            r=cur.fetchone()
            
            history.insert("",k,text=k+1,values=(r[0],r[3],r[1],r[2]))
        Button(record,text="Captainship Record",command=lambda:captainship(t1[0],t2[0],0,root)).pack(anchor="se")

    Label(record,text="Record of all the Players ").pack()
    history.pack()

def captainship(t1,t2,show_all,root):
    captains=Toplevel(root)
    rec=ttk.Treeview(captains)
    rec["columns"]=("M","W","D","L")
    rec.column("#0",width=150,minwidth=150)
    rec.column("M",width=100,minwidth=90)
    rec.column("W",width=150,minwidth=150)
    rec.column("D",width=150,minwidth=150)
    rec.column("L",width=150,minwidth=150)

    rec.heading("#0",text="Player name",anchor=W)
    rec.heading("M",text="Matches Played",anchor=W)
    rec.heading("W",text="Wins",anchor=W)
    rec.heading("D",text="Draw",anchor=W)
    rec.heading("L",text="Loses",anchor=W)

    q="select * from players;"
    cur.execute(q)
    r=cur.fetchall()

    if show_all:
        for rec in r:
            cap=rec[0]
            rec.insert("",1,cap,values=(r[1],r[2],r[4],r[3]))

    else:
        p1=t1.split("_")[0]
        p2=t2.split("_")[0]
        for rec in r:
            if r[0]==p1:
                rec.insert("",0,text=p1,values=(r[1],r[2],r[4],r[3]))
            if r[0]==p2:
                rec.insert("",0,text=p2,values=(r[1],r[2],r[4],r[3]))
        
    rec.pack()
def pplayer_data(fpl1,fpl2,scoreboard):
    fields=" (nm varchar(20),t_m int(4),mx int(4),t_r int(4))"
    q="create table if not exists "+fpl1[0].split("_")[0]+fields+";"
    cur.execute(q)
    cn.commit()
    q="create table if not exists "+fpl2[0].split("_")[0]+fields+";"
    cur.execute(q)
    cn.commit()
    for team in [fpl1,fpl2]:
        for p in team:
            ld1=team[0].split("_")[0]
            pl=p.split("_")[0]
            print(pl)
            q="select * from {} where nm='{}';".format(ld1,pl)
            print(q)
            cur.execute(q)
            r=cur.fetchall()
            if not r:
                q="insert into {} values('{}',0,0,0);".format(ld1,pl)
                cur.execute(q)
                cn.commit()
            
            if scoreboard[p]!=-1:
                q="select * from {} where nm='{}';".format(ld1,pl)
                cur.execute(q)
                r=cur.fetchone()
                mx=max([r[2],scoreboard[p]])
                q="update {} set t_m=t_m+1,mx={},t_r=t_r+{} where nm='{}';".format(ld1,mx,scoreboard[p],pl)
                cur.execute(q)
                cn.commit()


def storedata(six,fours,balls,scoreboard,fpl1,fpl2,pl1,pl2,total_ball,iscomputer):
    if iscomputer:
        return
    p1=fpl1[0].split("_")[0]
    p2=fpl2[0].split("_")[0]
    for pl in (p1,p2):
        q="select * from players where pl_nm='{}';".format(pl)
        cur.execute(q)
        r=cur.fetchall()
        if not r:
            q="insert into players values('{}',0,0,0,0);".format(pl)
            cur.execute(q)
            cn.commit()
        q="update players set m=m+1 where pl_nm='{}';".format(pl)
        cur.execute(q)
    if pl1>pl2:
        q="update players set win=win+1 where pl_nm='{}';".format(p1)
        cur.execute(q)
        q="update players set lose=lose+1 where pl_nm='{}';".format(p2)
        cur.execute(q)
    elif pl1<pl2:
        q="update players set win=win+1 where pl_nm='{}';".format(p2)
        cur.execute(q)
        q="update players set lose=lose+1 where pl_nm='{}';".format(p1)
        cur.execute(q)
    else:
        q="update players set draw=draw+1 where pl_nm='{}' or pl_nm='{}';".format(p1,p2)
        cur.execute(q)
    
    pplayer_data(fpl1,fpl2,scoreboard)
                
def captainship(t1,t2,show_all,root):
    captains=Toplevel(root)
    rec=ttk.Treeview(captains)
    rec["columns"]=("M","W","D","L")
    rec.column("#0",width=150,minwidth=150)
    rec.column("M",width=100,minwidth=90)
    rec.column("W",width=150,minwidth=150)
    rec.column("D",width=150,minwidth=150)
    rec.column("L",width=150,minwidth=150)

    rec.heading("#0",text="Player name",anchor=W)
    rec.heading("M",text="Matches Played",anchor=W)
    rec.heading("W",text="Wins",anchor=W)
    rec.heading("D",text="Draw",anchor=W)
    rec.heading("L",text="Loses",anchor=W)

    q="select * from players;"
    cur.execute(q)
    R=cur.fetchall()

    if show_all:
        for r in R:
            cap=r[0]
            rec.insert("",1,text=cap,values=(r[1],r[2],r[4],r[3]))

    else:
        p1=t1.split("_")[0]
        p2=t2.split("_")[0]
        for r in R:
            if r[0]==p1:
                rec.insert("",0,text=p1,values=(r[1],r[2],r[4],r[3]))
            if r[0]==p2:
                rec.insert("",0,text=p2,values=(r[1],r[2],r[4],r[3]))
        
    rec.pack()
