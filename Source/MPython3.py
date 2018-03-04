###################################imports#############################
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import *
from pygame import mixer
from mutagen.mp3 import MP3
from PIL import ImageTk, Image
import threading as tr
import time as t
import pref as P
import random as r
import os
import os.path
###################################classes#############################


class Window(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master)
        self.master = master
        self.vol = P.volume
        self.interval = P.interval
        self.recentlyPlayed = ["Recently played:\n"]
        self.Logo = Image.open("MPython3Icon.png")
        self.LogoLab = ImageTk.PhotoImage(self.Logo)
        # running the base window
        self.init_window()
        self.mtypes = [("Music files", "*.mp3")]
        self.ptypes = [("Playlist files", "*.pylist")]

    def NoFileError(self):
        self.ErrorMessage = Toplevel()
        self.app = (self.ErrorMessage)
        self.ErrorMessage.title("ERROR!")
        self.ErrorMessage.iconbitmap("MPython3Icon.ico")
        self.ErrorMessage.geometry("200x100")
        ExitB = Button(self.ErrorMessage, text="OK!",
                       command=self.ErrorMessage.destroy)
        ExitB.pack()
        T = Text(self.ErrorMessage)
        T.insert(END, "An Error has occured\ncurrent song cannot\nbe found")
        T.pack()

    def playlistMaker(self):
        self.ListName = self.PName.get()
        self.folderPlaylist.destroy()
        self.Folder = askdirectory()
        if not self.Folder:
            pass
        else:
            self.FItems = os.listdir(self.Folder)
            self.FItemsLoc = []
            for x in self.FItems:
                self.FItemsLoc.append(self.Folder + "/" + x)

            if not self.ListName:
                temp = self.Folder.split('/')
                self.ListName = temp[-1]

            else:
                pass

            while os.path.exists("Playlists/" + self.ListName):
                x = 1
                self.ListName += str(x)
                x += 1

            with open("Playlists/" + self.ListName + ".pylist", "w") as F:
                for x in self.FItemsLoc:
                    F.write(x + "\n")

    def PPlayerThread(self):
        try:
            self.playing.destroy()
        except:
            pass
        self.PThreadBreak = False
        nums = []
        current = -1
        try:
            self.audio = MP3(self.SList[current])

        except:
            self.NoFileError()
            return
        Found = False
        self.ALength = round(self.audio.info.length / 60, 2)
        self.currentLabel = Label(self, text=self.SList[current])
        self.currentLabel.pack()
        while self.PLen >= len(nums):
            if self.PThreadBreak == True:
                self.currentLabel.destroy()
                break
            if len(nums) == self.PLen:
                break
            if mixer.music.get_busy() != 1:
                current += 1
                nums.append([current])
                while Found == False:
                    try:
                        self.audio = MP3(self.SList[current])
                        Found = True
                    except:
                        self.NoFileError()
                        nums.append([current])
                        current += 1
                        Found = False
                Found = False
                mixer.music.load(self.SList[current])
                self.currentLabel.update_idletasks()
                """self.currentLabel = Label(self, text=self.SList[current])
                self.currentLabel.pack()"""
                mixer.music.play()

                self.ALength = round(self.audio.info.length / 60, 2)
                try:
                    self.thread.exit()
                except:
                    pass

                self.TimeThread()
            else:
                pass
            t.sleep(self.interval)

    def PShufflerThread(self):
        try:
            self.playing.destroy()
        except:
            pass
        Found = False
        self.PThreadBreak = False
        nums = []
        current = r.randint(0, self.PLen - 1)
        while self.PLen >= len(nums):
            if self.PThreadBreak == True:
                self.currentLabel.destroy()
                break
            else:
                pass
            if len(nums) == self.PLen:
                break
            else:
                pass
            if mixer.music.get_busy() != 1:
                current = r.randint(0, self.PLen - 1)
                while current in nums:
                    current = r.randint(0, self.PLen - 1)
                nums.append(current)
                while Found == False:
                    try:
                        self.audio = MP3(self.SList[current])
                        Found = True
                    except:
                        self.NoFileError()
                        nums.append(current)
                        current = r.randint(0, self.PLen - 1)
                        Found = False
                Found = False
                mixer.music.load(self.SList[current])
                try:
                    self.currentLabel.destroy()
                except:
                    pass
                self.currentLabel = Label(self, text=self.SList[current])
                self.currentLabel.pack()
                mixer.music.play()

                self.ALength = round(self.audio.info.length / 60, 2)
                print(nums)
                try:
                    self.thread.exit()
                except:
                    pass

                self.TimeThread()
            else:
                pass
            t.sleep(self.interval)

    def PShuffler(self):
        self.PSThread = tr.Thread(target=self.PShufflerThread, args=())
        self.PSThread.daemon = True
        self.PSThread.start()

    def PPlayer(self):
        self.PThread = tr.Thread(target=self.PPlayerThread, args=())
        self.PThread.daemon = True
        self.PThread.start()

    def playlistPlay(self):
        try:
            self.current.destroy()
            self.currentLabel.destroy()

        except:
            pass
        self.ThreadBreak = True
        self.PThreadBreak = True
        mixer.music.stop()
        self.PList = askopenfilename(filetypes=self.ptypes)
        self.SList = []
        if self.PList:
            with open(self.PList, "r") as F:
                self.PLen = len(F.readlines())
            with open(self.PList, "r") as F:
                for line in F:
                    self.SList.append(line.strip("\n"))

            self.PPlayer()
        else:
            pass

    def playlistShuffle(self):
        try:
            self.current.destroy()
            self.currentLabel.destroy()
        except:
            pass
        self.ThreadBreak = True
        self.PThreadBreak = True
        mixer.music.stop()
        self.PList = askopenfilename(filetypes=self.ptypes)
        self.SList = []
        if self.PList:
            with open(self.PList, "r") as F:
                self.PLen = len(F.readlines())
            with open(self.PList, "r") as F:
                for line in F:
                    self.SList.append(line.strip("\n"))

            self.PShuffler()
        else:
            pass

    def playlistStop(self):
        self.ThreadBreak = True
        self.PThreadBreak = True
        mixer.music.stop()
        self.MPosL.destroy()

    def folderPlaylist(self):
        self.folderPlaylist = Toplevel()
        self.app = (self.folderPlaylist)
        self.folderPlaylist.iconbitmap("MPython3Icon.ico")
        self.folderPlaylist.title("Warning")
        self.folderPlaylist.geometry("310x220")
        Name = Label(self.folderPlaylist, text="Playlist name:")
        Name.pack()
        self.PName = Entry(self.folderPlaylist)
        self.PName.pack()
        OkB = Button(self.folderPlaylist, text="OK",
                     command=self.playlistMaker)
        OkB.place()
        OkB.pack()
        T = Text(self.folderPlaylist)
        T.place()
        T.insert(END, "Please select a folder\nwhich will then be converted\nto a supported playlist format.\n(WARNING:Please make sure all items in folder are MP3 type)\n\n\nNOTE:If playlist name already exists\nit will be overwrote")
        T.pack()

    def AddFile(self):
        File = askopenfilename(filetypes=self.mtypes)
        if not File:
            pass
        else:
            FCheck = File.split('.')
            FCheck = str(FCheck[-1])
            if str.casefold(FCheck) == 'mp3':
                self.Files.append(File)
            else:
                pass

    def FPlaylistMaker(self):
        PListName = self.PEntry.get()
        if not PListName:
            PListName = "Unknown"
            while os.path.exists("Playlists/" + PListName):
                x = 1
                PListName += str(x)
                x += 1
        else:
            pass

        while os.path.exists("Playlists/" + PListName):
            x = 1
            PListName += str(x)
            x += 1
        with open("Playlists/" + PListName + ".pylist", "w") as F:
            for x in self.Files:
                F.write(x + "\n")
        self.FinFile.destroy()
        self.filePlaylist.destroy()

    def FinFile(self):
        self.FinFile = Toplevel()
        self.app = (self.FinFile)
        self.FinFile.iconbitmap("MPython3Icon.ico")
        self.FinFile.title("Enter Playlist name")
        self.FinFile.geometry("300x100")
        Lab = Label(self.FinFile, text="Playlist name:")
        Lab.pack(side=LEFT)
        self.PEntry = Entry(self.FinFile)
        self.PEntry.pack(side=LEFT)
        PBut = Button(self.FinFile, text="Submit", command=self.FPlaylistMaker)
        PBut.pack(side=LEFT)

    def filePlaylist(self):
        self.Files = []
        self.filePlaylist = Toplevel()
        self.app = (self.filePlaylist)
        self.filePlaylist.iconbitmap("MPython3Icon.ico")
        self.filePlaylist.title("Playlist from files")
        self.filePlaylist.geometry("350x150")
        AddB = Button(self.filePlaylist, text="Add file", command=self.AddFile)
        AddB.pack()
        FinB = Button(self.filePlaylist, text="Finish", command=self.FinFile)
        FinB.pack()
        T = Text(self.filePlaylist)
        T.insert(END, "To add a file to the playlist click the add button\nDo this as many times as you wish\nThen click ok to finalise")
        T.pack()

    def TimeThread(self):

        self.thread = tr.Thread(target=self.MPos, args=())
        self.thread.daemon = True
        try:
            self.MPosL.destroy()
        except:
            pass
        self.thread.start()

    def MPos(self):
        MP3Pos = 0
        self.ThreadBreak = False
        while mixer.music.get_busy() == 1:
            MP3Pos = mixer.music.get_pos()
            MP3Pos = MP3Pos / 1000
            MP3Pos = MP3Pos / 60
            self.PosStr = str(round(MP3Pos, 2)) + "/" + str(self.ALength)
            try:
                self.MPosL.destroy()
            except:
                pass
            if self.ThreadBreak == True:
                self.MPosL.destroy()
                break
            else:
                pass
            self.MPosL = Label(self, text=self.PosStr)
            self.MPosL.place()
            self.MPosL.pack()

            t.sleep(self.interval)

    def pauser(self):
        mixer.music.pause()

    def unpauser(self):
        mixer.music.unpause()

    def stopper(self):
        mixer.music.stop()
        try:
            self.MPosL.destroy()
            self.playing.destroy()
        except:
            pass

    def rewinder(self):
        mixer.music.stop()
        mixer.music.play()

    def recent(self):
        try:
            self.RP.destroy()
        except:
            pass
        self.RP = Label(self, text=self.recentlyPlayed)
        self.RP.place()
        self.RP.pack()

    def clear(self):
        self.recentlyPlayed = ["Recently played:\n"]
        self.recent()

    def subVol(self):
        self.vol = self.v.get()
        mixer.music.set_volume(float(self.vol))
        self.volChange.destroy()

    def volChange(self):
        i = "Please enter a value between 0 and 1\nIf you would like to\n permanently change the volume\nplease change the pref.py volume."
        self.volChange = Toplevel()
        self.app = (self.volChange)
        self.volChange.title("Volume")
        self.volChange.geometry("300x200")
        self.volChange.iconbitmap("MPython3Icon.ico")
        self.pack(fill=BOTH, expand=1)
        info = Label(self.volChange, text=i)
        info.pack()
        self.v = Entry(self.volChange)
        self.v.place(x=0, y=0)
        self.v.pack()
        self.curVolStr = "Current volume is " + str(mixer.music.get_volume())
        self.curVol = Label(self.volChange, text=self.curVolStr)
        self.curVol.place(x=120, y=0)
        self.curVol.pack()
        submit = Button(self.volChange, text="Submit", command=self.subVol)
        submit.place(x=90, y=0)
        submit.pack()

    def current(self):
        try:
            self.playing.destroy()
        except:
            pass
        self.playing = Label(self, text=self.dir)
        self.playing.place(x=45, y=350)
        self.playing.pack()

    def player(self):
        self.ThreadBreak = True
        if mixer.music.get_busy() == 1:
            self.stopper()
        else:
            pass
        self.dir = askopenfilename(filetypes=self.mtypes)
        self.recentlyPlayed.append(self.dir + "\n")
        self.audio = MP3(self.dir)
        self.ALength = round(self.audio.info.length / 60, 2)
        mixer.music.stop()
        mixer.music.load(self.dir)
        mixer.music.play()
        self.recent()
        self.current()
        self.TimeThread()

    def init_window(self):  # main window
        # changing the title of the master widget
        self.master.title("MPython3")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        mixer.init()
        mixer.music.set_volume(self.vol)
        self.MBar = Menu(self.master)
        self.master.config(menu=self.MBar)
        self.MBar.add_command(label="Play song", command=self.player)
        self.PlayMenu = Menu(self.master)
        self.PlayMenu.add_command(
            label="Change Volume", command=self.volChange)
        self.PlayMenu.add_command(label="Pause", command=self.pauser)
        self.PlayMenu.add_command(label="Resume", command=self.unpauser)
        self.PlayMenu.add_command(label="Restart song", command=self.rewinder)
        self.PlayMenu.add_command(label="Stop song", command=self.stopper)
        self.PlaylistMenu = Menu(self.MBar)
        self.PlaylistMenu.add_command(
            label="Play playlist", command=self.playlistPlay)
        self.PlaylistMenu.add_command(
            label="Shuffle playlist", command=self.playlistShuffle)
        self.PlaylistMenu.add_command(
            label="Stop playlist", command=self.playlistStop)
        self.PlaylistMenu.add_command(
            label="Create playlist from folder", command=self.folderPlaylist)
        self.PlaylistMenu.add_command(
            label="Create playlist from files", command=self.filePlaylist)
        self.MBar.add_cascade(
            label="Controls", underline=0, menu=self.PlayMenu)
        self.MBar.add_cascade(
            label="Playlists", underline=0, menu=self.PlaylistMenu)
        self.MBar.add_cascade(label="Clear recent", command=self.clear)
        self.MBar.add_cascade(label="Quit", command=sys.exit)
        self.LogoLabel = Label(self, image=self.LogoLab)
        self.LogoLabel.place(x=200, y=400)
        self.LogoLabel.pack()


#################################main##################################
root = Tk()
root.geometry("700x500")
app = Window(root)
root.iconbitmap("MPython3Icon.ico")
root.mainloop()
