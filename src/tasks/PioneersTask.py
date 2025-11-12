from ok import Logger
from src.tasks.BaseGfTask import BaseGfTask, map_re
import re
logger = Logger.get_logger(__name__)
pattern_kt = re.compile(r'^(?!(?=.*开拓之王)(?=.*区域开拓))(?:开拓之王|区域开拓(?:I|II|III|IV|V|VI|VII))$')


class PioneersTask(BaseGfTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "开拓之王"
        self.description = "从开拓之王主界面开始"

    def use_cmd_die(self):
        """辅助函数：使用指令骰"""
        print("执行指令骰操作（无限次数）")
        # TODO: 在这里实现指令骰的具体逻辑
        pass

    def use_rc_die(self,rc_die):
        """辅助函数：使用遥控骰"""
        rc_die -= 1
        print(f"执行遥控骰，剩余遥控骰={rc_die}")
        # TODO: 在这里实现遥控骰的具体逻辑
        return rc_die

    def function_a(self):
        print("执行主函数A逻辑（占位）")

    def function_b(self):
        print("执行主函数B逻辑（占位）")
    def main(self):
        """主函数：包含A、B两部分逻辑"""



        # 调用主函数逻辑部分
        self.function_a()
        self.function_b()

    def run(self):
        """核心死循环逻辑"""
        rc_die = 3  # 遥控骰：可消耗

        while True:
            if rc_die > 0:
                # 优先执行遥控骰逻辑
                rc_die = self.use_rc_die(rc_die)
                # 遥控骰执行完后调用主函数
                self.main()
            else:
                # 遥控骰耗尽后，执行指令骰逻辑
                self.use_cmd_die()
                # 指令骰执行完后调用主函数
                self.main()

            # 退出条件示例（可修改）
