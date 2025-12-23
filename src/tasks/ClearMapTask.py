from ok import Logger
from src.tasks.BaseGfTask import BaseGfTask, map_re

logger = Logger.get_logger(__name__)


class ClearMapTask(BaseGfTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "推图"
        self.description = "从要推的图的最左边开始"

    def run(self):
        count = 0
        clicked = []
        while True:
            last_clicked = None
            maps = self.ocr(box=self.box_of_screen(0, 0.2, 1, 0.8), match=map_re, log=True, threshold=0.5)
            maps = sorted(maps, key=lambda obj: obj.x)
            self.log_debug('maps: {}'.format(maps))
            if len(maps) == 0:
                if count == 0:
                    raise Exception('未找到要推的图!')
                else:
                    self.log_info(f'推图完成, 共{count}个!', notify=True)
                    return
            checked = False
            for m in maps:
                if m.name not in clicked:
                    clicked.append(m.name)
                    checked = True
                    last_clicked = m
                    self.click(m)
                    break
            if not checked:
                self.log_info(f'推图完成, 共{count}个!', notify=True)
                return
            self.sleep(1)
            if boxes := self.wait_ocr(box="right", match=["特殊奖励", '观看', '挑战'], time_out=3, log=True):
                # self.log_debug(f'特殊奖励 {boxes}')
                if self.find_boxes(boxes, match=["特殊奖励"]):
                    text = self.find_boxes(boxes, match=['观看', '挑战'])
                    self.click(text)
                    count += 1
                    if text[0].name == '挑战':
                        self.auto_battle(end_match=map_re, has_dialog=True)
                    else:
                        self.skip_dialogs(end_match=map_re)
                    if last_clicked:
                        self.log_debug(f'重新点击上一次关卡: {last_clicked.name}')
                        self.sleep(1)
                        self.wait_click_ocr(match=last_clicked.name, time_out=3, log=True, after_sleep=1)
                        self.back()
                else:
                    self.back()
            self.sleep(1)
# from ok import Logger
# from src.tasks.BaseGfTask import BaseGfTask, map_re
#
# logger = Logger.get_logger(__name__)
#
#
# class ClearMapTask(BaseGfTask):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.name = "推图"
#         self.description = "从要推的图的最左边开始"
#
#     def run(self):
#         count = 0
#         clicked = []
#         while True:
#             maps = self.ocr(box=self.box_of_screen(0, 0.2, 1, 0.8), match=map_re, log=True, threshold=0.5)
#             maps = sorted(maps, key=lambda obj: obj.x)
#             self.log_debug('maps: {}'.format(maps))
#             if len(maps) == 0:
#                 if count == 0:
#                     raise Exception('未找到要推的图!')
#                 else:
#                     self.log_info(f'推图完成, 共{count}个!', notify=True)
#                     return
#             checked = False
#             for m in maps:
#                 if m.name not in clicked:
#                     clicked.append(m.name)
#                     checked = True
#                     self.click(m)
#                     break
#             if not checked:
#                 self.log_info(f'推图完成, 共{count}个!', notify=True)
#                 return
#             self.sleep(1)
#             if boxes := self.wait_ocr(box="right", match=["特殊奖励", '观看', '挑战'], time_out=3, log=True):
#                 # self.log_debug(f'特殊奖励 {boxes}')
#                 if self.find_boxes(boxes, match=["特殊奖励", '观看']):
#                     text = self.find_boxes(boxes, match=['观看', '挑战'])
#                     self.click(text)
#                     count += 1
#                     if text[0].name == '挑战':
#                         self.auto_battle(end_match=map_re, has_dialog=True)
#                     else:
#                         self.skip_dialogs(end_match=map_re)
#                 else:
#                     self.back()
#             else:
#                 self.back()
#             self.sleep(1)
