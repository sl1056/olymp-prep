<template>
  <div class="match-settings-page">
    <div class="settings-header">
      <h1>НАСТРОЙКИ МАТЧА</h1>
      <p>Настройте параметры перед началом PvP-боя</p>
    </div>

    <div class="settings-container">
      <!-- Предметы -->
      <div class="setting-section">
        <h2>ПРЕДМЕТ</h2>
        <div class="subjects-grid">
          <button 
            v-for="subject in subjects" 
            :key="subject.id"
            :class="['subject-btn', { active: currentSubject === subject.id }]"
            @click="pickSubject(subject)"
          >
            <span class="subject-emoji">{{ subject.icon }}</span>
            <span class="subject-title">{{ subject.name }}</span>
          </button>
        </div>
      </div>

      <!-- Сложность -->
      <div class="setting-section">
        <h2>СЛОЖНОСТЬ</h2>
        <div class="difficulty-options">
          <button 
            v-for="diff in difficultyLevels" 
            :key="diff.id"
            :class="['diff-btn', { selected: currentDifficulty === diff.id }]"
            @click="setDifficulty(diff)"
          >
            <span class="diff-name">{{ diff.name }}</span>
            <span class="diff-hint">{{ diff.hint }}</span>
          </button>
        </div>
      </div>

      <!-- Опции -->
      <div class="setting-section">
        <h2>ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ</h2>
        <div class="options-list">
          <div class="option-row">
            <label class="option-checkbox">
              <input 
                type="checkbox" 
                v-model="options.timer" 
                @change="toggleTimer"
              />
              <span class="checkmark"></span>
              <span class="option-label-text">Таймер на ответ</span>
            </label>
            <span class="option-help" @click="showTimerHelp = !showTimerHelp">?</span>
          </div>
          
          <div class="option-row">
            <label class="option-checkbox">
              <input type="checkbox" v-model="options.hints" />
              <span class="checkmark"></span>
              <span class="option-label-text">Подсказки</span>
            </label>
          </div>
          
          <div class="option-row">
            <label class="option-checkbox">
              <input type="checkbox" v-model="options.random" />
              <span class="checkmark"></span>
              <span class="option-label-text">Случайный порядок</span>
            </label>
          </div>
          
          <div class="option-row">
            <label class="option-checkbox">
              <input type="checkbox" v-model="options.private" />
              <span class="checkmark"></span>
              <span class="option-label-text">Закрытый матч</span>
            </label>
            <span v-if="options.private" class="private-note">(только по приглашению)</span>
          </div>
        </div>
        
        <!-- Временная подсказка про таймер -->
        <div v-if="showTimerHelp" class="help-tooltip">
          При включенном таймере на каждый вопрос будет 10 минут
        </div>
      </div>

      <!-- Кнопки -->
      <div class="button-group">
        <button class="btn-back" @click="goBack">
          ← НАЗАД
        </button>
        <button 
          class="btn-start" 
          @click="createMatch"
          :disabled="!canStart"
          :class="{ loading: isStarting }"
        >
          {{ startButtonText }}
        </button>
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
  </div>
</template>

<script>
import axios from 'axios';
// Хардкод для предметов - в проде будет API
const subjectsData = [
  { id: 'math', name: 'Математика', icon: '∫' },
  { id: 'geometry', name: 'Геометрия', icon: '△' },
  { id: 'discrete_math', name: 'Дискретная математика', icon: '⊂' },
  { id: 'physics', name: 'Физика', icon: '⚛' },
  { id: 'chemistry', name: 'Химия', icon: '⚗' },
  { id: 'biology', name: 'Биология', icon: '🧬' },
  { id: 'ecology', name: 'Экология', icon: '🌿' },
  { id: 'geography', name: 'География', icon: '🌎' },
  { id: 'astronomy', name: 'Астрономия', icon: '🌌' },
  { id: 'russian', name: 'Русский язык', icon: '🇷🇺' },
  { id: 'literature', name: 'Литература', icon: '📚' },
  { id: 'english', name: 'Английский язык', icon: '🇬🇧' },
  { id: 'german', name: 'Немецкий язык', icon: '🇩🇪' },
  { id: 'french', name: 'Французский язык', icon: '🇫🇷' },
  { id: 'chinese', name: 'Китайский язык', icon: '🇨🇳' },
  { id: 'spanish', name: 'Испанский язык', icon: '🇪🇸' },
  { id: 'latin', name: 'Латинский язык', icon: '🏛' },
  { id: 'history', name: 'История', icon: '📜' },
  { id: 'social', name: 'Обществознание', icon: '👥' },
  { id: 'law', name: 'Право', icon: '⚖' },
  { id: 'economics', name: 'Экономика', icon: '📈' },
  { id: 'finance', name: 'Финансовая грамотность', icon: '💰' },
  { id: 'art', name: 'Искусство (МХК)', icon: '🎨' },
  { id: 'technology', name: 'Технология', icon: '🔧' },
  { id: 'informatics', name: 'Информатика', icon: '💻' },
  { id: 'robotics', name: 'Робототехника', icon: '🤖' },
  { id: 'ai', name: 'Искусственный интеллект', icon: '🧠' },
  { id: 'pe', name: 'Физкультура', icon: '⚽' },
  { id: 'safety', name: 'ОБЖ', icon: '🛡' },
  { id: 'all', name: 'Все предметы', icon: '🌟' }
]

export default {
  name: 'MatchSetup',
  
  data() {
    return {
      // Текущие выборы
      currentSubject: 'math',
      currentDifficulty: 'medium',
      userData: '',
      
      // Опции
      options: {
        timer: true,
        hints: false,
        random: true,
        private: false
      },
      
      // UI состояния
      showTimerHelp: false,
      isStarting: false,
      
      // Списки
      subjects: subjectsData,
      difficultyLevels: [
        { id: 'easy', name: 'Лёгкая', hint: 'для разминки' },
        { id: 'medium', name: 'Средняя', hint: 'обычная игра' },
        { id: 'hard', name: 'Сложная', hint: 'экспертный уровень' }
      ]
    }
  },

  async created() {
    await this.fetchUserData();
  },
  
  computed: {
    // Можно ли начинать
    canStart() {
      return !this.isStarting && this.currentSubject && this.currentDifficulty
    },
    
    // Текст кнопки
    startButtonText() {
      if (this.isStarting) return 'Создаём матч...'
      return 'НАЧАТЬ МАТЧ'
    },
    
    // Отладочная инфа
    debugInfo() {
      return {
        subject: this.currentSubject,
        difficulty: this.currentDifficulty,
        options: this.options,
        timestamp: new Date().toLocaleTimeString()
      }
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

    // Выбор предмета
    pickSubject(subject) {
      console.log('Выбрали предмет:', subject.name)
      this.currentSubject = subject.id
      
      // Костыль: для сложных предметов предлагаем среднюю сложность
      const hardSubjects = ['physics', 'informatics', 'discrete_math', 'ai', 'robotics', 'latin']
      if (hardSubjects.includes(subject.id) && this.currentDifficulty === 'easy') {
        this.currentDifficulty = 'medium'
      }
    },
    
    // Установка сложности
    setDifficulty(diff) {
      this.currentDifficulty = diff.id
      // TODO: отправка метрики в аналитику
    },
    
    // Включение/выключение таймера
    toggleTimer() {
      if (this.options.timer) {
        // Если включили таймер, выключаем подсказки (логика игры)
        this.options.hints = false
      }
    },
    
    // Назад
    goBack() {
      // Проверяем, были ли изменения
      const hasChanges = this.currentSubject !== 'math' || 
                        this.currentDifficulty !== 'medium' ||
                        !this.options.timer ||
                        !this.options.random
      
      if (hasChanges) {
        if (!confirm('Вернуться без сохранения настроек?')) {
          return
        }
      }
      
      this.$router.back()
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
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );
        
        this.matchId = response.data.match_id;
        this.matchCode = response.data.code;
        
        localStorage.setItem('currentMatchId', this.matchId);
        localStorage.setItem('currentMatchCode', this.matchCode);
        localStorage.setItem('currentMatchDifficulty', this.currentDifficulty);
        localStorage.setItem('currentMatchSubject', this.currentSubject);
        localStorage.setItem('matchRole', 'host');
        
        // 3. Переходим на страницу ожидания
        await this.$router.push('/PvP/create/wait');
        
        console.log('Матч создан:', response.data);
        
      } catch (error) {
        console.error('Ошибка при создании матча:', error);
        if (error.response) {
          console.error('Ответ сервера:', error.response.data);
        }
        alert('Не удалось создать матч. Попробуйте еще раз.');
      } finally {
        this.creatingMatch = false;
      }
    },
    
    // Заглушка для API
    fakeApiCall() {
      return new Promise(resolve => {
        setTimeout(() => {
          resolve()
        }, 500 + Math.random() * 500)
      })
    },
    
    // Получение ID пользователя (заглушка)
    getUserId() {
      return localStorage.getItem('user_id') || 'guest_' + Math.random().toString(36).substr(2, 5)
    },
    
    // Сброс настроек (для тестов)
    resetSettings() {
      this.currentSubject = 'math'
      this.currentDifficulty = 'medium'
      this.options = {
        timer: true,
        hints: false,
        random: true,
        private: false
      }
    }
  },
  
  // Хуки жизненного цикла
  mounted() {
    console.log('Компонент настроек матча загружен')
    
    // Попытка восстановить предыдущие настройки
    const saved = localStorage.getItem('last_match_settings')
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        this.currentSubject = parsed.subject || 'math'
        this.currentDifficulty = parsed.difficulty || 'medium'
      } catch (e) {
        // Игнорируем ошибки парсинга
      }
    }
  },
  
  beforeDestroy() {
    // Сохраняем настройки
    localStorage.setItem('last_match_settings', JSON.stringify({
      subject: this.currentSubject,
      difficulty: this.currentDifficulty,
      timestamp: Date.now()
    }))
  }
}
</script>

<style scoped>
.match-settings-page {
  min-height: 100vh;
  background: rgb(250, 246, 239);
  padding: 30px 15px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.settings-header {
  text-align: center;
  margin-bottom: 40px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.settings-header h1 {
  font-size: 36px;
  color: #1a365d;
  margin-bottom: 10px;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.settings-header p {
  font-size: 17px;
  color: #4a5568;
  line-height: 1.5;
  opacity: 0.9;
}

.settings-container {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 20px;
  padding: 35px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
}

.setting-section {
  margin-bottom: 45px;
}

.setting-section:last-of-type {
  margin-bottom: 30px;
}

.setting-section h2 {
  font-size: 24px;
  color: #2d3748;
  margin-bottom: 20px;
  font-weight: 700;
  padding-left: 12px;
  border-left: 4px solid #3182ce;
}

/* Стили для предметов */
.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 14px;
  max-height: 380px;
  overflow-y: auto;
  padding: 10px 5px;
  margin-bottom: 5px;
}

.subjects-grid::-webkit-scrollbar {
  width: 6px;
}

.subjects-grid::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.subject-btn {
  background: #f7fafc;
  border: 2px solid #e2e8f0;
  border-radius: 14px;
  padding: 18px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 100px;
  justify-content: center;
}

.subject-btn:hover {
  border-color: #3182ce;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(49, 130, 206, 0.1);
}

.subject-btn.active {
  background: linear-gradient(135deg, #ebf8ff, #bee3f8);
  border-color: #3182ce;
  box-shadow: 0 5px 15px rgba(49, 130, 206, 0.15);
}

.subject-emoji {
  font-size: 28px;
  margin-bottom: 10px;
  display: block;
}

.subject-title {
  font-size: 13px;
  font-weight: 600;
  color: #2d3748;
  text-align: center;
  line-height: 1.3;
}

/* Сложность */
.difficulty-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 18px;
}

.diff-btn {
  background: #f7fafc;
  border: 2px solid #e2e8f0;
  border-radius: 14px;
  padding: 22px 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.diff-btn:hover {
  border-color: #3182ce;
  transform: translateY(-2px);
}

.diff-btn.selected {
  background: linear-gradient(135deg, #ebf8ff, #e6fffa);
  border-color: #3182ce;
  box-shadow: 0 5px 15px rgba(49, 130, 206, 0.15);
}

.diff-name {
  font-size: 18px;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 5px;
}

.diff-hint {
  font-size: 13px;
  color: #718096;
  text-align: center;
}

/* Опции */
.options-list {
  display: grid;
  gap: 15px;
}

.option-row {
  display: flex;
  align-items: center;
  background: #f7fafc;
  border-radius: 10px;
  padding: 16px 20px;
  border: 1px solid #e2e8f0;
}

.option-checkbox {
  display: flex;
  align-items: center;
  cursor: pointer;
  flex-grow: 1;
}

.option-checkbox input {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid #cbd5e0;
  border-radius: 4px;
  margin-right: 12px;
  position: relative;
  transition: all 0.2s;
}

.option-checkbox input:checked + .checkmark {
  background: #3182ce;
  border-color: #3182ce;
}

.option-checkbox input:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  color: white;
  font-size: 12px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.option-label-text {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
}

.option-help {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #4a5568;
  cursor: help;
  margin-left: 10px;
  flex-shrink: 0;
}

.private-note {
  font-size: 12px;
  color: #718096;
  margin-left: 10px;
  font-style: italic;
}

.help-tooltip {
  background: #f0fff4;
  border: 1px solid #9ae6b4;
  border-radius: 8px;
  padding: 10px 15px;
  margin-top: 10px;
  font-size: 14px;
  color: #276749;
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Кнопки */
.button-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 40px;
  padding-top: 25px;
  border-top: 1px solid #e2e8f0;
}

.btn-back {
  background: #edf2f7;
  border: 2px solid #cbd5e0;
  border-radius: 10px;
  padding: 14px 25px;
  font-size: 15px;
  font-weight: 600;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-back:hover {
  background: #e2e8f0;
  border-color: #a0aec0;
}

.btn-start {
  background: #4a90e2;
  border: none;
  border-radius: 10px;
  padding: 15px 35px;
  font-size: 16px;
  font-weight: 700;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  letter-spacing: 0.3px;
  min-width: 160px;
}

.btn-start:hover:not(:disabled) {
  background: #417fc7;
  transform: translateY(-1px);
  box-shadow: 0 5px 20px rgba(74, 144, 226, 0.25);
}

.btn-start:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-start.loading {
  position: relative;
  color: transparent;
}

.btn-start.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 18px;
  height: 18px;
  border: 2px solid white;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Адаптивность */
@media (max-width: 768px) {
  .match-settings-page {
    padding: 20px 10px;
  }
  
  .settings-header h1 {
    font-size: 28px;
  }
  
  .settings-container {
    padding: 25px 20px;
    border-radius: 16px;
  }
  
  .setting-section h2 {
    font-size: 22px;
  }
  
  .subjects-grid {
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 12px;
    max-height: 320px;
  }
  
  .subject-btn {
    padding: 15px 8px;
    min-height: 90px;
  }
  
  .subject-emoji {
    font-size: 24px;
  }
  
  .subject-title {
    font-size: 12px;
  }
  
  .difficulty-options {
    grid-template-columns: 1fr;
  }
  
  .button-group {
    flex-direction: column;
    gap: 15px;
  }
  
  .btn-back,
  .btn-start {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .subjects-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .option-row {
    padding: 12px 15px;
  }
  
  .option-label-text {
    font-size: 14px;
  }
}

/* Костыль для старых браузеров */
@supports not (display: grid) {
  .subjects-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .subject-btn {
    width: 150px;
    margin: 5px;
  }
}
</style>
