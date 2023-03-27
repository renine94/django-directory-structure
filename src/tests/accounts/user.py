from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


# Create your tests here.
class UserTestCase(APITestCase):

    def test_회원가입_성공(self):
        """회원가입"""
        # Given
        url = reverse('accounts:user-list')
        data = {'username': 'testuser01', 'password': 'qwer1234!', 'password2': 'qwer1234!'}
        # When
        res = self.client.post(url, data, format='json')
        # Then
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_회원가입_실패(self):
        """회원가입시, 비밀번호를 서로 다르게 입력"""
        # Given
        url = reverse('accounts:user-list')
        data = {'username': 'testuser01', 'password': 'qwer1234!', 'password2': 'qwer1234'}
        # When
        res = self.client.post(url, data, format='json')
        # Then
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['non_field_errors'][0].__str__(), 'password 가 같은지 다시 확인부탁드립니다.')

    def test_회원조회(self):
        """회원 목록 조회"""
        # Given
        url = reverse('accounts:user-list')
        self.test_회원가입_성공()
        # When
        res = self.client.get(url)
        # Then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)

    def test_로그인(self):
        """로그인하면 토큰 획득"""
        # Given
        url = reverse('accounts:login')
        self.test_회원가입_성공()
        login_data = {'username': 'testuser01', 'password': 'qwer1234!'}
        # When
        res = self.client.post(url, login_data)
        # Then
        self.assertEqual(list(res.data.keys()), ['refresh', 'access'])

    def test_로그아웃(self):
        """회원가입후, 로그인하여 refresh 토큰 획득후 로그아웃하여 블랙리스트에 등록"""
        # Given
        login_url = reverse('accounts:login')
        logout_url = reverse('accounts:logout')

        self.test_회원가입_성공()
        login_data = {'username': 'testuser01', 'password': 'qwer1234!'}
        res = self.client.post(login_url, login_data)

        logout_data = {'refresh': res.data['refresh']}
        headers = {'HTTP_AUTHORIZATION': f'Bearer {res.data["access"]}'}

        # When
        logout_res = self.client.post(logout_url, logout_data, **headers)

        # Then
        self.assertEqual(logout_res.status_code, status.HTTP_205_RESET_CONTENT)

    def test_회원탈퇴(self):
        # Given
        self.test_회원가입_성공()
        login_data = {'username': 'testuser01', 'password': 'qwer1234!'}
        res = self.client.post(reverse('accounts:login'), login_data)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {res.data["access"]}'}

        delete_url = reverse('accounts:user-list') + '1/'
        # When
        res = self.client.delete(delete_url, **headers)
        # Then
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
