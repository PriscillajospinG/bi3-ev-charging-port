class WebSocketService {
  constructor() {
    this.ws = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectInterval = 3000
    this.listeners = new Map()
  }

  connect(url = 'ws://localhost:8000/ws') {
    try {
      this.ws = new WebSocket(url)

      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.reconnectAttempts = 0
        this.emit('connected', { status: 'connected' })
      }

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          this.emit(data.type, data.payload)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        this.emit('error', { error })
      }

      this.ws.onclose = () => {
        console.log('WebSocket disconnected')
        this.emit('disconnected', { status: 'disconnected' })
        this.attemptReconnect(url)
      }
    } catch (error) {
      console.error('Failed to connect WebSocket:', error)
      this.attemptReconnect(url)
    }
  }

  attemptReconnect(url) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      setTimeout(() => this.connect(url), this.reconnectInterval)
    } else {
      console.error('Max reconnection attempts reached')
      this.emit('reconnect_failed', { attempts: this.reconnectAttempts })
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  send(type, payload) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, payload }))
    } else {
      console.warn('WebSocket is not connected')
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event).push(callback)
  }

  off(event, callback) {
    if (!this.listeners.has(event)) return
    const callbacks = this.listeners.get(event)
    const index = callbacks.indexOf(callback)
    if (index > -1) {
      callbacks.splice(index, 1)
    }
  }

  emit(event, data) {
    if (!this.listeners.has(event)) return
    this.listeners.get(event).forEach(callback => callback(data))
  }

  // Subscribe to specific data streams
  subscribeToMetrics() {
    this.send('subscribe', { stream: 'metrics' })
  }

  subscribeToChargerStatus() {
    this.send('subscribe', { stream: 'charger_status' })
  }

  subscribeToTraffic() {
    this.send('subscribe', { stream: 'traffic' })
  }

  subscribeToCameraFeed(cameraId) {
    this.send('subscribe', { stream: 'camera', cameraId })
  }

  unsubscribeFromStream(stream) {
    this.send('unsubscribe', { stream })
  }
}

export default new WebSocketService()
