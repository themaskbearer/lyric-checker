
from tkinter import *
import requests
from bs4 import BeautifulSoup
import time


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
        print("Getting album...")
        URL = "https://www.azlyrics.com/" + self._artist_text.get()[0] + "/" + self._artist_text.get() + ".html"
        print(URL)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
        r = requests.get(URL, headers=headers)

        soup = BeautifulSoup(r.content, 'html5lib')

        albums = soup.find_all('div', attrs={'class': 'album'})
        for album in albums:
            if self._album_text.get() in str(album):
                selected_album = album

        songs = []
        for sibling in selected_album.next_siblings:
            if "id=" in str(sibling):
                break

            if "comment" in str(sibling):
                continue

            if sibling is None:
                continue

            if str(sibling).isspace() or "br/" in str(sibling):
                continue

            songs.append(sibling)

        print("Getting songs...")
        clean_album = True
        for song in songs:
            new_url = song["href"]
            new_url = "https://www.azlyrics.com/" + new_url[3:]
            song_request = requests.get(new_url, headers=headers)

            songsoup = BeautifulSoup(song_request.content, 'html5lib')
            if not self.check_song(songsoup):
                clean_album = False
                print("Failing song: " + new_url)

            time.sleep(2)

        if clean_album:
            self._check_result["text"] = "Pass!"
            self._check_result["fg"] = "green"
        else:
            self._check_result["text"] = "Fail!"
            self._check_result["fg"] = "red"

    def check_song(self, song):
        div = song.find('div', attrs={'class': 'ringtone'})

        for sibling in div.next_siblings:
            copy_comment = "!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that."
            if copy_comment in str(sibling):
                lyrics = str(sibling)
                break

        return self.check_profanity(lyrics)

    def check_profanity(self, lyrics):
        contraband = {"shit", "damn", "fuck", "bitch", " ass "}

        for word in contraband:
            if word in lyrics:
                return False

        return True

    def stop(self):
        self.quit()


def on_window_close():
    app.stop()


root = Tk()
root.protocol("WM_DELETE_WINDOW", on_window_close)
app = Application(master=root)
app.mainloop()
root.destroy()
