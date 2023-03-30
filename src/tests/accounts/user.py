from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


# Create your tests here.
class UserTestCase(APITestCase):
    """ 테스트 코드 작성 순서
    Given
    When
    Then
    """

    def setUp(self):  # Spring에서 BeforeEach 함수와 유사
        self.client = APIClient()
        self.user_data = {'username': 'testuser01', 'password': 'qwer1234!', 'password2': 'qwer1234!'}
        self.url = reverse('src:user_v1-list')
        self.login_url = reverse('src:user_v1-login')
        self.logout_url = reverse('src:user_v1-logout')

    def test_회원가입_성공(self):
        """회원가입 성공 시 201 상태코드를 반환해야 함"""
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_회원가입_실패(self):
        """비밀번호가 일치하지 않으면 400 상태코드와 에러 메시지를 반환해야 함"""
        self.user_data['password2'] = 'wrong_password'
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'password 가 같은지 다시 확인부탁드립니다.')

    def test_회원조회(self):
        """회원 목록 조회 시, 가입한 회원이 한 명이어야 함"""
        self.client.post(self.url, self.user_data, format='json')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_로그인(self):
        """로그인 시, refresh와 access 토큰이 반환되어야 함"""
        self.client.post(self.url, self.user_data, format='json')  # 회원가입
        response = self.client.post(self.login_url, {'username': 'testuser01', 'password': 'qwer1234!'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_로그아웃(self):
        """회원가입후, 로그인하여 refresh 토큰 획득후 로그아웃하여 블랙리스트에 등록"""
        # Given
        self.client.post(self.url, self.user_data, format='json')
        login_data = {'username': 'testuser01', 'password': 'qwer1234!'}
        res = self.client.post(self.login_url, login_data)

        logout_data = {'refresh': res.data['refresh']}
        headers = {'HTTP_AUTHORIZATION': f'Bearer {res.data["access"]}'}

        # When
        logout_res = self.client.post(self.logout_url, logout_data, **headers)

        # Then
        self.assertEqual(logout_res.status_code, status.HTTP_205_RESET_CONTENT)

    def test_회원탈퇴(self):
        # Given
        self.client.post(self.url, self.user_data, format='json')
        login_data = {'username': 'testuser01', 'password': 'qwer1234!'}
        res = self.client.post(self.login_url, login_data)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {res.data["access"]}'}

        # When
        delete_url = reverse('src:user_v1-list') + '1/'
        res = self.client.delete(delete_url, **headers)

        # Then
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
