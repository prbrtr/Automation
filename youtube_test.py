import time
import logging
logging.basicConfig(format='%(levelname)s:%(message)s:%(asctime)s', level=logging.INFO)
import unittest
from datetime import datetime
import selenium_helper
import inspect

youtube_url = "https://www.youtube.com/watch?v=7zhw8h6bXgw"

class YoutubeTest(unittest.TestCase):
    def setUp(self):
        try:
            self.youtube_obj = selenium_helper.SeleniumTest()
            #  Opening and playing youtube
            self.youtube_obj.open_url(youtube_url,"ytp-id-22")
            self.youtube_obj.wait_to_play()
            self.youtube_obj.skip_add()
        except Exception as e:
            raise Exception(f"[FAIL] {e}{inspect.stack()[0][3]} {datetime.now()}")
        
    def test_play_pause(self):
        try:
            #  Pause test
            self.youtube_obj.pause_video()
            if not self.youtube_obj.player_state() == "paused":
                raise Exception("Youtube Failed to Pause")
            #  Play after Pause test
            self.youtube_obj.play_video()
            if self.youtube_obj.player_state() == "buffering":
                time.sleep(2)
            if not self.youtube_obj.player_state() == "playing":
                raise Exception("Youtube Failed to Play after Pause")
        except Exception as e:
            raise Exception(f"[FAIL] {e}{inspect.stack()[0][3]} {datetime.now()}")

    def test_about_volume(self):
        try:
            #  Changing the Volume 
            self.youtube_obj.browser.execute_script(r"return document.querySelector('video').volume=0.5")
            if not self.youtube_obj.browser.execute_script("return document.querySelector('video').volume")==0.5:
                raise Exception("Failed to set volume")
            #  Mute Video
            self.youtube_obj.browser.execute_script("return document.getElementById('movie_player').mute()")
            #  unMute Video 
            self.youtube_obj.browser.execute_script("return document.getElementById('movie_player').unMute()")
        except Exception as e:
            raise Exception(f"[FAIL] {e} {inspect.stack()[0][3]} {datetime.now()}")
        
    def test_window(self):
        try:
            #  Browser maximize 
            self.youtube_obj.browser.maximize_window()
            #  Full Screen Mode
            self.youtube_obj.browser.fullscreen_window()
            #  Window Minimize 
            self.youtube_obj.browser.minimize_window()
            #  Revert back to normal size 
            self.youtube_obj.browser.maximize_window()
        except Exception as e:
            raise Exception(f"[FAIL] {e} {inspect.stack()[0][3]} {datetime.now()}")
        
    def test_playback(self):
        try:
            #  Video Forwarding
            current_time=self.youtube_obj.browser.execute_script("return document.querySelector('video').currentTime")
            print(current_time)
            self.youtube_obj.browser.execute_script("return document.getElementsByTagName('video')[0].currentTime+=5")
            time.sleep(2) 
            current_time_after_forward = self.youtube_obj.browser.execute_script("return document.querySelector('video').currentTime")
            logging.info("Current Video Time after Forward: {0}".format(str(current_time_after_forward) ))
            if not (current_time_after_forward >= current_time+5):
                raise Exception("Failed to Forward Youtube Video")
            #  Video Rewind 
            current_time=self.youtube_obj.browser.execute_script("return document.querySelector('video').currentTime")
            self.youtube_obj.browser.execute_script("return document.getElementsByTagName('video')[0].currentTime-=5")
            time.sleep(2) 
            current_time_after_forward = self.youtube_obj.browser.execute_script("return document.querySelector('video').currentTime")
            logging.info("Current Video Time after Forward: {0}".format(str(current_time_after_forward) ))
            if not (current_time_after_forward >= current_time-5):
                raise Exception("Failed to Forward Youtube Video")
        except Exception as e:
            raise Exception(f"[FAIL] {e}{inspect.stack()[0][3]} {datetime.now()}")


    def tearDown(self):
        self.youtube_obj.browser.close()
        
if __name__== "__main__":
    unittest.main()