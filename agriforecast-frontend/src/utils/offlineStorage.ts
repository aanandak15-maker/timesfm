// Offline storage utilities for farmer field use
// Works without internet connection

interface OfflineData {
  id: string
  type: 'soil' | 'weather' | 'crop' | 'observation'
  data: any
  timestamp: string
  synced: boolean
}

class OfflineStorage {
  private dbName = 'AgriForecastOffline'
  private version = 1
  private db: IDBDatabase | null = null

  async init(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version)

      request.onerror = () => reject(request.error)
      request.onsuccess = () => {
        this.db = request.result
        resolve()
      }

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result
        
        // Create object stores for different data types
        if (!db.objectStoreNames.contains('soilData')) {
          db.createObjectStore('soilData', { keyPath: 'id' })
        }
        if (!db.objectStoreNames.contains('weatherData')) {
          db.createObjectStore('weatherData', { keyPath: 'id' })
        }
        if (!db.objectStoreNames.contains('cropData')) {
          db.createObjectStore('cropData', { keyPath: 'id' })
        }
        if (!db.objectStoreNames.contains('observations')) {
          db.createObjectStore('observations', { keyPath: 'id' })
        }
      }
    })
  }

  async saveData(type: OfflineData['type'], data: any): Promise<string> {
    if (!this.db) await this.init()

    const id = `${type}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    const offlineData: OfflineData = {
      id,
      type,
      data,
      timestamp: new Date().toISOString(),
      synced: false
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([`${type}Data`], 'readwrite')
      const store = transaction.objectStore(`${type}Data`)
      const request = store.add(offlineData)

      request.onsuccess = () => resolve(id)
      request.onerror = () => reject(request.error)
    })
  }

  async getData(type: OfflineData['type']): Promise<OfflineData[]> {
    if (!this.db) await this.init()

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([`${type}Data`], 'readonly')
      const store = transaction.objectStore(`${type}Data`)
      const request = store.getAll()

      request.onsuccess = () => resolve(request.result)
      request.onerror = () => reject(request.error)
    })
  }

  async markAsSynced(id: string, type: OfflineData['type']): Promise<void> {
    if (!this.db) await this.init()

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([`${type}Data`], 'readwrite')
      const store = transaction.objectStore(`${type}Data`)
      const getRequest = store.get(id)

      getRequest.onsuccess = () => {
        const data = getRequest.result
        if (data) {
          data.synced = true
          const updateRequest = store.put(data)
          updateRequest.onsuccess = () => resolve()
          updateRequest.onerror = () => reject(updateRequest.error)
        } else {
          resolve()
        }
      }
      getRequest.onerror = () => reject(getRequest.error)
    })
  }

  async getUnsyncedData(): Promise<OfflineData[]> {
    if (!this.db) await this.init()

    const allData: OfflineData[] = []
    const types: OfflineData['type'][] = ['soil', 'weather', 'crop', 'observation']

    for (const type of types) {
      const data = await this.getData(type)
      allData.push(...data.filter(item => !item.synced))
    }

    return allData
  }

  async clearSyncedData(): Promise<void> {
    if (!this.db) await this.init()

    const types: OfflineData['type'][] = ['soil', 'weather', 'crop', 'observation']

    for (const type of types) {
      const transaction = this.db!.transaction([`${type}Data`], 'readwrite')
      const store = transaction.objectStore(`${type}Data`)
      const request = store.getAll()

      request.onsuccess = () => {
        const data = request.result
        data.forEach(item => {
          if (item.synced) {
            store.delete(item.id)
          }
        })
      }
    }
  }

  // Check if device is online
  isOnline(): boolean {
    return navigator.onLine
  }

  // Get storage usage
  async getStorageUsage(): Promise<number> {
    if (!this.db) await this.init()

    let totalSize = 0
    const types: OfflineData['type'][] = ['soil', 'weather', 'crop', 'observation']

    for (const type of types) {
      const data = await this.getData(type)
      totalSize += JSON.stringify(data).length
    }

    return totalSize
  }
}

export const offlineStorage = new OfflineStorage()
export default offlineStorage
