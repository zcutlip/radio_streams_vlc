try:
    import streamlink
except ImportError:
    streamlink = None

from .station_list import StationList, StationListParseException


class VideoStreamException(Exception):
    pass


class VideoStreamDependencyException(Exception):
    pass


class VideoStreamList(StationList):
    LIST_NAME = "Video Streams"
    STATION_CSV = "videostreams.csv"
    VIDEO_STREAMS = True

    def parse_csv_record(self, csv_record: list):
        name, description, url = super().parse_csv_record(csv_record)
        try:
            url = self.get_video_stream(url)
        except VideoStreamException as e:
            print(e)
            raise StationListParseException from e
        return (name, description, url)

    @staticmethod
    def get_video_stream(website_url):
        if not streamlink:
            raise VideoStreamDependencyException(
                "Can't extract video stream without 'streamlink' package")
        stream_url = None
        try:
            streams: dict = streamlink.streams(website_url)
        except (
                streamlink.NoPluginError,
                streamlink.PluginError) as e:
            raise VideoStreamException("Failed to extract video stream") from e
        try:
            stream_url = streams['best'].to_url()
        except KeyError:
            # 'best' wasn't available, so not sure what to do
            raise VideoStreamException(
                "Unable to find 'best' stream from streams dict")

        return stream_url
