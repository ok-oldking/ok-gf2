import re
import time

from ok import BaseTask, find_boxes_by_name
from ok import Logger

logger = Logger.get_logger(__name__)
pop_ups = ['点击空白处关闭', '点击屏幕任意位置继续', '点击任意位置继续']
number_re = re.compile(r"^\d+$")
stamina_re = re.compile(r"^\d+/\d+")
map_re = re.compile(r'-?\d{1,2}-\d{1,2}\*?')


class BaseGfTask(BaseTask):

    def ensure_main(self, recheck_time=1, time_out=30, esc=True):
        self.info_set('current_task', 'go_to_main')
        if not self.wait_until(lambda: self.is_main(recheck_time=recheck_time, esc=esc), time_out=time_out):
            raise Exception("请从游戏主页进入")

    def skip_dialogs(self, end_match, end_box=None, time_out=120, has_dialog=True):
        self.info_set('current_task', 'skip_dialogs')
        self.sleep(5)
        start = time.time()
        while time.time() - start < time_out:
            boxes = self.ocr()
            if skip := self.find_boxes(boxes, match=['跳过']):
                self.click(skip)
                self.sleep(2)
            elif no_alert := self.find_boxes(boxes, match='今日不再提示'):
                self.click(no_alert)
                self.sleep(0.2)
                self.click(self.find_boxes(boxes, match='确认'))
            elif result := self.find_boxes(boxes, match=end_match, boundary=end_box):
                self.sleep(1)
                return result
            elif self.find_boxes(boxes, match=re.compile(r'回合$'), boundary='top_left'):
                self.sleep(3)
            elif pop_up := self.find_boxes(boxes, match=pop_ups):
                self.back()
                self.sleep(2)
            else:
                if has_dialog:
                    self.click_relative(0.95, 0.04)
                self.sleep(2)
            self.next_frame()
        raise Exception('跳过剧情超时!')

    def auto_battle(self, end_match=None, end_box=None, has_dialog=False):
        self.info_set('current_task', 'auto battle')
        result = self.skip_dialogs(end_match=['作战开始', '行动结束'], end_box='bottom', time_out=120,
                                   has_dialog=has_dialog)
        if result[0].name == '作战开始':
            self.sleep(2)
            self.click_box(result, after_sleep=1)
            start_result = self.wait_ocr(match=[re.compile('行动结束'), re.compile('还有可部署')],
                                         raise_if_not_found=False, time_out=15)
            if start_result and '行动结束' != start_result[0].name:
                self.log_info('阵容没上满!', notify=True)

                self.wait_click_ocr(match=['确认'], box='bottom', time_out=5,
                                    raise_if_not_found=True)

                start_result = self.wait_ocr(match=['行动结束'], box='bottom_right',
                                             raise_if_not_found=False, time_out=15)
            if start_result:
                self.sleep(0.5)
                if self.is_adb():
                    self.click_relative(0.85, 0.05, after_sleep=1)
                else:
                    self.click_relative(0.88, 0.04, after_sleep=1)

        while results := self.skip_dialogs(
                end_match=['任务完成', '任务失败', '战斗失败', '对战胜利', '对战失败', '确认','确认结算'], time_out=900,
                has_dialog=has_dialog):
            for result in results:
                if result.name in ("确认","确认结算"):
                    self.click_box(result, after_sleep=2)
                    break
            self.sleep(2)
            self.click_box(results, after_sleep=2)
            if results[0].name not in pop_ups:
                break
        if not results:
            raise Exception('自动战斗异常')
        if results[0].name == '任务失败':
            raise Exception('任务失败, 没打过!')
        while self.wait_click_ocr(match='确认', box='bottom_right', raise_if_not_found=False, time_out=3):
            pass
        if end_match:
            if isinstance(end_match, list):
                end_match = end_match + pop_ups
            else:
                end_match = [end_match] + pop_ups
            end_match.append('确认')
            end_match.append('确认结算')
            while True:
                match = self.wait_ocr(match=end_match, box=end_box, raise_if_not_found=True, time_out=30)
                if match[0].name in pop_ups:
                    self.back(after_sleep=2)
                    continue
                if match:
                    self.log_info(f'battle end matched: {match}')
                    if match[0].name in ("确认","确认结算"):
                        self.click_box(match, after_sleep=8)
                    break
        self.sleep(2)

    def is_main(self, recheck_time=0, esc=True):
        boxes = self.ocr(match=['整备室', '公共区', '活动层', re.compile('招募')], box='right', log=True)
        self.log_info(f'is main {len(boxes)} {boxes}')
        if len(boxes) == 3:
            if recheck_time:
                self.sleep(recheck_time)
                return self.is_main(recheck_time=0, esc=False)
            else:
                return True
        # if not self.do_handle_alert()[0]:
        if box := self.ocr(box="bottom", match=["点击开始", "点击空白处关闭", "取消"],
                           log=True):
            self.click(box, after_sleep=2)
            return False
        if esc:
            if self.check_interval(2):
                self.back()
        self.next_frame()

    def click(self, x=0, y=0, move_back=False, name=None, interval=-1, move=True,
              down_time=0.01, after_sleep=0, key="left"):
        frame = self.frame
        super().click(x, y, move_back=move_back, name=name, move=move, down_time=0.04, after_sleep=after_sleep,
                      interval=interval, key=key)
        if self.debug:
            self.screenshot('click', frame=frame)

    def back(self, after_sleep=0):
        frame = self.frame
        self.send_key('esc', down_time=0.04, after_sleep=after_sleep)
        if self.debug:
            self.screenshot('back', frame=frame)

    def find_top_right_count(self):
        result = self.ocr(0.89, 0.01, 0.99, 0.1, match=re.compile(r"^\d+/\d+$"), box='top_right')
        if not result:
            raise Exception('找不到当前体力或票')
        return int(result[0].name.split('/')[0])

    def find_cost(self, boxes=None, default=30):
        boundary = self.box_of_screen(0.48, 0.56, 0.57, 0.7)
        if not boxes:
            boxes = self.ocr(box=boundary)

        if costs := self.find_boxes(boxes, match=number_re, boundary=boundary):
            cost = int(costs[0].name)
        else:
            cost = default
        return cost

    def fast_combat(self, battle_max=10, plus_x=0.64, plus_y=0.54, default_cost=10,set_cost=None,activity=False):
        self.wait_click_ocr(match=['自律'], box='bottom_right', after_sleep=2, raise_if_not_found=True)
        boxes = self.ocr(log=True, threshold=0.8)
        if next := self.find_boxes(boxes, '下一步', "bottom_right"):
            self.click(next, after_sleep=1)
            boxes = self.ocr(log=True, threshold=0.8)
            default_cost = 30
        current = self.find_boxes(boxes, match=[stamina_re, number_re],
                                  boundary=self.box_of_screen(0.84, 0, 0.99, 0.10))
        if current:
            current = int(current[0].name.split('/')[0])
        elif activity:
            current = 3
        else:
            current = 1
        self.sleep(1)
        if len(find_boxes_by_name(boxes, ["确认", "取消", "上一步"])) != 2 and len(find_boxes_by_name(boxes, ["确认", "取消", "上","一步"])) != 3:
            if self.debug:
                self.screenshot('fast_no_zilv')
            self.log_info("自律没有弹窗, 可能是调度权限不足")
            return current
        if set_cost:
            cost=set_cost
        else:
            cost = self.find_cost(boxes, default=default_cost)

        self.info_set('current_stamina', current)
        self.info_set('battle_cost', cost)
        self.info_set('battle_max', battle_max)
        can_fast_count = min(int(current / cost), battle_max)
        self.info_set('can_fast_count', can_fast_count)
        self.info_set('click_battle_plus', 0)
        self.log_info(f'battle cost: {cost} current_stamina: {current} can_fast_count: {can_fast_count}')
        for _ in range(can_fast_count - 1):
            self.click(plus_x, plus_y)
            self.info_incr('click_battle_plus')
            self.sleep(0.2)
        self.sleep(1)
        remaining = current - can_fast_count*cost
        self.info_set('remaining_stamina', remaining)
        if can_fast_count > 0:
            self.click(find_boxes_by_name(boxes, "确认"))
            self.wait_pop_up(count=1)
            self.wait_ocr(match=['自律'], box='bottom_right', raise_if_not_found=True)
        else:
            self.click(find_boxes_by_name(boxes, "取消"))
        return remaining

    def wait_pop_up(self, time_out=15, other=None, box='bottom', count=100):
        start = time.time()
        check = pop_ups.copy()
        if other:
            if isinstance(other, list):
                check += other
            else:
                check.append(other)
        found_count = 0
        while self.wait_ocr(match=pop_ups, box=box, settle_time=2, time_out=(time_out - (time.time() - start)),
                            raise_if_not_found=False) and found_count < count:
            found_count += 1
            self.back(after_sleep=3)
