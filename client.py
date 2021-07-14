import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 8002

class Client:

    def __init__(self,host,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))

        msg = tkinter.Tk()
        msg.withdraw()
        self.nickname = simpledialog.askstring("Name", "Please choose a nickname",parent = msg)
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target= self.gui_loop)
        receive_thread = threading.Thread(target = self.receive)
        gui_thread.start()
        receive_thread.start()
    
    
    def gui_loop(self):
        print("2")
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        print("3")
        self.chat_label.config(font=("Arial",12))
       
        self.chat_label.pack(padx=20,pady=5)
        
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20,pady=5)
        self.text_area.config(state='disabled')
        
        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        
        self.msg_label.config(font=("Arial",12))
        self.msg_label.pack(padx=20,pady=5)

        self.input_area = tkinter.Text(self.win, height = 3)
        self.input_area.pack(padx=20,pady=5)
        
        self.send_button = tkinter.Button(self.win,text="Send", command=self.write)
        self.send_button.config(font=("Arial",12))
        self.send_button.pack(padx=20,pady=5)
        self.gui_done = True
        print("4")
        #when we close window
        self.win.protocol("WM_DELETE_WINDOW",self.stop)
        

    def write(self):
        message = f"{self.nickname}:{self.input_area.get('1.0','end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0','end')
        

    def receive(self):
        while self.running:
            try:
                print("s")
                message = self.sock.recv(1024)
                #check if server is asking for nickname
                if message == 'name_key':
                    self.sock.send(self.nickname.encoded("utf-8"))
                    print("v")
                else:
                    if self.gui_done:
                        print("j")
                        self.text_area.config(state="normal")
                        self.text_area.insert('end',message)
                        self.text_area.yview('end')
                        self.text_area.config(state="disabled")
                       
            except ConnectionAbortedError:
                break
            except:
                print("error")
                self.sock.close()
                break
                

    #terminate program
    def stop(self):
        self.running= False
        self.win.destroy()
        self.sock.close()
        exit(0)

client = Client(HOST, PORT)
    