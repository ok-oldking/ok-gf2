from src.tasks.BaseGfTask import BaseGfTask,stamina_re


class TestTask(BaseGfTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "测试用"
    def run(self):
        self.click(10,540)
        self.scroll(10,540,count=-30)