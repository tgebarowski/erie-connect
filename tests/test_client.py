"""Erie Connect tests."""
import unittest
from erie_connect.client import ErieConnect
from unittest import mock


class ErieConnectTestCase(unittest.TestCase):

    def mocked_execute_request_with_login_200_OK(method, url, params, **kwargs):
        return ErieConnect.Response(headers={ 'Access-Token': 'XYZ',
                                              'Client' : '123',
                                              'Uid': 'john@foo.bar',
                                              'Expiry': '123456789'}, 
                                    content="")

    @mock.patch('erie_connect.client.ErieConnect._execute_request',
                 side_effect=mocked_execute_request_with_login_200_OK)
    def test_login_should_set_auth_info(self, mock_get):
        client = ErieConnect('foo', 'bar')
        client.login()
        
        assert True == client.is_logged_in
        assert False == client.is_device_selected
       
if __name__ == '__main__':
    unittest.main()
