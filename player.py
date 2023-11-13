# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
#  
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  
#     http://www.apache.org/licenses/LICENSE-2.0
#  
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import _thread
import audio
from usr.modules.common import Condition, Event
from usr.modules.logging import getLogger


logger = getLogger(__name__)


class InfiniteIter(object):

    def __init__(self, obj):
        self.obj = obj
        self.iterator = iter(self.obj)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.iterator = iter(self.obj)  # 重置迭代器
            return next(self.iterator)


class Player(object):

    def __init__(self, device=0, pa_gpio=None):
        self.aud = audio.Audio(device)
        if pa_gpio is not None:  # 设置pa的gpio, 放大声音(如有需要则设置)
            self.aud.set_pa(pa_gpio, 2)
        self.aud.setCallback(self.audio_cb)
        self.play_next_cond = Condition()  # 用于阻塞等待下一首的条件变量
        self.play_stop_event = Event()  # 停止播放事件

    def audio_cb(self, event):
        if event == 0:
            logger.info('audio play start.')
        elif event == 7:
            logger.info('audio play finish.')
            self.play_next_cond.notify()

    def loop_play_executor(self, song_sheet):
        for file in InfiniteIter(song_sheet):
            if self.play_stop_event.is_set():
                logger.info('stop loop play.')
                break
            logger.info('play music "{}"'.format(file))
            self.aud.play(0, 0, file)
            self.play_next_cond.wait()  # 阻塞等待上一首播放完毕

    def loop_play(self, song_sheet):
        self.stop()
        if not isinstance(song_sheet, list):
            raise TypeError('param `song_sheet` must be list type, and it\'s member is music file path.')
        self.play_stop_event.clear()
        _thread.start_new_thread(self.loop_play_executor, (song_sheet, ))

    def stop(self):
        self.play_stop_event.set()
        self.play_next_cond.notify()
        self.aud.stopAll()

    def play(self, file):
        logger.info('play music "{}"'.format(file))
        self.stop()
        self.aud.play(0, 0, file)

    def setVolume(self, level):
        # level: 0~11音量大小，0表示静音
        self.aud.setVolume(level)
