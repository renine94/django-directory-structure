from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from unittest.mock import patch

from src.models.accounts.user import User


# Create your tests here.
class ThesisTestCase(APITestCase):
    """논문 API 관련 테스트 케이스"""

    def setUp(self) -> None:
        self.url = reverse('src:thesis-list')
        self.user = User.objects.create_user(username='testuser01', password='qwer1234!')
        data = {'username': self.user.username, 'password': 'qwer1234!'}
        res = self.client.post(reverse('src:login'), data)
        self.access_token = res.data['access']

    @patch('core.utils.openai.OpenAI.get_answer', return_value='OpenAI Result Mock')
    @patch('src.models.User.get_cached_thesis_by_url', return_value=None)
    def test_논문요약_요청_성공(self, mocked_redis_call, mock_openai_call):
        """논문 요약 요청, Redis 가져오는부분 mocking 처리"""
        # Given
        url = reverse('src:thesis-list')
        data = {'url': 'https://arxiv.org/pdf/2303.13323'}
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

        # When
        res = self.client.post(url, data, format='json', **headers)

        # Then
        mocked_redis_call.assert_called_once()
        mock_openai_call.assert_called_once()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    @patch('core.utils.openai.OpenAI.get_answer', return_value='OpenAI Result Mock')
    @patch('src.models.accounts.User.get_cached_thesis_by_url', return_value=None)
    def test_논문요약_요청_실패_토큰부족(self, mocked_redis_call, mock_openai_call):
        """논문 요약 요청, 토큰부족으로 인한 실패"""
        # Given
        self.test_논문요약_요청_성공()
        url = reverse('src:thesis-list')
        data = {'url': 'https://arxiv.org/pdf/2303.13323'}
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

        # When
        res = self.client.post(url, data, format='json', **headers)
        # Then
        mocked_redis_call.assert_called_once()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'], '보유 토큰이 부족합니다.')
