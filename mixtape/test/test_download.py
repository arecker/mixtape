import unittest

from .. import download


class TestDownload(unittest.TestCase):
    def test_extract_video_info(self):
        actual = download.extract_video_info('Rick Astley - Never Gonna Give You Up (Official Music Video)')
        self.assertEqual(actual.artist, 'rick astley')
        self.assertEqual(actual.title, 'never gonna give you up')

        actual = download.extract_video_info('Katy Perry - Dark Horse ft. Juicy J')
        self.assertEqual(actual.artist, 'katy perry')
        self.assertEqual(actual.title, 'dark horse')
