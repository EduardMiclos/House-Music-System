from __future__ import unicode_literals

video = {
    'format': 'bestaudio/best',
    
     # The dot at the end is mandatory! (Avoiding some kind of conversion error).
     # If we were to put the .mp3 extension explicitly, the mpg123 won't
     # be able to play the song.
    'outtmpl': '%(title).',

    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]
}

playlist = {
    'extract_flat': 'in_playlist'
}
