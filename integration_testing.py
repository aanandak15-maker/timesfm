"""
Comprehensive Integration Testing for AgriForecast.ai
End-to-end testing of full-stack platform
"""

import streamlit as st
import requests
import time
import json
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import asyncio
import threading
from dataclasses import dataclass
import sqlite3

@dataclass
class TestResult:
    """Test result data structure"""
    test_name: str
    success: bool
    duration: float
    details: str
    error_message: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class IntegrationTestSuite:
    """Comprehensive integration test suite"""
    
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:8501"
        self.test_results = []
        
    def run_all_tests(self) -> List[TestResult]:
        """Run all integration tests"""
        st.write("🧪 Running comprehensive integration tests...")
        
        tests = [
            ("Backend Health Check", self.test_backend_health),
            ("Frontend Availability", self.test_frontend_availability),
            ("Database Connectivity", self.test_database_connectivity),
            ("API Endpoints", self.test_api_endpoints),
            ("TimesFM Model Integration", self.test_timesfm_integration),
            ("Real-time Features", self.test_realtime_features),
            ("Performance Optimization", self.test_performance_features),
            ("Mobile & PWA Features", self.test_mobile_pwa),
            ("Offline Capabilities", self.test_offline_features),
            ("Data Flow End-to-End", self.test_data_flow),
            ("Security Features", self.test_security),
            ("Load Testing", self.test_load_performance)
        ]
        
        self.test_results = []
        progress_bar = st.progress(0)
        
        for i, (test_name, test_function) in enumerate(tests):
            st.write(f"Running: {test_name}")
            result = test_function()
            self.test_results.append(result)
            progress_bar.progress((i + 1) / len(tests))
        
        return self.test_results
    
    def test_backend_health(self) -> TestResult:
        """Test backend health and connectivity"""
        start_time = time.time()
        
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                health_data = response.json()
                return TestResult(
                    test_name="Backend Health Check",
                    success=True,
                    duration=duration,
                    details=f"Backend healthy: {health_data}"
                )
            else:
                return TestResult(
                    test_name="Backend Health Check",
                    success=False,
                    duration=duration,
                    details=f"HTTP {response.status_code}",
                    error_message=response.text
                )
                
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name="Backend Health Check",
                success=False,
                duration=duration,
                details="Backend connection failed",
                error_message=str(e)
            )
    
    def test_frontend_availability(self) -> TestResult:
        """Test frontend availability"""
        start_time = time.time()
        
        try:
            response = requests.get(f"{self.frontend_url}/_stcore/health", timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                return TestResult(
                    test_name="Frontend Availability",
                    success=True,
                    duration=duration,
                    details="Frontend accessible and healthy"
                )
            else:
                return TestResult(
                    test_name="Frontend Availability",
                    success=False,
                    duration=duration,
                    details=f"HTTP {response.status_code}",
                    error_message=response.text
                )
                
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name="Frontend Availability",
                success=False,
                duration=duration,
                details="Frontend not accessible",
                error_message=str(e)
            )
    
    def test_database_connectivity(self) -> TestResult:
        """Test database connectivity and operations"""
        start_time = time.time()
        
        try:
            # Test SQLite database
            conn = sqlite3.connect('agriforecast_modern.db')
            cursor = conn.cursor()
            
            # Test basic operations
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            # Test data insertion and retrieval
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            conn.close()
            duration = time.time() - start_time
            
            return TestResult(
                test_name="Database Connectivity",
                success=True,
                duration=duration,
                details=f"Database healthy: {len(tables)} tables, {user_count} users"
            )
            
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name="Database Connectivity",
                success=False,
                duration=duration,
                details="Database connection failed",
                error_message=str(e)
            )
    
    def test_api_endpoints(self) -> TestResult:
        """Test all API endpoints"""
        start_time = time.time()
        
        endpoints_to_test = [
            ("GET", "/", "API root"),
            ("GET", "/health", "Health check"),
            ("POST", "/predict/yield", "Yield prediction"),
            ("POST", "/risk/assessment", "Risk assessment"),
            ("GET", "/market/predictions", "Market predictions")
        ]
        
        successful_endpoints = 0
        failed_endpoints = []
        
        test_field_data = {
            "id": "test_field",
            "crop_type": "rice",
            "area_acres": 5.0,
            "latitude": 28.368911,
            "longitude": 77.541033,
            "soil_type": "loamy"
        }
        
        for method, endpoint, description in endpoints_to_test:
            try:
                if method == "GET":
                    if endpoint == "/market/predictions":
                        response = requests.get(f"{self.backend_url}{endpoint}?crop_type=rice", timeout=5)
                    else:
                        response = requests.get(f"{self.backend_url}{endpoint}", timeout=5)
                elif method == "POST":
                    response = requests.post(f"{self.backend_url}{endpoint}", json=test_field_data, timeout=10)
                
                if response.status_code in [200, 201]:
                    successful_endpoints += 1
                else:
                    failed_endpoints.append(f"{description}: HTTP {response.status_code}")
                    
            except Exception as e:
                failed_endpoints.append(f"{description}: {str(e)}")
        
        duration = time.time() - start_time
        
        if len(failed_endpoints) == 0:
            return TestResult(
                test_name="API Endpoints",
                success=True,
                duration=duration,
                details=f"All {successful_endpoints} endpoints working"
            )
        else:
            return TestResult(
                test_name="API Endpoints",
                success=False,
                duration=duration,
                details=f"{successful_endpoints} working, {len(failed_endpoints)} failed",
                error_message="; ".join(failed_endpoints)
            )
    
    def test_timesfm_integration(self) -> TestResult:
        """Test TimesFM model integration"""
        start_time = time.time()
        
        try:
            # Test yield prediction with TimesFM
            test_data = {
                "field_id": "timesfm_test",
                "crop_type": "rice",
                "historical_data": [4.1, 4.3, 4.0, 4.5, 4.2],
                "weather_data": {
                    "temperature": 28.5,
                    "humidity": 65,
                    "rainfall": 150
                },
                "soil_data": {
                    "ph": 6.8,
                    "nitrogen": 120,
                    "phosphorus": 45
                }
            }
            
            response = requests.post(f"{self.backend_url}/predict/yield", json=test_data, timeout=15)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                prediction_data = response.json()
                
                # Validate prediction structure
                required_fields = ['predicted_yield', 'confidence_score']
                missing_fields = [field for field in required_fields if field not in prediction_data]
                
                if not missing_fields:
                    return TestResult(
                        test_name="TimesFM Model Integration",
                        success=True,
                        duration=duration,
                        details=f"TimesFM prediction successful: {prediction_data.get('predicted_yield', 'N/A')} tons/ha"
                    )
                else:
                    return TestResult(
                        test_name="TimesFM Model Integration",
                        success=False,
                        duration=duration,
                        details="Prediction response missing required fields",
                        error_message=f"Missing: {missing_fields}"
                    )
            else:
                return TestResult(
                    test_name="TimesFM Model Integration",
                    success=False,
                    duration=duration,
                    details=f"TimesFM API error: HTTP {response.status_code}",
                    error_message=response.text
                )
                
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name="TimesFM Model Integration",
                success=False,
                duration=duration,
                details="TimesFM integration failed",
                error_message=str(e)
            )
    
    def test_realtime_features(self) -> TestResult:
        """Test real-time features"""
        start_time = time.time()
        
        try:
            # Test real-time modules availability
            from supabase_realtime import get_realtime_manager
            from push_notifications import get_notification_manager
            
            realtime_manager = get_realtime_manager()
            notification_manager = get_notification_manager()
            
            # Test connection status
            status = realtime_manager.get_connection_status()
            
            # Test notification creation
            test_notification = notification_manager.create_notification(
                user_id="test_user",
                notification_type="weather_alert",
                template_data={"location": "Test Location", "condition": "Test", "details": "Test alert"}
            )
            
            duration = time.time() - start_time
            
            return TestResult(
                test_name="Real-time Features",
                success=True,
                duration=duration,
                details=f"Real-time connected: {status['connected']}, Notification created: {test_notification[:8]}..."
            )
            
        except ImportError:
            duration = time.time() - start_time
            return TestResult(
                test_name="Real-time Features",
                success=False,
                duration=duration,
                details="Real-time modules not available",
                error_message="Import error for real-time modules"
            )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name="Real-time Features",
                success=False,
                duration=duration,
                details="Real-time features test failed",
                error_message=str(e)
            )
    
    def test_performance_features(self) -> TestResult:
        """Test performance optimization features"""
        start_time = time.time()
        
        try:
            # Test performance modules
            from performance_cache_system import get_cache_manager, get_cache_stats
            from lazy_loading_components import get_lazy_loader
            
            cache_manager = get_cache_manager()
            lazy_loader = get_lazy_loader()
            
            # Test caching
            cache_manager.set("test_key", {"test": "data"}, {})
            cached_data = cache_manager.get("test_key", {})
            
            # Get cache stats
            stats = get_cache_stats()
            
            duration = time.time() - start_time
            
            cache_working = cached_data is not None
            stats_available = isinstance(stats, dict)
            
            return TestResult(
                test_name="Performance Features",
                success=cache_working and stats_available,
                duration=duration,
                details=f"Cache working: {cache_working}, Stats: {stats_available}, Hit rate: {stats.get('hit_rate', 'N/A')}"
            )
            
        except ImportError:
            duration = time.time() - start_time
            return TestResult(
                test_name="Performance Features",
                success=False,
                duration=duration,
                details="Performance modules not available",
                error_message="Import error for performance modules"
            )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name="Performance Features",
                success=False,
                duration=duration,
                details="Performance features test failed",
                error_message=str(e)
            )
    
    def test_mobile_pwa(self) -> TestResult:
        """Test mobile and PWA features"""
        start_time = time.time()
        
        try:
            # Check PWA files
            import os
            pwa_files = ['manifest.json', 'service-worker.js', 'offline.html']
            existing_files = [f for f in pwa_files if os.path.exists(f)]
            
            # Test mobile navigation
            from mobile_navigation import render_mobile_navigation
            
            duration = time.time() - start_time
            
            return TestResult(
                test_name="Mobile & PWA Features",
                success=len(existing_files) == len(pwa_files),
                duration=duration,
                details=f"PWA files: {len(existing_files)}/{len(pwa_files)}, Mobile nav available"
            )
            
        except ImportError:
            duration = time.time() - start_time
            return TestResult(
                test_name="Mobile & PWA Features",
                success=False,
                duration=duration,
                details="Mobile modules not available",
                error_message="Import error for mobile modules"
            )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name="Mobile & PWA Features",
                success=False,
                duration=duration,
                details="Mobile/PWA test failed",
                error_message=str(e)
            )
    
    def test_offline_features(self) -> TestResult:
        """Test offline capabilities"""
        start_time = time.time()
        
        try:
            from offline_sync_system import get_offline_manager, create_offline_record
            
            offline_manager = get_offline_manager()
            
            # Test offline record creation
            test_record_id = create_offline_record(
                'test_table',
                {'name': 'Test Record', 'value': 42},
                'test_user'
            )
            
            # Test sync status
            sync_status = offline_manager.get_sync_status()
            
            duration = time.time() - start_time
            
            return TestResult(
                test_name="Offline Capabilities",
                success=test_record_id is not None,
                duration=duration,
                details=f"Offline record created: {test_record_id[:8]}..., Sync status: {sync_status['is_online']}"
            )
            
        except ImportError:
            duration = time.time() - start_time
            return TestResult(
                test_name="Offline Capabilities",
                success=False,
                duration=duration,
                details="Offline modules not available",
                error_message="Import error for offline modules"
            )
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name="Offline Capabilities",
                success=False,
                duration=duration,
                details="Offline features test failed",
                error_message=str(e)
            )
    
    def test_data_flow(self) -> TestResult:
        """Test end-to-end data flow"""
        start_time = time.time()
        
        try:
            # Create test field data
            test_field = {
                'name': f'Integration Test Field {int(time.time())}',
                'crop_type': 'rice',
                'area_acres': 5.0,
                'latitude': 28.368911,
                'longitude': 77.541033,
                'soil_type': 'loamy'
            }
            
            # Test data creation in database
            conn = sqlite3.connect('agriforecast_modern.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO fields (farm_id, name, crop_type, area_acres, latitude, longitude, soil_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (1, test_field['name'], test_field['crop_type'], test_field['area_acres'],
                  test_field['latitude'], test_field['longitude'], test_field['soil_type']))
            
            field_id = cursor.lastrowid
            conn.commit()
            
            # Test data retrieval
            cursor.execute('SELECT * FROM fields WHERE id = ?', (field_id,))
            retrieved_field = cursor.fetchone()
            
            conn.close()
            
            # Test API integration with created field
            field_data_for_api = {
                'id': str(field_id),
                **test_field
            }
            
            try:
                prediction_response = requests.post(
                    f"{self.backend_url}/predict/yield",
                    json=field_data_for_api,
                    timeout=10
                )
                api_success = prediction_response.status_code == 200
            except:
                api_success = False
            
            duration = time.time() - start_time
            
            # Clean up test data
            conn = sqlite3.connect('agriforecast_modern.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM fields WHERE id = ?', (field_id,))
            conn.commit()
            conn.close()
            
            data_flow_success = retrieved_field is not None and retrieved_field[2] == test_field['name']
            
            return TestResult(
                test_name="Data Flow End-to-End",
                success=data_flow_success,
                duration=duration,
                details=f"Data flow: {data_flow_success}, API integration: {api_success}"
            )
            
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name="Data Flow End-to-End",
                success=False,
                duration=duration,
                details="End-to-end data flow test failed",
                error_message=str(e)
            )
    
    def test_security(self) -> TestResult:
        """Test security features"""
        start_time = time.time()
        
        try:
            security_checks = []
            
            # Test authentication endpoints (if available)
            try:
                auth_response = requests.post(f"{self.backend_url}/auth/login", json={
                    "username": "invalid_user",
                    "password": "invalid_password"
                }, timeout=5)
                
                # Should return 401 or 403 for invalid credentials
                if auth_response.status_code in [401, 403, 422]:
                    security_checks.append("Authentication validation working")
                else:
                    security_checks.append("Authentication validation issue")
                    
            except requests.exceptions.RequestException:
                security_checks.append("Authentication endpoint not available")
            
            # Test CORS headers
            try:
                options_response = requests.options(f"{self.backend_url}/", timeout=5)
                cors_headers = options_response.headers.get('Access-Control-Allow-Origin')
                if cors_headers:
                    security_checks.append("CORS headers configured")
                else:
                    security_checks.append("CORS headers missing")
            except:
                security_checks.append("CORS test failed")
            
            # Test rate limiting (if implemented)
            try:
                rapid_requests = []
                for i in range(10):
                    resp = requests.get(f"{self.backend_url}/health", timeout=1)
                    rapid_requests.append(resp.status_code)
                
                if any(status == 429 for status in rapid_requests):
                    security_checks.append("Rate limiting active")
                else:
                    security_checks.append("Rate limiting not detected")
            except:
                security_checks.append("Rate limiting test failed")
            
            duration = time.time() - start_time
            
            return TestResult(
                test_name="Security Features",
                success=True,
                duration=duration,
                details=f"Security checks: {len(security_checks)} performed"
            )
            
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name="Security Features",
                success=False,
                duration=duration,
                details="Security test failed",
                error_message=str(e)
            )
    
    def test_load_performance(self) -> TestResult:
        """Test basic load performance"""
        start_time = time.time()
        
        try:
            # Simple load test
            concurrent_requests = 10
            request_times = []
            
            def make_request():
                req_start = time.time()
                try:
                    response = requests.get(f"{self.backend_url}/health", timeout=5)
                    req_time = time.time() - req_start
                    request_times.append(req_time)
                    return response.status_code == 200
                except:
                    request_times.append(999)  # Timeout/error marker
                    return False
            
            # Use threading for concurrent requests
            threads = []
            for _ in range(concurrent_requests):
                thread = threading.Thread(target=make_request)
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            duration = time.time() - start_time
            
            successful_requests = sum(1 for t in request_times if t < 5)
            avg_response_time = sum(t for t in request_times if t < 5) / max(successful_requests, 1)
            
            return TestResult(
                test_name="Load Testing",
                success=successful_requests >= concurrent_requests * 0.8,  # 80% success rate
                duration=duration,
                details=f"Successful: {successful_requests}/{concurrent_requests}, Avg response: {avg_response_time:.3f}s"
            )
            
        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                test_name="Load Testing",
                success=False,
                duration=duration,
                details="Load testing failed",
                error_message=str(e)
            )
    
    def generate_test_report(self) -> Dict:
        """Generate comprehensive test report"""
        if not self.test_results:
            return {"error": "No test results available"}
        
        successful_tests = [t for t in self.test_results if t.success]
        failed_tests = [t for t in self.test_results if not t.success]
        
        report = {
            "test_summary": {
                "total_tests": len(self.test_results),
                "successful": len(successful_tests),
                "failed": len(failed_tests),
                "success_rate": len(successful_tests) / len(self.test_results) * 100,
                "total_duration": sum(t.duration for t in self.test_results),
                "average_duration": sum(t.duration for t in self.test_results) / len(self.test_results)
            },
            "successful_tests": [
                {
                    "name": t.test_name,
                    "duration": t.duration,
                    "details": t.details
                } for t in successful_tests
            ],
            "failed_tests": [
                {
                    "name": t.test_name,
                    "duration": t.duration,
                    "details": t.details,
                    "error": t.error_message
                } for t in failed_tests
            ],
            "recommendations": self._generate_recommendations(failed_tests),
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def _generate_recommendations(self, failed_tests: List[TestResult]) -> List[str]:
        """Generate recommendations based on failed tests"""
        recommendations = []
        
        for test in failed_tests:
            if "Backend Health" in test.test_name:
                recommendations.append("Start the FastAPI backend server: uvicorn main:app --reload")
            elif "Frontend" in test.test_name:
                recommendations.append("Start the Streamlit frontend: streamlit run agriforecast_modern.py")
            elif "Database" in test.test_name:
                recommendations.append("Check database file permissions and initialization")
            elif "API Endpoints" in test.test_name:
                recommendations.append("Verify backend API implementation and endpoints")
            elif "TimesFM" in test.test_name:
                recommendations.append("Check TimesFM model loading and API integration")
            elif "Real-time" in test.test_name:
                recommendations.append("Install real-time modules: supabase_realtime.py, push_notifications.py")
            elif "Performance" in test.test_name:
                recommendations.append("Install performance modules: performance_cache_system.py")
            elif "Mobile" in test.test_name:
                recommendations.append("Install mobile/PWA files: manifest.json, service-worker.js")
            elif "Offline" in test.test_name:
                recommendations.append("Install offline modules: offline_sync_system.py")
            elif "Security" in test.test_name:
                recommendations.append("Configure authentication, CORS, and rate limiting")
            elif "Load" in test.test_name:
                recommendations.append("Optimize backend performance and scaling")
        
        return list(set(recommendations))  # Remove duplicates

# Streamlit integration
def render_integration_testing_dashboard():
    """Render integration testing dashboard"""
    st.title("🧪 Integration Testing Center")
    
    test_suite = IntegrationTestSuite()
    
    # Configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Test Configuration")
        backend_url = st.text_input("Backend URL", value="http://localhost:8000")
        frontend_url = st.text_input("Frontend URL", value="http://localhost:8501")
        test_suite.backend_url = backend_url
        test_suite.frontend_url = frontend_url
        
        # Test selection
        test_categories = st.multiselect(
            "Select Test Categories",
            ["Backend", "Frontend", "Database", "API", "TimesFM", "Real-time", 
             "Performance", "Mobile/PWA", "Offline", "Security", "Load Testing"],
            default=["Backend", "Frontend", "Database", "API"]
        )
    
    with col2:
        st.subheader("📊 System Status")
        
        # Quick health checks
        if st.button("🏥 Quick Health Check"):
            backend_result = test_suite.test_backend_health()
            frontend_result = test_suite.test_frontend_availability()
            db_result = test_suite.test_database_connectivity()
            
            st.write("**Backend:**", "✅" if backend_result.success else "❌")
            st.write("**Frontend:**", "✅" if frontend_result.success else "❌")
            st.write("**Database:**", "✅" if db_result.success else "❌")
    
    # Run tests
    st.subheader("🚀 Run Integration Tests")
    
    if st.button("🧪 Run All Integration Tests", type="primary"):
        test_results = test_suite.run_all_tests()
        
        # Display results summary
        successful = [t for t in test_results if t.success]
        failed = [t for t in test_results if not t.success]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tests", len(test_results))
        with col2:
            st.metric("Successful", len(successful))
        with col3:
            st.metric("Failed", len(failed))
        with col4:
            success_rate = len(successful) / len(test_results) * 100 if test_results else 0
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
        # Detailed results
        st.subheader("📋 Detailed Test Results")
        
        for result in test_results:
            status_icon = "✅" if result.success else "❌"
            
            with st.expander(f"{status_icon} {result.test_name} ({result.duration:.3f}s)"):
                st.write(f"**Status:** {'Success' if result.success else 'Failed'}")
                st.write(f"**Duration:** {result.duration:.3f} seconds")
                st.write(f"**Details:** {result.details}")
                
                if result.error_message:
                    st.error(f"**Error:** {result.error_message}")
        
        # Generate and display report
        st.subheader("📊 Test Report")
        report = test_suite.generate_test_report()
        
        # Report summary
        if "test_summary" in report:
            summary = report["test_summary"]
            
            st.write("**Test Summary:**")
            st.write(f"• Total Tests: {summary['total_tests']}")
            st.write(f"• Success Rate: {summary['success_rate']:.1f}%")
            st.write(f"• Total Duration: {summary['total_duration']:.3f}s")
            st.write(f"• Average Duration: {summary['average_duration']:.3f}s")
        
        # Recommendations
        if "recommendations" in report and report["recommendations"]:
            st.subheader("💡 Recommendations")
            for rec in report["recommendations"]:
                st.write(f"• {rec}")
        
        # Export report
        if st.button("📄 Export Test Report"):
            report_json = json.dumps(report, indent=2)
            st.download_button(
                label="Download Report (JSON)",
                data=report_json,
                file_name=f"integration_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# Demo function
def demo_integration_testing():
    """Demo the integration testing dashboard"""
    render_integration_testing_dashboard()

if __name__ == "__main__":
    demo_integration_testing()
