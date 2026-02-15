<template>
  <div class="waiting-page">
    <div class="page-header">
      <div class="step-indicator">
        <h1 class="page-title">Ожидание соперника</h1>
        <p class="page-description">Отправьте ссылку для присоединения к матчу</p>
      </div>
    </div>

    <div class="page-content">
      <div class="match-card">
        <div class="match-info-header">
          <div class="match-status">
            <div class="status-dot"></div>
            <span class="status-text">Ожидается</span>
          </div>
          <div class="match-code-display">Код: {{ currentMatch.matchId }}</div>
        </div>

        <div class="match-properties">
          <div class="property-row">
            <span class="property-label">Предмет:</span>
            <span class="property-value">{{ currentMatch.subject }}</span>
          </div>
          <div class="property-row">
            <span class="property-label">Сложность:</span>
            <span class="property-value">{{ currentMatch.difficulty }}</span>
          </div>
        </div>

        <div class="invitation-section">
          <h3 class="section-title">Ссылка для приглашения</h3>
          <div class="invitation-link-container">
            <div class="link-display">
              {{ invitationLink }}
            </div>
            <button @click="handleCopyLink" class="copy-link-btn">  <!-- тут копирование работает -->
              Копировать
            </button>
          </div>
        </div>

        <div class="players-overview">
          <div class="player-info first-player">
            <div class="player-label">Вы</div>
            <div class="player-state ready-state">✓ Готов</div>
          </div>
          
          <div class="versus-separator">vs</div>
          
          <div class="player-info second-player">
            <div class="player-label">Ожидание соперника</div>
            <div class="player-state waiting-state">⌛ Присоединится</div>
          </div>
        </div>

        <button @click="handleCancelMatch" class="cancel-match-btn">
          Отменить матч
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios';

export default {
  name: 'WaitingPage',
  
  setup() {
    const router = useRouter()
    // Исправление: используем ref правильно
    const ws = ref(null)
    const socket = ref(null) // У вас дублирование, оставим один
    
    // Реактивные данные
    const currentMatch = ref({
      subject: localStorage.getItem('currentMatchSubject') || 'Не указан', // Исправлено: был пробел в ключе
      difficulty: localStorage.getItem('currentMatchDifficulty') || 'Средняя',
      matchId: localStorage.getItem('currentMatchId') || 'Нет кода'
    })
    
    const userData = ref(null)
    const checkInterval = ref(null)
    const isLoading = ref(true)

    // Computed
    const invitationLink = computed(() => {
      const baseUrl = window.location.origin
      return `${baseUrl}/join/${currentMatch.value.matchId}`
    })

    // Методы
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('authToken');
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Token ${token}`;
          const response = await axios.get('http://localhost:8000/api/auth/profile/');
          userData.value = response.data;
          console.log('Данные пользователя:', userData.value);
        }
      } catch (err) {
        console.error('Ошибка при загрузке данных пользователя:', err);
        userData.value = null;
      } finally {
        isLoading.value = false;
      }
    }

    // ИСПРАВЛЕНО: connectWebSocket - убрано использование this
    const connectWebSocket = async (role) => {
      // Закрываем предыдущее соединение, если есть
      if (ws.value && ws.value.readyState === WebSocket.OPEN) {
        ws.value.close();
      }

      // Подключаемся к WebSocket
      const token = localStorage.getItem('authToken');
      const matchId = localStorage.getItem('currentMatchId');
      
      if (token && matchId) {
        const wsUrl = `ws://localhost:8000/ws/pvp/${matchId}/?token=${token}`;
        ws.value = new WebSocket(wsUrl);
        console.log('WebSocket: ', ws.value);

        ws.value.onopen = () => {
          console.log('WebSocket подключен');
          
          // Отправляем информацию о пользователе
          if (userData.value) {
            const message = {
              type: 'join',
              role: role,
              user_id: userData.value.id,
              username: userData.value.username
            };
            ws.value.send(JSON.stringify(message));
          }
        };

        ws.value.onmessage = (event) => {
          const data = JSON.parse(event.data);
          handleWebSocketMessage(data); // Убедитесь, что этот метод определен
        };

        // ИСПРАВЛЕНО: onerror - используем стрелочную функцию и не обращаемся к arguments
        ws.value.onerror = (error) => {
          console.error('WebSocket ошибка:', error);
          // Не используем arguments, error.message, error.type
          if (error && error.message) {
            console.log('Детали ошибки:', error.message);
          }
        };

        ws.value.onclose = (event) => {
          console.log('WebSocket отключен. Код:', event.code, 'Причина:', event.reason);
        };
      }
    }

    // ИСПРАВЛЕНО: checkStatus - убрано использование this
    const checkStatus = async () => {
      try {
        const matchId = currentMatch.value?.matchId;
        if (!matchId || matchId === 'Нет кода') {
          console.error('Match code not found');
          return;
        }

        const token = localStorage.getItem('authToken');
        if (!token) {
          console.error('Auth token not found');
          router.push('/login');
          return;
        }

        console.log("Token: ", token, matchId);
        const response = await axios.get(`http://localhost:8000/api/pvp/status/${matchId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        console.log('Current status:', response.data);

        if (response.data.status === 'active') {
          stopStatusChecking();
          // Закрываем WebSocket перед переходом
          if (ws.value && ws.value.readyState === WebSocket.OPEN) {
            ws.value.close(1000, 'Match started');
          }
          router.push(`/PvP/answer`);
        }
      } catch (err) {
        console.error('Error checking match status:', err);
        // ИСПРАВЛЕНО: используем ws.value вместо this.ws
        if (ws.value && ws.value.readyState === WebSocket.OPEN) {
          ws.value.close();
        }
        if (err.response?.status === 401) {
          console.error('Unauthorized: Invalid or expired token');
          localStorage.removeItem('authToken');
          router.push('/login');
        }
      }
    }

    // Добавим обработчик сообщений WebSocket, если он нужен
    const handleWebSocketMessage = (data) => {
      console.log('Получено сообщение:', data);
      // Обработка различных типов сообщений
      switch(data.type) {
        case 'player_joined':
          console.log('Игрок присоединился:', data.username);
          // Можно обновить UI
          break;
        case 'match_started':
          console.log('Матч начался!');
          stopStatusChecking();
          router.push(`/PvP/answer`);
          break;
        default:
          console.log('Неизвестный тип сообщения:', data.type);
      }
    }

    const startStatusChecking = () => {
      // Вызываем сразу один раз
      checkStatus();
      
      // Затем устанавливаем интервал
      checkInterval.value = setInterval(() => {
        checkStatus();
      }, 1000);
    }

    const stopStatusChecking = () => {
      if (checkInterval.value) {
        clearInterval(checkInterval.value);
        checkInterval.value = null;
      }
    }

    const handleCopyLink = async () => {
      const linkText = invitationLink.value
      
      try {
        await navigator.clipboard.writeText(linkText)
        alert('Ссылка скопирована!')
      } catch {
        const tempInput = document.createElement('input')
        tempInput.value = linkText
        document.body.appendChild(tempInput)
        tempInput.select()
        document.execCommand('copy')
        document.body.removeChild(tempInput)
        alert('Ссылка скопирована в буфер!')
      }
    }

    const handleCancelMatch = () => {
      const userConfirmed = confirm('Вы уверены, что хотите отменить матч?')
      
      if (userConfirmed) {
        // Закрываем WebSocket если открыт
        if (ws.value && ws.value.readyState === WebSocket.OPEN) {
          ws.value.close(1000, 'User cancelled match');
        }
        
        stopStatusChecking();
        router.push('/')
      }
    }

    // Хуки жизненного цикла
    onMounted(async () => {
      console.log('Компонент монтирован');
      console.log('Match ID из localStorage:', currentMatch.value.matchId);
      
      await fetchUserData();
      // Ждем загрузки данных пользователя перед подключением
      if (userData.value) {
        connectWebSocket("host");
      } else {
        // Если данные не загрузились, пробуем еще раз через небольшую задержку
        setTimeout(() => {
          if (userData.value) {
            connectWebSocket("host");
          } else {
            console.warn('Данные пользователя не загружены, WebSocket не подключен');
          }
        }, 500);
      }
      startStatusChecking();
    })

    onUnmounted(() => {
      // Очистка при размонтировании
      if (ws.value && ws.value.readyState === WebSocket.OPEN) {
        ws.value.close(1000, 'Component unmounted');
      }
      
      stopStatusChecking();
    })

    // Возвращаем всё что нужно в шаблоне
    return {
      currentMatch,
      invitationLink,
      handleCopyLink,
      handleCancelMatch,
      isLoading
    }
  }
}
</script>

<style scoped>


.waiting-page {
  min-height: 100vh;
  background-color: rgb(250, 246, 239);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.page-header {
  padding: 40px 20px 20px;
  max-width: 800px;
  margin: 0 auto;
}

.step-indicator {
  text-align: center;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.page-description {
  color: #64748b;
  font-size: 16px;
  line-height: 1.5;
}

.page-content {
  padding: 0 20px 40px;
  max-width: 800px;
  margin: 0 auto;
}

.match-card {
  background-color: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
}

.match-info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.match-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 10px;
  height: 10px;
  background-color: #f59e0b;
  border-radius: 50%;
  animation: statusPulse 2s infinite;
}

@keyframes statusPulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.status-text {
  color: #f59e0b;
  font-weight: 600;
  font-size: 15px;
}

.match-code-display {
  background-color: #f1f5f9;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 14px;
  color: #475569;
  font-family: 'Monaco', 'Consolas', monospace;
}

.match-properties {
  margin-bottom: 32px;
}

.property-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.property-row:last-child {
  border-bottom: none;
}

.property-label {
  color: #64748b;
  font-size: 14px;
}

.property-value {
  color: #1e293b;
  font-weight: 600;
  font-size: 15px;
}

.invitation-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 16px;
  color: #475569;
  margin-bottom: 12px;
  font-weight: 600;
}

.invitation-link-container {
  display: flex;
  gap: 12px;
}

.link-display {
  flex: 1;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 14px;
  color: #334155;
  font-family: 'Monaco', 'Consolas', monospace;
  word-break: break-all;
  line-height: 1.4;
}

.copy-link-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.copy-link-btn:hover {
  background-color: #2563eb;
}

.players-overview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 40px 0;
  padding: 24px;
  background-color: #f1f5f9;
  border-radius: 12px;
}

.player-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.player-label {
  font-size: 16px;
  font-weight: 600;
  color: #475569;
}

.player-state {
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 20px;
  width: fit-content;
  font-weight: 500;
}

.ready-state {
  background-color: #d1fae5;
  color: #065f46;
}

.waiting-state {
  background-color: #fef3c7;
  color: #92400e;
}

.versus-separator {
  color: #94a3b8;
  font-size: 18px;
  font-weight: 700;
  margin: 0 20px;
}

.cancel-match-btn {
  width: 100%;
  background-color: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-match-btn:hover {
  background-color: #fee2e2;
}

@media (max-width: 640px) {
  .page-header {
    padding: 24px 16px 16px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .match-card {
    padding: 24px;
  }
  
  .match-info-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .invitation-link-container {
    flex-direction: column;
  }
  
  .players-overview {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .versus-separator {
    margin: 8px 0;
  }
  
  .player-info {
    align-items: center;
  }
}
</style>
