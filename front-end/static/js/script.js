const socket = io('ws://localhost:5001');

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

// document.addEventListener("DOMContentLoaded", function () {
//     loadSongs();
//     loadArtists();
// });

// function loadSongs() {
//     // Simulate loading songs (replace with an API call or local file)
//     const songs = [
//         { name: "Song A", artist: "Artist A", genre: "House" },
//         { name: "Song B", artist: "Artist B", genre: "Deep House" },
//         { name: "Song A", artist: "Artist A", genre: "House" },
//         { name: "Song B", artist: "Artist B", genre: "Deep House" },
//         { name: "Song A", artist: "Artist A", genre: "House" },
//         { name: "Song B", artist: "Artist B", genre: "Deep House" },
//         { name: "Song A", artist: "Artist A", genre: "House" },
//         { name: "Song B", artist: "Artist B", genre: "Deep House" },
//         { name: "Song B", artist: "Artist B", genre: "Deep House" },
//         { name: "Song A", artist: "Artist A", genre: "House" },
//         { name: "Song B", artist: "Artist B", genre: "Deep House" },
//         { name: "Song A", artist: "Artist A", genre: "House" },
//         { name: "Song B", artist: "Artist B", genre: "Deep House" },
//         { name: "Song A", artist: "Artist A", genre: "House" },
//         { name: "Song B", artist: "Artist B", genre: "Deep House" },
//         // Add more songs here
//     ];

//     const songList = document.getElementById("songs");
//     songList.innerHTML = "";
//     songs.forEach(song => {
//         const li = document.createElement("li");
//         li.textContent = `${song.name} - ${song.artist} (${song.genre})`;
//         li.onclick = () => playSong(song.name);
//         songList.appendChild(li);
//     });
// }

// function loadArtists() {
//     // Simulate loading artists (replace with an API call or local file)
//     const artists = ["Artist A", "Artist B", "Artist C"];
//     const artistList = document.getElementById("artists");
//     artistList.innerHTML = "";
//     artists.forEach(artist => {
//         const li = document.createElement("li");
//         li.textContent = artist;
//         artistList.appendChild(li);
//     });
// }

// function filterSongs() {
//     const search = document.getElementById("searchBar").value.toLowerCase();
//     const songs = document.querySelectorAll("#songs li");
//     songs.forEach(song => {
//         song.style.display = song.textContent.toLowerCase().includes(search)
//             ? "block"
//             : "none";
//     });
// }

// function playSong(songName) {
//     const currentSong = document.getElementById("currentSong");
//     currentSong.innerHTML = `<p>Now Playing: ${songName}</p>`;
// }

// function playPause() {
//     alert("Toggle Play/Pause");
// }

// function playNext() {
//     alert("Play Next Song");
// }

// function playPrevious() {
//     alert("Play Previous Song");
// }

// function adjustVolume(volume) {
//     console.log(`Volume set to ${volume}`);
// }

// function refreshSongs() {
//     alert("Refreshing song list...");
// }
