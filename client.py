from tkinter import *
from tkinter import messagebox
import threading
import socket


# Window Configuration
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
app_width = 500
app_height = 500
x = (screen_width // 2) - (app_width // 2)
y = (screen_height // 2) - (app_height // 2)
root.geometry(f"{app_width}x{app_height}+{x}+{y}")
root.resizable(False, False)
root.title("Pythonic Chat")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# draw the gui
def draw_gui():
    ip_lbl = Label(root, text="IP Address").place(x=50, y=10)
    ip_entry = Entry(root)
    ip_entry.place(x=120 ,y=10)
    port_lbl = Label(root, text="Port").place(x=288, y=10)
    port_entry = Entry(root)
    port_entry.place(x=326, y=10)
    nickname_lbl = Label(root, text="Nickname").place(x=150, y=40)
    nickname_entry = Entry(root)
    nickname_entry.place(x=220, y=40)
    receive_message_box = Text(root, width=59, height=15)
    receive_message_box.config(state="disabled")
    receive_message_box.place(x=12, y=120)
    connect_button = Button(root, text="Connect", command=lambda: configure_client(ip_entry, port_entry, nickname_entry, receive_message_box))
    connect_button.place(x=220 ,y=75)
    send_message_box = Text(root, width=59, height=4)
    send_message_box.place(x=12, y=380)
    send_button = Button(root, text="Send", command=lambda: send_msg(nickname_entry, send_message_box))
    send_button.place(x=220, y=460)


# setup the client and prepare for connection
def configure_client(ip_entry, port_entry, nickname_entry, receive_message_box):
    try:
        ip = ip_entry.get()
        port = int(port_entry.get())
        nickname = nickname_entry.get()
        
        if ip != "" and port != None and nickname != "":
            connect(ip, port, nickname, receive_message_box)
            messagebox.showinfo("Operation Successful!", f"Successfully Connected To {ip} : {str(port)}")
        else:
            raise EXCEPTION
    except:
        messagebox.showerror("Operation Failed!", "Invalid Arguments Supplied!")
        
        
# connect to the server
def connect(ip, port, nickname, receive_message_box):
    try:
        enc_nick = nickname.encode('utf-8')
        s.connect((ip, port))
        threading.Thread(target=lambda: handle_messages(receive_message_box)).start()
        s.sendall(enc_nick)
    except:
        messagebox.showerror("Operation Failed!", "Failed To Connect To Server!")
        

# handle received messages
def handle_messages(receive_message_box):
    while True:
        try:
            data = s.recv(1024).decode('utf-8')
            
            if data:
                receive_message_box.config(state="normal")
                receive_message_box.insert(END, data)
                receive_message_box.config(state="disabled")
        except socket.error as e:
            print(str(e))
            
            
# send message to server
def send_msg(nickname_entry, send_message_box):
    nickname = nickname_entry.get()
    msg = send_message_box.get('1.0', END)
    send_message_box.delete('1.0', END)
    message = f"[{nickname}]: {msg}".encode('utf-8')
    s.sendall(message)


draw_gui()
root.mainloop()