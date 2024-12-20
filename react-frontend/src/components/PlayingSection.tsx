  import React from "react";
import { FaRegPauseCircle} from "react-icons/fa";
import { FaRegCirclePlay   } from "react-icons/fa6";
import PlayingSong from "./PlayingSong";

interface PlayingSectionProps {
  currentSong: string;
  play: () => void;
  pause: () => void;
  volume: number;
  adjustVolume: (value: number) => void;
  isPlaying: boolean;
}

const PlayingSection: React.FC<PlayingSectionProps> = ({
  currentSong,
  play,
  pause,
  isPlaying
}) => {
  
  return (
    <section id="player" className="text-center">
      <h3 style={{ color: "var(--accent-color)" }}>Now playing</h3>
      <div id="currentSong" className="mb-1">
        <PlayingSong 
          songTitle={currentSong}
          songArtist="Eminem"
          />
      </div>
      <div id="controls" className="d-flex justify-content-center gap-2">

        {
          isPlaying ?
          <button className="btn pause-btn" onClick={pause}>
            <FaRegPauseCircle  />
          </button>

          : 

          <button className="btn play-btn" onClick={play}>
            <FaRegCirclePlay  />
          </button>
        }

      </div>
    </section>
  );
};

export default PlayingSection;
