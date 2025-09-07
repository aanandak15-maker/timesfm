"""
Enhanced Offline Capabilities for AgriForecast.ai
Background sync, offline data storage, and conflict resolution
"""

import streamlit as st
import sqlite3
import json
import time
import threading
from typing import Dict, List, Optional, Callable, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import uuid
import hashlib
from enum import Enum
import queue
import os

class SyncStatus(Enum):
    PENDING = "pending"
    SYNCING = "syncing"
    SYNCED = "synced"
    FAILED = "failed"
    CONFLICT = "conflict"

class OperationType(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class ConflictResolution(Enum):
    SERVER_WINS = "server_wins"
    CLIENT_WINS = "client_wins"
    MERGE = "merge"
    MANUAL = "manual"

@dataclass
class OfflineOperation:
    """Represents an offline operation to be synced"""
    id: str
    table: str
    operation_type: OperationType
    data: Dict
    timestamp: datetime
    user_id: str
    local_id: Optional[str] = None
    server_id: Optional[str] = None
    sync_status: SyncStatus = SyncStatus.PENDING
    retry_count: int = 0
    last_retry: Optional[datetime] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'id': self.id,
            'table': self.table,
            'operation_type': self.operation_type.value,
            'data': json.dumps(self.data),
            'timestamp': self.timestamp.isoformat(),
            'user_id': self.user_id,
            'local_id': self.local_id,
            'server_id': self.server_id,
            'sync_status': self.sync_status.value,
            'retry_count': self.retry_count,
            'last_retry': self.last_retry.isoformat() if self.last_retry else None,
            'error_message': self.error_message
        }

@dataclass
class SyncConflict:
    """Represents a sync conflict"""
    id: str
    table: str
    local_data: Dict
    server_data: Dict
    operation_id: str
    timestamp: datetime
    resolution: Optional[ConflictResolution] = None
    resolved_data: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'id': self.id,
            'table': self.table,
            'local_data': json.dumps(self.local_data),
            'server_data': json.dumps(self.server_data),
            'operation_id': self.operation_id,
            'timestamp': self.timestamp.isoformat(),
            'resolution': self.resolution.value if self.resolution else None,
            'resolved_data': json.dumps(self.resolved_data) if self.resolved_data else None
        }

class OfflineStorage:
    """Manages offline data storage and operations"""
    
    def __init__(self, db_path: str = "offline_data.db"):
        self.db_path = db_path
        self.init_database()
        self.operation_queue = queue.Queue()
        
    def init_database(self):
        """Initialize offline storage database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Offline operations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offline_operations (
                id TEXT PRIMARY KEY,
                table_name TEXT NOT NULL,
                operation_type TEXT NOT NULL,
                data TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                user_id TEXT NOT NULL,
                local_id TEXT,
                server_id TEXT,
                sync_status TEXT DEFAULT 'pending',
                retry_count INTEGER DEFAULT 0,
                last_retry TEXT,
                error_message TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sync conflicts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_conflicts (
                id TEXT PRIMARY KEY,
                table_name TEXT NOT NULL,
                local_data TEXT NOT NULL,
                server_data TEXT NOT NULL,
                operation_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                resolution TEXT,
                resolved_data TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Offline cache table for read operations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offline_cache (
                id TEXT PRIMARY KEY,
                table_name TEXT NOT NULL,
                record_id TEXT NOT NULL,
                data TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                expires_at TEXT,
                user_id TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(table_name, record_id, user_id)
            )
        ''')
        
        # Sync metadata table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_operation(self, operation: OfflineOperation) -> bool:
        """Add an offline operation to the queue"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            op_dict = operation.to_dict()
            cursor.execute('''
                INSERT INTO offline_operations (
                    id, table_name, operation_type, data, timestamp, user_id,
                    local_id, server_id, sync_status, retry_count, last_retry, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                op_dict['id'], op_dict['table'], op_dict['operation_type'],
                op_dict['data'], op_dict['timestamp'], op_dict['user_id'],
                op_dict['local_id'], op_dict['server_id'], op_dict['sync_status'],
                op_dict['retry_count'], op_dict['last_retry'], op_dict['error_message']
            ))
            
            conn.commit()
            conn.close()
            
            # Add to in-memory queue for immediate processing
            self.operation_queue.put(operation)
            
            print(f"📥 Added offline operation: {operation.operation_type.value} on {operation.table}")
            return True
            
        except Exception as e:
            print(f"Failed to add offline operation: {e}")
            return False
    
    def get_pending_operations(self, limit: int = 50) -> List[OfflineOperation]:
        """Get pending offline operations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM offline_operations 
            WHERE sync_status = 'pending' OR sync_status = 'failed'
            ORDER BY timestamp ASC
            LIMIT ?
        ''', (limit,))
        
        operations = []
        for row in cursor.fetchall():
            operations.append(self.row_to_operation(row))
        
        conn.close()
        return operations
    
    def row_to_operation(self, row) -> OfflineOperation:
        """Convert database row to OfflineOperation"""
        return OfflineOperation(
            id=row[0],
            table=row[1],
            operation_type=OperationType(row[2]),
            data=json.loads(row[3]),
            timestamp=datetime.fromisoformat(row[4]),
            user_id=row[5],
            local_id=row[6],
            server_id=row[7],
            sync_status=SyncStatus(row[8]),
            retry_count=row[9],
            last_retry=datetime.fromisoformat(row[10]) if row[10] else None,
            error_message=row[11]
        )
    
    def update_operation_status(self, operation_id: str, status: SyncStatus, 
                              error_message: str = None, server_id: str = None) -> bool:
        """Update operation sync status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        update_fields = ['sync_status = ?']
        params = [status.value]
        
        if error_message:
            update_fields.append('error_message = ?')
            params.append(error_message)
        
        if server_id:
            update_fields.append('server_id = ?')
            params.append(server_id)
        
        if status == SyncStatus.FAILED:
            update_fields.extend(['retry_count = retry_count + 1', 'last_retry = datetime("now")'])
        
        params.append(operation_id)
        
        query = f'''
            UPDATE offline_operations 
            SET {', '.join(update_fields)}
            WHERE id = ?
        '''
        
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    def cache_data(self, table: str, record_id: str, data: Dict, user_id: str, expires_in_hours: int = 24):
        """Cache data for offline access"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        expires_at = datetime.now() + timedelta(hours=expires_in_hours)
        
        cursor.execute('''
            INSERT OR REPLACE INTO offline_cache (
                id, table_name, record_id, data, timestamp, expires_at, user_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            str(uuid.uuid4()),
            table,
            record_id,
            json.dumps(data),
            datetime.now().isoformat(),
            expires_at.isoformat(),
            user_id
        ))
        
        conn.commit()
        conn.close()
    
    def get_cached_data(self, table: str, record_id: str = None, user_id: str = None) -> List[Dict]:
        """Get cached data for offline access"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT record_id, data, timestamp FROM offline_cache 
            WHERE table_name = ? AND (expires_at IS NULL OR expires_at > datetime('now'))
        '''
        params = [table]
        
        if record_id:
            query += ' AND record_id = ?'
            params.append(record_id)
        
        if user_id:
            query += ' AND user_id = ?'
            params.append(user_id)
        
        query += ' ORDER BY timestamp DESC'
        
        cursor.execute(query, params)
        results = []
        
        for row in cursor.fetchall():
            data = json.loads(row[1])
            data['_cache_info'] = {
                'record_id': row[0],
                'cached_at': row[2]
            }
            results.append(data)
        
        conn.close()
        return results
    
    def clear_expired_cache(self):
        """Clear expired cache entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM offline_cache 
            WHERE expires_at IS NOT NULL AND expires_at <= datetime('now')
        ''')
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            print(f"🧹 Cleared {deleted_count} expired cache entries")
        
        return deleted_count

class BackgroundSync:
    """Handles background synchronization of offline operations"""
    
    def __init__(self, offline_storage: OfflineStorage):
        self.storage = offline_storage
        self.is_running = False
        self.sync_thread = None
        self.sync_interval = 30  # seconds
        self.max_retries = 3
        self.conflict_handlers = {}
        
    def start(self):
        """Start background sync process"""
        if self.is_running:
            return
        
        self.is_running = True
        self.sync_thread = threading.Thread(target=self.sync_loop, daemon=True)
        self.sync_thread.start()
        print("🔄 Background sync started")
    
    def stop(self):
        """Stop background sync process"""
        self.is_running = False
        if self.sync_thread:
            self.sync_thread.join(timeout=5)
        print("⏹️ Background sync stopped")
    
    def sync_loop(self):
        """Main sync loop"""
        while self.is_running:
            try:
                self.sync_pending_operations()
                self.storage.clear_expired_cache()
                time.sleep(self.sync_interval)
            except Exception as e:
                print(f"Sync error: {e}")
                time.sleep(self.sync_interval * 2)  # Wait longer on error
    
    def sync_pending_operations(self):
        """Sync all pending operations"""
        operations = self.storage.get_pending_operations()
        
        if not operations:
            return
        
        print(f"📤 Syncing {len(operations)} pending operations")
        
        for operation in operations:
            if operation.retry_count >= self.max_retries:
                print(f"⚠️ Operation {operation.id} exceeded max retries")
                continue
            
            try:
                success = self.sync_operation(operation)
                if success:
                    self.storage.update_operation_status(operation.id, SyncStatus.SYNCED)
                else:
                    self.storage.update_operation_status(operation.id, SyncStatus.FAILED, "Sync failed")
            except Exception as e:
                self.storage.update_operation_status(operation.id, SyncStatus.FAILED, str(e))
    
    def sync_operation(self, operation: OfflineOperation) -> bool:
        """Sync a single operation"""
        try:
            # Simulate API call to server
            print(f"🔄 Syncing {operation.operation_type.value} on {operation.table}")
            
            # In production, this would make actual API calls
            if operation.operation_type == OperationType.CREATE:
                return self.sync_create_operation(operation)
            elif operation.operation_type == OperationType.UPDATE:
                return self.sync_update_operation(operation)
            elif operation.operation_type == OperationType.DELETE:
                return self.sync_delete_operation(operation)
            
            return False
            
        except Exception as e:
            print(f"Sync operation failed: {e}")
            return False
    
    def sync_create_operation(self, operation: OfflineOperation) -> bool:
        """Sync create operation"""
        # Simulate server response
        time.sleep(0.1)  # Simulate network delay
        
        # Generate server ID
        server_id = str(uuid.uuid4())
        
        # Update operation with server ID
        self.storage.update_operation_status(
            operation.id, 
            SyncStatus.SYNCED, 
            server_id=server_id
        )
        
        print(f"✅ Created {operation.table} record on server: {server_id}")
        return True
    
    def sync_update_operation(self, operation: OfflineOperation) -> bool:
        """Sync update operation"""
        # Simulate server response
        time.sleep(0.1)  # Simulate network delay
        
        # Check for conflicts (simulate)
        if self.has_conflict(operation):
            self.handle_conflict(operation)
            return False
        
        print(f"✅ Updated {operation.table} record on server")
        return True
    
    def sync_delete_operation(self, operation: OfflineOperation) -> bool:
        """Sync delete operation"""
        # Simulate server response
        time.sleep(0.1)  # Simulate network delay
        
        print(f"✅ Deleted {operation.table} record on server")
        return True
    
    def has_conflict(self, operation: OfflineOperation) -> bool:
        """Check if operation has conflicts (simulate)"""
        # Simulate 10% conflict rate for demonstration
        import random
        return random.random() < 0.1
    
    def handle_conflict(self, operation: OfflineOperation):
        """Handle sync conflict"""
        # Create conflict record
        conflict = SyncConflict(
            id=str(uuid.uuid4()),
            table=operation.table,
            local_data=operation.data,
            server_data={"server_version": "newer", **operation.data},
            operation_id=operation.id,
            timestamp=datetime.now()
        )
        
        # Store conflict
        self.store_conflict(conflict)
        
        # Update operation status
        self.storage.update_operation_status(
            operation.id, 
            SyncStatus.CONFLICT, 
            "Data conflict detected"
        )
        
        print(f"⚠️ Conflict detected for operation {operation.id}")
    
    def store_conflict(self, conflict: SyncConflict):
        """Store sync conflict in database"""
        conn = sqlite3.connect(self.storage.db_path)
        cursor = conn.cursor()
        
        conflict_dict = conflict.to_dict()
        cursor.execute('''
            INSERT INTO sync_conflicts (
                id, table_name, local_data, server_data, operation_id, timestamp, resolution, resolved_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            conflict_dict['id'], conflict_dict['table'], conflict_dict['local_data'],
            conflict_dict['server_data'], conflict_dict['operation_id'], 
            conflict_dict['timestamp'], conflict_dict['resolution'], conflict_dict['resolved_data']
        ))
        
        conn.commit()
        conn.close()
    
    def get_conflicts(self, user_id: str = None) -> List[SyncConflict]:
        """Get unresolved conflicts"""
        conn = sqlite3.connect(self.storage.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT c.* FROM sync_conflicts c
            JOIN offline_operations o ON c.operation_id = o.id
            WHERE c.resolution IS NULL
        '''
        params = []
        
        if user_id:
            query += ' AND o.user_id = ?'
            params.append(user_id)
        
        query += ' ORDER BY c.timestamp DESC'
        
        cursor.execute(query, params)
        conflicts = []
        
        for row in cursor.fetchall():
            conflict = SyncConflict(
                id=row[0],
                table=row[1],
                local_data=json.loads(row[2]),
                server_data=json.loads(row[3]),
                operation_id=row[4],
                timestamp=datetime.fromisoformat(row[5]),
                resolution=ConflictResolution(row[6]) if row[6] else None,
                resolved_data=json.loads(row[7]) if row[7] else None
            )
            conflicts.append(conflict)
        
        conn.close()
        return conflicts
    
    def resolve_conflict(self, conflict_id: str, resolution: ConflictResolution, resolved_data: Dict = None) -> bool:
        """Resolve a sync conflict"""
        conn = sqlite3.connect(self.storage.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sync_conflicts 
            SET resolution = ?, resolved_data = ?
            WHERE id = ?
        ''', (resolution.value, json.dumps(resolved_data) if resolved_data else None, conflict_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Resolved conflict {conflict_id} with {resolution.value}")
        return cursor.rowcount > 0

class OfflineManager:
    """Main offline functionality manager"""
    
    def __init__(self):
        self.storage = OfflineStorage()
        self.background_sync = BackgroundSync(self.storage)
        self.is_online = True
        self.connection_handlers = []
        
        # Start background sync
        self.background_sync.start()
        
        # Start connection monitoring
        self.start_connection_monitoring()
    
    def start_connection_monitoring(self):
        """Start monitoring network connection"""
        def monitor_connection():
            while True:
                try:
                    # Simulate connection check
                    # In production, this would ping a server or check navigator.onLine
                    import random
                    self.is_online = random.random() > 0.1  # 90% online simulation
                    
                    # Notify handlers of connection change
                    for handler in self.connection_handlers:
                        handler(self.is_online)
                    
                    time.sleep(10)  # Check every 10 seconds
                except Exception as e:
                    print(f"Connection monitoring error: {e}")
                    time.sleep(30)
        
        thread = threading.Thread(target=monitor_connection, daemon=True)
        thread.start()
    
    def add_connection_handler(self, handler: Callable[[bool], None]):
        """Add connection status change handler"""
        self.connection_handlers.append(handler)
    
    def create_record(self, table: str, data: Dict, user_id: str) -> str:
        """Create a record (offline-capable)"""
        local_id = str(uuid.uuid4())
        
        if self.is_online:
            # Try immediate sync
            try:
                # Simulate API call
                time.sleep(0.1)
                server_id = str(uuid.uuid4())
                
                # Cache the data
                self.storage.cache_data(table, local_id, data, user_id)
                
                print(f"✅ Created {table} record online: {server_id}")
                return server_id
            except Exception as e:
                print(f"Online create failed, queuing for offline sync: {e}")
        
        # Queue for offline sync
        operation = OfflineOperation(
            id=str(uuid.uuid4()),
            table=table,
            operation_type=OperationType.CREATE,
            data=data,
            timestamp=datetime.now(),
            user_id=user_id,
            local_id=local_id
        )
        
        self.storage.add_operation(operation)
        
        # Cache locally
        self.storage.cache_data(table, local_id, data, user_id)
        
        print(f"📥 Queued {table} creation for offline sync")
        return local_id
    
    def update_record(self, table: str, record_id: str, data: Dict, user_id: str) -> bool:
        """Update a record (offline-capable)"""
        if self.is_online:
            # Try immediate sync
            try:
                # Simulate API call
                time.sleep(0.1)
                
                # Update cache
                self.storage.cache_data(table, record_id, data, user_id)
                
                print(f"✅ Updated {table} record online: {record_id}")
                return True
            except Exception as e:
                print(f"Online update failed, queuing for offline sync: {e}")
        
        # Queue for offline sync
        operation = OfflineOperation(
            id=str(uuid.uuid4()),
            table=table,
            operation_type=OperationType.UPDATE,
            data=data,
            timestamp=datetime.now(),
            user_id=user_id,
            server_id=record_id
        )
        
        self.storage.add_operation(operation)
        
        # Update local cache
        self.storage.cache_data(table, record_id, data, user_id)
        
        print(f"📥 Queued {table} update for offline sync")
        return True
    
    def delete_record(self, table: str, record_id: str, user_id: str) -> bool:
        """Delete a record (offline-capable)"""
        if self.is_online:
            # Try immediate sync
            try:
                # Simulate API call
                time.sleep(0.1)
                
                print(f"✅ Deleted {table} record online: {record_id}")
                return True
            except Exception as e:
                print(f"Online delete failed, queuing for offline sync: {e}")
        
        # Queue for offline sync
        operation = OfflineOperation(
            id=str(uuid.uuid4()),
            table=table,
            operation_type=OperationType.DELETE,
            data={'id': record_id},
            timestamp=datetime.now(),
            user_id=user_id,
            server_id=record_id
        )
        
        self.storage.add_operation(operation)
        
        print(f"📥 Queued {table} deletion for offline sync")
        return True
    
    def get_records(self, table: str, user_id: str = None) -> List[Dict]:
        """Get records (offline-capable)"""
        if self.is_online:
            try:
                # Simulate API call
                time.sleep(0.1)
                
                # Simulate server data
                server_data = [
                    {'id': str(uuid.uuid4()), 'name': 'Server Record 1', 'type': 'online'},
                    {'id': str(uuid.uuid4()), 'name': 'Server Record 2', 'type': 'online'}
                ]
                
                # Cache server data
                for record in server_data:
                    self.storage.cache_data(table, record['id'], record, user_id or 'system')
                
                print(f"✅ Retrieved {len(server_data)} {table} records online")
                return server_data
            except Exception as e:
                print(f"Online retrieval failed, using cached data: {e}")
        
        # Use cached data
        cached_data = self.storage.get_cached_data(table, user_id=user_id)
        print(f"📱 Retrieved {len(cached_data)} {table} records from cache")
        return cached_data
    
    def get_sync_status(self) -> Dict:
        """Get offline sync status"""
        pending_ops = self.storage.get_pending_operations()
        conflicts = self.background_sync.get_conflicts()
        
        return {
            'is_online': self.is_online,
            'pending_operations': len(pending_ops),
            'conflicts': len(conflicts),
            'sync_running': self.background_sync.is_running,
            'last_sync': datetime.now().isoformat()
        }
    
    def force_sync(self) -> Dict:
        """Force immediate sync of all pending operations"""
        if not self.is_online:
            return {'success': False, 'message': 'Cannot sync while offline'}
        
        pending_ops = self.storage.get_pending_operations()
        success_count = 0
        
        for operation in pending_ops:
            try:
                if self.background_sync.sync_operation(operation):
                    self.storage.update_operation_status(operation.id, SyncStatus.SYNCED)
                    success_count += 1
                else:
                    self.storage.update_operation_status(operation.id, SyncStatus.FAILED, "Force sync failed")
            except Exception as e:
                self.storage.update_operation_status(operation.id, SyncStatus.FAILED, str(e))
        
        return {
            'success': True,
            'synced_operations': success_count,
            'total_operations': len(pending_ops)
        }

# Global offline manager instance
_offline_manager = None

def get_offline_manager() -> OfflineManager:
    """Get global offline manager instance"""
    global _offline_manager
    if _offline_manager is None:
        _offline_manager = OfflineManager()
    return _offline_manager

# Convenience functions
def create_offline_record(table: str, data: Dict, user_id: str) -> str:
    """Create record with offline support"""
    return get_offline_manager().create_record(table, data, user_id)

def update_offline_record(table: str, record_id: str, data: Dict, user_id: str) -> bool:
    """Update record with offline support"""
    return get_offline_manager().update_record(table, record_id, data, user_id)

def delete_offline_record(table: str, record_id: str, user_id: str) -> bool:
    """Delete record with offline support"""
    return get_offline_manager().delete_record(table, record_id, user_id)

def get_offline_records(table: str, user_id: str = None) -> List[Dict]:
    """Get records with offline support"""
    return get_offline_manager().get_records(table, user_id)

def get_offline_status() -> Dict:
    """Get offline sync status"""
    return get_offline_manager().get_sync_status()

# Demo function
def demo_offline_capabilities():
    """Demo offline capabilities"""
    st.title("📱 Offline Capabilities Demo")
    
    manager = get_offline_manager()
    
    # Connection status
    status = manager.get_sync_status()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if status['is_online']:
            st.success("🟢 Online")
        else:
            st.error("🔴 Offline")
    
    with col2:
        st.metric("Pending Ops", status['pending_operations'])
    
    with col3:
        st.metric("Conflicts", status['conflicts'])
    
    with col4:
        if status['sync_running']:
            st.success("🔄 Syncing")
        else:
            st.warning("⏸️ Sync Paused")
    
    # Test operations
    st.subheader("🧪 Test Offline Operations")
    
    user_id = st.text_input("User ID", value="demo_user")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Create Record"):
            record_id = create_offline_record(
                "fields", 
                {"name": f"Test Field {int(time.time())}", "crop": "rice"}, 
                user_id
            )
            st.success(f"Created: {record_id[:8]}...")
    
    with col2:
        if st.button("📝 Update Record"):
            records = get_offline_records("fields", user_id)
            if records:
                record_id = records[0].get('id') or records[0].get('_cache_info', {}).get('record_id')
                if record_id:
                    update_offline_record(
                        "fields", 
                        record_id,
                        {"name": "Updated Field", "status": "updated"}, 
                        user_id
                    )
                    st.success("Updated record")
                else:
                    st.warning("No record ID found")
            else:
                st.warning("No records to update")
    
    with col3:
        if st.button("🗑️ Delete Record"):
            records = get_offline_records("fields", user_id)
            if records:
                record_id = records[0].get('id') or records[0].get('_cache_info', {}).get('record_id')
                if record_id:
                    delete_offline_record("fields", record_id, user_id)
                    st.success("Deleted record")
                else:
                    st.warning("No record ID found")
            else:
                st.warning("No records to delete")
    
    # Show cached records
    st.subheader("📱 Cached Records")
    records = get_offline_records("fields", user_id)
    
    if records:
        for i, record in enumerate(records[:5]):  # Show first 5
            with st.expander(f"Record {i+1}: {record.get('name', 'Unknown')}"):
                st.json(record)
    else:
        st.info("No cached records found")
    
    # Sync controls
    st.subheader("🔄 Sync Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Force Sync"):
            result = manager.force_sync()
            if result['success']:
                st.success(f"Synced {result['synced_operations']}/{result['total_operations']} operations")
            else:
                st.error(result['message'])
    
    with col2:
        if st.button("🔄 Refresh Status"):
            st.rerun()
    
    # Show conflicts
    conflicts = manager.background_sync.get_conflicts(user_id)
    if conflicts:
        st.subheader("⚠️ Sync Conflicts")
        for conflict in conflicts:
            with st.expander(f"Conflict: {conflict.table} - {conflict.id[:8]}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Local Data:**")
                    st.json(conflict.local_data)
                with col2:
                    st.write("**Server Data:**")
                    st.json(conflict.server_data)
                
                if st.button(f"Resolve - Use Local", key=f"local_{conflict.id}"):
                    manager.background_sync.resolve_conflict(
                        conflict.id, 
                        ConflictResolution.CLIENT_WINS, 
                        conflict.local_data
                    )
                    st.rerun()

if __name__ == "__main__":
    demo_offline_capabilities()
