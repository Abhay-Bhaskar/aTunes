# Imports are here
import os
import time
import tkinter.messagebox
import threading
from tkinter import *
from pygame import mixer
from tkinter import filedialog
from mutagen.mp3 import MP3

# Global Variables go here

root = Tk()  # creates a window under the variable name root which spans the whole length of window and has the
# left_frame and right_frame
mixer.init()  # initialising the mixer
paused = FALSE
muted = FALSE  # Set it to muted = FALSE(unmuted) to be able to use the mute_music function in  logically correct way
play = PhotoImage(file="images/play.png")  # Don't need "@" sign for specifying paths when using PhotoImage function
vol = PhotoImage(file="images/vol.png")  # Volume image for unmuted state
mute = PhotoImage(file="images/mute.png")  # Volume image for muted state
playlist = []  # An array created to store the entire path and the directory of the song we add to the playlist_box
'''We need an array to store the entire filepath because that will need to be accessed in order to play the music 
   selected from the playlist_box. Without the full path the song cannot be played'''

# Functions will be here!!


def browse_song():  # The command used to open the browse window to browse to and select the song we want to play
    global song_path
    song_path = filedialog.askopenfilename()  # Opens the browse dialogue box
    add_music(song_path)  # Calls the function that enables us to add the music to the listbox


def about_us():  # The task being performed when the about us cascade option is clicked
    tkinter.messagebox.showinfo('About us', 'This music player has been created by Abhay Bhaskar on 24th December 2018')


def show_details(play_song):
    file_data = os.path.splitext(play_song)  # Takes in the currently selected song in the playlist
    '''The file_data stores the list containing two elements, the first element(index = 0) is the path of the song and 
       the name of the song, the second element(index = 1) is the extension of the song '''

    if file_data[1] == '.mp3':  # Checks if the file extension is .mp3
        audio = MP3(play_song)  # stores the metadata of the song
        total_length = audio.info.length  # Retrieves the length of the song from the metadata

    else:
        a = mixer.Sound(play_song)  # A variable used for storing the song that we are loading to play
        total_length = a.get_length()  # The length of the song(in seconds) that is being played

    mins, secs = divmod(total_length, 60)
    # Divides the total_length by 60 and stores the quotient in mins and remainder in secs
    mins = round(mins)  # Rounding off the original number of mins and storing it
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    '''The above format is to show the length of the track being played in the format --:--. The 02d states that the the 
       numbers before and after the : should be in two digits and if it happens to be
       a one digit number, make it a two digit number by suffixing a 0 in front of the digit'''
    lengthlabel['text'] = "Total Length -- " + " " + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    '''Since the start_count() function involves time delay loops, the python interpreter will be stuck in it for a 
        considerable amount of time and during that time nothing else will work. So we have to use threading to ensure 
        that all the individual functions of the program run simultanoeusly in a smooth way. The command assigns a 
        thread to run the start_count() function.'''
    t1.start()  # The Thread is started


def start_count(t):
    global paused
    #  mixer.music.get_busy() returns false when we press the stop button and the music stops playing stopping the timer
    while t and mixer.music.get_busy():
        if paused:  # The condition to stop the timer once the song is paused
            continue

        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Time Remaining -- " + " " + timeformat
            time.sleep(1)  # The time delay loop to ensure that t-=1 runs after every one second and not continously
            t -= 1  # Decreases the time left on the timer by 1 second everytime this line is executed


def pause_music():
    global paused  # Creating a variable that will be used to unpause the song
    paused = TRUE
    mixer.music.pause()  # mixer pauses the music that was playing
    status_bar['text'] = "Music Paused"  # Changes the text displayed in the status bar


def play_music():
    global paused  # Importing the value of paused value

    if paused:
        # This executes only if paused variable has been set to true
        mixer.music.unpause()  # Unpause the song
        # statusbar['text'] = "Music Resumed"
        # time.sleep(5)
        status_bar['text'] = "Playing Music -- " + os.path.basename(song_path)
        # Changes the text displayed in the status bar to playing music
        # The command os.path.basename(song) ensures that only the name of the song and not the path is visible
        paused = FALSE

    else:
        try:
            stop_music()
            time.sleep(1)
            '''The above lines of code destroy the thread whenever the play buton is pressed so that the timer reads the
               time remaining correctly. The sleep is 1 second because each iteration of the thread is of one second'''
            selected_song = playlist_box.curselection()  # creates a tuple to save the index number of the playlist_box
            #  item that we click on. curselection() is an inbuilt function of the Listbox
            selected_song = int(selected_song[0])
            # Converts the tuple to an integer that can be used to access the path of the song to be played

            play_it = playlist[selected_song]
            # Uses the integer value obtained from the previous statement as the index number for the playlist array to
            # get the path of the song that has to be played.

            mixer.music.load(play_it)  # mixer loads the song so that it can be played
            mixer.music.play()  # mixer plays the song
            status_bar['text'] = "Playing Music -- " + os.path.basename(play_it)
            show_details(play_it)
            # We send the path of the song being currently played as the parameter so that it can changes when we change
            #  the song

        except:
            tkinter.messagebox.showerror('Error!!', 'No Song Selected!! Please select a song to play!')


def stop_music():
    mixer.music.stop()  # mixer stops the music that was playing
    status_bar['text'] = "Music Stopped"  # Changes the text displayed in the status bar


def set_vol(val):  # Accepts the value at which the scale is released, the value is in string format
    volume = int(val)/100  # converts the value from the scale to integer format then divides it by 100
    mixer.music.set_volume(volume)
    # Accepts a value between 0 to 1 only and sets volume accordingly (hence the division by 100)


def rewind_music():
    global paused
    paused = FALSE  # Failsafe in case someone presses the rewind after pressing the pause button
    # Without the above line the timer will not restart
    # statusbar['text'] = "Rewinding Music"  # Change the status bar text
    # time.sleep(5)
    play_music()  # Play the music from the beginning


def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.5)  # Unmute the music and set a volume
        vol_bt.configure(image=vol)  # Change the icon from muted to Volume
        scale.set(50)  # Change the scale to default volume
        muted = FALSE  # Change the condition to be able to toggle between mute and unmute

    else:
        mixer.music.set_volume(0)  # Mute the music
        vol_bt.configure(image=mute)  # Change the icon from volume to muted
        scale.set(0)  # Change the scale to 0
        muted = TRUE  # Change the condition to be able to toggle between mute and unmute


def on_closing():  # This function overrides the abrupt closing of the music player
    stop_music()  # First the music is stopped
    root.destroy()  # Now the window is closed


def add_music(song):
    song = os.path.basename(song)  # Takes only the filename and not the path
    index = 0
    playlist_box.insert(index, song)  # Adds an item to the listbox
    playlist.insert(index, song_path)  # Adds the full path of the song to the playlist array
    index += 1  # Increments the index by 1 to add the next song at the next index


def remove_music():
    delete_song = playlist_box.curselection()
    delete_song = int(delete_song[0])
    playlist_box.delete(delete_song)  # Deleting the song from the playlist_box
    playlist.pop(delete_song)  # Deleting the directory of the song from the playlist array (list actually xD)


# Status Bar is declared here because it is the only widget using root and has to occupy the full x axis so it has been
# declared first to avoid clash with frames that will be created hereafter

status_bar = Label(root, text='Welcome to aTunes', relief=SUNKEN, anchor=W)
# Adds a status bar with the default text as a welcome message the effect of the status bar is sunken and the message
# is displayed at the extreme left of the status bar
status_bar.pack(side=BOTTOM, fill=X)  # Ensures that the status bar is at the bottom of the window and fills the x axis


# Frames Are Here

left_frame = Frame(root)
left_frame.pack(side=LEFT, padx=10, pady=10)

right_frame = Frame(root)
right_frame.pack(side=LEFT, padx=10, pady=10)

top_frame = Frame(right_frame)
top_frame.pack(padx=10, pady=10)

mid_frame = Frame(right_frame)
mid_frame.pack(padx=10, pady=10)

bot_frame = Frame(right_frame)
bot_frame.pack(padx=10, pady=10)

# Menus go here!!

# Creating a menu bar
menu_bar = Menu(root)  # creating a menubar to be displayed on top of the application window
root.config(menu=menu_bar)

# Creating the various submenus

# Creating the File cascading menu
submenu = Menu(menu_bar, tearoff=0)  # Creates a submenu and removes the dashed delimiter using the tearoff=0 command
menu_bar.add_cascade(label="File", menu=submenu)  # Creates a cascade menu named File as a sub-menu of the menubar
submenu.add_command(label="Open", command=browse_song)  # Adds a command named Open to the cascade menu under Files
submenu.add_command(label="Exit", command=root.destroy)
# Adds a command named Exit to the cascade menu under Files and adds a command to exit the window via destroy command

# Creating the Help cascading menu
submenu = Menu(menu_bar, tearoff=0)  # Creates a submenu and removes the dashed delimiter using the tearoff=0 command
menu_bar.add_cascade(label="Help", menu=submenu)  # Creates a cascade menu named Help as a sub-menu of the menubar
submenu.add_command(label="About us", command=about_us)
# Adds a command named About uss to the cascade menu under Files and adds a popup display

# root.geometry('300x300')  # changing the size of the window
root.title("aTunes")  # changes the name of the window
root.iconbitmap('@images/audio.XBM')  # specifies the path for the image of the app as shown beside the title
''' While specifying an icon in linux we have to use a .xbm fle and use an "@" sign at the beginning of the path
     While specifying an icon on widows the file extension should be .ico and "@" sign is not required'''

# left_frame items

# Adding a list box to maintain our playlist
playlist_box = Listbox(left_frame)
playlist_box.pack(padx=10, pady=10)

# Buttons for adding and removing songs

# Creating the add button to add songs
add_bt = Button(left_frame, text="+ Add", command=browse_song)  # Calls the browse_song function when clicked
add_bt.pack(side=LEFT, padx=10, pady=5)

# Creating the Remove Button to remove songs
remove_bt = Button(left_frame, text="- Remove", command=remove_music)
remove_bt.pack(side=LEFT, padx=10, pady=5)

# right_frame items
# top_frame Items!!

lengthlabel = Label(top_frame, text="Total Length -- --:--")
# A label containing the format in which the length of the song will be displayed
lengthlabel.pack(pady=10)

currenttimelabel = Label(top_frame, text="Time Remaining -- --:--", relief=GROOVE)
# A label containing the format in which the current time of the song will be displayed
currenttimelabel.pack(pady=10)

# mid_frame items

# A button for playing song
play_bt = Button(mid_frame, image=play, command=play_music)
# play_bt.pack(side=LEFT, padx=10)  # Arranging the elements using pack layout
play_bt.grid(row=0, column=0, padx=10)  # Arranging the elements using grid layout

# A button for stopping song
stop_bt = Button(mid_frame, text='Stop', command=stop_music)
# stop_bt.pack(side=LEFT, padx=10)  # Arranging the elements using pack layout
stop_bt.grid(row=0, column=1, padx=10)  # Arranging the elements using grid layout

# A button for pausing song
pause_bt = Button(mid_frame, text='Pause', command=pause_music)
# pause_bt.pack(side=LEFT, padx=10)  # Arranging the elements using pack layout
pause_bt.grid(row=0, column=2, padx=10)  # Arranging the elements using grid layout

# bot_frame items

# A button for rewinding song
rewind_bt = Button(bot_frame, text='Rewind', command=rewind_music)
# rewind_bt.pack(side=LEFT, padx=10)  # Arranging the elements using pack layout
rewind_bt.grid(row=0, column=0)  # Arranging the elements using grid layout

# A button for muting and restoring the volume of the song
vol_bt = Button(bot_frame, image=vol, command=mute_music)
# mute_bt.pack(side=LEFT, padx=10)  # Arranging the elements using pack layout
vol_bt.grid(row=0, column=1, padx=10)  # Arranging the elements using grid layout

# A volume control made using the scale widget
scale = Scale(bot_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
# A scale is made with a range that can be set to any integer between 0 to 100
scale.set(50)  # sets default scale value only as 50
mixer.music.set_volume(0.5)  # sets the default volume at 50
# scale.pack(pady=10)
scale.grid(row=0, column=2, padx=30, pady=15)  # Arranging the elements using grid layout

# Overriding the close Button so that it doesn't show us an error for abruptly closing the music player when we click it

root.protocol("WM_DELETE_WINDOW", on_closing)
# The WM_DELETE_WINDOW protocol is responsible for destroying the window on clicking the close button

root.mainloop()  # engages the window in an infinite loop
