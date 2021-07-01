"""A video playlist class."""

from typing import Sequence

class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self,title: str):
        self._pl_title = title
        self._pl_videos = []


    @property
    def pl_title(self) -> str:
        """Returns the title of a Playlist."""
        return self._pl_title

    @property
    def pl_videos(self) -> Sequence[str]:
        """Returns the video id of a video."""
        return self._pl_videos

    # add video to playlist
    def addVideo(self,videoID):
        self._pl_videos.append(videoID)
    
    # remove video from playlist
    def removeVideo(self,videoID):
        self._pl_videos.remove(videoID)

    # check if video is in playlist
    def checkVideo(self,videoID):
        if len(self._pl_videos) == 0:
            return False
        for id in self._pl_videos:
            if id == videoID:
                return True
        return False

    def clearPlaylist(self):
        self._pl_videos = []