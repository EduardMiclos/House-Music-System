import React from "react";

interface ListedSongProps {
  songTitle: string;
  songArtist: string;
  songDuration: string;
}

const ListedSong: React.FC<ListedSongProps> = ({
  songTitle,
  songArtist,
  songDuration
}) => {
  return (
    <li className="list-group-item">
        <div><b>{songTitle}</b></div>
        <div>{songArtist}</div>
        <div>{songDuration}</div>
        
    </li>
  );
};

export default ListedSong;
