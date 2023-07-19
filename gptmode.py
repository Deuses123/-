import requests


def chat_with_model(prompt):
    url = 'https://api.openai.com/v1/engines/davinci/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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'
    }

    data = {
        'prompt': prompt,
        'max_tokens': 50,
        'temperature': 0.7,
        'n': 1
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    if 'choices' in response_data and len(response_data['choices']) > 0:
        completion_text = response_data['choices'][0]
        print(completion_text)

    return response_data


chat_with_model("Как зовут президента Казахстана?")
