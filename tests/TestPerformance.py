# Test case
import time
import unittest

from config import config
from ok import DiagnosisTask
from ok.test.TaskTestCase import TaskTestCase


class TestBattleBaseSerialization(TaskTestCase):
    task_class = DiagnosisTask

    config = config
    config["ocr"] = {"lib": "paddleocr", "params": {"device": "gpu",
                                                    "text_detection_model_name": "PP-OCRv5_server_det",
                                                    "text_recognition_model_name": "PP-OCRv5_server_rec",
                                                    "text_rec_score_thresh": 0.5, "cpu_threads": 1}}

    def test_paiqian(self):
        # Create a BattleReport object

        self.set_image('tests/images/main.png')
        import threading

        for i in range(1):
            start = time.time()
            boxes = self.task.ocr()
            self.task.log_debug(f'ocr time: {time.time() - start} , boxes: {len(boxes)}')
            print(threading.enumerate())


if __name__ == '__main__':
    unittest.main()
