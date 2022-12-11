import spotipy 
import time
from spotipy.oauth2 import SpotifyClientCredentials
from IPython.display import clear_output
import lyricsgenius 
import time
import re

##### Get the lyrics from Genius #####
def get_lyrics(playlist_id):
    """
    Uses the Spotify API to get the track names and artists from a playlist 
    and Genius API to get the lyrics. Takes the playlist ID as input.
    """

    token= "mfo8xJYWCndDMJTpEQW6yFUZC86cIMCCnRCM0bKXF4vnesFRB4CxCFdhTDPLA_m1"
    genius = lyricsgenius.Genius(token)

    auth_manager = SpotifyClientCredentials(client_id="283407b01d784f0fabf18b7fdb401dc6", client_secret="4df73017ea994b5aa4c71908a663d2ea")
    #token = "BQDtE4pXlxFnfwYnyixdd-Tm55lCIYqLiNwAeLc7TEWH2Tk4dMkWJqHPzedE220_mgyrnTqxNIunHVKTmnPALGHchp5PAJy6oNOMD0th0hS0E_uhOnP0YDniADWQ9Q9tp_8bAwHYi_x1dyY8R5A0imH6qwK28vNT-DvhQjJ0qhmLYHg"
    sp = spotipy.Spotify(auth_manager=auth_manager) #,  auth=token

    playlist = sp.playlist(playlist_id)

    tracks = (playlist['tracks'])
    names = []
    artist = []

   

    for i in range(len(tracks['items'])):

        names.append(tracks['items'][i]['track']['name'])
        artist.append(tracks['items'][i]['track']['artists'][0]['name'])
        
        

    text = []
    failed_song = []

    n_songs = len(names)
    index = 0
    print("Number of songs in playlist: ", n_songs)

    for idx in range(len(names)):
        try:
            song = genius.search_song(names[idx], artist[idx])
            text.append(song.lyrics)
            text.append("#CLAES#") # Added to seperate songs with unique token
            time.sleep(1)
        except:
            failed_song.append(idx)
            time.sleep(3)
            continue

        index += 1
        if index % 10 == 0:
            #clear_output(wait=True)
            print("Songs processed: ", index)
            print("Songs left: ", n_songs - index)
            
            time.sleep(1)

    time.sleep(10) # Wait 10 seconds before retrying failed songs

    for idx in range(len(failed_song)):
        try:
            song = genius.search_song(names[idx], artist[idx])
            text.append(song.lyrics)
            text.append("#CLAES#") # Added to seperate songs with unique token
            time.sleep(2)
        except:
            print("Failed to get lyrics for song: " + names[idx])
            continue

    return text

##### Clean the lyrics #####
def txt_cleaner(lyrics, claes_remove=False):
    """
    Take a lyric for a single song and removes unwanted parts and cleans the text
    """
    for i in range(len(lyrics)):
        d = {
            r'\[.+\]' : '',
            '\n+' : '\n',
            'You might also like\d*Embed' : '',
            '\d*Embed' : '',
            'You might also like' : '',
        }

        for key, value in d.items():
            lyrics[i] = re.sub(key, value, lyrics[i])

        # Optional step removing song separators
        if claes_remove:                
            lyrics[i] = re.sub(r'CLAES', '', lyrics[i])

        # Remove all titles from the songs, including the "\n" after the title, if it is there
        m=re.search(r'lyrics\n*', lyrics[i], re.IGNORECASE)

        if m: # Only runs if it finds a match
            text_temp = lyrics[i]
            lyrics[i] = text_temp[m.span()[1]:]
            
    text = "\n".join(lyrics)
    return text

##### Save the lyrics to a text file #####
def save_lyrics(lyrics, filename="lyrics.txt"):
    """
    Save lyrics to a text file
    """

    text = lyrics #"\n".join(lyrics)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
  

##### Loading the lyrics from a text file #####
def load_lyrics(filename="lyrics.txt"):
    """
    Load lyrics from a text file
    """

    #open text file
    text_file = open(filename, "r", encoding="utf-8")
 
    #read file to string
    text = text_file.read()
 
    #close file
    text_file.close()

    return text

##### Seperate the lyrics into list of sentences
def senctence_seperator(lyrics):
    """
    Takes a string of lyrics and seperates it into sentences
    """
    sentences = re.split(r'\n', lyrics)
    return sentences