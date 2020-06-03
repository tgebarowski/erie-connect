from dataclasses import dataclass
from requests import Session
from requests import RequestException
from typing import Dict
from simplejson.errors import JSONDecodeError

class ErieConnect(object):

    @dataclass
    class Response:
        headers: Dict[str, str]
        content: str

    @dataclass
    class Auth:
        access_token: str
        client: str
        uid: str
        expiry: int
    
    @dataclass
    class Device:
        id: int
        name: str

    def __init__(self, username: str, password: str, auth:Auth = None, device: Device = None):
        self._username = username
        self._password = password
        self._auth = auth
        self._device = device
        self._base_url = "https://erieconnect.eriewatertreatment.com/api/erieapp/"
        self._api = "v1"
        self._session = Session()
        self._session.verify = False
        self._debugmode = False
    
    def login(self):
        """Login to Erie Connect using provided username and password and get authorization token"""
        response = self._post('auth/sign_in', data={'email': self._username, 'password' : self._password})
        self._debuglog(str(response))
        self._auth = ErieConnect.Auth(access_token=response.headers["Access-Token"],
                                      client=response.headers["Client"],
                                      uid=response.headers["Uid"],
                                      expiry=response.headers["Expiry"])

    def list_watersofteners(self):
        """List all devices registered in Erie Connect cloud"""
        self._debuglog("List watersofteners")
        response = self._get('/water_softeners/')
        self._debuglog(str(response.content))
        return response

    def dashboard(self):
        """
        Get Dashboard data (water consumption) of the first registered device.
        Note: This method may do initial setup when needed. If user is not logged in
              it will do so and will select first available device.
        """
        self._setup_if_needed()
        self._debuglog("Getting dashboard")
        response = self._get(f'/water_softeners/{self._device.id}/dashboard')
        self._debuglog(str(response.content))
        return response

    def flow(self):
        """
        Get current water flow
        Note: This method may do initial setup when needed. If user is not logged in
              it will do so and will select first available device.
        """
        self._setup_if_needed()
        self._debuglog("Get current flow")
        response = self._get(f'/water_softeners/{self._device.id}/flow')
        self._debuglog(str(response.content))
        return response

    def features(self):
        """
        Get device features
        Note: This method may do initial setup when needed. If user is not logged in
              it will do so and will select first available device.
        """
        self._setup_if_needed()
        self._debuglog("Get features")
        response = self._get(f'/water_softeners/{self._device.id}/features')
        self._debuglog(str(response.content))
        return response

    def settings(self):
        """
        Get device settings including salt alert, service date etc.
        Note: This method may do initial setup when needed. If user is not logged in
              it will do so and will select first available device.
        """
        self._setup_if_needed()
        self._debuglog("Get settings")
        response = self._get(f'/water_softeners/{self._device.id}/settings')
        self._debuglog(str(response.content))
        return response

    def info(self):
        """
        Get device info including service date, total water consumption etc.
        Note: This method may do initial setup when needed. If user is not logged in
              it will do so and will select first available device.
        """
        self._setup_if_needed()
        self._debuglog("Get Info")
        response = self._get(f'/water_softeners/{self._device.id}/info')
        self._debuglog(str(response.content))
        return response        

    def logout(self):
        """Logout currently logged in user"""
        if self._auth != None:
            self._delete('/auth/sign_out')
        self._auth = None

    def select_first_active_device(self):
        """List devices and select first available device as the one on which all queries will be invoked"""
        response = self.list_watersofteners()
        self._device = ErieConnect.Device(id=response.content[0]['profile']['id'],
                                          name=response.content[0]['profile']['name'])

    @property
    def is_logged_in(self):
        return self._auth != None

    @property
    def is_device_selected(self):
        return self._device != None

    @property
    def device(self):
        return self._device

    @property
    def auth(self):
        return self._auth

    def _setup_if_needed(self):
        """Setup client by logging in and selecting default device"""
        if self._auth == None: self.login()
        if self._device == None: self.select_first_active_device()

    def _get(self, path: str, params=None, **kwargs):
        """Handles API GET request."""
        return self._request("GET", self._api, path, params, **kwargs)

    def _post(self, path: str, params=None, data=None, json=None, **kwargs):
        """Handles API POST request"""
        return self._request("POST", self._api, path, data=data, json=json, **kwargs)   

    def _delete(self, path: str, params=None, **kwargs):
        """Handles API DELETE request"""
        return self._request("DELETE", self._api, path, params, **kwargs)     

    def _request(self, request_method: str, api: str, path: str, params=None, retry_once=True, **kwargs):
        """Function to prepare and execute request"""
        # Request data
        url = self._build_url(api, path)
        
        response = self._execute_request(request_method, url, params=params, **kwargs)
        self._debuglog("Successful returned data")
        self._debuglog("API: " + api)
        self._debuglog(str(response))
        return response

    def _execute_request(self, method, url, params, **kwargs):
        """Function to execute and handle a request"""
        headers = {'User-Agent': 'App/2.1.1 (iPhone; iOS 13.3.1; Scale/2.0.0)',
                   'app_version': '2.1.1',
                   'language': 'en'}
        try:
            if method == "GET":
                encoded_params = None
                if params != None:
                    encoded_params = "&".join(
                        "%s=%s" % (key, quote(str(value))) for key, value in params
                    )
                headers['Accept'] = 'application/json'
                headers.update(self._auth_headers())
                response = self._session.get(url, params=encoded_params, headers=headers, **kwargs)
            elif method == "POST":
                headers['Accept'] = 'application/x-www-form-urlencoded'
                response = self._session.post(url, headers=headers, **kwargs)
            elif method == "DELETE":
                headers.update(self._auth_headers())
                response = self._session.delete(url, headers=headers, **kwargs)                

            self._debuglog("Request url: " + response.url)
            self._debuglog("Response status_code: " + str(response.status_code))
            self._debuglog("Response headers: " + str(response.headers))

            if response.status_code == 200:
                return ErieConnect.Response(headers=response.headers, content=response.json())

            # We got a 400, 401 or 404 ...
            raise RequestException(response)

        except (RequestException, JSONDecodeError) as exception:
            raise exception

    def _auth_headers(self):
        """Return authorization headers from configured client"""
        headers = dict()

        if self._auth != None:
            headers['Client'] = self._auth.client
            headers['Access-Token'] = self._auth.access_token
            headers['uid'] = self._auth.uid
        return headers

    def _build_url(self, api, path):
        """Construct endpoint URL"""
        return f'{self._base_url}/{api}/{path}'

    def _debuglog(self, message):
        """Helper for debugging"""
        """Outputs message if debug mode is enabled."""
        if self._debugmode:
            print("DEBUG: " + message)


if __name__ == "__main__":
    client = ErieConnect('foo@bar', 'passwd')
    client.login()
    client.dashboard()
    client.flow()
    client.settings()
    client.features()
    client.logout()
