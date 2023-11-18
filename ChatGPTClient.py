import os
import openai

# -> None 은 함수 반환값의 주석

class ChatGPTClient():
    def __init__(self) -> None:
        self.openai = openai
        self.openai.api_key = "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"

    def request_summary(self, transcript) -> str:
        messages = []
        content = "다음 뉴스 스크립트를 5개의 문장으로 요약해줘\n 뉴스 스크립트:\n" + transcript
        messages.append({"role": "user", "content": f"{content}"})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages
        )
        return response['choices'][0]['message']['content'].strip()

