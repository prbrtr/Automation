import subprocess
import time,sys,os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.keys import Keys
import datetime
from bs4 import BeautifulSoup

class SeleniumTest:
    def __init__(self):
        self.browser=webdriver.Chrome(executable_path=r"C:\Program Files\Google\Chrome\chromedriver.exe")
    
    def open_url(self,url,id=""):
        self.browser.get(url)
        if id:
            element_present = EC.presence_of_element_located((By.ID, id))
    
    def new_tab(self,tab_name,url):
        self.browser.execute_script(f"window.open('about:blank', '{tab_name}');")
        # It is switching to second tab now
        self.browser.switch_to.window(tab_name)
        self.browser.get(url)
    
    def activity(self,xpath,click=False, key=False):
        if click:
            Wait(self.browser,20).until(EC.presence_of_element_located((By.XPATH,xpath))).click()
        elif key :
            Wait(self.browser,20).until(EC.presence_of_element_located((By.XPATH,xpath))).send_keys(key)
        else:
            Wait(self.browser,20).until(EC.presence_of_element_located((By.XPATH,xpath)))

    def click_play_btn(self):
        play_button = self.browser.find_element_by_css_selector('.ytp-play-button')
        play_button.click()  

    def pause_video(self):
        return self.browser.execute_script("document.querySelector('video').pause()")
    
    def play_video(self):
        return self.browser.execute_script("document.querySelector('video').play()")

    def player_state(self):
        status = self.browser.execute_script("return document.getElementById('movie_player').getPlayerState()")
        player_state = "undefined"
        if status == 1:
            player_state = "playing"
        elif status == 2:
            player_state = "paused"
        elif status == 3:
            player_state = "buffering"
        elif status == 0:
            player_state = "ended"
        elif status == -1:
            player_state = "unstarted"
        return player_state

    def wait_to_play(self, timeout=30):
        start = time.time()
        playing = False
        try:
            while (time.time() - start) <= timeout:
                if self.player_state()=="playing":
                    playing = True
                    print("Youtube video is playing")
                    break
                time.sleep(2)
                try:
                    self.click_play_btn()
                except:
                    pass
        except Exception as e:
            raise Exception("FAIL: {0} : {1}".format(datetime.datetime.now(), e))
        
    def skip_add(self):
        """Skip add on youtube video"""
        i = 1
        while i < 60:
            if self.player_state() == "unstarted":
                print("Skipping add")
                self.browser.execute_script( "var SkipButton = document.getElementsByClassName('ytp-ad-skip-button-slot')[0]; if (SkipButton) { SkipButton.click() }")
                self.wait_to_play()
            else:
                break
            time.sleep(1)
            i += 1
