"""
PWA Integration Module for AgriForecast.ai
Streamlit integration for Progressive Web App features
"""

import streamlit as st
import json
import os
from typing import Dict, List, Optional

class PWAIntegration:
    """PWA integration for Streamlit applications"""
    
    def __init__(self, app_name: str = "AgriForecast.ai"):
        self.app_name = app_name
        self.base_path = os.path.dirname(os.path.abspath(__file__))
    
    def inject_pwa_head(self):
        """Inject PWA meta tags and manifest link into Streamlit head"""
        pwa_head = """
        <!-- PWA Meta Tags -->
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
        <meta name="apple-mobile-web-app-title" content="AgriForecast.ai">
        
        <!-- PWA Icons for iOS -->
        <link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/icons/favicon-16x16.png">
        
        <!-- PWA Manifest -->
        <link rel="manifest" href="/manifest.json">
        
        <!-- Theme Color -->
        <meta name="theme-color" content="#2E7D32">
        <meta name="msapplication-TileColor" content="#2E7D32">
        
        <!-- Disable Zoom on iOS -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
        
        <!-- PWA Splash Screens for iOS -->
        <link rel="apple-touch-startup-image" href="/icons/splash-2048x2732.png" media="(device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
        <link rel="apple-touch-startup-image" href="/icons/splash-1668x2388.png" media="(device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
        <link rel="apple-touch-startup-image" href="/icons/splash-1536x2048.png" media="(device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
        <link rel="apple-touch-startup-image" href="/icons/splash-1125x2436.png" media="(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
        <link rel="apple-touch-startup-image" href="/icons/splash-1242x2208.png" media="(device-width: 414px) and (device-height: 736px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
        <link rel="apple-touch-startup-image" href="/icons/splash-750x1334.png" media="(device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
        <link rel="apple-touch-startup-image" href="/icons/splash-640x1136.png" media="(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
        
        <!-- Microsoft Tiles -->
        <meta name="msapplication-config" content="/browserconfig.xml">
        """
        
        st.markdown(pwa_head, unsafe_allow_html=True)
    
    def register_service_worker(self):
        """Register service worker for PWA functionality"""
        sw_registration = """
        <script>
        // Service Worker Registration
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(registration => {
                        console.log('SW registered: ', registration);
                        
                        // Check for updates
                        registration.addEventListener('updatefound', () => {
                            const newWorker = registration.installing;
                            newWorker.addEventListener('statechange', () => {
                                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                    // New content available, show update notification
                                    showUpdateNotification();
                                }
                            });
                        });
                    })
                    .catch(registrationError => {
                        console.log('SW registration failed: ', registrationError);
                    });
            });
        }
        
        // Install PWA Banner
        let deferredPrompt;
        let installButton;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            showInstallBanner();
        });
        
        window.addEventListener('appinstalled', () => {
            console.log('PWA was installed');
            hideInstallBanner();
            deferredPrompt = null;
        });
        
        function showInstallBanner() {
            if (document.getElementById('pwa-install-banner')) return;
            
            const banner = document.createElement('div');
            banner.id = 'pwa-install-banner';
            banner.innerHTML = `
                <div style="
                    position: fixed;
                    bottom: 20px;
                    left: 20px;
                    right: 20px;
                    background: #2E7D32;
                    color: white;
                    padding: 16px;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    z-index: 10000;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                ">
                    <div style="flex: 1;">
                        <div style="font-weight: 600; margin-bottom: 4px;">
                            🌾 Install AgriForecast.ai
                        </div>
                        <div style="font-size: 14px; opacity: 0.9;">
                            Get the full app experience with offline access
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px; margin-left: 16px;">
                        <button onclick="installPWA()" style="
                            background: white;
                            color: #2E7D32;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 8px;
                            font-weight: 600;
                            cursor: pointer;
                            font-size: 14px;
                        ">Install</button>
                        <button onclick="hideInstallBanner()" style="
                            background: transparent;
                            color: white;
                            border: 1px solid rgba(255,255,255,0.3);
                            padding: 8px 12px;
                            border-radius: 8px;
                            cursor: pointer;
                            font-size: 14px;
                        ">Later</button>
                    </div>
                </div>
            `;
            document.body.appendChild(banner);
        }
        
        function hideInstallBanner() {
            const banner = document.getElementById('pwa-install-banner');
            if (banner) {
                banner.remove();
            }
        }
        
        function installPWA() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('User accepted the install prompt');
                    } else {
                        console.log('User dismissed the install prompt');
                    }
                    deferredPrompt = null;
                    hideInstallBanner();
                });
            }
        }
        
        function showUpdateNotification() {
            const notification = document.createElement('div');
            notification.innerHTML = `
                <div style="
                    position: fixed;
                    top: 20px;
                    left: 20px;
                    right: 20px;
                    background: #ff9800;
                    color: white;
                    padding: 16px;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    z-index: 10000;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                ">
                    <div>
                        <div style="font-weight: 600;">
                            📱 Update Available
                        </div>
                        <div style="font-size: 14px; opacity: 0.9;">
                            A new version of AgriForecast.ai is ready
                        </div>
                    </div>
                    <button onclick="refreshApp()" style="
                        background: white;
                        color: #ff9800;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 8px;
                        font-weight: 600;
                        cursor: pointer;
                        font-size: 14px;
                    ">Update</button>
                </div>
            `;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 5000);
        }
        
        function refreshApp() {
            if (navigator.serviceWorker) {
                navigator.serviceWorker.ready.then(registration => {
                    if (registration.waiting) {
                        registration.waiting.postMessage({ type: 'SKIP_WAITING' });
                    }
                    window.location.reload();
                });
            } else {
                window.location.reload();
            }
        }
        
        // Handle PWA display mode
        function handleDisplayMode() {
            if (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) {
                console.log('Running as PWA');
                document.body.classList.add('pwa-mode');
                
                // Hide install banner if already installed
                hideInstallBanner();
                
                // Add PWA-specific styles
                const pwaStyles = document.createElement('style');
                pwaStyles.textContent = `
                    .pwa-mode .stDeployButton {
                        display: none !important;
                    }
                    .pwa-mode #MainMenu {
                        display: none !important;
                    }
                `;
                document.head.appendChild(pwaStyles);
            }
        }
        
        // Check display mode on load and when it changes
        handleDisplayMode();
        if (window.matchMedia) {
            window.matchMedia('(display-mode: standalone)').addEventListener('change', handleDisplayMode);
        }
        
        // Performance monitoring
        function trackPWAMetrics() {
            if ('performance' in window && 'getEntriesByType' in performance) {
                window.addEventListener('load', () => {
                    setTimeout(() => {
                        const navigation = performance.getEntriesByType('navigation')[0];
                        const loadTime = navigation.loadEventEnd - navigation.fetchStart;
                        
                        console.log('PWA Load Time:', loadTime + 'ms');
                        
                        // Track if loaded from cache
                        if (navigation.transferSize === 0) {
                            console.log('PWA loaded from cache');
                        }
                    }, 1000);
                });
            }
        }
        
        trackPWAMetrics();
        
        // Handle network status
        function updateNetworkStatus() {
            const isOnline = navigator.onLine;
            document.body.classList.toggle('offline', !isOnline);
            
            if (!isOnline) {
                showOfflineIndicator();
            } else {
                hideOfflineIndicator();
            }
        }
        
        function showOfflineIndicator() {
            if (document.getElementById('offline-indicator')) return;
            
            const indicator = document.createElement('div');
            indicator.id = 'offline-indicator';
            indicator.innerHTML = `
                <div style="
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    background: #f44336;
                    color: white;
                    padding: 8px;
                    text-align: center;
                    font-size: 14px;
                    z-index: 10001;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                ">
                    📵 You're offline - Some features may be limited
                </div>
            `;
            document.body.appendChild(indicator);
        }
        
        function hideOfflineIndicator() {
            const indicator = document.getElementById('offline-indicator');
            if (indicator) {
                indicator.remove();
            }
        }
        
        window.addEventListener('online', updateNetworkStatus);
        window.addEventListener('offline', updateNetworkStatus);
        updateNetworkStatus();
        </script>
        """
        
        st.markdown(sw_registration, unsafe_allow_html=True)
    
    def add_mobile_meta_tags(self):
        """Add mobile-specific meta tags"""
        mobile_meta = """
        <!-- Mobile Optimization -->
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="mobile-web-app-status-bar-style" content="default">
        <meta name="format-detection" content="telephone=no">
        <meta name="format-detection" content="address=no">
        <meta name="format-detection" content="email=no">
        
        <!-- Prevent auto-zoom on input focus -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
        
        <!-- Home screen icons -->
        <meta name="apple-mobile-web-app-title" content="AgriForecast.ai">
        <meta name="application-name" content="AgriForecast.ai">
        
        <!-- Status bar appearance -->
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
        
        <!-- Disable automatic detection and formatting -->
        <meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no">
        """
        
        st.markdown(mobile_meta, unsafe_allow_html=True)
    
    def load_mobile_css(self):
        """Load mobile-optimized CSS"""
        try:
            css_path = os.path.join(self.base_path, 'mobile_optimizations.css')
            if os.path.exists(css_path):
                with open(css_path, 'r') as f:
                    css_content = f.read()
                
                st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
            else:
                st.warning("Mobile CSS file not found")
        except Exception as e:
            st.error(f"Error loading mobile CSS: {e}")
    
    def check_pwa_support(self) -> Dict[str, bool]:
        """Check PWA feature support in current browser"""
        support_check = """
        <script>
        // Check PWA support
        const pwaSupport = {
            serviceWorker: 'serviceWorker' in navigator,
            manifest: 'manifest' in document.createElement('link'),
            standalone: window.matchMedia && window.matchMedia('(display-mode: standalone)').matches,
            installPrompt: 'onbeforeinstallprompt' in window,
            pushNotifications: 'PushManager' in window,
            backgroundSync: 'serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype,
            periodicSync: 'serviceWorker' in navigator && 'periodicSync' in window.ServiceWorkerRegistration.prototype,
            webShare: 'share' in navigator,
            geolocation: 'geolocation' in navigator,
            camera: 'mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices,
            offline: 'onLine' in navigator
        };
        
        console.log('PWA Support:', pwaSupport);
        
        // Store in session storage for Python access
        sessionStorage.setItem('pwaSupport', JSON.stringify(pwaSupport));
        </script>
        """
        
        st.markdown(support_check, unsafe_allow_html=True)
    
    def setup_complete_pwa(self):
        """Set up complete PWA integration"""
        # Add PWA head tags
        self.inject_pwa_head()
        
        # Add mobile meta tags
        self.add_mobile_meta_tags()
        
        # Load mobile CSS
        self.load_mobile_css()
        
        # Register service worker
        self.register_service_worker()
        
        # Check PWA support
        self.check_pwa_support()
        
        # Add global PWA styles
        global_pwa_styles = """
        <style>
        /* PWA-specific adjustments */
        .main > div {
            padding-top: 0 !important;
        }
        
        /* Hide Streamlit elements in PWA mode */
        .pwa-mode .stDeployButton,
        .pwa-mode #MainMenu,
        .pwa-mode footer,
        .pwa-mode header {
            display: none !important;
        }
        
        /* Add safe area support */
        @supports (padding: max(0px)) {
            .main .block-container {
                padding-left: max(1rem, env(safe-area-inset-left));
                padding-right: max(1rem, env(safe-area-inset-right));
            }
        }
        
        /* Offline indicator */
        body.offline {
            filter: grayscale(0.2);
        }
        
        /* Loading states */
        .stSpinner {
            color: #2E7D32 !important;
        }
        </style>
        """
        
        st.markdown(global_pwa_styles, unsafe_allow_html=True)

# Helper function for easy integration
def setup_pwa(app_name: str = "AgriForecast.ai"):
    """
    Easy setup function for PWA integration in Streamlit
    
    Args:
        app_name: Name of the application
    """
    pwa = PWAIntegration(app_name)
    pwa.setup_complete_pwa()
    
    return pwa

# Usage example
if __name__ == "__main__":
    # Example usage in your Streamlit app
    st.set_page_config(
        page_title="AgriForecast.ai",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Setup PWA
    pwa = setup_pwa("AgriForecast.ai")
    
    st.title("🌾 AgriForecast.ai - PWA Ready!")
    st.write("This app now has full PWA capabilities with offline support.")
