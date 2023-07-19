import base64
import io
import time
import webbrowser
from datetime import datetime
import pytesseract
import httpx
import keyboard
import pyautogui
import pygetwindow as gw
import pyperclip
import win32clipboard
from PIL import Image

import main


def compress_image(input_path, output_path, quality=85):
    image = Image.open(input_path)
    image.save(output_path, optimize=True, quality=20)


def extract_texts():
    image_path = "D:\\SDKMODEL\\cropped_image.jpg"
    folder_id = "b1g3ki01pbguna3cb7q1"
    token = 't1.9euelZqSyorHypydnZnKiovKj8aKy-3rnpWayszJlZKVz5KJyceXmMyJyZvl8_czRCFa-e8bSkQw_t3z93NyHlr57xtKRDD-zef1656VmpePm8qKnp2OjZ2Oz8nMmJic7_zF656VmpePm8qKnp2OjZ2Oz8nMmJic.C2CQP8VWIK3fXBy-R0v47WlkMbRTDXrYW6v9VSNfa_fJ9QWGJZOu3dwzrpHpu8eUEr4FcxEgQqStLeohZRvbCg'
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode()

    body = {
        "folderId": folder_id,
        "analyze_specs": [
            {
                "features": [
                    {
                        "type": "TEXT_DETECTION",
                        "text_detection_config": {
                            "language_codes": ["*"]
                        }
                    }
                ],
                "content": encoded_image
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    a = datetime.now()

    response = httpx.post("https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze", json=body, headers=headers)

    json_data = response.json()
    results = json_data["results"]
    b = datetime.now()

    print(b - a)

    texts = []
    question = []
    flag = False
    temp = ''

    for result in results:
        for text_result in result.get('results', []):
            for page in text_result.get('textDetection', {}).get('pages', []):
                for block in page.get('blocks', []):
                    if not flag:
                        for line in block.get('lines', []):
                            for word in line.get('words', []):
                                question.append(word.get('text', ''))
                        flag = True
                    else:
                        for line in block.get('lines', []):
                            for word in line.get('words', []):
                                temp = temp + word.get('text', '') + ' '
                        texts.append(temp)
                        temp = ''

    return ' '.join(question), texts


def find_answers(snippet, answers, variables):
    for i in answers:
        if snippet.lower().__contains__(i.lower()):
            j = answers.index(i)
            variables[j] = variables[j] + 1


def on_key_press(event):
    if keyboard.is_pressed('shift+z'):
        print("______________")
        left = (pyautogui.size().width // 2) - 300
        top = (pyautogui.size().height // 2) - 330
        width = 600
        height = 500
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot.save("cropped_image.png")
        compress_image("cropped_image.png", "cropped_image.jpg", quality=30)

        question, answers = extract_texts()
        print(question)
        cse_api_url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyDRuOH3tzTgnrwliUz8c0VlO9yYyzzmnko&cx" \
                      f"=f4dec4a8b46e546c4&q={question}"

        response = httpx.get(cse_api_url)

        if response.status_code == 200:
            data = response.json()

            if 'spelling' in data:
                a = []
            if True:
                if len(answers) != 4:
                    webbrowser.open(f"https://www.google.kz/search?q={question}")
                else:
                    search_results = data['items']
                    variables = [0, 0, 0, 0]
                    for result in search_results:
                        title = result['title']
                        link = result['link']
                        snippet = result['snippet']

                        find_answers(snippet, answers, variables)

                    print(answers[variables.index(max(variables))])

        elif response.status_code == 429:
            print("Брат слишком дохуя вопросов к серверу")

        else:
            print(f"А хуй пойми что за ошибка {response.status_code}")


    elif keyboard.is_pressed('shift+c'):
        print("______________")
        left = (pyautogui.size().width // 2) - 300
        top = (pyautogui.size().height // 2) - 330
        width = 600
        height = 500
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot.save("cropped_image.png")
        compress_image("cropped_image.png", "cropped_image.jpg", 30)

        te = ''
        answers = []
        flag = False
        text = extract_texts()
        for i in text:
            if flag:
                answers.append(i)
                continue
            if '?' not in i:
                te = te + " " + i
            else:
                te = te + " " + i
                flag = True

        for i in answers:
            webbrowser.open(f"https://www.google.kz/search?q={i}")

    elif keyboard.is_pressed('shift+v'):
        print("______________")
        left = (pyautogui.size().width // 2) - 300
        top = (pyautogui.size().height // 2) - 330
        width = 600
        height = 500
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot.save("cropped_image.png")
        compress_image("cropped_image.png", "cropped_image.jpg", 30)

        te = ''
        for i in extract_texts():
            te = te + i + " "
        pyperclip.copy(te)

    elif keyboard.is_pressed('shift+f'):
        print("______________")
        left = (pyautogui.size().width // 2) - 300
        top = (pyautogui.size().height // 2) - 330
        width = 600
        height = 500
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot.save("cropped_image.png")
        compress_image("cropped_image.png", "cropped_image.jpg", 30)
        te = 'Ответь максимально кратко на этот вопрос выбрав один из 4 вариантов. '
        for i in extract_texts():
            te = te + i + " "
        print(te)
        pyperclip.copy(te)

        window = gw.getWindowsWithTitle('Edge')[0]
        window.activate()
        pyautogui.sleep(0.1)
        pyautogui.click(1606, 967, button='left')
        pyautogui.sleep(0.1)
        pyautogui.keyDown('ctrl')
        pyautogui.press('v')
        pyautogui.keyUp('ctrl')
        pyautogui.sleep(0.1)
        pyautogui.press('enter')

    elif keyboard.is_pressed('shift+d'):
        print("______________")
        left = (pyautogui.size().width // 2) - 300
        top = (pyautogui.size().height // 2) - 330
        width = 600
        height = 500
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot.save('cropped_image.png')
        compress_image('cropped_image.png', 'cropped_image.jpg', 30)
        screenshot = Image.open('cropped_image.jpg')
        output = io.BytesIO()
        screenshot.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        variables = [0, 0, 0, 0]
        question, answers = extract_texts()

        main.poisk(variables, answers)

        print(max(variables))
        print(answers[variables.index(max(variables))])
        # send_to_clipboard(win32clipboard.CF_DIB, data)
        #
        # webbrowser.open("https://www.google.kz/")
        # time.sleep(1)
        # pyautogui.click(1314, 467, button='left')
        # time.sleep(1)
        # pyautogui.keyDown('ctrl')
        # pyautogui.press('v')
        # pyautogui.keyUp('ctrl')


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


keyboard.on_press(on_key_press)
keyboard.wait()
