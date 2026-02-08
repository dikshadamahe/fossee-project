"""
API Client - Django REST API Integration
Chemical Equipment Parameter Visualizer - PyQt5 Desktop
FOSSEE Scientific Analytics

Centralized API client matching web-frontend/src/api/client.js (axios).
See API_SPEC.yaml for full specification.
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import pandas as pd
from io import BytesIO


# =============================================================================
# CONFIGURATION (matches React client.js)
# =============================================================================

class Config:
    """API Configuration - centralized settings"""
    BASE_URL = "http://localhost:8000"
    API_PREFIX = "/api"
    TIMEOUT = 30  # seconds


# =============================================================================
# ENDPOINTS (matches React Endpoints object)
# =============================================================================

class Endpoints:
    """
    Centralized endpoint definitions.
    Identical to web-frontend/src/api/client.js Endpoints.
    """
    # POST - Upload CSV file
    UPLOAD = '/upload/'
    
    # GET - List all datasets (history)
    DATASETS = '/datasets/'
    
    @staticmethod
    def summary(dataset_id: int) -> str:
        """GET - Dataset summary statistics"""
        return f'/summary/{dataset_id}/'
    
    @staticmethod
    def dataset(dataset_id: int) -> str:
        """GET/DELETE - Single dataset with records"""
        return f'/datasets/{dataset_id}/'
    
    @staticmethod
    def report(dataset_id: int) -> str:
        """GET - Download PDF report"""
        return f'/report/{dataset_id}/'


# =============================================================================
# RESPONSE WRAPPER
# =============================================================================

@dataclass
class APIResponse:
    """Standard API response wrapper"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# =============================================================================
# API CLIENT
# =============================================================================

class APIClient:
    """
    REST API client for Django backend (requests library).
    Mirrors web-frontend/src/api/client.js (axios).
    
    Usage:
        from api_client import get_client, Endpoints
        client = get_client()
        result = client.upload('/path/to/file.csv')
    """
    
    def __init__(self, base_url: str = None):
        self.base_url = (base_url or Config.BASE_URL).rstrip('/')
        self.session = requests.Session()
        self.timeout = Config.TIMEOUT
    
    def _url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        return f"{self.base_url}{Config.API_PREFIX}{endpoint}"
    
    def _handle_response(self, response: requests.Response) -> APIResponse:
        """Process API response"""
        try:
            if response.status_code in (200, 201):
                return APIResponse(success=True, data=response.json())
            elif response.status_code == 204:
                return APIResponse(success=True, data={})
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', f'HTTP {response.status_code}')
                except:
                    error_msg = f'HTTP {response.status_code}: {response.text[:200]}'
                return APIResponse(success=False, error=error_msg)
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def check_connection(self) -> bool:
        """Check if backend is reachable"""
        try:
            response = self.session.get(
                self._url(Endpoints.DATASETS),
                timeout=5
            )
            return response.status_code in (200, 401, 403)
        except:
            return False
    
    # =====================================================================
    # UPLOAD (POST /api/upload/)
    # =====================================================================
    
    def upload(self, filepath: str, filename: Optional[str] = None) -> APIResponse:
        """
        Upload CSV file to backend
        
        Args:
            filepath: Local path to CSV file
            filename: Optional custom filename
            
        Returns:
            APIResponse with dataset_id and summary on success
        """
        try:
            with open(filepath, 'rb') as f:
                files = {'file': (filename or filepath.split('/')[-1], f, 'text/csv')}
                data = {}
                if filename:
                    data['filename'] = filename
                
                response = self.session.post(
                    self._url(Endpoints.UPLOAD),
                    files=files,
                    data=data,
                    timeout=self.timeout
                )
            
            return self._handle_response(response)
        except FileNotFoundError:
            return APIResponse(success=False, error=f"File not found: {filepath}")
        except requests.exceptions.ConnectionError:
            return APIResponse(success=False, error="Cannot connect to server. Is Django running?")
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    # =====================================================================
    # SUMMARY (GET /api/summary/<id>/)
    # =====================================================================
    
    def get_summary(self, dataset_id: int) -> APIResponse:
        """Get dataset summary statistics"""
        try:
            response = self.session.get(
                self._url(Endpoints.summary(dataset_id)),
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.ConnectionError:
            return APIResponse(success=False, error="Cannot connect to server")
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    # =====================================================================
    # DATASETS (GET /api/datasets/)
    # =====================================================================
    
    def get_datasets(self) -> APIResponse:
        """Get list of all uploaded datasets (history)"""
        try:
            response = self.session.get(
                self._url(Endpoints.DATASETS),
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.ConnectionError:
            return APIResponse(success=False, error="Cannot connect to server")
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def get_dataset(self, dataset_id: int) -> APIResponse:
        """Get single dataset with all records"""
        try:
            response = self.session.get(
                self._url(Endpoints.dataset(dataset_id)),
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.ConnectionError:
            return APIResponse(success=False, error="Cannot connect to server")
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def delete_dataset(self, dataset_id: int) -> APIResponse:
        """DELETE /api/datasets/<id>/ - Delete a dataset"""
        try:
            response = self.session.delete(
                self._url(Endpoints.dataset(dataset_id)),
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.ConnectionError:
            return APIResponse(success=False, error="Cannot connect to server")
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    # =====================================================================
    # REPORT (GET /api/report/<id>/)
    # =====================================================================
    
    def download_report(self, dataset_id: int, save_path: str) -> APIResponse:
        """Download PDF report for dataset"""
        try:
            response = self.session.get(
                self._url(Endpoints.report(dataset_id)),
                timeout=60  # PDF generation may take longer
            )
            
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return APIResponse(success=True, data={'path': save_path})
            else:
                return self._handle_response(response)
        except requests.exceptions.ConnectionError:
            return APIResponse(success=False, error="Cannot connect to server")
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    # =====================================================================
    # HELPERS
    # =====================================================================
    
    def dataset_to_dataframe(self, dataset_id: int) -> Optional[pd.DataFrame]:
        """
        Fetch dataset and convert to pandas DataFrame
        """
        result = self.get_dataset(dataset_id)
        if not result.success or not result.data:
            return None
        
        records = result.data.get('records', [])
        if not records:
            return None
        
        df = pd.DataFrame(records)
        
        # Rename fields to match expected columns
        column_map = {
            'equipment_name': 'Equipment Name',
            'equipment_type': 'Type',
            'flowrate': 'Flowrate',
            'pressure': 'Pressure',
            'temperature': 'Temperature',
        }
        df = df.rename(columns=column_map)
        
        return df


# Singleton instance
_client: Optional[APIClient] = None


def get_client(base_url: str = "http://localhost:8000") -> APIClient:
    """Get or create API client singleton"""
    global _client
    if _client is None:
        _client = APIClient(base_url)
    return _client
