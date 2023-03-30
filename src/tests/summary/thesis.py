from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from unittest.mock import patch

from src.models.accounts.user import User


# Create your tests here.
class ThesisTestCase(APITestCase):
    """논문 API 관련 테스트 케이스"""

    def setUp(self) -> None:
        self.user_data = {'username': 'testuser01', 'password': 'qwer1234!'}
        self.url = reverse('src:thesis_v1-list')
        self.login_url = reverse('src:user_v1-login')
        self.user = User.objects.create_user(**self.user_data)
        self.access_token = self.client.post(self.login_url, self.user_data).data['access']

    @patch('core.utils.openai.OpenAI.get_answer', return_value='OpenAI Result Mock')
    @patch('src.models.User.get_cached_thesis_by_url', return_value=None)
    def test_논문요약_요청_성공(self, mocked_redis_call, mock_openai_call):
        """논문 요약 요청, Redis 가져오는부분 mocking 처리"""
        # Given
        data = {'url': 'https://arxiv.org/pdf/2303.13323'}
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

        # When
        res = self.client.post(self.url, data, format='json', **headers)  # 논문요약 요청

        # Then
        mocked_redis_call.assert_called_once()
        mock_openai_call.assert_called_once()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    @patch('core.utils.openai.OpenAI.get_answer', return_value='OpenAI Result Mock')
    @patch('src.models.accounts.User.get_cached_thesis_by_url', return_value=None)
    def test_논문요약_요청_실패_토큰부족(self, mocked_redis_call, mock_openai_call):
        """논문 요약 요청, 토큰부족으로 인한 실패"""
        # Given
        data = {'url': 'https://arxiv.org/pdf/2303.13323'}
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

        # When
        self.client.post(self.url, data, format='json', **headers)  # 이미 한번 요청
        res = self.client.post(self.url, data, format='json', **headers)  # 2번째 요청

        # Then
        self.assertEqual(mocked_redis_call.call_count, 2)
        self.assertEqual(mock_openai_call.call_count, 1)  # 2번째 요청에선 이미 캐싱된 값을 return 하므로 1번만 호출된다.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'], '보유 토큰이 부족합니다.')
