__author__ = 'Odd'

import tkinter as tk
import tkinter.filedialog
import tvshowmover
import OddTools.oddconfig as oddconfig
import os

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.config()
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.path_frame = tk.Frame(self)
        oddconfig.read(os.path.dirname(os.path.realpath(__file__)) + "\settings.ini")
        print(oddconfig.read_files)
        inn = oddconfig.get_setting("input")
        self.in_path = create_fileselect(self.path_frame, True, inn)
        self.in_path.pack(side="top")
        out = oddconfig.get_setting("output")
        self.out_path = create_fileselect(self.path_frame, True, out)
        self.out_path.pack(side="top")
        self.path_frame.pack()
        self.display_button = tk.Button(self, text="Find", command=self.list_shows)
        self.display_button.pack()
        self.showlist = tk.Frame(self)
        self.showlist.pack(side="left")

        MOVE = tk.Button(self, text="Move", command=self.movefiles)
        MOVE.pack(side="bottom")
        QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        QUIT.pack(side="bottom")

    def list_shows(self):
        self.showlist.destroy()
        self.selected = set()
        self.showlist = tk.Canvas(self)

        def select(event):
            if event.widget not in self.selected:
                event.widget.config(bg="red")
                self.selected.add(event.widget)
            else:
                self.selected.remove(event.widget)
                event.widget.config(bg="white")

        i = 0
        for item in tvshowmover.get_showfiles(
                self.path_frame.winfo_children()[0].winfo_children()[0].get()):

            initem = tk.Label(self.showlist, text=item, bg="white")
            initem.grid(row=i, column=0, sticky=tk.W)
            initem.bind("<ButtonRelease 1>", select)
            tk.Label(self.showlist, text=self.path_frame.winfo_children()[1].winfo_children()[0].get() + "\\" +
                                        tvshowmover.newname_show(item)).grid(row=i, column=1, sticky=tk.W)
            i += 1
        scroll = tk.Scrollbar(self.showlist)
        scroll.grid(column=2, row=0, rowspan=i)
        self.showlist.pack(side="left")

    def movefiles(self):
        for item in self.selected:
            item_id = item.cget("text")
            tvshowmover.move_tvshow(item_id, self.path_frame.winfo_children()[1].winfo_children()[0].get())
        self.list_shows()


def create_fileselect(root, dir=True, value="", func=None):
    file_frame = tk.Frame(root)
    entry = tk.Entry(file_frame)
    entry.insert(0, value)

    def open_file():
        if dir:
            newpath = tk.filedialog.askdirectory()
        else:
            newpath = tk.filedialog.askopenfilename()

        if entry.get() != newpath and newpath != '':
            entry.delete(0, tk.END)
            entry.insert(0, newpath)

    entry.config(width=30)
    #entry.bind("<ButtonRelease 1>", open_file)
    entry.pack(side="left")

    button = tk.Button(file_frame, command=open_file)
    button.config(text="Select")

    button.pack(side="left")
    return file_frame

if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(master=root)
    app.mainloop()