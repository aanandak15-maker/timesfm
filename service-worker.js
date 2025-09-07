/**
 * AgriForecast.ai Service Worker
 * Provides offline capabilities and caching for the agricultural platform
 */

const CACHE_NAME = 'agriforecast-v1.0.0';
const OFFLINE_URL = '/offline.html';

// Resources to cache immediately
const STATIC_CACHE_URLS = [
  '/',
  '/manifest.json',
  '/agriforecast_modern.css',
  '/mobile_navigation.py',
  OFFLINE_URL
];

// Resources to cache when accessed
const RUNTIME_CACHE_URLS = [
  // Streamlit static files
  '/_stcore/static/',
  '/_stcore/vendor/',
  // API endpoints
  '/api/',
  // Weather and market data (cache for short periods)
  '/weather/',
  '/market/'
];

// Cache strategies
const CACHE_STRATEGIES = {
  static: 'CacheFirst',
  api: 'NetworkFirst',
  weather: 'StaleWhileRevalidate',
  images: 'CacheFirst'
};

/**
 * Install event - cache static resources
 */
self.addEventListener('install', event => {
  console.log('[ServiceWorker] Install event');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[ServiceWorker] Pre-caching static resources');
        return cache.addAll(STATIC_CACHE_URLS);
      })
      .then(() => {
        // Skip waiting to activate immediately
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('[ServiceWorker] Pre-caching failed:', error);
      })
  );
});

/**
 * Activate event - clean up old caches
 */
self.addEventListener('activate', event => {
  console.log('[ServiceWorker] Activate event');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[ServiceWorker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      // Take control of all clients immediately
      return self.clients.claim();
    })
  );
});

/**
 * Fetch event - handle network requests with caching strategies
 */
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-HTTP requests
  if (!request.url.startsWith('http')) {
    return;
  }
  
  // Handle different types of requests
  if (isStaticResource(url.pathname)) {
    event.respondWith(handleStaticResource(request));
  } else if (isApiRequest(url.pathname)) {
    event.respondWith(handleApiRequest(request));
  } else if (isWeatherRequest(url.pathname)) {
    event.respondWith(handleWeatherRequest(request));
  } else if (isImageRequest(url.pathname)) {
    event.respondWith(handleImageRequest(request));
  } else {
    event.respondWith(handleNavigationRequest(request));
  }
});

/**
 * Background sync for offline data submission
 */
self.addEventListener('sync', event => {
  console.log('[ServiceWorker] Background sync:', event.tag);
  
  if (event.tag === 'field-data-sync') {
    event.waitUntil(syncFieldData());
  } else if (event.tag === 'weather-data-sync') {
    event.waitUntil(syncWeatherData());
  }
});

/**
 * Push notification handling
 */
self.addEventListener('push', event => {
  console.log('[ServiceWorker] Push received:', event);
  
  let notificationData = {
    title: 'AgriForecast.ai',
    body: 'You have a new update!',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    tag: 'agriforecast-notification',
    requireInteraction: false,
    actions: [
      {
        action: 'view',
        title: 'View',
        icon: '/icons/action-view.png'
      },
      {
        action: 'dismiss',
        title: 'Dismiss',
        icon: '/icons/action-dismiss.png'
      }
    ]
  };
  
  if (event.data) {
    try {
      const data = event.data.json();
      notificationData = { ...notificationData, ...data };
    } catch (error) {
      console.error('[ServiceWorker] Error parsing push data:', error);
    }
  }
  
  event.waitUntil(
    self.registration.showNotification(notificationData.title, notificationData)
  );
});

/**
 * Notification click handling
 */
self.addEventListener('notificationclick', event => {
  console.log('[ServiceWorker] Notification clicked:', event);
  
  event.notification.close();
  
  if (event.action === 'view') {
    event.waitUntil(
      clients.openWindow('/')
    );
  } else if (event.action === 'dismiss') {
    // Just close the notification
    return;
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Helper functions for request handling

function isStaticResource(pathname) {
  return pathname.startsWith('/_stcore/') || 
         pathname.endsWith('.css') || 
         pathname.endsWith('.js') ||
         pathname === '/manifest.json';
}

function isApiRequest(pathname) {
  return pathname.startsWith('/api/');
}

function isWeatherRequest(pathname) {
  return pathname.includes('/weather/') || pathname.includes('/forecast/');
}

function isImageRequest(pathname) {
  return /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(pathname);
}

// Cache-first strategy for static resources
async function handleStaticResource(request) {
  try {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.error('[ServiceWorker] Static resource fetch failed:', error);
    return new Response('Resource not available offline', { status: 503 });
  }
}

// Network-first strategy for API requests
async function handleApiRequest(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[ServiceWorker] Network failed, trying cache for API request');
    
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline API response
    return new Response(JSON.stringify({
      error: 'Offline',
      message: 'This feature requires an internet connection',
      cached: false
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Stale-while-revalidate for weather data
async function handleWeatherRequest(request) {
  const cache = await caches.open(CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  // Always try to fetch fresh data in the background
  const fetchPromise = fetch(request).then(response => {
    if (response.ok) {
      cache.put(request, response.clone());
    }
    return response;
  }).catch(() => null);
  
  // Return cached response immediately if available
  if (cachedResponse) {
    fetchPromise; // Update cache in background
    return cachedResponse;
  }
  
  // Wait for network if no cache
  try {
    return await fetchPromise || new Response(JSON.stringify({
      error: 'Weather data unavailable offline',
      temperature: 'N/A',
      humidity: 'N/A',
      condition: 'Unknown'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    return new Response(JSON.stringify({
      error: 'Weather service offline'
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Cache-first for images with fallback
async function handleImageRequest(request) {
  try {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    // Return placeholder image for offline
    return new Response(
      '<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="200" height="200" fill="#f0f0f0"/><text x="100" y="100" text-anchor="middle" fill="#666">Image unavailable offline</text></svg>',
      { headers: { 'Content-Type': 'image/svg+xml' } }
    );
  }
}

// Handle navigation requests with offline fallback
async function handleNavigationRequest(request) {
  try {
    return await fetch(request);
  } catch (error) {
    // Return offline page for navigation failures
    const cache = await caches.open(CACHE_NAME);
    const offlineResponse = await cache.match(OFFLINE_URL);
    
    return offlineResponse || new Response(
      '<!DOCTYPE html><html><head><title>AgriForecast.ai - Offline</title></head><body><h1>🌾 AgriForecast.ai</h1><p>You are currently offline. Please check your internet connection.</p></body></html>',
      { headers: { 'Content-Type': 'text/html' } }
    );
  }
}

// Enhanced background sync functions with offline system integration
async function syncFieldData() {
  try {
    console.log('[ServiceWorker] Syncing field data...');
    
    // Notify main app to trigger offline sync
    const clients = await self.clients.matchAll();
    clients.forEach(client => {
      client.postMessage({
        type: 'TRIGGER_OFFLINE_SYNC',
        payload: { syncType: 'field_data' }
      });
    });
    
    // Get pending field data from IndexedDB
    const pendingData = await getPendingFieldData();
    
    for (const data of pendingData) {
      try {
        const response = await fetch('/api/fields', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        
        if (response.ok) {
          await removePendingFieldData(data.id);
          console.log('[ServiceWorker] Field data synced:', data.id);
          
          // Notify success
          clients.forEach(client => {
            client.postMessage({
              type: 'SYNC_SUCCESS',
              payload: { type: 'field', id: data.id }
            });
          });
        }
      } catch (error) {
        console.error('[ServiceWorker] Failed to sync field data:', error);
        
        // Notify failure
        clients.forEach(client => {
          client.postMessage({
            type: 'SYNC_ERROR',
            payload: { type: 'field', error: error.message }
          });
        });
      }
    }
  } catch (error) {
    console.error('[ServiceWorker] Background sync failed:', error);
  }
}

async function syncWeatherData() {
  console.log('[ServiceWorker] Syncing weather data...');
  
  try {
    // Refresh weather cache
    const weatherEndpoints = [
      '/api/weather/current',
      '/api/weather/forecast'
    ];
    
    const cache = await caches.open(CACHE_NAME);
    
    for (const endpoint of weatherEndpoints) {
      try {
        const response = await fetch(endpoint);
        if (response.ok) {
          await cache.put(endpoint, response.clone());
          console.log('[ServiceWorker] Weather data updated:', endpoint);
        }
      } catch (error) {
        console.log('[ServiceWorker] Failed to update weather:', endpoint);
      }
    }
    
    // Notify clients of fresh weather data
    const clients = await self.clients.matchAll();
    clients.forEach(client => {
      client.postMessage({
        type: 'WEATHER_DATA_UPDATED',
        payload: { timestamp: Date.now() }
      });
    });
    
  } catch (error) {
    console.error('[ServiceWorker] Weather sync failed:', error);
  }
}

// Enhanced IndexedDB helpers for offline operations
async function getPendingFieldData() {
  try {
    // Open IndexedDB connection
    const db = await openOfflineDB();
    const transaction = db.transaction(['offline_operations'], 'readonly');
    const store = transaction.objectStore('offline_operations');
    
    const request = store.getAll();
    
    return new Promise((resolve, reject) => {
      request.onsuccess = () => {
        const operations = request.result.filter(op => 
          op.table === 'fields' && op.sync_status === 'pending'
        );
        resolve(operations);
      };
      request.onerror = () => reject(request.error);
    });
  } catch (error) {
    console.error('[ServiceWorker] Failed to get pending field data:', error);
    return [];
  }
}

async function removePendingFieldData(id) {
  try {
    const db = await openOfflineDB();
    const transaction = db.transaction(['offline_operations'], 'readwrite');
    const store = transaction.objectStore('offline_operations');
    
    await store.delete(id);
    console.log('[ServiceWorker] Removed synced data:', id);
  } catch (error) {
    console.error('[ServiceWorker] Failed to remove pending data:', error);
  }
}

async function openOfflineDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('AgriforecastOfflineDB', 1);
    
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      
      if (!db.objectStoreNames.contains('offline_operations')) {
        const store = db.createObjectStore('offline_operations', { keyPath: 'id' });
        store.createIndex('table', 'table', { unique: false });
        store.createIndex('sync_status', 'sync_status', { unique: false });
        store.createIndex('timestamp', 'timestamp', { unique: false });
      }
      
      if (!db.objectStoreNames.contains('cache_metadata')) {
        const metaStore = db.createObjectStore('cache_metadata', { keyPath: 'key' });
      }
    };
  });
}

// Utility functions
function generateOfflineId() {
  return 'offline_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function isOnline() {
  return navigator.onLine;
}

// Periodic background tasks
self.addEventListener('periodicsync', event => {
  if (event.tag === 'weather-update') {
    event.waitUntil(updateWeatherCache());
  }
});

async function updateWeatherCache() {
  try {
    console.log('[ServiceWorker] Updating weather cache...');
    
    // Fetch fresh weather data for cached locations
    const cache = await caches.open(CACHE_NAME);
    const requests = await cache.keys();
    
    const weatherRequests = requests.filter(req => 
      req.url.includes('/weather/') || req.url.includes('/forecast/')
    );
    
    for (const request of weatherRequests.slice(0, 5)) { // Limit to 5 requests
      try {
        const response = await fetch(request);
        if (response.ok) {
          await cache.put(request, response);
        }
      } catch (error) {
        console.log('[ServiceWorker] Failed to update weather for:', request.url);
      }
    }
  } catch (error) {
    console.error('[ServiceWorker] Weather cache update failed:', error);
  }
}
