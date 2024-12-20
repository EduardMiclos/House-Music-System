import React from "react";

interface PlayingSongProps {
  songTitle: string;
  songArtist: string;
}

const PlayingSong: React.FC<PlayingSongProps> = ({
  songTitle,
  songArtist
}) => {
  return (
    <section id="playingSong" className="text-center">
        <div>
           <b>{songTitle}</b>
        </div>
        {songArtist}
    </section>
  );
};

export default PlayingSong;
