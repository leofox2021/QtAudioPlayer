import os, sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from audio_import import AudioFileImport
from pop_ups.playlist_name import PlaylistName
from pop_ups.warning import WarningMessage

class PlaylistImport:

    def __init__(self, all_playlists, all_songs, playlist, info_bar):
        self.path = os.path.join(os.getcwd(), 'playlists/')
        self.playlists = []
        self.all_playlists = all_playlists
        self.all_songs = all_songs
        self.playlist = playlist
        self.info_bar = info_bar
        self.filenames = []
        self.name = None
        self.x = AudioFileImport(self.all_songs, self.playlist)
        self.y = PlaylistName(self.name)


    #Display all existing playlists
    #in the 'playlists' folder
    def displayPlaylists(self):
        self.playlists.clear()
        self.all_playlists.clear()
        in_path = os.listdir(self.path)
        print(self.path)

        for var in in_path:

            try:
                file = open(self.path + var)
                q = len(file.read().splitlines())
            except UnicodeDecodeError:
                file.close()
                print('This playlist cannot be opened.')
                print('It will be deleted immediately.')
                os.remove(self.path + var)
            else:
                file = open(self.path + var)
                q = len(file.read().splitlines())
                self.playlists.append(f'{self.path}{var}')
                self.all_playlists.addItem(f'{var[:-4]} ({q})')
                file.close()
                print(var)


    #Clear all songs displayed
    def clearPlaylist(self):
        self.playlist.clear()
        self.filenames.clear()
        self.all_songs.clear()


    #Open a playlist on click
    def openPlaylist(self):
        current_playlist = self.all_playlists.currentRow()
        dir = self.playlists[current_playlist]

        #Avoid crashing due to absent playlist
        try:
            file = open(dir)
        except FileNotFoundError:
            self.info_bar.setText('This playlist has been corrupted/removed')
        else:
            self.clearPlaylist()
            file = open(dir)
            var2 = file.read().splitlines()

            for var in var2:
                self.filenames.append(var)
                print(var)

            self.x.addToAllSongs(self.filenames)


    #Create a new playlist
    def createPlaylist(self):
        self.y.launch()

        def returnName():
            self.name = ''
            self.name = self.y.name_input.toPlainText()
            print(self.name)

        def openFile():
            #Avoid crashing due to file existing and invalid playlist name
            try:
                file = open(f'{self.path}{self.name}.m3u', 'w+', encoding="utf-8")
            except FileExistsError:
                self.info_bar.setText('This name already exists.')
            except UnicodeDecodeError:
                self.info_bar.setText("This name can't be set.")
            except OSError:
                self.info_bar.setText("This name can't be set.")
            else:
                #Open a playlist for writing
                file = open(f'{self.path}{self.name}.m3u', 'w+', encoding="utf-8")

                #Write all entries
                for var in self.all_songs:
                    print(var)
                    file.write(var + '\n')

                #Close the file
                file.close()

            #Refresh playlists and the quantity of songs
            self.displayPlaylists()

        self.y.button_box.accepted.connect(returnName)
        self.y.button_box.accepted.connect(openFile)


    #Update an existing playlist
    def updatePlaylist(self):
        #To avoid carshing due to playlist not being selected
        try:
            x = self.all_playlists.currentItem().text()
        except AttributeError:
            print("Please select your playlist first.")
        else:
            x = self.all_playlists.currentItem().text()

            #Remove the old versiong of playlist
            #Otherwise 2 versions will be created
            print(f'{self.path}{x[:-4]}.m3u')
            os.remove(f'{self.path}{x[:-4]}.m3u')
            file = open(f'{self.path}{x[:-4]}.m3u', 'w+', encoding="utf-8")

            for var in self.all_songs:
                print(var)
                file.write(var + '\n')

            file.close()
            #self.playlists.clear()
            #self.all_playlists.clear()
            self.displayPlaylists()
