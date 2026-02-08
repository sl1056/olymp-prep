<template>
  <HeaderEnter v-if="userData"></HeaderEnter>
  <Header v-else></Header>
  <div class="page">
    <div class="header">
      <h1>PVP МАТЧ</h1>
      <p>СРАЖАЙТЕСЬ С ДРУГОМ, РЕШАЯ ОЛИМПИАДНЫЕ ЗАДАНИЯ ПО ВСЕМ ПРЕДМЕТАМ</p>
    </div>

    <div class="cards">
      <div class="card card-create">
        <h2>СОЗДАТЬ МАТЧ</h2>
        <p>Начни новый PvP-бой и пригласи соперника</p>
        <button @click="createMatch" :disabled="creatingMatch">
          {{ creatingMatch ? 'СОЗДАНИЕ...' : 'НАЧАТЬ БОЙ' }}
        </button>
      </div>

      <div class="card card-join">
        <h2>ПРИСОЕДИНИТЬСЯ</h2>
        <p>Войди в матч по ссылке от друга</p>
        <input v-model="matchCode" placeholder="Введите код матча" />
        <button @click="joinMatch" :disabled="joiningMatch">
          {{ joiningMatch ? 'ПОДКЛЮЧЕНИЕ...' : 'ВОЙТИ В БОЙ' }}
        </button>
      </div>
    </div>

    <!-- Модальное окно ожидания -->
    <div v-if="showWaitingModal" class="modal-overlay">
      <div class="modal">
        <h3>Ожидание соперника</h3>
        <p>Код матча: <strong>{{ matchCode }}</strong></p>
        <p>Поделитесь этим кодом с другом</p>
        <div class="loader"></div>
        <button @click="cancelMatch" class="cancel-btn">ОТМЕНИТЬ</button>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import HeaderEnter from '@/components/HeaderEnter.vue';
import axios from 'axios';

export default {
  components: { Header, HeaderEnter },
  name: "PVPHome",
  
  data() {
    return {
      matchCode: '',
      userData: null,
      isLoading: true,
      creatingMatch: false,
      joiningMatch: false,
      showWaitingModal: false,
      ws: null,
      matchId: null
    }
  },

  async created() {
    await this.fetchUserData();
  },

  beforeUnmount() {
    // Закрываем соединение WebSocket при покидании страницы
    if (this.ws) {
      this.ws.close();
    }
  },

  methods: {
    async fetchUserData() {
      try {
        const token = localStorage.getItem('authToken');
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Token ${token}`;
          const response = await axios.get('http://localhost:8000/api/auth/profile/');
          this.userData = response.data;
        }
      } catch (err) {
        console.error('Ошибка при загрузке данных пользователя:', err);
        this.userData = null;
      } finally {
        this.isLoading = false;
      }
    },

    async createMatch() {
      if (!this.userData) {
        alert('Пожалуйста, войдите в систему для создания матча');
        return;
      }

      this.creatingMatch = true;
      
      try {
        // 1. Создаем матч на сервере
        const token = localStorage.getItem('authToken');
        const response = await axios.post(
          'http://localhost:8000/api/pvp/create/',
          {},
          {
            headers: {
              'Authorization': `Token ${token}`
            }
          }
        );

        this.matchId = response.data.match_id;
        this.matchCode = response.data.code;
        
        // 2. Подключаемся к WebSocket
        this.connectWebSocket('host');
        
        // 3. Показываем окно ожидания
        this.showWaitingModal = true;

        console.log('Матч создан')
        
      } catch (error) {
        console.error('Ошибка при создании матча:', error);
        alert('Не удалось создать матч. Попробуйте еще раз.');
      } finally {
        this.creatingMatch = false;
      }
    },

    async joinMatch() {
      const code = this.matchCode.trim();
      
      if (!code) {
        alert('Введите код матча');
        return;
      }

      if (!this.userData) {
        alert('Пожалуйста, войдите в систему для присоединения к матчу');
        return;
      }

      this.joiningMatch = true;
      
      try {
        // 1. Проверяем существование матча
        const token = localStorage.getItem('authToken');
        const response = await axios.post(
          'http://localhost:8000/api/pvp/join/',
          { code: code },
          {
            headers: {
              'Authorization': `Token ${token}`
            }
          }
        );

        this.matchId = response.data.match_id;
        
        // 2. Подключаемся к WebSocket как участник
        this.connectWebSocket('player');
        
        // 3. Перенаправляем на страницу матча
        this.$router.push(`/pvp/match/${this.matchId}`);
        
      } catch (error) {
        console.error('Ошибка при присоединении к матчу:', error);
        if (error.response?.status === 404) {
          alert('Матч не найден. Проверьте код.');
        } else if (error.response?.status === 400) {
          alert('Матч уже начался или заполнен.');
        } else {
          alert('Не удалось присоединиться к матчу.');
        }
      } finally {
        this.joiningMatch = false;
      }
    },

    connectWebSocket(role) {
      // Закрываем предыдущее соединение, если есть
      if (this.ws) {
        this.ws.close();
      }

      // Подключаемся к WebSocket
      const wsUrl = `ws://localhost:8000/ws/pvp/${this.matchId}/`;
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('WebSocket подключен');
        
        // Отправляем информацию о пользователе
        const message = {
          type: 'join',
          role: role,
          user_id: this.userData.id,
          username: this.userData.username
        };
        this.ws.send(JSON.stringify(message));
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.handleWebSocketMessage(data);
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket ошибка:', error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket отключен');
      };
    },

    handleWebSocketMessage(data) {
      console.log('Получено сообщение:', data);
      
      switch (data.type) {
        case 'match_ready':
          // Матч готов к началу (оба игрока подключились)
          this.showWaitingModal = false;
          this.$router.push(`/pvp/match/${this.matchId}`);
          break;
          
        case 'player_joined':
          // В матч присоединился игрок (для хоста)
          alert(`Игрок ${data.username} присоединился к матчу!`);
          break;
          
        case 'match_cancelled':
          // Матч отменен
          this.showWaitingModal = false;
          alert('Матч был отменен создателем');
          break;
          
        case 'error':
          alert(`Ошибка: ${data.message}`);
          break;
      }
    },

    cancelMatch() {
      if (this.ws) {
        const message = {
          type: 'cancel_match'
        };
        this.ws.send(JSON.stringify(message));
      }
      this.showWaitingModal = false;
      this.matchId = null;
      this.matchCode = '';
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: rgb(250, 246, 239);
  min-height: 100vh;
}

.page {
  max-width: 1000px;
  margin: 0 auto;
  margin-top: -8%;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 60px;
}

h1 {
  font-size: 48px;
  color: #1a365d;
  margin-bottom: 16px;
  font-weight: 800;
}

.header p {
  font-size: 20px;
  color: #4a5568;
  line-height: 1.5;
  max-width: 600px;
}

.cards {
  display: flex;
  gap: 40px;
  width: 100%;
  justify-content: center;
}

.card {
  flex: 1;
  min-width: 280px;
  max-width: 400px;
  background: white;
  border-radius: 20px;
  padding: 40px 32px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  border-top: 5px solid;
}

.card-create {
  border-color: #d69e2e;
  background: linear-gradient(to bottom, #fffaf0, #fed7d7);
}

.card-join {
  border-color: #3182ce;
  background: linear-gradient(to bottom, #ebf8ff, #e6fffa);
}

.card h2 {
  font-size: 28px;
  margin-bottom: 16px;
  color: #2d3748;
}

.card p {
  color: #4a5568;
  margin-bottom: 32px;
  line-height: 1.5;
}

.card input {
  width: 100%;
  padding: 14px 18px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 16px;
  margin-bottom: 24px;
  text-align: center;
}

.card-join input {
  border-color: #90cdf4;
}

.card button {
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.card button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.card-create button {
  background: #d69e2e;
  color: white;
}

.card-create button:hover:not(:disabled) {
  background: #b7791f;
}

.card-join button {
  background: #3182ce;
  color: white;
}

.card-join button:hover:not(:disabled) {
  background: #2c5282;
}

/* Стили для модального окна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 40px;
  border-radius: 20px;
  text-align: center;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.modal h3 {
  font-size: 24px;
  margin-bottom: 16px;
  color: #1a365d;
}

.modal p {
  margin-bottom: 20px;
  color: #4a5568;
}

.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3182ce;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 20px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.cancel-btn {
  background: #e53e3e;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
  margin-top: 20px;
}

.cancel-btn:hover {
  background: #c53030;
}

@media (max-width: 768px) {
  .page {
    padding: 30px 16px;
  }
  
  h1 {
    font-size: 36px;
  }
  
  .header p {
    font-size: 18px;
  }
  
  .cards {
    flex-direction: column;
    align-items: center;
    gap: 30px;
  }
  
  .modal {
    padding: 30px 20px;
  }
}
</style>