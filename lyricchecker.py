
from tkinter import *
import requests
from bs4 import BeautifulSoup


class Application(Frame):
    CONST_MOUSE_TRACK_REFRESH_sec = 0.1

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self._artist_label = Label(self)
        self._artist_text = Entry(self)

        self._album_label = Label(self)
        self._album_text = Entry(self)

        self._run_check_button = Button(self)
        self._check_result = Label(self)

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self._artist_label["text"] = "Artist Name:"
        self._artist_label.grid(row=0, column=0, sticky=W)

        self._artist_text.grid(row=0, column=1)
        self._artist_text.insert(0, "blessthefall")

        self._album_label["text"] = "Album Name:"
        self._album_label["justify"] = LEFT
        self._album_label.grid(row=1, column=0)

        self._album_text.grid(row=1, column=1)
        self._album_text.insert(0, "Hollow Bodies")

        self._run_check_button["command"] = self.run_lyric_check
        self._run_check_button["text"] = "Check Lyrics"
        self._run_check_button.grid(row=2, column=0, columnspan=2)

        self._check_result.grid(row=3, column=0, columnspan=2)

    def run_lyric_check(self):
        URL = "https://www.azlyrics.com/" + self._artist_text.get()[0] + "/" + self._artist_text.get() + ".html"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
        r = requests.get(URL, headers=headers)

        soup = BeautifulSoup(r.content, 'html5lib')


        self._check_result["text"] = "Pass!"
        # self._check_result["fg"] = "green"

    def stop(self):
        self.quit()


def on_window_close():
    app.stop()


root = Tk()
root.protocol("WM_DELETE_WINDOW", on_window_close)
app = Application(master=root)
app.mainloop()
root.destroy()
