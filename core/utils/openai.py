from django.conf import settings

import os
import openai


class OpenAI:
    openai.api_key = settings.OPENAI_API_KEY

    @classmethod
    def get_answer(cls, text: str) -> str:
        """chatGPT 에게 요청, 실패시 빈 문자열 리턴"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are thesis summary machine"},
                {"role": "user", "content": f"{text} \n Please summarize the above link's thesis in English in less than 500 bytes"},
            ],
            timeout=10
        )

        is_success = True if response['choices'][0]['finish_reason'] == 'stop' else False
        if not is_success:
            return ''

        result = response['choices'][0]['message']['content']
        return result
