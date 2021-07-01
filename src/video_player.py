"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._video_playing = ''
        self._video_status = 'stopped'
        self._playlists = {}

    def getVideoInfo(self,videoID):
        title = self._video_library.get_video(videoID)._title
        id = '('+self._video_library.get_video(videoID)._video_id+')'
        tags_videos = self._video_library.get_video(videoID)._tags
        flag = self._video_library.get_video(videoID)._flag

        tags = ""
        for i in range(len(tags_videos)):
            tags += tags_videos[i]
            if i < len(tags_videos)-1:
                tags += ' '
        tags = '['+tags+']'

        flagtxt = ''
        if flag:
            flagtxt = ' - FLAGGED (reason: {})'.format(flag)

        status = title + ' ' + id + ' ' + tags + flagtxt

        return status

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        list_videos = self._video_library.get_all_videos()
        videoTitles = []
        for video in list_videos:
            videoTitles.append(self.getVideoInfo(video._video_id))
        videoTitles.sort()

        print("Here's a list of all available videos:")
        for i in videoTitles:
            print('  '+i)
        

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        videoToPlay = self._video_library.get_video(video_id)
        if videoToPlay == None:
            print('Cannot play video: Video does not exist')
        elif videoToPlay.flag:
            print('Cannot play video: Video is currently flagged (reason: {})'.format(videoToPlay.flag))
        else:
            if self._video_playing != '':
                print('Stopping video: '+self._video_library.get_video(self._video_playing)._title)
            
            print('Playing video: '+videoToPlay._title)
            self._video_playing = video_id
            self._video_status = 'playing'


    def stop_video(self):
        """Stops the current video."""

        videoToPlay = self._video_library.get_video(self._video_playing)
        if videoToPlay == None:
            print('Cannot stop video: No video is currently playing')
        else:
            print('Stopping video: '+videoToPlay._title)
            self._video_playing = ''
            self._video_status = 'stopped'


    def play_random_video(self):
        """Plays a random video from the video library."""
    
        list_videos = self._video_library.get_all_videos()

        if len(list_videos) == 0:
            print('No videos available')
            return

        choice = random.choice(list_videos)

        while choice.flag:
            list_videos.remove(choice)

            if len(list_videos) == 0:
                print('No videos available')
                return

            choice = random.choice(list_videos)

        self.play_video(choice._video_id)

    def pause_video(self):
        """Pauses the current video."""

        if self._video_status == 'paused':
            print('Video already paused: '+self._video_library.get_video(self._video_playing)._title)
            return
        if self._video_status == 'stopped':
            print('Cannot pause video: No video is currently playing')
            return
        
        self._video_status = 'paused'
        print('Pausing video: '+self._video_library.get_video(self._video_playing)._title)
        

    def continue_video(self):
        """Resumes playing the current video."""

        if self._video_status == 'playing':
            print('Cannot continue video: Video is not paused')
            return
        if self._video_status == 'stopped':
            print('Cannot continue video: No video is currently playing')
            return
        
        self._video_status = 'playing'
        print('Continuing video: '+self._video_library.get_video(self._video_playing)._title)
        

    def show_playing(self):
        """Displays video currently playing."""

        if self._video_status == 'stopped':
            print('No video is currently playing')
            return

        status = 'Currently playing: ' + self.getVideoInfo(self._video_playing)
        if self._video_status == 'paused':
            print(status + ' - PAUSED')
        else:
            print(status)



# /////////////////////////////////////////////////////////////////////////////////////////////////



    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lowename = playlist_name.lower()
        if lowename in self._playlists:
            print('Cannot create playlist: A playlist with the same name already exists')
        else:
            self._playlists[lowename] = Playlist(playlist_name)
            print('Successfully created new playlist:',self._playlists[lowename]._pl_title)



    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        lowename = playlist_name.lower()
        if lowename not in self._playlists:
            print('Cannot add video to {}: Playlist does not exist'.format(playlist_name))
            return
        if self._video_library.get_video(video_id) == None:
            print('Cannot add video to {}: Video does not exist'.format(playlist_name))
            return

        if self._playlists[lowename].checkVideo(video_id):
            print('Cannot add video to {}: Video already added'.format(playlist_name))
        else:
            self._playlists[lowename].addVideo(video_id)
            videoName = self._video_library.get_video(video_id)

            if videoName.flag:
                print('Cannot add video to {}: Video is currently flagged (reason: {})'.format(playlist_name,videoName.flag))
                return

            print('Added video to {}: {}'.format(playlist_name,videoName._title))


    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._playlists) == 0:
            print('No playlists exist yet')
        else:
            print('Showing all playlists:')
            allPLs = []
            for pl in self._playlists:
                allPLs.append(self._playlists[pl]._pl_title)
            allPLs.sort()
            for i in allPLs:
                print('  '+i)


    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        lowename = playlist_name.lower()
        if lowename not in self._playlists:
            print('Cannot show playlist {}: Playlist does not exist'.format(playlist_name))
            return

        print('Showing playlist:',playlist_name)

        allVideos = self._playlists[lowename]._pl_videos
        if len(allVideos) == 0:
            print('  No videos here yet')
            return
        for video in allVideos:
            print('  '+self.getVideoInfo(video))


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        
        lowename = playlist_name.lower()
        if lowename not in self._playlists:
            print('Cannot remove video from {}: Playlist does not exist'.format(playlist_name))
            return
        if self._video_library.get_video(video_id) == None:
            print('Cannot remove video from {}: Video does not exist'.format(playlist_name))
            return

        if self._playlists[lowename].checkVideo(video_id) == False:
            print('Cannot remove video from {}: Video is not in playlist'.format(playlist_name))
        else:
            self._playlists[lowename].removeVideo(video_id)
            videoName = self._video_library.get_video(video_id)
            print('Removed video from {}: {}'.format(playlist_name,videoName._title))


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lowename = playlist_name.lower()
        if lowename not in self._playlists:
            print('Cannot clear playlist {}: Playlist does not exist'.format(playlist_name))
            return
        self._playlists[lowename].clearPlaylist()
        print('Successfully removed all videos from',playlist_name)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lowename = playlist_name.lower()
        if lowename not in self._playlists:
            print('Cannot delete playlist {}: Playlist does not exist'.format(playlist_name))
            return
        self._playlists.pop(playlist_name)
        print('Deleted playlist:',playlist_name)





# //////////////////////////////////////////////////////////////////////////////////



    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        list_videos = self._video_library.get_all_videos()
        videoTitles = []
        for video in list_videos:
            lowerSearch = search_term.lower()
            lowerTitle = video.title
            if lowerSearch in lowerTitle.lower():
                videoName = self.getVideoInfo(video._video_id)
                if 'FLAGGED' not in videoName:
                    videoTitles.append(videoName)
        videoTitles.sort()

        if len(videoTitles) == 0:
            print('No search results for',search_term)
            return

        print("Here are the results for {}:".format(search_term))
        numIndex = 1
        for title in videoTitles:
            print('  '+str(numIndex)+') '+title)
            numIndex += 1
        
        print('Would you like to play any of the above? If yes, specify the number of the video.')
        print("If your answer is not a valid number, we will assume it's a no.")
        ans = input()
        if ans.isnumeric():
            ans = int(ans)
            if ans > 0 and ans <= numIndex:
                videoIdFromName = videoTitles[ans-1].split('(')
                videoIdFromName = videoIdFromName[1].split(')')
                self.play_video(videoIdFromName[0])
        


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        list_videos = self._video_library.get_all_videos()
        videoTitles = []
        for video in list_videos:
            lowerSearch = video_tag.lower()
            lowerTitle = video.tags
            if lowerSearch in lowerTitle:
                videoName = self.getVideoInfo(video._video_id)
                if 'FLAGGED' not in videoName:
                    videoTitles.append(videoName)
        videoTitles.sort()

        if len(videoTitles) == 0:
            print('No search results for',video_tag)
            return

        print("Here are the results for {}:".format(video_tag))
        numIndex = 1
        for title in videoTitles:
            print('  '+str(numIndex)+') '+title)
            numIndex += 1

        print('Would you like to play any of the above? If yes, specify the number of the video.')
        print("If your answer is not a valid number, we will assume it's a no.")
        ans = input()
        if ans.isnumeric():
            ans = int(ans)
            if ans > 0 and ans <= numIndex:
                videoIdFromName = videoTitles[ans-1].split('(')
                videoIdFromName = videoIdFromName[1].split(')')
                self.play_video(videoIdFromName[0])



# ////////////////////////////////////////////////////////////////////////////////////////////////


    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if flag_reason == "":
            flag_reason = "Not supplied"

        videoToFlag = self._video_library.get_video(video_id)
        if videoToFlag == None:
            print('Cannot flag video: Video does not exist')
        elif videoToFlag.flag:
            print('Cannot flag video: Video is already flagged')
        else:
            videoToFlag.flag = flag_reason
            if self._video_status == 'playing' or self._video_status == 'paused':
                if self._video_playing == video_id:
                    self.stop_video()

            print('Successfully flagged video: {} (reason: {})'.format(videoToFlag.title,flag_reason))

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        videoToFlag = self._video_library.get_video(video_id)
        if videoToFlag == None:
            print('Cannot remove flag from video: Video does not exist')
            return
        if videoToFlag.flag:
            videoToFlag.flag = None
            print('Successfully removed flag from video:',videoToFlag.title)
        else:
            print('Cannot remove flag from video: Video is not flagged')
        
