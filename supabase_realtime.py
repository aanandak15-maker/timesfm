"""
Supabase Real-time Subscriptions for AgriForecast.ai
Live data updates, real-time notifications, and collaborative features
"""

import streamlit as st
import asyncio
import json
import time
import threading
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime, timedelta
import sqlite3
from dataclasses import dataclass, asdict
import uuid
import hashlib

# Simulated Supabase real-time client (replace with actual Supabase client in production)
class SupabaseRealtimeClient:
    """Simulated Supabase real-time client for development"""
    
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.subscriptions = {}
        self.channels = {}
        self.is_connected = False
        self.connection_status = "disconnected"
        
    def connect(self):
        """Simulate connection to Supabase"""
        self.is_connected = True
        self.connection_status = "connected"
        print("🔌 Supabase real-time connected")
        
    def disconnect(self):
        """Disconnect from Supabase"""
        self.is_connected = False
        self.connection_status = "disconnected"
        print("🔌 Supabase real-time disconnected")
        
    def channel(self, channel_name: str):
        """Create or get a channel"""
        if channel_name not in self.channels:
            self.channels[channel_name] = RealtimeChannel(channel_name, self)
        return self.channels[channel_name]

class RealtimeChannel:
    """Supabase real-time channel for specific table/topic"""
    
    def __init__(self, name: str, client):
        self.name = name
        self.client = client
        self.subscriptions = []
        self.is_subscribed = False
        
    def on(self, event: str, schema: str = None, table: str = None, filter_expr: str = None):
        """Subscribe to real-time events"""
        def decorator(callback: Callable):
            subscription = {
                'event': event,
                'schema': schema,
                'table': table,
                'filter': filter_expr,
                'callback': callback
            }
            self.subscriptions.append(subscription)
            return callback
        return decorator
    
    def subscribe(self, callback: Callable = None):
        """Subscribe to the channel"""
        self.is_subscribed = True
        print(f"📡 Subscribed to channel: {self.name}")
        if callback:
            callback({'status': 'SUBSCRIBED', 'channel': self.name})
        return self
    
    def unsubscribe(self):
        """Unsubscribe from the channel"""
        self.is_subscribed = False
        self.subscriptions.clear()
        print(f"📡 Unsubscribed from channel: {self.name}")

@dataclass
class RealtimeEvent:
    """Real-time event data structure"""
    event_type: str  # INSERT, UPDATE, DELETE
    table: str
    schema: str
    old_record: Optional[Dict] = None
    new_record: Optional[Dict] = None
    timestamp: datetime = None
    user_id: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class RealtimeManager:
    """Manages real-time subscriptions and events"""
    
    def __init__(self, supabase_url: str = None, supabase_key: str = None):
        # In production, use actual Supabase credentials
        self.supabase_url = supabase_url or "https://your-project.supabase.co"
        self.supabase_key = supabase_key or "your-anon-key"
        
        # Initialize Supabase client (simulated for now)
        self.client = SupabaseRealtimeClient(self.supabase_url, self.supabase_key)
        self.client.connect()
        
        # Event handlers
        self.event_handlers = {}
        self.active_subscriptions = {}
        self.event_queue = []
        
        # Database for local events simulation
        self.db_path = "realtime_events.db"
        self.init_local_db()
        
        # Start event processor
        self.start_event_processor()
    
    def init_local_db(self):
        """Initialize local database for event simulation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS realtime_events (
                id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                table_name TEXT NOT NULL,
                schema_name TEXT DEFAULT 'public',
                old_record TEXT,
                new_record TEXT,
                timestamp TEXT,
                user_id TEXT,
                processed BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def start_event_processor(self):
        """Start background event processor"""
        def process_events():
            while True:
                try:
                    self.process_pending_events()
                    time.sleep(1)  # Check every second
                except Exception as e:
                    print(f"Event processor error: {e}")
                    time.sleep(5)  # Wait longer on error
        
        thread = threading.Thread(target=process_events, daemon=True)
        thread.start()
    
    def process_pending_events(self):
        """Process pending events from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, event_type, table_name, schema_name, old_record, new_record, timestamp, user_id
            FROM realtime_events 
            WHERE processed = FALSE 
            ORDER BY timestamp ASC
            LIMIT 10
        ''')
        
        events = cursor.fetchall()
        
        for event_data in events:
            event = RealtimeEvent(
                event_type=event_data[1],
                table=event_data[2],
                schema=event_data[3],
                old_record=json.loads(event_data[4]) if event_data[4] else None,
                new_record=json.loads(event_data[5]) if event_data[5] else None,
                timestamp=datetime.fromisoformat(event_data[6]),
                user_id=event_data[7]
            )
            
            # Trigger event handlers
            self.trigger_event_handlers(event)
            
            # Mark as processed
            cursor.execute('UPDATE realtime_events SET processed = TRUE WHERE id = ?', (event_data[0],))
        
        conn.commit()
        conn.close()
    
    def trigger_event_handlers(self, event: RealtimeEvent):
        """Trigger registered event handlers"""
        for subscription_id, handler in self.event_handlers.items():
            try:
                handler(event)
            except Exception as e:
                print(f"Error in event handler {subscription_id}: {e}")
    
    def subscribe_to_table(self, table: str, callback: Callable, event_types: List[str] = None, schema: str = "public"):
        """
        Subscribe to real-time changes on a table
        
        Args:
            table: Table name to subscribe to
            callback: Function to call when events occur
            event_types: List of event types to listen for (INSERT, UPDATE, DELETE)
            schema: Database schema name
        
        Returns:
            Subscription ID for unsubscribing
        """
        if event_types is None:
            event_types = ["INSERT", "UPDATE", "DELETE"]
        
        subscription_id = str(uuid.uuid4())
        
        def event_filter(event: RealtimeEvent):
            if (event.table == table and 
                event.schema == schema and 
                event.event_type in event_types):
                callback(event)
        
        self.event_handlers[subscription_id] = event_filter
        self.active_subscriptions[subscription_id] = {
            'table': table,
            'schema': schema,
            'event_types': event_types,
            'callback': callback
        }
        
        # Create Supabase channel subscription
        channel = self.client.channel(f"table-{schema}-{table}")
        
        @channel.on('postgres_changes', schema=schema, table=table)
        def handle_postgres_changes(payload):
            event = RealtimeEvent(
                event_type=payload.get('eventType', '').upper(),
                table=table,
                schema=schema,
                old_record=payload.get('old'),
                new_record=payload.get('new'),
                user_id=payload.get('userId')
            )
            callback(event)
        
        channel.subscribe()
        
        print(f"📡 Subscribed to {schema}.{table} for events: {event_types}")
        return subscription_id
    
    def unsubscribe(self, subscription_id: str):
        """Unsubscribe from a real-time subscription"""
        if subscription_id in self.event_handlers:
            del self.event_handlers[subscription_id]
        if subscription_id in self.active_subscriptions:
            del self.active_subscriptions[subscription_id]
        print(f"📡 Unsubscribed: {subscription_id}")
    
    def simulate_event(self, table: str, event_type: str, new_record: Dict, old_record: Dict = None, user_id: str = None):
        """
        Simulate a real-time event (for testing/development)
        
        Args:
            table: Table name
            event_type: INSERT, UPDATE, or DELETE
            new_record: New record data
            old_record: Old record data (for UPDATE/DELETE)
            user_id: User who triggered the event
        """
        event_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO realtime_events (id, event_type, table_name, schema_name, old_record, new_record, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event_id,
            event_type.upper(),
            table,
            'public',
            json.dumps(old_record) if old_record else None,
            json.dumps(new_record),
            timestamp,
            user_id
        ))
        
        conn.commit()
        conn.close()
        
        print(f"🎯 Simulated {event_type} event on {table}")
    
    def get_connection_status(self) -> Dict:
        """Get real-time connection status"""
        return {
            'connected': self.client.is_connected,
            'status': self.client.connection_status,
            'active_subscriptions': len(self.active_subscriptions),
            'url': self.supabase_url
        }
    
    def get_subscription_stats(self) -> Dict:
        """Get subscription statistics"""
        stats = {}
        for sub_id, sub_info in self.active_subscriptions.items():
            table_key = f"{sub_info['schema']}.{sub_info['table']}"
            if table_key not in stats:
                stats[table_key] = {
                    'subscriptions': 0,
                    'event_types': set()
                }
            stats[table_key]['subscriptions'] += 1
            stats[table_key]['event_types'].update(sub_info['event_types'])
        
        # Convert sets to lists for JSON serialization
        for table_key in stats:
            stats[table_key]['event_types'] = list(stats[table_key]['event_types'])
        
        return stats

# Agricultural-specific real-time handlers
class AgricultureRealtimeHandlers:
    """Agricultural-specific real-time event handlers"""
    
    def __init__(self, realtime_manager: RealtimeManager):
        self.realtime = realtime_manager
        self.notification_queue = []
        
    def setup_field_monitoring(self, user_id: str, callback: Callable = None):
        """Setup real-time monitoring for user's fields"""
        
        def handle_field_changes(event: RealtimeEvent):
            if callback:
                callback(event)
            else:
                self.default_field_handler(event)
        
        return self.realtime.subscribe_to_table(
            'fields',
            handle_field_changes,
            ['INSERT', 'UPDATE', 'DELETE']
        )
    
    def setup_weather_alerts(self, user_id: str, callback: Callable = None):
        """Setup real-time weather alerts"""
        
        def handle_weather_alerts(event: RealtimeEvent):
            if event.event_type == 'INSERT' and event.new_record:
                weather_data = event.new_record
                if self.should_alert_weather(weather_data):
                    alert = {
                        'type': 'weather_alert',
                        'severity': self.get_weather_severity(weather_data),
                        'message': self.generate_weather_message(weather_data),
                        'timestamp': datetime.now(),
                        'data': weather_data
                    }
                    
                    if callback:
                        callback(alert)
                    else:
                        self.queue_notification(alert)
        
        return self.realtime.subscribe_to_table(
            'weather_data',
            handle_weather_alerts,
            ['INSERT', 'UPDATE']
        )
    
    def setup_crop_monitoring(self, user_id: str, callback: Callable = None):
        """Setup real-time crop health monitoring"""
        
        def handle_crop_updates(event: RealtimeEvent):
            if event.event_type in ['INSERT', 'UPDATE'] and event.new_record:
                crop_data = event.new_record
                
                # Check for critical crop conditions
                if self.detect_crop_issues(crop_data):
                    alert = {
                        'type': 'crop_alert',
                        'field_id': crop_data.get('field_id'),
                        'issue': self.identify_crop_issue(crop_data),
                        'severity': 'high',
                        'message': self.generate_crop_message(crop_data),
                        'timestamp': datetime.now(),
                        'data': crop_data
                    }
                    
                    if callback:
                        callback(alert)
                    else:
                        self.queue_notification(alert)
        
        return self.realtime.subscribe_to_table(
            'crop_health',
            handle_crop_updates,
            ['INSERT', 'UPDATE']
        )
    
    def should_alert_weather(self, weather_data: Dict) -> bool:
        """Determine if weather data warrants an alert"""
        temp = weather_data.get('temperature', 0)
        humidity = weather_data.get('humidity', 0)
        wind_speed = weather_data.get('wind_speed', 0)
        rainfall = weather_data.get('rainfall', 0)
        
        # Alert conditions
        extreme_temp = temp > 40 or temp < 5
        high_wind = wind_speed > 50
        heavy_rain = rainfall > 50
        extreme_humidity = humidity > 90 or humidity < 20
        
        return extreme_temp or high_wind or heavy_rain or extreme_humidity
    
    def get_weather_severity(self, weather_data: Dict) -> str:
        """Get weather alert severity"""
        temp = weather_data.get('temperature', 0)
        wind_speed = weather_data.get('wind_speed', 0)
        rainfall = weather_data.get('rainfall', 0)
        
        if temp > 45 or temp < 0 or wind_speed > 80 or rainfall > 100:
            return 'critical'
        elif temp > 40 or temp < 5 or wind_speed > 50 or rainfall > 50:
            return 'high'
        else:
            return 'medium'
    
    def generate_weather_message(self, weather_data: Dict) -> str:
        """Generate human-readable weather alert message"""
        temp = weather_data.get('temperature', 0)
        wind_speed = weather_data.get('wind_speed', 0)
        rainfall = weather_data.get('rainfall', 0)
        condition = weather_data.get('condition', 'Unknown')
        
        messages = []
        
        if temp > 40:
            messages.append(f"🌡️ Extreme heat: {temp}°C")
        elif temp < 5:
            messages.append(f"🧊 Extreme cold: {temp}°C")
        
        if wind_speed > 50:
            messages.append(f"💨 High winds: {wind_speed} km/h")
        
        if rainfall > 50:
            messages.append(f"🌧️ Heavy rainfall: {rainfall}mm")
        
        if not messages:
            messages.append(f"🌤️ Weather update: {condition}")
        
        return " | ".join(messages)
    
    def detect_crop_issues(self, crop_data: Dict) -> bool:
        """Detect crop health issues"""
        health_score = crop_data.get('health_score', 100)
        moisture_level = crop_data.get('soil_moisture', 50)
        pest_detected = crop_data.get('pest_detected', False)
        disease_risk = crop_data.get('disease_risk', 0)
        
        return (health_score < 70 or 
                moisture_level < 20 or moisture_level > 90 or
                pest_detected or 
                disease_risk > 0.7)
    
    def identify_crop_issue(self, crop_data: Dict) -> str:
        """Identify specific crop issue"""
        issues = []
        
        health_score = crop_data.get('health_score', 100)
        if health_score < 70:
            issues.append('low_health')
        
        moisture_level = crop_data.get('soil_moisture', 50)
        if moisture_level < 20:
            issues.append('drought_stress')
        elif moisture_level > 90:
            issues.append('waterlogged')
        
        if crop_data.get('pest_detected', False):
            issues.append('pest_infestation')
        
        if crop_data.get('disease_risk', 0) > 0.7:
            issues.append('disease_risk')
        
        return issues[0] if issues else 'unknown'
    
    def generate_crop_message(self, crop_data: Dict) -> str:
        """Generate human-readable crop alert message"""
        field_name = crop_data.get('field_name', 'Unknown Field')
        issue = self.identify_crop_issue(crop_data)
        
        issue_messages = {
            'low_health': f"🌾 {field_name}: Crop health declining",
            'drought_stress': f"🏜️ {field_name}: Drought stress detected",
            'waterlogged': f"💧 {field_name}: Waterlogging detected",
            'pest_infestation': f"🐛 {field_name}: Pest activity detected",
            'disease_risk': f"🦠 {field_name}: Disease risk elevated"
        }
        
        return issue_messages.get(issue, f"⚠️ {field_name}: Issue detected")
    
    def queue_notification(self, notification: Dict):
        """Queue notification for delivery"""
        self.notification_queue.append(notification)
    
    def get_pending_notifications(self) -> List[Dict]:
        """Get and clear pending notifications"""
        notifications = self.notification_queue.copy()
        self.notification_queue.clear()
        return notifications
    
    def default_field_handler(self, event: RealtimeEvent):
        """Default handler for field changes"""
        if event.event_type == 'INSERT':
            st.toast(f"🌾 New field added: {event.new_record.get('name', 'Unknown')}")
        elif event.event_type == 'UPDATE':
            st.toast(f"🔄 Field updated: {event.new_record.get('name', 'Unknown')}")
        elif event.event_type == 'DELETE':
            st.toast(f"🗑️ Field removed: {event.old_record.get('name', 'Unknown')}")

# Global real-time manager instance
_realtime_manager = None
_agriculture_handlers = None

def get_realtime_manager() -> RealtimeManager:
    """Get global real-time manager instance"""
    global _realtime_manager
    if _realtime_manager is None:
        _realtime_manager = RealtimeManager()
    return _realtime_manager

def get_agriculture_handlers() -> AgricultureRealtimeHandlers:
    """Get global agriculture handlers instance"""
    global _agriculture_handlers
    if _agriculture_handlers is None:
        _agriculture_handlers = AgricultureRealtimeHandlers(get_realtime_manager())
    return _agriculture_handlers

# Convenience functions for Streamlit apps
def setup_realtime_monitoring(user_id: str):
    """Setup complete real-time monitoring for a user"""
    handlers = get_agriculture_handlers()
    
    subscriptions = {
        'fields': handlers.setup_field_monitoring(user_id),
        'weather': handlers.setup_weather_alerts(user_id),
        'crops': handlers.setup_crop_monitoring(user_id)
    }
    
    return subscriptions

def simulate_field_update(field_id: str, field_name: str, updates: Dict):
    """Simulate a field update event"""
    manager = get_realtime_manager()
    manager.simulate_event(
        'fields',
        'UPDATE',
        {'id': field_id, 'name': field_name, **updates},
        user_id='current_user'
    )

def simulate_weather_alert(location: str, weather_data: Dict):
    """Simulate a weather alert event"""
    manager = get_realtime_manager()
    manager.simulate_event(
        'weather_data',
        'INSERT',
        {'location': location, **weather_data},
        user_id='system'
    )

def simulate_crop_alert(field_id: str, crop_data: Dict):
    """Simulate a crop health alert"""
    manager = get_realtime_manager()
    manager.simulate_event(
        'crop_health',
        'UPDATE',
        {'field_id': field_id, **crop_data},
        user_id='system'
    )

# Demo function
def demo_realtime_features():
    """Demo real-time features"""
    st.title("🔄 Real-time Features Demo")
    
    # Initialize real-time manager
    manager = get_realtime_manager()
    handlers = get_agriculture_handlers()
    
    # Connection status
    status = manager.get_connection_status()
    if status['connected']:
        st.success(f"🟢 Real-time connected: {status['active_subscriptions']} active subscriptions")
    else:
        st.error("🔴 Real-time disconnected")
    
    # Subscription stats
    stats = manager.get_subscription_stats()
    if stats:
        st.subheader("📊 Active Subscriptions")
        for table, info in stats.items():
            st.write(f"**{table}**: {info['subscriptions']} subscriptions, Events: {info['event_types']}")
    
    # Simulate events
    st.subheader("🎯 Simulate Events")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌾 Simulate Field Update"):
            simulate_field_update("field_1", "Test Field", {"health_score": 85})
            st.success("Field update simulated!")
    
    with col2:
        if st.button("🌤️ Simulate Weather Alert"):
            simulate_weather_alert("Test Location", {
                "temperature": 42,
                "humidity": 25,
                "wind_speed": 55,
                "condition": "Extreme Heat"
            })
            st.success("Weather alert simulated!")
    
    with col3:
        if st.button("🌱 Simulate Crop Alert"):
            simulate_crop_alert("field_1", {
                "health_score": 65,
                "soil_moisture": 15,
                "pest_detected": True,
                "field_name": "Test Field"
            })
            st.success("Crop alert simulated!")
    
    # Show pending notifications
    notifications = handlers.get_pending_notifications()
    if notifications:
        st.subheader("🔔 Recent Notifications")
        for notif in notifications[-5:]:  # Show last 5
            st.info(f"**{notif['type']}**: {notif['message']}")

if __name__ == "__main__":
    demo_realtime_features()
