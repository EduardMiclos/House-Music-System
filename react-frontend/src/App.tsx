import { useEffect, useState } from "react";
import { socket } from './socket';
import Header from "./components/Header";
import Footer from "./components/Footer";
import "./App.css";
import PlayingSection from "./components/PlayingSection";
import ListedSong from "./components/ListedSong";

function App() {
  const [currentSong, setCurrentSong] = useState("");
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(50);
  const [searchTerm, setSearchTerm] = useState("");
  const [recentSongs, setRecentSongs] = useState(["Lose yourself", "Vinovatii fara vina", "Radioactive"]);
  const [recentArtist, setRecentArtists] = useState(["Eminem", "Pasarea Colibri", "Imagine Dragons"]);
  
  useEffect(() => {
    function set_bluetooth_status(data) {
      const statusElement = $('#bluetooth-device-status');
      if (data.status == 'connecting') {
          statusElement.html('<div class="loader"></div>')
      }
      else {
          statusElement.html(`<b>${data.device}</b>`)
      }
    }
  
    socket.on('bluetooth', (data) => {set_bluetooth_status(data);});
      return () => {
      socket.off('bluetooth', set_bluetooth_status);
    }

  });


  const play = () => {
    setCurrentSong("Song is playing... 🎶");
  };

  const pause = () => {
    setCurrentSong("Playback paused ⏸️");
  };

  const adjustVolume = (v) => {

  }

  const filterSongs = (e) => {
    const search = e.target.value;
    setSearchTerm(search);
    setCurrentSong(search);
  }


  return (
    <div className="page-wrapper">
    <Header/>
    
    <div className="container content">
      
      <div className="mb-4">
        <h2 className="text-center" style={{ color: "var(--text-color)" }}>
          Welcome back.
        </h2>
      </div>

      {
        currentSong != "" &&
      
        <PlayingSection
          currentSong={currentSong}
          play={play}
          pause={pause}
          volume={volume}
          adjustVolume={adjustVolume}
          isPlaying={isPlaying}
        />
      }

      <section id="search" className="mt-4">
        <h3 className="text-center" style={{ color: "var(--text-light)" }}>
          Search for a song
        </h3>
        <input
          type="text"
          id="searchBar"
          className="form-control"
          placeholder="Search by song name..."
          value={searchTerm}
          onChange={filterSongs}
        />
      </section>

      <section id="songList" className="mt-4">
        <h3 className="text-center" style={{ color: "var(--accent-color)" }}>
          Recently played
        </h3>
        <ul id="songs" className="list-group">
          {recentSongs.length > 0 ? (
            recentSongs.map((song, index) => (
              <ListedSong
                songTitle={song}
                songArtist={recentArtist[index]}
                songDuration='2:34'
              />
            ))
          ) : (
            <li className="list-group-item">No songs found.</li>
          )}
        </ul>
      </section>
    </div>

    <Footer/>
    </div>
  );
}

export default App;
