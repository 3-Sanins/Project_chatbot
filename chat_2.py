import tkinter as tk
from tkinter import scrolledtext
import time
import pymysql

cn = pymysql.connect(host="sql12.freesqldatabase.com", user="sql12765493", password="EXEMGyxpJ5", database="sql12765493")
#cn=pymysql.connect(host="localhost",user="root",passwd="admin",database="chatein")
cur=cn.cursor()
cur.execute("set autocommit=1;")

q="create table if not exists chat(name varchar(30),time varchar(30),message varchar(45));"
cur.execute(q)

q="select * from chat;"
cur.execute(q)

chats=cur.fetchall()

def display_chats():
    """Displays chat messages in the chat window."""
    chat_display.config(state=tk.NORMAL)
    chat_display.delete(1.0, tk.END)  # Clear previous messages

    for sender, msg_time, message in chats:
        if sender == you:
            chat_display.insert(tk.END, f"{msg_time} [You]:\n", "your_time")
            chat_display.insert(tk.END, f"  {message}\n\n", "your_message")
        else:
            chat_display.insert(tk.END, f"{sender} [{msg_time}]:\n", "other_time")
            chat_display.insert(tk.END, f"  {message}\n\n", "other_message")

    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)  # Scroll to the last message

def send_message():
    global chats
    """Gets user input, adds it to the chat, and updates the display."""
    message = input_box.get()
    if message.strip():
        current_time = time.strftime("%I:%M %p")  # Get current time
        chats=chats+((you, current_time, message),)  # Add to chat list
        q="insert into chat values('{}','{}','{}');".format(you,current_time,message)
        cur.execute(q)
        display_chats()  # Refresh chat display
        input_box.delete(0, tk.END)  # Clear input field

def refresh_messages():
    global chats
    cur.execute("select * from chat;")
    chats = cur.fetchall()
    display_chats()

# Main window
root = tk.Tk()
root.title("Trio Chat App")
root.geometry("420x500")
root.configure(bg="#f0f0f0")

def get_ready():
    global chat_display,input_frame,input_box,send_button,refresh_button
    # Chat Display
    chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
    chat_display.pack(padx=10, pady=10)

    # Apply styles
    chat_display.tag_config("other_time", foreground="#0078D7", font=("Arial", 10, "bold"))
    chat_display.tag_config("other_message", foreground="#333333", font=("Arial", 10, "italic"))

    chat_display.tag_config("your_time", foreground="#009688", font=("Arial", 10, "bold"), justify="right")
    chat_display.tag_config("your_message", foreground="#333333", font=("Arial", 10), justify="right")

    # Input and Buttons Frame
    input_frame = tk.Frame(root)
    input_frame.pack(pady=5, fill="x", padx=10)

    input_box = tk.Entry(input_frame, font=("Arial", 12), width=25)
    input_box.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

    send_button = tk.Button(input_frame, text="Send", command=send_message)
    send_button.pack(side=tk.LEFT, padx=5)

    refresh_button = tk.Button(input_frame, text="Refresh", command=refresh_messages)
    refresh_button.pack(side=tk.RIGHT)


def submit():
    global nm,you,Root
    
    you=str(nm.get())
    q="select name from users where c_name='{}';".format(you)
    cur.execute(q)
    try:
        you=cur.fetchone()[0]
        Root.destroy()
        get_ready()
        display_chats()
    except:
        pass
    

def get_name():
    global nm,Root
    Root=tk.Frame(root)
    Root.pack()
    tk.Label(Root,text="Your Secret Name").pack()
    tk.Entry(Root,textvariable=nm).pack()
    tk.Button(Root,text="Submit",command=submit).pack()

nm=tk.StringVar()
get_name()

root.mainloop()


cn.close()
