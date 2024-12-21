    import React, { useState, useEffect } from "react";
import axios from 'axios';
import ListedSong from "./ListedSong";

interface Song {
    title: string;
    artist: string;
    duration: string;
  }

const RecentlyPlayed: React.FC = () => {
    const [recentSongs, setRecentSongs] = useState<Song[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    // reduce the song title/artist name striong size by cutting characters and replacing them with '...'
    // we do this if the screen width is too small
    function reduceIfNecessary(text: string): string {
        // tbd
        return text;
    }

    useEffect(() => {
        const fetchSongs = async () => {
            try {
                const response = await axios.get('http://housemusic.local:5001/recently-played')
                if (response.status !== 200) throw new Error("Failed to fetch songs.");
                setRecentSongs(response.data.songs);
            }
            catch(err) {
                setError(true);
            }
            finally {
                setLoading(false);
            }
        }

        fetchSongs();
       
    }, []);


    return (
        <section id="songList" className="mt-4">
        <h3 className="text-center" style={{ color: "var(--accent-color)" }}>
          Recently played
        </h3>
        <ul id="recently-played-songs" className="list-group d-flex align-items-center">
          {loading && <div className="recently-played-loader "/>}
          {error && <div style={{fontSize: 12}}>Unable to fetch songs.</div>}
          {
          recentSongs.map((song, index) => (
          <ListedSong
            key={index} 
            songTitle={reduceIfNecessary(song.title)}
            songArtist={reduceIfNecessary(song.artist)}
            songDuration={song.duration}
          />
        ))}
      </ul>
    </section>
    );
};

export default RecentlyPlayed;
