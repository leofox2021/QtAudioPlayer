import sys, os, numpy, audio_import, media_player
from mutagen.id3 import ID3
from mutagen import File
from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QApplication, QMenuBar, QStyleFactory
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.Qt import *
from media_player import MediaPlayer
from audio_import import AudioFileImport
from playlist_import import PlaylistImport


Form, Window = uic.loadUiType("gui/audio_player.ui")
Form2, Window2 = uic.loadUiType("gui/playlists.ui")


#Set up window
app = QApplication(sys.argv)
x = QStyleFactory.keys()
print(x)
#app.setStyle((QStyleFactory.create("Windowsvista")))


window = Window()
form = Form()
form.setupUi(window)
name = form.label


#Playlists window
app_2 = QApplication([])
window_2 = Window2()
form_2 = Form2()
form_2.setupUi(window_2)

def openPlaylistWindow():
    #App execution
    window_2.show()
    app_2.exec()


#QT elements
slider = form.horizontalSlider #Position slider
play = form.pushButton #Play button
stop = form.pushButton_2 #Stop button
prev = form.pushButton_4 #Play previous track
next = form.pushButton_5 #Play next track
remove_song = form.pushButton_6 #Remove song from a playlist
save_to_playlist = form.pushButton_7 #Create a new playlist
clear = form.pushButton_8 #Clear button
openfile = form.pushButton_3 #Open file dialog button
shuffled = form.pushButton_9 #Shuffle button
update_playlist = form.pushButton_10 #Update playlist
playlists_button = form.pushButton_11 #Playlists button
cover = form.label_3 #Album art
title = form.label #Song title
artist = form.label_4 #Song artist
album = form.label_5 #Song album
timer_display = form.label_6 #Show time
info_bar = form.label_7 #Info bar
volume_label = form.label_10 #volume text
volume = form.dial #Volume dial
playlist = form.listWidget #Playlist window
volume_value = form.label_2 #Volume value label
all_playlists = form_2.listWidget
player = QMediaPlayer() #Player


#Menu
preferences = form.actionPreferences

#Variables
all_songs = []


#Theming 
def setWidgetStyle(style):
    app.setStyle((QStyleFactory.create(style)))
    app_2.setStyle((QStyleFactory.create(style)))

def lightTheme():

    #Windows
    window.setStyleSheet('background: white')
    window_2.setStyleSheet('background: white')

    #Buttons
    #(All buttons set to light gray)
    save_to_playlist.setStyleSheet('background: #F0F0F0')
    clear.setStyleSheet('background: #F0F0F0')
    openfile.setStyleSheet('background: #F0F0F0')
    remove_song.setStyleSheet('background: #F0F0F0')
    update_playlist.setStyleSheet('background: #F0F0F0')
    playlists_button.setStyleSheet('background: #F0F0F0')
    playlist.setStyleSheet('background: #F0F0F0')

    #Icons
    play.setIcon(QtGui.QIcon('icons/play.png'))
    play.setIconSize(QtCore.QSize(12,12))

    #STOP
    stop.setIcon(QtGui.QIcon('icons/stop.png'))
    stop.setIconSize(QtCore.QSize(12,12))

    #PREVIOUS
    prev.setIcon(QtGui.QIcon('icons/backward.png'))
    prev.setIconSize(QtCore.QSize(24,24))

    #NEXT
    next.setIcon(QtGui.QIcon('icons/forward.png'))
    next.setIconSize(QtCore.QSize(24,24))

    #SHUFFLE
    shuffled.setIcon(QtGui.QIcon('icons/shuffle.png'))
    shuffled.setIconSize(QtCore.QSize(24,24))

    

def darkTheme():
    #Buttons
    window.setStyleSheet('background: #282829')
    window_2.setStyleSheet('background: #282829')
    save_to_playlist.setStyleSheet('background: #414142')
    clear.setStyleSheet('background: #414142')
    openfile.setStyleSheet('background: #414142')
    remove_song.setStyleSheet('background: #414142')
    update_playlist.setStyleSheet('background: #414142')
    playlists_button.setStyleSheet('background: #414142')

    #Light gray / white for text
    palette = QPalette()
    palette.setColor(QPalette.Foreground, QtGui.QColor('#F0F0F0'))

    #Light gray / white for button text
    palette2 = QPalette()
    palette2.setColor(QPalette.ButtonText, QtGui.QColor('#F0F0F0'))

    #Light gray / white for listwidget
    palette3 = QPalette()
    palette3.setColor(QPalette.Text, QtGui.QColor('#F0F0F0'))

    #Button text
    remove_song.setPalette(palette2)
    clear.setPalette(palette2)
    save_to_playlist.setPalette(palette2)
    openfile.setPalette(palette2)
    remove_song.setPalette(palette2)
    update_playlist.setPalette(palette2)
    playlists_button.setPalette(palette2)

    #QLabels 
    title.setPalette(palette)
    artist.setPalette(palette)
    album.setPalette(palette)
    cover.setPalette(palette)
    volume_value.setPalette(palette)
    volume_label.setPalette(palette)
    info_bar.setPalette(palette)
    timer_display.setPalette(palette)

    #Widgets
    playlist.setStyleSheet('background: #414142')
    playlist.setPalette(palette3)
    all_playlists.setStyleSheet('background: #414142')
    all_playlists.setPalette(palette3)
    slider.setStyleSheet('handle.horizontal: #F0F0F0')

    play.setIcon(QtGui.QIcon('icons/play_dark.png'))
    play.setIconSize(QtCore.QSize(12,12))

    #STOP
    stop.setIcon(QtGui.QIcon('icons/stop_dark.png'))
    stop.setIconSize(QtCore.QSize(12,12))

    #PREVIOUS
    prev.setIcon(QtGui.QIcon('icons/backward_dark.png'))
    prev.setIconSize(QtCore.QSize(24,24))

    #NEXT
    next.setIcon(QtGui.QIcon('icons/forward_dark.png'))
    next.setIconSize(QtCore.QSize(24,24))

    #SHUFFLE
    shuffled.setIcon(QtGui.QIcon('icons/shuffle_dark.png'))
    shuffled.setIconSize(QtCore.QSize(24,24))


#Style to assign 
current_theme = None
current_style = None
file = open('config/theme.txt', 'r+', encoding="utf-8") 
a = file.read()
print(file.readlines())

#Read theme config file 
#And set a theme according to it
if 'fusion' in a:
    current_style = 'Fusion'
elif 'windows' in a: 
    current_style = 'Windows'
elif 'windows_vista' in a:
    current_style = 'windowsvista'
else:
    #Default style is always fusion
    file.write('\n' + 'style = fusion')
    current_style = 'Fusion'

if 'light' in a: 
    lightTheme()
    current_theme = 'light'
elif 'dark' in a:
    darkTheme()
    current_theme = 'dark'
else:
    lightTheme()
    file.write('\n' + 'theme = light')

file.close()
setWidgetStyle(current_style)


#Initial values when the player is started
volume.setRange(0, 100)
volume_value.setText(f'{volume.value()}')
title.setText('Open a music file')
artist.setText('-')
album.setText('-')
slider.setTickInterval(1000)


#Media player class
#  INCLUDES:
#  Play, pause, stop functions
#  Tracking player position, changing volume
#  Displayling tags, displaying time
x = MediaPlayer(player, timer_display, play, title, artist, album, slider, volume, volume_value, cover, playlist, all_songs, shuffled, current_theme)

#Audio File Import class
#  INCLUDES:
#  Importing files to the 'all_songs' list, using QFileDialog
#  Displaying imported songs in the 'playlist' ListView
#  Current track, next track, previous track methods
#  (each of them returns a 'current song' value that represents an exact path to respective track)
y = AudioFileImport(all_songs, playlist)

#Playlist Import class
#  INCLUDES:
#  Creating a playlist, opening a playlist,
#  Display all playlists in the 'playlists' folder in working directory
z = PlaylistImport(all_playlists, all_songs, playlist, info_bar)


#Load all existing playlists into GUI
z.displayPlaylists()

preferences.triggered.connect(lambda: print('Testing'))

#Buttons
play.clicked.connect(x.playSong)
stop.clicked.connect(x.stopSong)
prev.clicked.connect(x.prevTrack)
next.clicked.connect(x.nextTrack)
openfile.clicked.connect(y.importFromFiles)
save_to_playlist.clicked.connect(z.createPlaylist)
clear.clicked.connect(z.clearPlaylist)
remove_song.clicked.connect(y.removeTrack)
update_playlist.clicked.connect(z.updatePlaylist)
playlists_button.clicked.connect(openPlaylistWindow)

#Playlist
playlist.itemDoubleClicked.connect(x.currentTrack)
all_playlists.itemDoubleClicked.connect(z.openPlaylist)


#Volume slider
volume.sliderMoved.connect(x.volumeChange)
volume.sliderPressed.connect(x.volumeChange)


#Player position and slider
player.positionChanged.connect(x.displayPosition)
slider.valueChanged.connect(x.autoForward)
slider.valueChanged.connect(x.showTime)
slider.sliderReleased.connect(x.changePosition)
slider.sliderMoved.connect(x.showTime)



#App execution
window.show()
app.exec()
