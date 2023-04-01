from tkinter import *
from tkinter import filedialog
from Test import video_classify, image_classify
import os
from PIL import ImageTk, Image

def open_files():
	H = Label(root, text="Classification from Image", font=("Times", 25), fg='red')
	H.pack()
	H.place(x=675,y=10)
	global filename
	filename = filedialog.askopenfilename(initialdir=r"img", title="Select A File", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))

	T = Label(root, text="Input", font=("Times", 22), fg='black')
	T.pack()
	T.place(x=510,y=100)

	global inp
	inp = ImageTk.PhotoImage(Image.open(filename).resize((400, 250), Image.ANTIALIAS))
	p=w.create_image(350,150, anchor=NW, image=inp)

	image_classify(filename)

	T = Label(root, text="Output", font=("Times", 22), fg='black')
	T.pack()
	T.place(x=1030,y=100)
	global out
	out = ImageTk.PhotoImage(Image.open("img/out.jpg").resize((400, 250), Image.ANTIALIAS))
	q=w.create_image(850,150, anchor=NW, image=out)
	
def image_c():
	open_file=Button(root, text='Open Image', height=2, width=25, bg='navy blue', fg='black', command=open_files)
	open_file.pack()
	open_file.place(x=300,y=500)
	
root = Tk()
root.title("Facial Expression Recognition")
w = Canvas(root, width=1366, height=768)
w.pack()

Video_execute = Button(root, text='Video Classifier', height=3, width=25, bg='navy blue', fg='black', command=video_classify)
Video_execute.pack() 
Video_execute.place(x=20, y=60)

Image_execute = Button(root, text='Image Classifier', height=3, width=25, bg='navy blue', fg='black', command=image_c)
Image_execute.pack() 
Image_execute.place(x=20, y=120)


exit = Button(root, text='Exit', width=10, fg='black', command=quit)
exit.pack() 
exit.place(x=1150, y=650)

w.create_line(250,0,250,900, fill="black")
w.create_line(250,600,1360,600, fill="black")

root.mainloop()