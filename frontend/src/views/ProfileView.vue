<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import axios from 'axios'

const router = useRouter()

// Реактивные данные
const userData = ref(null)
const token = ref(null)
const isLoading = ref(true)
const userName = ref('')
const isModalOpen = ref(false)
const newName = ref('')

// Цветовая палитра для аватаров
const avatarColors = {
  'B': ['#FFD166', '#FF9E6D'],
  'A': ['#118AB2', '#06D6A0'],
  'M': ['#EF476F', '#FF9E6D'],
  'S': ['#4A7B9D', '#118AB2'],
  'D': ['#224762', '#4A7B9D'],
  'J': ['#06D6A0', '#118AB2'],
  'K': ['#FF9E6D', '#EF476F'],
  'P': ['#EF476F', '#FFD166'],
  'R': ['#118AB2', '#06D6A0'],
  'T': ['#4A7B9D', '#224762'],
  'default': ['#FFD166', '#FF9E6D']
}

// Вычисляемые свойства для аватара
const avatarStyle = computed(() => {
  const firstLetter = userName.value?.charAt(0)?.toUpperCase() || ''
  const colors = avatarColors[firstLetter] || avatarColors['default']
  
  return {
    background: `linear-gradient(135deg, ${colors[0]} 0%, ${colors[1]} 100%)`
  }
})

const avatarLetter = computed(() => {
  return userName.value?.charAt(0)?.toUpperCase() || '?'
})

// Методы
const openEditModal = () => {
  newName.value = userName.value
  isModalOpen.value = true
}

const closeEditModal = () => {
  isModalOpen.value = false
  newName.value = ''
}

const saveName = () => {
  const name = newName.value.trim()
  
  if (name.length < 2) {
    alert('Имя должно содержать минимум 2 символа')
    return
  }
  
  if (name.length > 20) {
    alert('Имя слишком длинное (максимум 20 символов)')
    return
  }
  
  userName.value = name
  closeEditModal()
}

const fetchUserData = async () => {
  try {
    const token = localStorage.getItem('authToken')
    if (!token) {
      router.push('/auth')
      return
    }

    const response = await axios.get('http://localhost:8000/api/auth/profile/')
    
    userData.value = response.data
    userName.value = response.data.username || ''
  } catch (err) {
    console.error('Ошибка при загрузке данных пользователя:', err)
  } finally {
    isLoading.value = false
  }
}

const logout = () => {
  // Очистка токена
  localStorage.removeItem('authToken')
  // Перенаправление на страницу логина
  router.push('/auth')
}

const profileLink = () => {
  router.push('/profile')
}

onMounted(() => {
  fetchUserData()
})
</script>

<template>
  <div>
      <header>
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/800px-NASA_logo.svg.png" height="88" width="108">
          <a class="header-a">sasa and<br>olympiad</a>
          <div className="buttons">
              <button class="header-button">Предметы</button>
              <button style="background-color: #7896AA" class="header-button">Меню</button>
              <button class="header-button">PvP</button>
          </div>
          <button className="header-enter_button" style="float: right;" @click="profileLink">{{ userData?.username }}</button>
      </header>
  </div>
  
  <div class="profile-page">
    <!-- Основная карточка профиля -->
    <div class="profile-card">
      <!-- Шапка профиля -->
      <div class="profile-header">
        <div class="avatar-container">
          <div class="avatar" :style="avatarStyle">
            {{ avatarLetter }}
          </div>
        </div>
        
        <div class="user-info">
          <div class="name-section">
            <h1 class="user-name">{{ userData?.username }}</h1>
            <button class="edit-btn" @click="openEditModal" title="Редактировать имя">
              <i class="fas fa-edit"></i>
            </button>
          </div>
          <div class="user-id">ID: 2562341</div>
        </div>
      </div>
      
      <!-- Основной контент -->
      <div class="profile-content">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-number">91</div>
            <div class="stat-label">Выполнено тестов</div>
          </div>
          
          <div class="stat-card">
            <div class="stat-number percentage">87%</div>
            <div class="stat-label">Правильных тестов</div>
          </div>
          
          <div class="stat-card">
            <div class="stat-number">181</div>
            <div class="stat-label">Сражений в PvP</div>
          </div>
        </div>
        
        <div class="info-section">
          <div class="info-item">
            <div class="info-icon">
              <i class="fas fa-envelope"></i>
            </div>
            <div class="info-content">
              <div class="info-label">Email</div>
              <div class="info-value">{{userData?.email}}</div>
            </div>
          </div>
          
          <div class="info-item">
            <div class="info-icon">
              <i class="fas fa-calendar-alt"></i>
            </div>
            <div class="info-content">
              <div class="info-label">Дата регистрации</div>
              <div class="info-value">15 января 2023</div>
            </div>
          </div>
        </div>
        
        <button class="logout-btn" @click="logout">
          <i class="fas fa-sign-out-alt"></i> Выйти
        </button>
      </div>
    </div>

    <!-- Модальное окно редактирования имени -->
    <div class="modal-overlay" v-if="isModalOpen" @click.self="closeEditModal">
      <div class="modal">
        <h2>Изменить имя</h2>
        <p>Введите новое имя пользователя</p>
        
        <div class="form-group">
          <input 
            type="text" 
            class="form-input" 
            v-model="newName"
            maxlength="20" 
            placeholder="Введите имя..."
            @keyup.enter="saveName"
          >
          <div class="char-counter">{{ newName.length }}/20</div>
        </div>
        
        <div class="modal-buttons">
          <button class="modal-btn secondary" @click="closeEditModal">Отмена</button>
          <button class="modal-btn primary" @click="saveName">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
html, body {
  overflow-x: hidden;
  width: 100%;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', system-ui, sans-serif; 
}

.profile-page {
  background: #FAF6EF;
  min-height: calc(100vh - 160px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 30px;
  margin-top: -4%;
  /* Добавил это */
  width: 100%;
  overflow: hidden;
}

.profile-card {
  background: white;
  border-radius: 24px;
  width: 100%;
  max-width: 900px;
  box-shadow: 0 20px 50px rgba(34, 71, 98, 0.12);
  overflow: hidden;
  border: 1px solid #E8E2D8;
}

/* Шапка профиля */
.profile-header {
  background: #224762;
  padding: 50px 70px;
  text-align: center;
  color: white;
  position: relative;
}

.avatar-container {
  display: inline-block;
  margin-bottom: 25px;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 42px;
  font-weight: bold;
  color: #224762;
  border: 4px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  margin: 0 auto;
  /* ДОБАВИЛ ШРИФТ НА АВАТАР */
  font-family: 'Alexandria', sans-serif;
}

.user-info {
  margin-top: 20px;
}

.name-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 15px;
}

.user-name {
  font-size: 36px;
  font-weight: 700;
  margin: 0;
  color: white;
  /* ШРИФТ КАК В ПРИМЕРЕ */
  font-family: 'Alexandria', sans-serif;
}

.edit-btn {
  background: rgba(255, 255, 255, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  background: white;
  color: #224762;
  transform: scale(1.1);
}

.user-id {
  font-size: 16px;
  opacity: 0.85;
  font-weight: 300;
  letter-spacing: 0.5px;
  color: rgba(255, 255, 255, 0.9);
  /* ШРИФТ КАК В ПРИМЕРЕ */
  font-family: 'Inter', sans-serif;
}

/* Основной контент */
.profile-content {
  padding: 50px 70px;
  background: #FAF6EF;
  /* ОСНОВНОЙ ШРИФТ КАК В ПРИМЕРЕ */
  font-family: 'Inter', sans-serif;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  border-radius: 18px;
  padding: 30px;
  text-align: center;
  border: 1px solid #E8E2D8;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(34, 71, 98, 0.12);
  border-color: #4A7B9D;
}

.stat-number {
  font-size: 34px;
  font-weight: 700;
  color: #224762;
  margin-bottom: 10px;
  /* ШРИФТ КАК В ПРИМЕРЕ */
  font-family: 'Alexandria', sans-serif;
}

.percentage {
  color: #06D6A0;
  font-size: 36px;
  /* ШРИФТ КАК В ПРИМЕРЕ */
  font-family: 'Alexandria', sans-serif;
}

.stat-label {
  font-size: 16px;
  color: #5A6C7D;
  font-weight: 500;
  /* ШРИФТ КАК В ПРИМЕРЕ */
  font-family: 'Inter', sans-serif;
}

/* Информация профиля */
.info-section {
  background: white;
  border-radius: 18px;
  padding: 35px;
  margin-bottom: 40px;
  border: 1px solid #E8E2D8;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #F0EBE2;
}

.info-item:last-child {
  border-bottom: none;
}

.info-icon {
  width: 44px;
  height: 44px;
  background: #EFF7FF;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  color: #224762;
  font-size: 18px;
}

.info-content {
  flex: 1;
}

.info-label {
  font-size: 14px;
  color: #7A8A9B;
  margin-bottom: 5px;
  /* ШРИФТ КАК В ПРИМЕРЕ */
  font-family: 'Inter', sans-serif;
}

.info-value {
  font-size: 18px;
  font-weight: 600;
  color: #2C3E50;
  /* ШРИФТ КАК В ПРИМЕРЕ */
  font-family: 'Alexandria', sans-serif;
}

/* Кнопка выхода */
.logout-btn {
  width: 100%;
  padding: 20px;
  background: #EF476F;
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  transition: all 0.3s ease;
  font-family: 'Anonymous Pro', monospace;
}

.logout-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(239, 71, 111, 0.3);
  background: #D43A5F;
}

/* Модальное окно */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(34, 71, 98, 0.7);
  backdrop-filter: blur(5px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

.modal {
  background: white;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 30px 60px rgba(34, 71, 98, 0.15);
  animation: slideUp 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.modal h2 {
  color: #224762;
  margin-bottom: 20px;
  text-align: center;
  font-size: 28px;
  font-weight: 600;
  font-family: 'Alexandria', sans-serif;
}

.modal p {
  color: #5A6C7D;
  text-align: center;
  margin-bottom: 30px;
  line-height: 1.5;
  font-size: 16px;
  /* ШРИФТ КАК В ПРИМЕРЕ */
  font-family: 'Inter', sans-serif;
}

.form-group {
  margin-bottom: 25px;
  position: relative;
}

.form-input {
  width: 100%;
  padding: 18px;
  border: 2px solid #E8E2D8;
  border-radius: 12px;
  font-size: 16px;
  color: #2C3E50;
  transition: border-color 0.3s ease;
  background: #FAF6EF;
  font-family: 'Inter', sans-serif;
}

.form-input:focus {
  outline: none;
  border-color: #4A7B9D;
  box-shadow: 0 0 0 3px rgba(74, 123, 157, 0.1);
  background: white;
}

.char-counter {
  text-align: right;
  font-size: 12px;
  color: #7A8A9B;
  margin-top: 5px;
  /* ШРИФТ КАК В ПРИМЕРЕ */
  font-family: 'Inter', sans-serif;
}

.modal-buttons {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.modal-btn {
  flex: 1;
  padding: 16px;
  border-radius: 12px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
  font-family: 'Alexandria', sans-serif;
}

.modal-btn.primary {
  background: #224762;
  color: white;
}

.modal-btn.primary:hover {
  transform: translateY(-2px);
  background: #1B3A50;
}

.modal-btn.secondary {
  background: #FAF6EF;
  color: #5A6C7D;
  border: 2px solid #E8E2D8;
}

.modal-btn.secondary:hover {
  background: #F0EBE2;
}
</style>
