import time

import cv2


def test():
    from paddleocr import PaddleOCR

    ocr = PaddleOCR(
        use_doc_orientation_classify=False,  # 通过 use_doc_orientation_classify 参数指定不使用文档方向分类模型
        use_doc_unwarping=False,  # 通过 use_doc_unwarping 参数指定不使用文本图像矫正模型
        use_textline_orientation=False,  # 通过 use_textline_orientation 参数指定不使用文本行方向分类模型
        # text_detection_model_name="PP-OCRv5_server_det",
        # text_recognition_model_name="PP-OCRv5_server_rec",
        device="gpu",
        cpu_threads=1
    )
    # ocr = PaddleOCR(lang="en") # 通过 lang 参数来使用英文模型
    # ocr = PaddleOCR(ocr_version="PP-OCRv4") # 通过 ocr_version 参数来使用 PP-OCR 其他版本
    # ocr = PaddleOCR(device="gpu") # 通过 device 参数使得在模型推理时使用 GPU
    # ocr = PaddleOCR(
    #     text_detection_model_name="PP-OCRv5_server_det",
    #     text_recognition_model_name="PP-OCRv5_server_rec",
    #     use_doc_orientation_classify=False,
    #     use_doc_unwarping=False,
    #     use_textline_orientation=False,
    # ) # 更换 PP-OCRv5_server 模型
    image = cv2.imread("1.png")
    # image = cv2.imread("tests/images/main.png")
    image = image[1:-1, 1:-1]
    for i in range(100):
        start = time.time()
        results = ocr.predict(image)
        detected_boxes = []
        # Process the results and create Box objects
        if results:
            result = results[0]

            for idx in range(len(result['rec_texts'])):
                pos = result['rec_boxes'][idx]
                text = result['rec_texts'][idx]
                confidence = result['rec_scores'][idx]

                width, height = round(pos[2] - pos[0]), round(pos[3] - pos[1])
                if width <= 0 or height <= 0:
                    continue
                # detected_box = res
                detected_box = [text, confidence, width, height]
                if detected_box:
                    detected_boxes.append(detected_box)
        print(f"detected box: {len(detected_box)} cost time: {time.time() - start}")


if __name__ == '__main__':
    # test()
    # import threading
    #
    # my_thread = threading.Thread(target=test)
    # my_thread.start()
    from config import config
    from ok import OK

    config = config
    config["ocr"] = {"lib": "paddleocr", "params": {"device": "gpu",
                                                    # "text_detection_model_name": "PP-OCRv5_server_det",
                                                    # "text_recognition_model_name": "PP-OCRv5_server_rec",
                                                    "text_rec_score_thresh": 0.5, "cpu_threads": 1}}
    # config["ocr"] = {"lib": "paddleocr", "params": {}}
    ok = OK(config)
    ok.start()
