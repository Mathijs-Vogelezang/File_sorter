import listing
import sort
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)


def setsourceFolder():
    try:
        src = filedialog.askdirectory()
        if not src == '':
            source.set(src)
            if not destination.get() == '':
                sortbtn.state(['!disabled'])
    except FileNotFoundError:
        pass


def setdestinationFolder():
    try:
        dest = filedialog.askdirectory()
        if not dest == '':
            destination.set(dest)
            subfolders.clear()
            subfolders.extend(listing.listfolders(dest))
            subfolderBools.clear()

            for checkbutton in checkbuttons:
                checkbutton.grid_forget()

            checkbuttons.clear()

            for i in range(len(subfolders)):
                subfolderBools.append(BooleanVar(value=True))
                checkbuttons.append(ttk.Checkbutton(checkboxframe, text=subfolders[i], variable=subfolderBools[i],
                                    command=lambda: checkchanged(i)))
                checkbuttons[i].grid(column=0, row=i, sticky=(E, W))

            addbtn.state(['!disabled'])

            if not source.get() == '':
                sortbtn.state(['!disabled'])

        folderCanvas.update_idletasks()
        folderCanvas.configure(scrollregion=folderCanvas.bbox('all'))
    except FileNotFoundError:
        pass


def sortcommand():
    for i in range(len(subfolderBools) - 1, -1, -1):
        if not subfolderBools[i].get():
            subfolders.pop(i)
        elif not os.path.exists(os.path.join(destination.get(), subfolders[i])):
            os.mkdir(os.path.join(destination.get(), subfolders[i]))

    currentfile = StringVar()
    currentfilenumber = IntVar()
    progress = StringVar()
    files = listing.listfiles(source.get())

    progressdialog = Toplevel(root, width=400, height=150)
    progressdialog.grid_propagate(False)
    progressdialog.resizable(False, False)
    progressframe = ttk.Frame(progressdialog, width=400, height=200, padding=5)
    progressframe.grid_propagate(False)
    progressframe.grid(column=0, row=0)
    progressbar = ttk.Progressbar(progressframe, orient=HORIZONTAL, mode='determinate', variable=currentfilenumber, length=390, maximum=len(files))
    progressbar.grid(column=0, row=0, sticky=W)
    ttk.Label(progressframe, textvariable=currentfile, width=400).grid(column=0, row=1, sticky=W)
    ttk.Label(progressframe, textvariable=progress).grid(column=0, row=2, sticky=W)

    for child in progressframe.winfo_children():
        child.grid_configure(pady=5)

    progressdialog.transient(root)
    progressdialog.wait_visibility()
    progressdialog.grab_set()

    for i in range(len(files)):
        currentfile.set(files[i].replace(source.get(), ''))
        progress.set(str(i+1) + ' from ' + str(len(files)))
        currentfilenumber.set(i)
        sort.sortfile(files[i], destination.get(), subfolders)
        progressdialog.update_idletasks()

    progressdialog.grab_release()
    progressdialog.destroy()


def add():
    inputframe.grid(column=0, row=6, columnspan=2, sticky=(E, W))
    inputEntry.focus()
    root.bind('<Return>', addfolder)


def addfolder(*args):
    if not addsubfolder.get() == '':
        if not addsubfolder.get() in subfolders:
            subfolders.append(addsubfolder.get())
            length = len(subfolders) - 1
            subfolderBools.append(BooleanVar(value=True))
            checkbuttons.append(ttk.Checkbutton(checkboxframe, text=subfolders[length], variable=subfolderBools[length]))
            checkbuttons[length].grid(column=0, row=length, sticky=(E, W))
            inputframe.grid_remove()
            addsubfolder.set('')
            folderCanvas.update_idletasks()
            folderCanvas.configure(scrollregion=folderCanvas.bbox('all'))
            folderFrame.focus()
            root.unbind('<Return>')


def checkchanged(index):
    # checkfont = font.Font()
    # checkfont.configure(overstrike=subfolderBools[index].get())
    # checkbuttons[index]['font'] = checkfont
    pass


def mousewheel(event):
    folderCanvas.yview_scroll(int(-1*(event.delta/120)), 'units')


def bindtomousewheel(event):
    folderCanvas.bind_all("<MouseWheel>", mousewheel)


def unbindfrommousewheel(event):
    folderCanvas.unbind_all('<MouseWheel>')


root = Tk()
root.title('File sorter')
root.minsize(750, 600)
root.eval('tk::PlaceWindow . center')

wheight = root.winfo_height()
wwidth = root.winfo_width()
sheight = root.winfo_screenheight()
swidth = root.winfo_screenwidth()

x = int(swidth/2 - wwidth/2)
y = int(sheight/2 - wheight/2)

root.geometry("{}x{}+{}+{}".format(wwidth, wheight, x, y))

mainframe = ttk.Frame(root, padding=5)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

source = StringVar()
destination = StringVar()
subfolders = []
subfolderBools = []
addsubfolder = StringVar()
checkbuttons = []

sourcebtn = ttk.Button(mainframe, text='Select source folder', command=setsourceFolder)
sourcebtn.grid(column=0, row=0, columnspan=2, sticky=(N, W))
ttk.Label(mainframe, textvariable=source).grid(column=0, row=1, columnspan=2, sticky=(N, W))
destinationbtn = ttk.Button(mainframe, text='Select destination folder', command=setdestinationFolder)
destinationbtn.grid(column=0, row=2, columnspan=2, sticky=(N, W))
ttk.Label(mainframe, textvariable=destination).grid(column=0, row=3, columnspan=2, sticky=(N, W))

folderFrame = ttk.Frame(mainframe, borderwidth=5, relief='sunken', width=400, height=200)
folderFrame.grid(column=0, row=4, columnspan=2, sticky=(N, E, S, W))
folderFrame.grid_propagate(False)
folderCanvas = Canvas(folderFrame, highlightthickness=0)
folderCanvas.grid(column=0, row=0, sticky=(N, E, S, W))
checkboxframe = ttk.Frame(folderCanvas)
folderCanvas.create_window(0, 0, anchor='nw', window=checkboxframe)

folderBar = ttk.Scrollbar(folderFrame, orient=VERTICAL, command=folderCanvas.yview)
folderBar.grid(column=1, row=0, sticky=(N, S))
folderCanvas.configure(yscrollcommand=folderBar.set)
folderCanvas.bind('<Enter>', bindtomousewheel)
folderCanvas.bind('<Leave>', unbindfrommousewheel)

addbtn = ttk.Button(mainframe, text='Add folder', command=add)
addbtn.grid(column=0, row=5, sticky=W)
addbtn.state(['disabled'])
sortbtn = ttk.Button(mainframe, text='Sort', command=sortcommand)
sortbtn.grid(column=1, row=7, sticky=E)
sortbtn.state(['disabled'])

inputframe = ttk.Frame(mainframe)
inputEntry = ttk.Entry(inputframe, textvariable=addsubfolder)
inputEntry.grid(column=0, row=0, sticky=(E, W))
ttk.Button(inputframe, text='Add', command=addfolder).grid(column=1, row=0)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.rowconfigure(4, weight=1)
folderFrame.columnconfigure(0, weight=1)
folderFrame.rowconfigure(0, weight=1)
inputframe.columnconfigure(0, weight=1)

root.mainloop()
