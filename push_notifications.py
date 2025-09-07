"""
Push Notifications System for AgriForecast.ai
Web push notifications, weather alerts, and field updates
"""

import streamlit as st
import json
import time
import threading
import sqlite3
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import uuid
import hashlib
from enum import Enum

class NotificationPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

class NotificationType(Enum):
    WEATHER_ALERT = "weather_alert"
    CROP_HEALTH = "crop_health"
    FIELD_UPDATE = "field_update"
    MARKET_ALERT = "market_alert"
    SYSTEM_UPDATE = "system_update"
    PEST_ALERT = "pest_alert"
    IRRIGATION_ALERT = "irrigation_alert"

@dataclass
class PushNotification:
    """Push notification data structure"""
    id: str
    user_id: str
    title: str
    body: str
    type: NotificationType
    priority: NotificationPriority
    data: Dict = None
    icon: str = None
    image: str = None
    badge: str = None
    tag: str = None
    timestamp: datetime = None
    expires_at: datetime = None
    sent: bool = False
    delivered: bool = False
    clicked: bool = False
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.expires_at is None:
            self.expires_at = self.timestamp + timedelta(days=7)
        if self.data is None:
            self.data = {}
        if self.icon is None:
            self.icon = self.get_default_icon()
    
    def get_default_icon(self) -> str:
        """Get default icon based on notification type"""
        icons = {
            NotificationType.WEATHER_ALERT: "🌤️",
            NotificationType.CROP_HEALTH: "🌾",
            NotificationType.FIELD_UPDATE: "🚜",
            NotificationType.MARKET_ALERT: "💰",
            NotificationType.SYSTEM_UPDATE: "🔄",
            NotificationType.PEST_ALERT: "🐛",
            NotificationType.IRRIGATION_ALERT: "💧"
        }
        return icons.get(self.type, "📱")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'body': self.body,
            'type': self.type.value,
            'priority': self.priority.value,
            'data': self.data,
            'icon': self.icon,
            'image': self.image,
            'badge': self.badge,
            'tag': self.tag,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'sent': self.sent,
            'delivered': self.delivered,
            'clicked': self.clicked
        }

class WebPushClient:
    """Web Push API client for browser notifications"""
    
    def __init__(self):
        self.vapid_keys = {
            'public': 'BEl62iUYgUivxIkv69yViEuiBIa40HI80NqIUHytOtArgOS9YSCS3NgYKq0XdWBU9BuOgEqNk8g_6gTm5Oy3TL0',
            'private': 'dKnOIB1jONZu4TIWxXnQ_3JJ1bYGHNOKjMZhx5Q9_8s'
        }
        self.subscribers = {}
    
    def get_vapid_public_key(self) -> str:
        """Get VAPID public key for client subscription"""
        return self.vapid_keys['public']
    
    def subscribe_user(self, user_id: str, subscription_data: Dict) -> bool:
        """Subscribe user to push notifications"""
        try:
            self.subscribers[user_id] = subscription_data
            print(f"📱 User {user_id} subscribed to push notifications")
            return True
        except Exception as e:
            print(f"Subscription error: {e}")
            return False
    
    def unsubscribe_user(self, user_id: str) -> bool:
        """Unsubscribe user from push notifications"""
        if user_id in self.subscribers:
            del self.subscribers[user_id]
            print(f"📱 User {user_id} unsubscribed from push notifications")
            return True
        return False
    
    def send_notification(self, notification: PushNotification) -> bool:
        """Send push notification to user"""
        if notification.user_id not in self.subscribers:
            print(f"User {notification.user_id} not subscribed")
            return False
        
        try:
            # In production, use actual web push library
            # Here we simulate the push notification
            payload = {
                'title': notification.title,
                'body': notification.body,
                'icon': notification.icon,
                'image': notification.image,
                'badge': notification.badge,
                'tag': notification.tag,
                'data': notification.data,
                'timestamp': notification.timestamp.timestamp() * 1000,
                'requireInteraction': notification.priority in [NotificationPriority.HIGH, NotificationPriority.CRITICAL]
            }
            
            # Simulate successful send
            notification.sent = True
            notification.delivered = True
            
            print(f"🚀 Push notification sent: {notification.title}")
            return True
            
        except Exception as e:
            print(f"Failed to send push notification: {e}")
            return False

class NotificationManager:
    """Manages push notifications and delivery"""
    
    def __init__(self):
        self.db_path = "notifications.db"
        self.init_database()
        
        self.push_client = WebPushClient()
        self.notification_handlers = {}
        self.templates = {}
        
        # Load default templates
        self.load_default_templates()
        
        # Start notification processor
        self.start_notification_processor()
    
    def init_database(self):
        """Initialize notifications database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                type TEXT NOT NULL,
                priority TEXT NOT NULL,
                data TEXT,
                icon TEXT,
                image TEXT,
                badge TEXT,
                tag TEXT,
                timestamp TEXT,
                expires_at TEXT,
                sent BOOLEAN DEFAULT FALSE,
                delivered BOOLEAN DEFAULT FALSE,
                clicked BOOLEAN DEFAULT FALSE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_subscriptions (
                user_id TEXT PRIMARY KEY,
                subscription_data TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_active TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_preferences (
                user_id TEXT PRIMARY KEY,
                weather_alerts BOOLEAN DEFAULT TRUE,
                crop_health BOOLEAN DEFAULT TRUE,
                field_updates BOOLEAN DEFAULT TRUE,
                market_alerts BOOLEAN DEFAULT TRUE,
                system_updates BOOLEAN DEFAULT TRUE,
                pest_alerts BOOLEAN DEFAULT TRUE,
                irrigation_alerts BOOLEAN DEFAULT TRUE,
                quiet_hours_start TEXT DEFAULT '22:00',
                quiet_hours_end TEXT DEFAULT '06:00',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_default_templates(self):
        """Load default notification templates"""
        self.templates = {
            NotificationType.WEATHER_ALERT: {
                'title': '🌤️ Weather Alert - {location}',
                'body': '{condition} - {details}. Take necessary precautions.',
                'priority': NotificationPriority.HIGH
            },
            NotificationType.CROP_HEALTH: {
                'title': '🌾 Crop Health Alert - {field_name}',
                'body': '{issue_type} detected. Health score: {health_score}%',
                'priority': NotificationPriority.HIGH
            },
            NotificationType.FIELD_UPDATE: {
                'title': '🚜 Field Update - {field_name}',
                'body': '{update_type}: {details}',
                'priority': NotificationPriority.NORMAL
            },
            NotificationType.MARKET_ALERT: {
                'title': '💰 Market Alert - {crop_type}',
                'body': 'Price {change_type}: {price} ({change_percent})',
                'priority': NotificationPriority.NORMAL
            },
            NotificationType.PEST_ALERT: {
                'title': '🐛 Pest Alert - {field_name}',
                'body': '{pest_type} detected. Immediate action recommended.',
                'priority': NotificationPriority.CRITICAL
            },
            NotificationType.IRRIGATION_ALERT: {
                'title': '💧 Irrigation Alert - {field_name}',
                'body': 'Soil moisture: {moisture_level}%. {action_needed}',
                'priority': NotificationPriority.HIGH
            }
        }
    
    def start_notification_processor(self):
        """Start background notification processor"""
        def process_notifications():
            while True:
                try:
                    self.process_pending_notifications()
                    time.sleep(5)  # Check every 5 seconds
                except Exception as e:
                    print(f"Notification processor error: {e}")
                    time.sleep(10)
        
        thread = threading.Thread(target=process_notifications, daemon=True)
        thread.start()
    
    def process_pending_notifications(self):
        """Process pending notifications"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM notifications 
            WHERE sent = FALSE AND expires_at > datetime('now')
            ORDER BY priority DESC, timestamp ASC
            LIMIT 10
        ''')
        
        notifications = cursor.fetchall()
        
        for notif_data in notifications:
            notification = self.row_to_notification(notif_data)
            
            # Check user preferences
            if self.should_send_notification(notification):
                # Send notification
                if self.push_client.send_notification(notification):
                    # Update database
                    cursor.execute('''
                        UPDATE notifications 
                        SET sent = TRUE, delivered = TRUE 
                        WHERE id = ?
                    ''', (notification.id,))
        
        conn.commit()
        conn.close()
    
    def row_to_notification(self, row) -> PushNotification:
        """Convert database row to notification object"""
        return PushNotification(
            id=row[0],
            user_id=row[1],
            title=row[2],
            body=row[3],
            type=NotificationType(row[4]),
            priority=NotificationPriority(row[5]),
            data=json.loads(row[6]) if row[6] else {},
            icon=row[7],
            image=row[8],
            badge=row[9],
            tag=row[10],
            timestamp=datetime.fromisoformat(row[11]) if row[11] else None,
            expires_at=datetime.fromisoformat(row[12]) if row[12] else None,
            sent=bool(row[13]),
            delivered=bool(row[14]),
            clicked=bool(row[15])
        )
    
    def should_send_notification(self, notification: PushNotification) -> bool:
        """Check if notification should be sent based on user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM notification_preferences WHERE user_id = ?
        ''', (notification.user_id,))
        
        prefs = cursor.fetchone()
        conn.close()
        
        if not prefs:
            return True  # Default to sending if no preferences set
        
        # Check type-specific preferences
        type_mapping = {
            NotificationType.WEATHER_ALERT: prefs[1],
            NotificationType.CROP_HEALTH: prefs[2],
            NotificationType.FIELD_UPDATE: prefs[3],
            NotificationType.MARKET_ALERT: prefs[4],
            NotificationType.SYSTEM_UPDATE: prefs[5],
            NotificationType.PEST_ALERT: prefs[6],
            NotificationType.IRRIGATION_ALERT: prefs[7]
        }
        
        if not type_mapping.get(notification.type, True):
            return False
        
        # Check quiet hours
        quiet_start = prefs[8]  # quiet_hours_start
        quiet_end = prefs[9]    # quiet_hours_end
        
        if quiet_start and quiet_end:
            current_time = datetime.now().time()
            start_time = datetime.strptime(quiet_start, '%H:%M').time()
            end_time = datetime.strptime(quiet_end, '%H:%M').time()
            
            # Skip quiet hours check for critical notifications
            if notification.priority != NotificationPriority.CRITICAL:
                if start_time <= end_time:
                    if start_time <= current_time <= end_time:
                        return False
                else:  # Overnight quiet hours
                    if current_time >= start_time or current_time <= end_time:
                        return False
        
        return True
    
    def create_notification(
        self, 
        user_id: str, 
        notification_type: NotificationType,
        template_data: Dict = None,
        custom_title: str = None,
        custom_body: str = None,
        priority: NotificationPriority = None,
        data: Dict = None
    ) -> str:
        """
        Create a new notification
        
        Args:
            user_id: Target user ID
            notification_type: Type of notification
            template_data: Data for template formatting
            custom_title: Custom title (overrides template)
            custom_body: Custom body (overrides template)
            priority: Notification priority (overrides template)
            data: Additional data for the notification
        
        Returns:
            Notification ID
        """
        notification_id = str(uuid.uuid4())
        template_data = template_data or {}
        
        # Get template
        template = self.templates.get(notification_type, {})
        
        # Format title and body
        title = custom_title or template.get('title', 'Notification').format(**template_data)
        body = custom_body or template.get('body', 'You have a new notification').format(**template_data)
        
        # Set priority
        notification_priority = priority or template.get('priority', NotificationPriority.NORMAL)
        
        # Create notification object
        notification = PushNotification(
            id=notification_id,
            user_id=user_id,
            title=title,
            body=body,
            type=notification_type,
            priority=notification_priority,
            data=data or {},
            tag=template_data.get('tag')
        )
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notifications (
                id, user_id, title, body, type, priority, data, icon, image, badge, tag,
                timestamp, expires_at, sent, delivered, clicked
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            notification.id,
            notification.user_id,
            notification.title,
            notification.body,
            notification.type.value,
            notification.priority.value,
            json.dumps(notification.data),
            notification.icon,
            notification.image,
            notification.badge,
            notification.tag,
            notification.timestamp.isoformat(),
            notification.expires_at.isoformat(),
            notification.sent,
            notification.delivered,
            notification.clicked
        ))
        
        conn.commit()
        conn.close()
        
        print(f"📝 Created notification: {title}")
        return notification_id
    
    def subscribe_user(self, user_id: str, subscription_data: Dict) -> bool:
        """Subscribe user to push notifications"""
        # Save subscription to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO notification_subscriptions (user_id, subscription_data, last_active)
            VALUES (?, ?, datetime('now'))
        ''', (user_id, json.dumps(subscription_data)))
        
        conn.commit()
        conn.close()
        
        # Subscribe with push client
        return self.push_client.subscribe_user(user_id, subscription_data)
    
    def unsubscribe_user(self, user_id: str) -> bool:
        """Unsubscribe user from push notifications"""
        # Remove from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM notification_subscriptions WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        # Unsubscribe from push client
        return self.push_client.unsubscribe_user(user_id)
    
    def update_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Update user notification preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO notification_preferences (
                user_id, weather_alerts, crop_health, field_updates, market_alerts,
                system_updates, pest_alerts, irrigation_alerts, quiet_hours_start, quiet_hours_end
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            preferences.get('weather_alerts', True),
            preferences.get('crop_health', True),
            preferences.get('field_updates', True),
            preferences.get('market_alerts', True),
            preferences.get('system_updates', True),
            preferences.get('pest_alerts', True),
            preferences.get('irrigation_alerts', True),
            preferences.get('quiet_hours_start', '22:00'),
            preferences.get('quiet_hours_end', '06:00')
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Updated notification preferences for user {user_id}")
        return True
    
    def get_user_notifications(self, user_id: str, limit: int = 20) -> List[PushNotification]:
        """Get user's recent notifications"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM notifications 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        notifications = [self.row_to_notification(row) for row in cursor.fetchall()]
        
        conn.close()
        return notifications
    
    def mark_notification_clicked(self, notification_id: str) -> bool:
        """Mark notification as clicked"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notifications SET clicked = TRUE WHERE id = ?
        ''', (notification_id,))
        
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    def get_notification_stats(self, user_id: str = None) -> Dict:
        """Get notification statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        base_query = "SELECT COUNT(*), type, priority FROM notifications"
        params = []
        
        if user_id:
            base_query += " WHERE user_id = ?"
            params.append(user_id)
        
        base_query += " GROUP BY type, priority"
        
        cursor.execute(base_query, params)
        results = cursor.fetchall()
        
        stats = {
            'total': 0,
            'by_type': {},
            'by_priority': {}
        }
        
        for count, notif_type, priority in results:
            stats['total'] += count
            stats['by_type'][notif_type] = stats['by_type'].get(notif_type, 0) + count
            stats['by_priority'][priority] = stats['by_priority'].get(priority, 0) + count
        
        conn.close()
        return stats

# Agricultural notification helpers
class AgriculturalNotifications:
    """Agriculture-specific notification helpers"""
    
    def __init__(self, notification_manager: NotificationManager):
        self.manager = notification_manager
    
    def send_weather_alert(self, user_id: str, location: str, weather_data: Dict) -> str:
        """Send weather alert notification"""
        condition = weather_data.get('condition', 'Weather Update')
        temperature = weather_data.get('temperature', 0)
        
        # Determine severity
        if temperature > 40 or temperature < 5:
            details = f"Extreme temperature: {temperature}°C"
            priority = NotificationPriority.CRITICAL
        elif weather_data.get('wind_speed', 0) > 50:
            details = f"High winds: {weather_data['wind_speed']} km/h"
            priority = NotificationPriority.HIGH
        else:
            details = f"Temperature: {temperature}°C"
            priority = NotificationPriority.NORMAL
        
        return self.manager.create_notification(
            user_id=user_id,
            notification_type=NotificationType.WEATHER_ALERT,
            template_data={
                'location': location,
                'condition': condition,
                'details': details
            },
            priority=priority
        )
    
    def send_crop_health_alert(self, user_id: str, field_name: str, health_data: Dict) -> str:
        """Send crop health alert notification"""
        health_score = health_data.get('health_score', 100)
        issue_type = health_data.get('issue_type', 'Health update')
        
        priority = NotificationPriority.HIGH if health_score < 70 else NotificationPriority.NORMAL
        
        return self.manager.create_notification(
            user_id=user_id,
            notification_type=NotificationType.CROP_HEALTH,
            template_data={
                'field_name': field_name,
                'issue_type': issue_type,
                'health_score': health_score
            },
            priority=priority
        )
    
    def send_pest_alert(self, user_id: str, field_name: str, pest_data: Dict) -> str:
        """Send pest alert notification"""
        pest_type = pest_data.get('pest_type', 'Unknown pest')
        
        return self.manager.create_notification(
            user_id=user_id,
            notification_type=NotificationType.PEST_ALERT,
            template_data={
                'field_name': field_name,
                'pest_type': pest_type
            },
            priority=NotificationPriority.CRITICAL
        )
    
    def send_irrigation_alert(self, user_id: str, field_name: str, irrigation_data: Dict) -> str:
        """Send irrigation alert notification"""
        moisture_level = irrigation_data.get('moisture_level', 50)
        
        if moisture_level < 20:
            action_needed = "Irrigation recommended"
            priority = NotificationPriority.HIGH
        elif moisture_level > 80:
            action_needed = "Check drainage"
            priority = NotificationPriority.NORMAL
        else:
            action_needed = "Monitor moisture levels"
            priority = NotificationPriority.LOW
        
        return self.manager.create_notification(
            user_id=user_id,
            notification_type=NotificationType.IRRIGATION_ALERT,
            template_data={
                'field_name': field_name,
                'moisture_level': moisture_level,
                'action_needed': action_needed
            },
            priority=priority
        )
    
    def send_market_alert(self, user_id: str, crop_type: str, market_data: Dict) -> str:
        """Send market price alert notification"""
        price = market_data.get('price', 0)
        change_percent = market_data.get('change_percent', 0)
        
        change_type = "increased" if change_percent > 0 else "decreased"
        priority = NotificationPriority.HIGH if abs(change_percent) > 10 else NotificationPriority.NORMAL
        
        return self.manager.create_notification(
            user_id=user_id,
            notification_type=NotificationType.MARKET_ALERT,
            template_data={
                'crop_type': crop_type,
                'price': f"₹{price}",
                'change_type': change_type,
                'change_percent': f"{change_percent:+.1f}%"
            },
            priority=priority
        )

# Global instances
_notification_manager = None
_agricultural_notifications = None

def get_notification_manager() -> NotificationManager:
    """Get global notification manager instance"""
    global _notification_manager
    if _notification_manager is None:
        _notification_manager = NotificationManager()
    return _notification_manager

def get_agricultural_notifications() -> AgriculturalNotifications:
    """Get global agricultural notifications instance"""
    global _agricultural_notifications
    if _agricultural_notifications is None:
        _agricultural_notifications = AgriculturalNotifications(get_notification_manager())
    return _agricultural_notifications

# Convenience functions
def subscribe_to_notifications(user_id: str, subscription_data: Dict) -> bool:
    """Subscribe user to push notifications"""
    return get_notification_manager().subscribe_user(user_id, subscription_data)

def send_weather_alert(user_id: str, location: str, weather_data: Dict) -> str:
    """Send weather alert"""
    return get_agricultural_notifications().send_weather_alert(user_id, location, weather_data)

def send_crop_alert(user_id: str, field_name: str, health_data: Dict) -> str:
    """Send crop health alert"""
    return get_agricultural_notifications().send_crop_health_alert(user_id, field_name, health_data)

def send_pest_alert(user_id: str, field_name: str, pest_data: Dict) -> str:
    """Send pest alert"""
    return get_agricultural_notifications().send_pest_alert(user_id, field_name, pest_data)

# Demo function
def demo_push_notifications():
    """Demo push notifications"""
    st.title("📱 Push Notifications Demo")
    
    manager = get_notification_manager()
    agri_notifs = get_agricultural_notifications()
    
    # Subscription section
    st.subheader("🔔 Notification Subscription")
    
    user_id = st.text_input("User ID", value="demo_user")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📱 Subscribe to Notifications"):
            success = manager.subscribe_user(user_id, {"endpoint": "demo", "keys": {}})
            if success:
                st.success("Subscribed successfully!")
            else:
                st.error("Subscription failed")
    
    with col2:
        if st.button("🔕 Unsubscribe"):
            success = manager.unsubscribe_user(user_id)
            if success:
                st.success("Unsubscribed successfully!")
            else:
                st.error("Unsubscribe failed")
    
    # Send test notifications
    st.subheader("🧪 Test Notifications")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌤️ Weather Alert"):
            notif_id = agri_notifs.send_weather_alert(
                user_id, "Delhi", 
                {"temperature": 42, "condition": "Extreme Heat", "wind_speed": 25}
            )
            st.success(f"Weather alert sent: {notif_id[:8]}...")
    
    with col2:
        if st.button("🌾 Crop Health Alert"):
            notif_id = agri_notifs.send_crop_health_alert(
                user_id, "Field 1", 
                {"health_score": 65, "issue_type": "Drought stress"}
            )
            st.success(f"Crop alert sent: {notif_id[:8]}...")
    
    with col3:
        if st.button("🐛 Pest Alert"):
            notif_id = agri_notifs.send_pest_alert(
                user_id, "Field 2", 
                {"pest_type": "Aphids"}
            )
            st.success(f"Pest alert sent: {notif_id[:8]}...")
    
    # Notification history
    st.subheader("📋 Recent Notifications")
    notifications = manager.get_user_notifications(user_id, 10)
    
    if notifications:
        for notif in notifications:
            with st.expander(f"{notif.icon} {notif.title}"):
                st.write(f"**Body:** {notif.body}")
                st.write(f"**Type:** {notif.type.value}")
                st.write(f"**Priority:** {notif.priority.value}")
                st.write(f"**Timestamp:** {notif.timestamp}")
                st.write(f"**Status:** {'✅ Delivered' if notif.delivered else '⏳ Pending'}")
    else:
        st.info("No notifications found")
    
    # Statistics
    st.subheader("📊 Notification Statistics")
    stats = manager.get_notification_stats(user_id)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Notifications", stats['total'])
    
    with col2:
        if stats['by_priority']:
            st.write("**By Priority:**")
            for priority, count in stats['by_priority'].items():
                st.write(f"• {priority}: {count}")
    
    with col3:
        if stats['by_type']:
            st.write("**By Type:**")
            for notif_type, count in list(stats['by_type'].items())[:3]:
                st.write(f"• {notif_type}: {count}")

if __name__ == "__main__":
    demo_push_notifications()
