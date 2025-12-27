from os import remove

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
        last_fallback_name = None
        last_failed_name = None  # 用来保存上次进入 if not text 分支的关卡名
        last_failed_flag = False  # 标记上次循环是否进入过 if not text 分支

        while True:
            last_clicked = None
            self.sleep(2)

            # 根据上次是否失败，选择 OCR 匹配规则
            if last_failed_flag and last_failed_name:
                maps = self.ocr(
                    box=self.box_of_screen(0, 0.2, 1, 0.8),
                    match=last_failed_name,
                    log=True,
                    threshold=0.5
                )
                if maps:
                    maps[0].name = "before_one_" + maps[0].name
                    print(self.frame.shape)
                    maps[0].x = maps[0].x - 80 / 256 * self.frame.shape[1]
                last_failed_flag = False  # 使用一次后清除标记
            else:
                maps = self.ocr(
                    box=self.box_of_screen(0, 0.2, 1, 0.8),
                    match=map_re,
                    log=True,
                    threshold=0.5
                )

            maps = sorted(maps, key=lambda obj: obj.x)
            self.log_debug('maps: {}'.format(maps))

            if len(maps) == 0:
                if count == 0:
                    raise Exception('未找到要推的图!')
                else:
                    self.log_info(f'推图完成, 共{count}个!', notify=True)
                    return

            checked = False
            current_map = None
            for i in range(len(maps)):
                current_map = maps[i]
                if current_map.name not in clicked:
                    clicked.append(current_map.name)
                    checked = True
                    last_clicked = current_map
                    self.click(current_map, after_sleep=2)
                    break

            if not checked:
                # 当前兜底目标
                fallback = maps[-1]
                if last_fallback_name == fallback.name:
                    self.log_info(f'推图完成, 共{count}个!', notify=True)
                    return
                last_fallback_name = fallback.name
                self.click(fallback, after_sleep=2)
                self.back(after_sleep=2)
                continue

            self.sleep(1)
            if len(maps[0].name) > 10:
                pass
            if boxes := self.wait_ocr(box="right", match=["特殊奖励", '观看', '挑战'], time_out=3, log=True):
                if self.find_boxes(boxes, match=["特殊奖励"]):
                    text = self.find_boxes(boxes, match=['观看', '挑战'])
                    if not text:
                        # 保存当前失败的关卡名，标记上次进入过该分支
                        last_failed_name = current_map.name
                        last_failed_flag = True

                        if current_map.name in clicked:
                            clicked.remove(current_map.name)
                        self.back(after_sleep=2)
                        continue

                    # 正常处理挑战或观看
                    self.click(text, after_sleep=2)
                    count += 1
                    if text[0].name == '挑战':
                        self.auto_battle(end_match=map_re, has_dialog=True)
                    else:
                        self.skip_dialogs(end_match=map_re)

                    if last_clicked:
                        self.log_debug(f'重新点击上一次关卡: {last_clicked.name}')
                        if self.wait_click_ocr(match=last_clicked.name, time_out=3, log=True, after_sleep=1):
                            self.back(after_sleep=2)
                else:
                    self.back(after_sleep=2)
            self.sleep(1)
