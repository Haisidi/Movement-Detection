import cv2 as cv
import numpy as np
import cv2
import math
import tkinter as tk
from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfilename
from pathlib import Path

# global string
temp_path=""

# detects moving object by using optical flow algorithm
def optical1():
    global temp_path
    # parameters for corner detection #
    feature_params = dict(maxCorners=300, qualityLevel=0.2, minDistance=2, blockSize=7)
    # Parameters for Lucas-Kanade optical flow algorithm #
    lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
    # the video feed is read in as a "VideoCapture" object #
    cap = cv.VideoCapture(temp_path)
    # variable for color to draw optical flow track in the video #
    color = (0, 255, 0)
    # ret = a boolean return value from getting the frame, first_frame = the first frame in the entire video sequence #
    ret, first_frame = cap.read()
    # converts frame (single image) from "RGB" colors to "grayscale" colors, to detect edges #
    prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
    # finds the strongest corners in the first frame by "Shi-Tomasi" method, we will track the "optical flow" for these corners #
    prev = cv.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)
    # creates an image filled with zero intensities with the same dimensions as the frame, for drawing purposes #
    mask = np.zeros_like(first_frame)

    while (cap.isOpened()):

        # ret = a boolean return value from getting the frame, frame = the current frame being projected in the video #
        ret, frame = cap.read()
        # converts each frame (single image), to "grayscale" colors #
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # calculates sparse optical flow by "Lucas-Kanade" method #
        next, status, error = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)
        # selects good feature points for the previous position #
        good_old = prev[status == 1]
        # selects good feature points for the next position #
        good_new = next[status == 1]
        # draws the optical flow tracks #
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            # returns a contiguous flattened array as (x,y) coordinates, for new point #
            a, b = new.ravel()
            # returns a contiguous flattened array as (x,y) coordinates, for old point #
            c, d = old.ravel()
            # draws filled circle at new position with green color #
            frame = cv.circle(frame, (a, b), 100, color, 15)
        # overlays the optical flow tracks on the original frame #
        output = cv.add(frame, mask)
        # updates previous frame #
        prev_gray = gray.copy()
        # updates previous good feature points #
        prev = good_new.reshape(-1, 1, 2)
        # opens a new window and displays the output frame #
        cv.imshow("CamouflageDetection", output)
        # frames are read by intervals of 10 milliseconds. the programs can be break out of the "while loop" when the user presses the 'q' key #
        if cv.waitKey(10) & 0xFF == ord('q'):
            break
    # frees up resources #
    cap.release()

# class for the first window - "log in" window #
class LOG_IN:
    def __init__(self, master):
        self.master = master
        # sets the size of the window #
        self.master.geometry("500x500")
        # sets the title of the window #
        master.title("CamouflageDetection")
        self.setLabel()

    # sets the labels in the window
    def setLabel(self):
        label1 = tk.Label(self.master, text="Login", fg="blue", relief="solid", width=20, font=("arial", 19, "bold"))
        label1.place(x=90, y=50)
        label2 = tk.Label(self.master, text="User Name:", width=20, font=("arial", 10, "bold"))
        label2.place(x=45, y=140)
        label2 = tk.Label(self.master, text="Password:", width=20, font=("arial", 10, "bold"))
        label2.place(x=45, y=180)

        # sets the button in the window #
        b1 = tk.Button(self.master, text="SIGN IN", width=12, bg="gray", fg="white", command=lambda: self.new_window(1, Win3))
        b1.place(x=200, y=300)

        label3 = tk.Label(self.master, text="Forgot", font=("arial", 8, "bold"))
        label3.place(x=80, y=390)
        label4 = tk.Label(self.master, text="User Name", fg="blue", font=("arial", 8, "bold"))
        label4.place(x=122, y=390)
        label5 = tk.Label(self.master, text="or", font=("arial", 8, "bold"))
        label5.place(x=187, y=390)
        label6 = tk.Label(self.master, text="Password", fg="blue", font=("arial", 8, "bold"))
        label6.place(x=205, y=390)
        label7 = tk.Label(self.master, text="?", font=("arial", 8, "bold"))
        label7.place(x=265, y=390)
        entry_1 = tk.Entry(self.master, textvar="")
        entry_1.place(x=210, y=142)

        # text box 2 #
        entry_2 = tk.Entry(self.master, textvar="")
        entry_2.place(x=210, y=182)


    # open new window
    def new_window(self, number, _class):
        # after opening a new window the previous one will closed #
        self.master.withdraw()
        self.new = tk.Toplevel(self.master)
        _class(self.new, number)

# class for the second window #
class Win3:
    def __init__(self, master, number):
        self.master = master
        # sets the size of the window #
        self.master.geometry("600x600")
        # sets the title of the window #
        master.title("CamouflageDetection")
        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.frame)
        self.label.pack()
        self.frame.pack()
        # define the "fn1" variable to be a string #
        fn1 = StringVar(self.master)
        # define the "fn2" variable to be a string #
        fn2 = StringVar(self.master)
        # define the "fn3" variable to be a string #
        fn3 = StringVar(self.master)
        # define the "fn4" variable to be a string #
        fn4 = StringVar(self.master)
        # define the "fn5" variable to be a string #
        fn5 = StringVar(self.master)
        # define the "fn6" variable to be a string #
        fn6 = StringVar(self.master)

        # exit from the program
        def ExitProg():
            exit()
        # open new file
        def OpenFile():
            global temp_path
            flag=1
            name = askopenfilename()
            filePath=name
            temp_path=filePath
            fileName=Path(filePath).stem

            # counting the total amount of frames in the video #
            vidcap = cv2.VideoCapture(filePath)
            success, image = vidcap.read()
            count = 0
            while success:
                success, image = vidcap.read()
                count += 1


            # counts the amount of frames per second in the video #
            cam = cv2.VideoCapture(filePath)
            frames_per_second = cam.get(cv2.CAP_PROP_FPS)


            # calculates the duration time of the video #
            vid = cv2.VideoCapture(filePath)
            height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

            # calculates the video duration time #
            duration = count / frames_per_second
            minutes = int(duration / 60)
            seconds = duration % 60
            duration_video_time=str(minutes) + ':' + str(seconds)

            # "flag=1" - the user choose file to process #
            if(flag==1):
                fn1.set(filePath)
                fn2.set(fileName)
                fn3.set(str(height) + " X " + str(width))
                fn4.set(duration_video_time)
                fn5.set(frames_per_second)
                fn6.set(count)
                flag=0

        menu = Menu(master)
        master.config(menu=menu)

        # file menu tool #
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Select DB for learning",command=lambda: self.new_window(1, select_db_window))
        filemenu.add_command(label="Select video to process",command=OpenFile)
        filemenu.add_command(label="Open processed video and results")
        filemenu.add_command(label="Save report")
        filemenu.add_separator()
        filemenu.add_command(label="Exit program",command=ExitProg)

        # view menu tool #
        viewmenu= Menu(menu)
        menu.add_cascade(label="View", menu=viewmenu)
        viewmenu.add_command(label="parameters of video")
        viewmenu.add_command(label="frame")
        viewmenu.add_command(label="frame with marked moving objects")
        viewmenu.add_command(label="video with marked moving objects")
        viewmenu.add_command(label="stabilized video with marked moving objects")
        viewmenu.add_command(label="statistics")

        # options menu tool #
        optionsmenu= Menu(menu)
        menu.add_cascade(label="Options", menu=optionsmenu)
        optionsmenu.add_command(label="frames per second to process",command=lambda: self.new_window(1, frames_per_second_window))
        optionsmenu.add_command(label="parameters of analysis",command=lambda: self.new_window(1, parameters_of_analysis_window))
        optionsmenu.add_command(label="parameters for output graphs",command=lambda: self.new_window(1, parameters_for_output_graphs_window))
        optionsmenu.add_command(label="Initial position",command=lambda: self.new_window(1, camera_position))


        # help menu tool #
        helpmenu= Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About the program",command=lambda: self.new_window(1, about_the_program_window))
        helpmenu.add_command(label="How to use?",command=lambda: self.new_window(1, how_to_use_window))

        # tab - 1 #
        tabControl = ttk.Notebook(master)  # Create Tab Control
        tab1 = Frame(tabControl)  # Create a tab
        tabControl.add(tab1, text='Video')  # Add the tab

        # tab - 1 - content #
        label8 = tk.Label(tab1, text="Choosen Video", font=("arial", 21, "bold"))
        label8.place(x=40, y=13)
        label9 = tk.Label(tab1, text="Video Path:", font=("arial",10))
        label9.place(x=30, y=70)
        label10 = tk.Label(tab1, text="Video Name:", font=("arial", 10))
        label10.place(x=30, y=103)
        label11 = tk.Label(tab1, text="Video Resolution:", font=("arial", 10))
        label11.place(x=30, y=136)
        label12 = tk.Label(tab1, text="Duration Of The Video:", font=("arial", 10))
        label12.place(x=30, y=169)
        label13 = tk.Label(tab1, text="Frames Per Second:", font=("arial", 10))
        label13.place(x=30, y=202)
        label14 = tk.Label(tab1, text="Total Frames:", font=("arial", 10))
        label14.place(x=30, y=235)

        # text box 1 #
        entry_1 = Entry(tab1, textvar=fn1)
        entry_1.place(x=210, y=73)
        # text box 2 #
        entry_2 = Entry(tab1, textvar=fn2)
        entry_2.place(x=210, y=105)
        # text box 3 #
        entry_3 = Entry(tab1, textvar=fn3)
        entry_3.place(x=210, y=138)
        # text box 4 #
        entry_4 = Entry(tab1, textvar=fn4)
        entry_4.place(x=210, y=171)
        # text box 5 #
        entry_5 = Entry(tab1, textvar=fn5)
        entry_5.place(x=210, y=205)
        # text box 6 #
        entry_6 = Entry(tab1, textvar=fn6)
        entry_6.place(x=210, y=239)

        # Restore Position
        b3 = tk.Button(tab1, text="Restore Position", width=12, bg="gray", fg="white",command=restorePosition)
        b3.place(x=345, y=460)
        self.frame.pack()
        # button for starting detection #
        b2 = tk.Button(tab1, text="Start Detection", width=12, bg="gray", fg="white",command=optical1)
        b2.place(x=200, y=460)

        # tab - 2 #
        tab2 = Frame(tabControl)  # Create a tab
        tabControl.add(tab2, text='Statistics')  # Add the tab
        load = Image.open(("graph1.jpg"))
        stat = ImageTk.PhotoImage(load)
        img = Label(tab2, image=stat)
        img.image = stat
        img.place(x=70, y=0)
        load = Image.open(("graph2.jpg"))
        stat2 = ImageTk.PhotoImage(load)
        img = Label(tab2, image=stat2)
        img.image = stat2
        img.place(x=12, y=260)

        tabControl.pack(expand=1, fill="both")  # Pack to make visible

        # tab - 3 #
        tab3 = Frame(tabControl)  # Create a tab
        tabControl.add(tab3, text='Video with marked objects')  # Add the tab
        tabControl.pack(expand=1, fill="both")  # Pack to make visible

# opens a new window
    def new_window(self, number, _class):
        self.new = tk.Toplevel(self.master)
        _class(self.new, number)

# closes the window
    def close_window(self):
        self.master.destroy()

# class for the - "about the program" action #
class about_the_program_window:
    def __init__(self, master, number):
        self.master = master
        self.master.geometry("400x400")
        self.frame = tk.Frame(self.master)
        label15 = Label(master,text="Camouflage is the use of any combination of materials, coloration for concealment,\n ",font=("arial",8))
        label15.place(x=-5, y=30)
        self.frame.pack()

# class for the - "how to use" action #
class how_to_use_window:
    def __init__(self, master, number):
        self.master = master
        self.master.geometry("400x400")
        self.frame = tk.Frame(self.master)
        label15 = Label(master,text="Camouflage is the use of any combination of materials, coloration for concealment,\n  ",font=("arial",8))
        label15.place(x=-5, y=30)
        self.frame.pack()

# class for the - "select data base" action #
class select_db_window:
    def __init__(self, master, number):
        self.master = master
        self.master.geometry("400x400")
        self.frame = tk.Frame(self.master)

        # define the "var1" variable to be a integer #
        var1 = IntVar()
        Checkbutton(master, text='DB1', variable=var1).place(x=10,y=30)
        # define the "var2" variable to be a integer #
        var2 = IntVar()
        Checkbutton(master, text='DB2', variable=var2).place(x=10,y=60)
        # define the "var3" variable to be a integer #
        var3 = IntVar()
        Checkbutton(master, text='DB3', variable=var3).place(x=10,y=90)
        # define the "var4" variable to be a integer #
        var4 = IntVar()
        Checkbutton(master, text='DB4', variable=var4).place(x=10,y=120)
        # define the "var5" variable to be a integer #
        var5 = IntVar()
        Checkbutton(master, text='DB5', variable=var5).place(x=10,y=150)
        # button for save #
        b2 = tk.Button(self.master, text="Save", width=12, bg="gray", fg="white", command=lambda: self.master.withdraw())
        b2.place(x=150, y=300)
        self.frame.pack()

# class for the - "parameters of analysis" action #
class parameters_of_analysis_window:
    def __init__(self, master, number):
        self.master = master
        self.master.geometry("400x400")
        self.frame = tk.Frame(self.master)

        # define the "var1" variable to be a integer #
        var1 = IntVar()
        Checkbutton(master, text='animal', variable=var1).place(x=10,y=30)
        # define the "var2" variable to be a integer #
        var2 = IntVar()
        Checkbutton(master, text='human', variable=var2).place(x=10,y=60)
        # define the "var3" variable to be a integer #
        var3 = IntVar()
        Checkbutton(master, text='ball', variable=var3).place(x=10,y=90)
        # define the "var4" variable to be a integer #
        var4 = IntVar()
        Checkbutton(master, text='general object', variable=var4).place(x=10,y=120)
        # define the "var5" variable to be a integer #
        var5 = IntVar()
        Checkbutton(master, text='tree', variable=var5).place(x=10,y=150)
        # button for save #
        b2 = tk.Button(self.master, text="Save", width=12, bg="gray", fg="white", command=lambda: self.master.withdraw())
        b2.place(x=150, y=300)
        self.frame.pack()

# class for the - "frames per second" action #
class frames_per_second_window:
    def __init__(self, master, number):
        self.master = master
        self.master.geometry("400x400")
        self.frame = tk.Frame(self.master)
        label16 = Label(master,text="frames per second:",font=("arial",8))
        label16.place(x=55, y=10)
        w = Scale(master, from_=0, to=30)
        w.pack()
        # button for save #
        b3 = tk.Button(self.master, text="Save", width=12, bg="gray", fg="white", command=lambda: self.master.withdraw())
        b3.place(x=150, y=300)
        self.frame.pack()

# class for the - "parameters for output graphs" action #
class parameters_for_output_graphs_window:
    def __init__(self, master, number):
        self.master = master
        self.master.geometry("400x400")
        self.frame = tk.Frame(self.master)

        # define the "var1" variable to be a integer #
        var1 = IntVar()
        Checkbutton(master, text='size', variable=var1).place(x=10,y=30)
        # define the "var2" variable to be a integer #
        var2 = IntVar()
        Checkbutton(master, text='name', variable=var2).place(x=10,y=60)
        # define the "var3" variable to be a integer #
        var3 = IntVar()
        Checkbutton(master, text='speed', variable=var3).place(x=10,y=90)
        # define the "var4" variable to be a integer #
        var4 = IntVar()
        Checkbutton(master, text='resolution', variable=var4).place(x=10,y=120)
        # define the "var5" variable to be a integer #
        var5 = IntVar()
        Checkbutton(master, text='frames per second', variable=var5).place(x=10,y=150)
        # define the "var6" variable to be a integer #
        var6 = IntVar()
        Checkbutton(master, text='processing time', variable=var6).place(x=10,y=180)
        # button for save #
        b2 = tk.Button(self.master, text="Save", width=12, bg="gray", fg="white", command=lambda: self.master.withdraw())
        b2.place(x=150, y=300)
        self.frame.pack()

# class for the - "parameters for output graphs" action #
class camera_position:
    def __init__(self, master, number):
        self.master = master
        self.master.geometry("400x400")
        self.frame = tk.Frame(self.master)

        label1 = tk.Label(self.master, text="Initail camera position", font=("arial", 15, "bold"))
        label1.place(x=25, y=13)
        label2 = tk.Label(self.master, text="x0:", width=20, font=("arial", 10, "bold"))
        label2.place(x=-5, y=85)
        label3 = tk.Label(self.master, text="y0:", width=20, font=("arial", 10, "bold"))
        label3.place(x=-5, y=115)
        label4 = tk.Label(self.master, text="zo:", width=20, font=("arial", 10, "bold"))
        label4.place(x=-5, y=145)
        label5 = tk.Label(self.master, text="αx:", width=20, font=("arial", 10, "bold"))
        label5.place(x=-5, y=175)
        label6 = tk.Label(self.master, text="αy:", width=20, font=("arial", 10, "bold"))
        label6.place(x=-5, y=205)
        label7 = tk.Label(self.master, text="αz:", width=20, font=("arial", 10, "bold"))
        label7.place(x=-5, y=235)
        label8 = tk.Label(self.master, text="dreal:", width=20, font=("arial", 10, "bold"))
        label8.place(x=-5, y=265)
        label9 = tk.Label(self.master, text="cm", width=20, font=("arial", 10, "bold"))
        label9.place(x=200, y=265)

        # text box 1 #
        entry_1 = tk.Entry(self.master, textvar="")
        entry_1.place(x=140, y=85)
        # text box 2 #
        entry_2 = tk.Entry(self.master, textvar="")
        entry_2.place(x=140, y=115)
        # text box 3 #
        entry_3 = tk.Entry(self.master, textvar="")
        entry_3.place(x=140, y=145)
        # text box 4 #
        entry_4 = tk.Entry(self.master, textvar="")
        entry_4.place(x=140, y=175)
        # text box 5 #
        entry_5 = tk.Entry(self.master, textvar="")
        entry_5.place(x=140, y=205)
        # text box 6 #
        entry_6 = tk.Entry(self.master, textvar="")
        entry_6.place(x=140, y=235)
        # text box 7 #
        entry_7 = tk.Entry(self.master, textvar="")
        entry_7.place(x=140, y=265)

        # button for save #
        b2 = tk.Button(self.master, text="Save", width=12, bg="gray", fg="white", command=lambda: self.master.withdraw())
        b2.place(x=150, y=300)
        self.frame.pack()

class clPoint():
    def __init__(self, x=0, y=0, z=0, val=0):
        self.x = x
        self.y = y
        self.z = z
        self.val = val


class clCamera():
    def __init__(self):
        self.distRealSize = 0.2  # (meters)
        self.dx = 0.18
        self.dy = 0.1
        self.pointsPerSm = 4
        self.x = 0
        self.y = 0
        self.z = 1.5
        self.axGrad = 0
        self.ayGrad = 0
        self.azGrad = 0
        self.vvCC = []
        # send here jpg picture after transfring to cordinates
        self.Photo = clPhoto()
        self.s = ""

# print to "txt" file
    def printToTxtFile(self, bPrint, bPrintBorder, f):
        xMin = -0.5 * self.dx
        yMin = -0.5 * self.dy
        xMax = 0.5 * self.dx
        yMax = 0.5 * self.dy
        d = float(0.01) / self.pointsPerSm
        f.write(self.s + "\n")
        self.Photo.printToTxtFile(xMin, yMin, xMax, yMax, d, bPrint, bPrintBorder, f)

# gets the angles, and return the total sum with speed
    def vvCC_get(self, axGrad, ayGrad, azGrad):  # rotation matrix
        def vByMatrix(vvM, v):
            n = len(v)
            v1 = []
            for vM in vvM:
                sum = 0
                for i in range(n):
                    sum += vM[i] * v[i]
                v1.append(sum)
            return v1

# gets the change in the light
        def vvI(n):
            vvI = []
            for i in range(n):
                vI = []
                for j in range(n):
                    if i == j:
                        vI.append(1)
                    else:
                        vI.append(0)
                vvI.append(vI)
            return vvI

# calculate th total "M" matrix
        def vvP(vvM1, vvM2):
            vv = []
            n = len(vvM1)
            m = len(vvM2[0])
            k = len(vvM1[0])
            for i in range(n):
                v = []
                for j in range(m):
                    sum = 0
                    for l in range(k):
                        sum += vvM1[i][l] * vvM2[l][j]
                    v.append(sum)
                vv.append(v)
            return vv

#this func gets the "speed" in axes "x"
        def vvMx_get(axGrad):
            vvMx = vvI(3)
            vvMx[1][1] = math.cos(math.radians(axGrad))
            vvMx[1][2] = -math.sin(math.radians(axGrad))
            vvMx[2][1] = math.sin(math.radians(axGrad))
            vvMx[2][2] = math.cos(math.radians(axGrad))
            return vvMx

# this func gets the "speed" in axes "y"
        def vvMy_get(ayGrad):
            vvMy = vvI(3)
            vvMy[0][0] = math.cos(math.radians(ayGrad))
            vvMy[0][2] = math.sin(math.radians(ayGrad))
            vvMy[2][0] = -math.sin(math.radians(ayGrad))
            vvMy[2][2] = math.cos(math.radians(ayGrad))
            return vvMy

# gets the "speed" in axes "z"
        def vvMz_get(azGrad):
            vvMz = vvI(3)
            vvMz[0][0] = math.cos(math.radians(azGrad))
            vvMz[0][1] = -math.sin(math.radians(azGrad))
            vvMz[1][0] = math.sin(math.radians(azGrad))
            vvMz[1][1] = math.cos(math.radians(azGrad))
            return vvMz

        vvCC = vvP(vvP(vvMx_get(axGrad), vvMy_get(ayGrad)), vvMz_get(azGrad))
        return vvCC
# get image for the restore action
    def getImage(self, Photo, x, y, z, axGrad, ayGrad, azGrad):
        self.x = x
        self.y = y
        self.z = z
        self.axGrad = axGrad
        self.ayGrad = ayGrad
        self.azGrad = azGrad
        self.Photo = clPhoto()

        self.s = "x=" + str(x) + " y=" + str(y) + " z=" + str(z) + " ax=" + str(axGrad) + " ay=" + str(
            ayGrad) + " az=" + str(azGrad)
        print(self.s)
        vvCC = self.vvCC_get(self.axGrad, self.ayGrad, self.azGrad + 180)  # +180 because we do not need negative photo
        self.vvCC = vvCC
        self.Photo = clPhoto()
        for p in Photo.vPoint:
            dx = p.x - self.x
            dy = p.y - self.y
            dz = p.z - self.z
            val = vvCC[0][2] * dx + vvCC[1][2] * dy + vvCC[2][2] * dz

            # print val
            if val != 0:
                valx = vvCC[0][0] * dx + vvCC[0][1] * dy + vvCC[0][2] * dz
                valy = vvCC[1][0] * dx + vvCC[1][1] * dy + vvCC[1][2] * dz
                xx = float(self.distRealSize * valx) / val
                yy = float(self.distRealSize * valy) / val
                self.Photo.vPoint.append(clPoint(xx, yy))

# sends single frame
    def getReal(self):
        Real = clPhoto()
        dz = 0 - self.z
        vvCC = self.vvCC
        for p in self.Photo.vPoint:
            val = vvCC[2][0] * p.x + vvCC[2][1] * p.y + vvCC[2][2] * self.distRealSize
            if val != 0:
                valx = vvCC[0][0] * p.x + vvCC[0][1] * p.y + vvCC[0][2] * self.distRealSize
                valy = vvCC[1][0] * p.x + vvCC[1][1] * p.y + vvCC[1][2] * self.distRealSize
                xx = self.x + float(dz * valx) / val
                yy = self.y + float(dz * valy) / val
                Real.vPoint.append(clPoint(xx, yy, 0))
        return Real


class clPhoto():
    def __init__(self):
        self.vPoint = []

# creates an image
    def myImage(self):
        d = 0.5
        nx = 3
        ny = 10
        k = 10
        dd = float(d) / k
        self.vPoint = []
        for ix in range(nx):
            for jx in range(k):
                for iy in range(ny):
                    for jy in range(k):
                        if jx == 0 or jy == 0:
                            x = ix * d + jx * dd
                            y = iy * d + jy * dd
                            z = 0
                            val = 1
                            Point = clPoint(x, y)
                            self.vPoint.append(Point)

# pulls out a list of points to draw from the image
    def vvPiointToShow(self, xMin, yMin, xMax, yMax, d):  # vvPioint,nx,ny=
        nx = int(float(xMax - xMin) / d) + 2
        ny = int(float(yMax - yMin) / d) + 2
        vvPioint = []
        for i in range(nx):
            p = []
            for j in range(ny):
                p.append(0)
            vvPioint.append(p)
        for point in self.vPoint:
            i = int(float(point.x - xMin) / d + 0.5)
            j = int(float(point.y - yMin) / d + 0.5)
            if i >= 0 and i < nx - 1 and j >= 0 and j < ny - 1:
                vvPioint[i][j] += 1
        return vvPioint, nx, ny

# draws the image in the form of text
    def printToTxtFile(self, xMin, yMin, xMax, yMax, d, bPrint, bPrintBorder, f):
        if bPrint:
            print("")
        f.write("\n")
        vvPioint, nx, ny = self.vvPiointToShow(xMin, yMin, xMax, yMax, d)
        for jy in range(ny):
            s = ""
            for ix in range(nx):
                iy = ny - jy - 1
                if vvPioint[ix][iy] == 0:
                    s += "  "
                else:
                    s += "[]"
            if bPrintBorder:
                if jy == int(0.5 * (ny + 1)):
                    s = "-" + s + "-"
                else:
                    s = "|" + s + "|"
            if bPrint:
                print(s)
            f.write(s + "\n")

# tests all kinds of options, after that the painted picture is chosen,
# the function restore the original area, from all kinds of angles
def restorePosition():
    Photo = clPhoto()
    # here the image is created
    Photo.myImage()
    xMin = -2
    yMin = -2
    xMax = 2
    yMax = 2
    d = 0.1
    f = open("test.txt", 'w')
    Photo.printToTxtFile(xMin, yMin, xMax, yMax, d, True, True, f)

    Camera = clCamera()
    Camera.Photo = Photo
    Camera.printToTxtFile(True, True, f)

    x = 0
    y = 0
    z = 8
    axGrad = 0
    ayGrad = 0
    azGrad = 0
    Camera.getImage(Photo, x, y, z, axGrad, ayGrad, azGrad)
    Camera.printToTxtFile(True, True, f)

    Camera.getImage(Photo, -1, 0, z, axGrad, ayGrad, azGrad)
    Camera.printToTxtFile(True, True, f)

    Camera.getImage(Photo, 0, -1, z, axGrad, ayGrad, azGrad)
    Camera.printToTxtFile(True, True, f)

    Camera.getImage(Photo, -1, -1, z, axGrad, ayGrad, azGrad)
    Camera.printToTxtFile(True, True, f)

    Camera.getImage(Photo, 0, 0, z, axGrad, ayGrad, 45)
    Camera.printToTxtFile(True, True, f)

    Camera.getImage(Photo, -1, 1, z, axGrad, ayGrad, 45)
    Camera.printToTxtFile(True, True, f)

    Camera.getImage(Photo, 1, 0, z, 0, 0, 0)
    Camera.printToTxtFile(True, True, f)

    Camera.getImage(Photo, 1, -2, z, 0, 0, 0)
    Camera.printToTxtFile(True, True, f)

    Camera.getImage(Photo, 1, -2, z, 10, 0, 0)
    Camera.printToTxtFile(True, True, f)

    Camera.getImage(Photo, 1, -2, z, 20, 0, 0)
    Camera.printToTxtFile(True, True, f)

    Camera.getImage(Photo, 0, 0, z, 10, 0, 0)
    Camera.printToTxtFile(True, True, f)

    Camera.getImage(Photo, 0, 0, z, 30, 0, 0)
    Camera.printToTxtFile(True, True, f)

    Real = Camera.getReal()
    Real.printToTxtFile(xMin, yMin, xMax, yMax, d, True, True, f)
    f.close()

root = tk.Tk()
app = LOG_IN(root)
root.mainloop()
