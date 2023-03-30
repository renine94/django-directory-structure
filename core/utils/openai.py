from django.conf import settings

from rest_framework.exceptions import APIException

import os
import openai


class OpenAI:
    openai.api_key = settings.OPENAI_API_KEY

    @classmethod
    def get_answer(cls, text: str) -> str:
        """chatGPT 에게 요청, 실패시 빈 문자열 리턴"""
        try:
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
        except Exception as e:
            raise APIException(f'OpenAI 서버 임시 오류입니다. 재시도 부탁드립니다.\n 오류: {e}')
