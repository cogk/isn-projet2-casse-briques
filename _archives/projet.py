from tkinter import*






fen=Tk() #On creér la fenêtre
fen.title("Y'a qu'a casser des briques") #On nomme la fenêtre

#On creér un canvas
fond= Canvas(fen,width=600, height=700, bg='white', bd=3)
fond.pack ()

image= PhotoImage(file='isn.png')
fond.create_image(0, 0, anchor=NW, image=image)
               
