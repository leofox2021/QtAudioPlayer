from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from mutagen import File
import random

class AudioFileImport:

    def __init__(self, all_songs, playlist):
        self.all_songs = all_songs
        self.playlist = playlist
        self.current_song = None
        self.filenames = ''
        self.pixmap = QPixmap()


    #Import selected files
    def importFiles(self):
        self.filenames, _ = QFileDialog.getOpenFileNames()


    #Add selected songs to "all_songs" list
    #and to the playlist
    def addToAllSongs(self, filenames):

        #Set the last row in playlist
        count = 0
        if self.playlist.count() != 0:
            count = self.playlist.count()
        else:
            pass

        #Record opened files into 'directory' variable
        if filenames == None:
            pass
        else:
            for var in filenames:
                self.all_songs.append(var)


            #Print tags into playlist
            for var2 in filenames:
                    #Avoid crashing due to absent title tag
                try:
                    audio_file = File(var2)
                    title = audio_file["TIT2"].text[0]
                except Exception:
                    title = 'Unknown'
                else:
                    title = audio_file["TIT2"].text[0]


                    #Avoid crashing due to absent artist tag
                try:
                    audio_file = File(var2)
                    artist = audio_file['TPE1'].text[0]
                except Exception:
                    artist = 'Unknown'
                else:
                    artist = audio_file['TPE1'].text[0]
                    #Final playlist name

                self.playlist.addItem(f'{artist} - {title}')


                #Avoid crashing due to absent covers
                try:
                    file = File(var2)
                    for tag in file.tags.values():
                        if tag.FrameID == 'APIC':
                            self.pixmap.loadFromData(tag.data)
                            break
                except Exception:
                    self.playlist.item(count).setIcon(QtGui.QIcon('icons/no_icon.png'))
                else:
                    file = File(var2)
                    for tag in file.tags.values():
                        if tag.FrameID == 'APIC':
                            self.pixmap.loadFromData(tag.data)
                            break
                    self.playlist.item(count).setIcon(QtGui.QIcon(self.pixmap))

                count +=1


    #Import selected files and add them into playlist
    #the methods were separated due to "addToAllSongs" method
    #being applied elsewhere.
    def importFromFiles(self):
        self.importFiles()
        self.addToAllSongs(self.filenames)


    #Play selected track
    def currentTrack(self):
        #Avoid crashing due to index out of range
        try:
            self.current_song = self.playlist.currentRow()
        except IndexError:
            pass
        else:
            self.current_song = self.playlist.currentRow()

        return self.current_song



    #Play next track
    def nextTrack(self):
        #Avoid crashing due to index out of range
        try:
            self.current_song = self.playlist.currentRow() + 1
        except IndexError:
            pass
        else:
            #If last song is selected, disable flipping forward
            #To avoid IndexErrors
            if self.current_song >= len(self.all_songs):
                self.current_song = self.playlist.currentRow()
            else:
                self.current_song = self.playlist.currentRow() + 1
                self.playlist.setCurrentRow(self.current_song)

        return self.current_song


    #Play previous track
    def previousTrack(self):
        #Avoid crashing due to index out of range
        try:
            self.current_song = self.playlist.currentRow() - 1
        except IndexError:
            pass
        else:
            self.current_song = self.playlist.currentRow() - 1

            #If song num1 selected, disable flipping back
            if self.current_song >= 0:
                self.playlist.setCurrentRow(self.current_song)
            else:
                self.current_song = self.playlist.currentRow()

        return self.current_song


    #Shuffled playback
    def shuffledMode(self):
        self.playlist.setCurrentRow(random.choice(range(len(self.all_songs))))
        self.current_song = self.playlist.currentRow()
        print(self.current_song)
        return self.current_song


    def removeTrack(self):
        try:
            x = self.playlist.currentRow()
            self.all_songs.pop(x)
        except IndexError:
            print('You have no song in a playlist!')
        else:
            self.playlist.takeItem(x)
