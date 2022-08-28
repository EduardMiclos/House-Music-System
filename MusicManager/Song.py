class Song:
    def __init__(self, title: str = "", artist: str = "Unknown", genre: str = "", path: str = "") -> None:
        self.title = title
        self.artist = artist
        self.genre = genre
        self.path = path

    def lower(self) -> None:
        self.title = self.title.lower()
        self.artist = self.artist.lower()
        self.genre = self.genre.lower()
        self.path = self.path.lower()
