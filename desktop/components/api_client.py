"""
API Client for Desktop Application
Connects to Django REST API
"""

import requests
from typing import Optional, Dict, Any, List
import os


class APIClient:
    """REST API client for the desktop application"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.user = None
    
    def _get_csrf_token(self) -> Optional[str]:
        """Get CSRF token from cookies"""
        return self.session.cookies.get('csrftoken')
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an authenticated request"""
        url = f"{self.base_url}{endpoint}"
        
        # Add CSRF token for unsafe methods
        if method.upper() in ['POST', 'PUT', 'PATCH', 'DELETE']:
            csrf_token = self._get_csrf_token()
            if csrf_token:
                headers = kwargs.get('headers', {})
                headers['X-CSRFToken'] = csrf_token
                kwargs['headers'] = headers
        
        response = self.session.request(method, url, **kwargs)
        return response
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login to the API"""
        # First get CSRF token
        self.session.get(f"{self.base_url}/auth/login/")
        
        response = self._request(
            'POST', 
            '/auth/login/',
            json={'username': username, 'password': password}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.user = data.get('user')
            return {'success': True, 'user': self.user}
        else:
            return {'success': False, 'error': response.json().get('error', 'Login failed')}
    
    def logout(self) -> bool:
        """Logout from the API"""
        try:
            self._request('POST', '/auth/logout/')
            self.user = None
            return True
        except:
            return False
    
    def get_user(self) -> Optional[Dict[str, Any]]:
        """Get current user info"""
        try:
            response = self._request('GET', '/auth/user/')
            if response.status_code == 200:
                self.user = response.json()
                return self.user
        except:
            pass
        return None
    
    def get_datasets(self) -> List[Dict[str, Any]]:
        """Get list of datasets"""
        response = self._request('GET', '/datasets/')
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_dataset(self, dataset_id: int) -> Optional[Dict[str, Any]]:
        """Get dataset details with records"""
        response = self._request('GET', f'/datasets/{dataset_id}/')
        if response.status_code == 200:
            return response.json()
        return None
    
    def upload_dataset(self, file_path: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Upload a CSV file"""
        if not os.path.exists(file_path):
            return {'success': False, 'error': 'File not found'}
        
        if name is None:
            name = os.path.basename(file_path).replace('.csv', '')
        
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/csv')}
            data = {'name': name}
            
            response = self._request('POST', '/datasets/upload/', files=files, data=data)
        
        if response.status_code == 201:
            return {'success': True, 'dataset': response.json()}
        else:
            return {'success': False, 'error': response.json().get('error', 'Upload failed')}
    
    def delete_dataset(self, dataset_id: int) -> bool:
        """Delete a dataset"""
        response = self._request('DELETE', f'/datasets/{dataset_id}/')
        return response.status_code == 204
    
    def get_report_url(self, dataset_id: int) -> str:
        """Get URL for PDF report download"""
        return f"{self.base_url}/datasets/{dataset_id}/report/"
    
    def download_report(self, dataset_id: int, save_path: str) -> bool:
        """Download PDF report to file"""
        try:
            response = self._request('GET', f'/datasets/{dataset_id}/report/')
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
        except:
            pass
        return False
