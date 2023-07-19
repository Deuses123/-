import base64
import requests
import Levenshtein
import httpx


def process_json_response(json_response, answers, variables):
    data = json_response

    responses = data["responses"]
    if len(responses) > 0:
        web_detection = responses[0].get("webDetection")
        if web_detection:
            web_entities = web_detection.get("webEntities")
            if web_entities:
                print("Web entities found:")
                for entity in web_entities:
                    entity_id = entity.get("entityId")
                    score = entity.get("score")
                    description = entity.get("description")
                    print(f"Entity ID: {entity_id}")
                    print(f"Score: {score}")
                    description = translate_text(description.lower())
                    for i in answers:
                        if translate_text(i.lower()).__contains__(description):
                            variables[answers.index(i)] = variables[answers.index(i)] + 1
                    print(f"Description: {description}")

            full_matching_images = web_detection.get("fullMatchingImages")
            if full_matching_images:
                print("Full matches found:")
                for image in full_matching_images:
                    url = image.get("url")
                    print(f"URL: {url}")

            partial_matching_images = web_detection.get("partialMatchingImages")
            if partial_matching_images:
                print("Partial matches found:")
                for image in partial_matching_images:
                    url = image.get("url")
                    print(f"URL: {url}")

            pages_with_matching_images = web_detection.get("pagesWithMatchingImages")
            if pages_with_matching_images:
                print("Pages with matching images found:")
                for page in pages_with_matching_images:
                    url = page.get("url")
                    print(f"URL: {url}")

            visually_similar_images = web_detection.get("visuallySimilarImages")
            if visually_similar_images:
                print("Visually similar images found:")
                for image in visually_similar_images:
                    url = image.get("url")
                    print(f"URL: {url}")

            best_guess_labels = web_detection.get("bestGuessLabels")
            if best_guess_labels:
                print("Best guess labels found:")
                for label in best_guess_labels:
                    label_text = label.get("label")
                    print(f"Label: {label_text}")
                    description = translate_text(label_text.lower())
                    for i in answers:
                        if description.__contains__(translate_text(i.lower())):
                            variables[answers.index(i)] = variables[answers.index(i)] + 1

def reverse_image_search(image_path, api_token):
    url = "https://vision.googleapis.com/v1/images:annotate?key={}".format(api_token)
    headers = {"Content-Type": "application/json"}

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    image_base64 = base64.b64encode(image_data).decode()

    payload = {
        "requests": [
            {
                "image": {
                    "content": image_base64
                },
                "features": [
                    {
                        "type": "WEB_DETECTION"
                    }
                ],
                "imageContext": {
                    "languageHints": ["ru"]
                }
            }
        ]
    }

    response = httpx.post(url, headers=headers, json=payload)
    response_json = response.json()

    return response_json




def translate_text(text):
    api_url = "https://translation.googleapis.com/language/translate/v2"
    api_key = "AIzaSyDGMOSupxDlk12r0qQKVDZjvWTspjTc-jE"

    params = {
        'key': api_key,
        'q': text,
        'target': 'ru',
    }

    response = httpx.get(api_url, params=params)
    print(response.json())
    translation = response.json()['data']['translations'][0]['translatedText']
    return translation



def poisk(variables, answers):
    image_path = "cropped_image.jpg"
    api_token = "AIzaSyDGMOSupxDlk12r0qQKVDZjvWTspjTc-jE"
    process_json_response(reverse_image_search(image_path, api_token), answers, variables)

#
# string1 = "Apple"
# string2 = "Яблако"
#
# string1 = translate_text(string1, 'ru')
# normalized_distance = Levenshtein.distance(string1, string2) / max(len(string1), len(string2))
# similarity_percentage = (1 - normalized_distance) * 100
#
# print(similarity_percentage)
# if similarity_percentage >= 50:
#     print("Строки похожи")
# else:
#     print("Строки не похожи")
