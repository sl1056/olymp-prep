<template>
  <div class="task-setup-page">
    <div class="settings-header">
      <h1>НАСТРОЙКА ТРЕНИРОВКИ</h1>
      <p>Выберите предмет, сложность и количество заданий</p>
    </div>

    <div class="settings-container">
      <!-- Предметы -->
      <div class="setting-section">
        <h2>ПРЕДМЕТ</h2>
        <div class="subjects-grid">
          <button 
            v-for="subject in subjects" 
            :key="subject.id"
            :class="['subject-btn', { active: selectedSubject === subject.id }]"
            @click="selectedSubject = subject.id"
          >
            <span class="subject-emoji">{{ subject.emoji }}</span>
            <span class="subject-title">{{ subject.name }}</span>
          </button>
        </div>
      </div>

      <!-- Сложность -->
      <div class="setting-section">
        <h2>СЛОЖНОСТЬ</h2>
        <div class="difficulty-options">
          <button 
            v-for="level in difficultyLevels" 
            :key="level.id"
            :class="['diff-btn', { selected: selectedDifficulty === level.id }]"
            @click="selectedDifficulty = level.id"
          >
            <span class="diff-name">{{ level.name }}</span>
            <span class="diff-hint">{{ level.hint }}</span>
          </button>
        </div>
      </div>

      <!-- Количество заданий -->
      <div class="setting-section">
        <h2>КОЛИЧЕСТВО ЗАДАНИЙ</h2>
        
        <div class="quantity-wrapper">
          <div class="quantity-controls">
            <button class="quantity-btn" @click="decreaseQuantity">−</button>
            <div class="quantity-display">
              <span class="quantity-number">{{ taskQuantity }}</span>
            </div>
            <button class="quantity-btn" @click="increaseQuantity">+</button>
          </div>
          
          <div class="preset-buttons">
            <button 
              v-for="preset in quantityPresets" 
              :key="preset"
              :class="['preset-chip', { active: taskQuantity === preset }]"
              @click="taskQuantity = preset"
            >
              {{ preset }}
            </button>
          </div>
        </div>
        
        <div class="quantity-hint">
          <span>Максимум: 50 заданий</span>
        </div>
      </div>

      <!-- Кнопки -->
      <div class="button-group">
        <button class="btn-back" @click="goBack">
          ← НАЗАД
        </button>
        <button 
          class="btn-start" 
          @click="startTraining"
          :class="{ loading: isStarting }"
        >
          {{ startButtonText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TaskSetup",
  data() {
    return {
      subjects: [
        // Точные науки
        { id: 'math', name: 'Математика', emoji: '∫' },
        { id: 'geometry', name: 'Геометрия', emoji: '△' },
        { id: 'discrete-math', name: 'Дискретная математика', emoji: '⊂' },
        { id: 'physics', name: 'Физика', emoji: '⚛' },
        { id: 'chemistry', name: 'Химия', emoji: '⚗' },
        
        // Естественные науки
        { id: 'biology', name: 'Биология', emoji: '🧬' },
        { id: 'ecology', name: 'Экология', emoji: '🌿' },
        { id: 'geography', name: 'География', emoji: '🌎' },
        { id: 'astronomy', name: 'Астрономия', emoji: '🌌' },
        
        // Языки
        { id: 'russian', name: 'Русский язык', emoji: '🇷🇺' },
        { id: 'literature', name: 'Литература', emoji: '📚' },
        { id: 'english', name: 'Английский язык', emoji: '🇬🇧' },
        { id: 'german', name: 'Немецкий язык', emoji: '🇩🇪' },
        { id: 'french', name: 'Французский язык', emoji: '🇫🇷' },
        { id: 'chinese', name: 'Китайский язык', emoji: '🇨🇳' },
        { id: 'spanish', name: 'Испанский язык', emoji: '🇪🇸' },
        { id: 'latin', name: 'Латинский язык', emoji: '🏛' },
        
        // Гуманитарные науки
        { id: 'history', name: 'История', emoji: '📜' },
        { id: 'social', name: 'Обществознание', emoji: '👥' },
        { id: 'law', name: 'Право', emoji: '⚖' },
        { id: 'economics', name: 'Экономика', emoji: '📈' },
        { id: 'finlit', name: 'Финансовая грамотность', emoji: '💰' },
        
        // Творчество и технологии
        { id: 'art', name: 'Искусство (МХК)', emoji: '🎨' },
        { id: 'technology', name: 'Технология', emoji: '🔧' },
        { id: 'informatics', name: 'Информатика', emoji: '💻' },
        { id: 'robotics', name: 'Робототехника', emoji: '🤖' },
        { id: 'ai', name: 'Искусственный интеллект', emoji: '🧠' },
        
        // Другое
        { id: 'sport', name: 'Физкультура', emoji: '⚽' },
        { id: 'safety', name: 'ОБЖ', emoji: '🛡' }
      ],
      selectedSubject: 'math',

      difficultyLevels: [
        { id: 'random', name: 'Любая', hint: 'все уровни подряд' },
        { id: 'easy', name: 'Лёгкая', hint: 'для разминки' },
        { id: 'medium', name: 'Средняя', hint: 'обычная тренировка' },
        { id: 'hard', name: 'Сложная', hint: 'экспертный уровень' }
      ],
      selectedDifficulty: 'random',

      taskQuantity: 10,
      quantityPresets: [5, 10, 15, 20, 25, 30, 40, 50],
      isStarting: false
    };
  },
  computed: {
    startButtonText() {
      if (this.isStarting) return 'Запуск...';
      return 'НАЧАТЬ ТРЕНИРОВКУ';
    }
  },
  methods: {
    increaseQuantity() {
      if (this.taskQuantity < 50) {
        this.taskQuantity++;
      }
    },
    decreaseQuantity() {
      if (this.taskQuantity > 1) {
        this.taskQuantity--;
      }
    },
    async startTraining() {
      this.isStarting = true;
      
      try {
        const trainingConfig = {
          subject: this.selectedSubject,
          difficulty: this.selectedDifficulty,
          quantity: this.taskQuantity
        };
        
        localStorage.setItem('trainingConfig', JSON.stringify(trainingConfig));
        
        // Имитация загрузки
        await new Promise(resolve => setTimeout(resolve, 500));
        
        this.$router.push('/training/study');
      } catch (error) {
        console.error('Ошибка при запуске тренировки:', error);
      } finally {
        this.isStarting = false;
      }
    },
    goBack() {
      const hasChanges = this.selectedSubject !== 'math' || 
                        this.selectedDifficulty !== 'random' ||
                        this.taskQuantity !== 10;
      
      if (hasChanges) {
        if (!confirm('Вернуться без сохранения настроек?')) {
          return;
        }
      }
      
      this.$router.back();
    }
  },
  mounted() {
    console.log('Компонент настроек тренировки загружен');
    
    // Восстанавливаем предыдущие настройки
    const saved = localStorage.getItem('last_training_settings');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        this.selectedSubject = parsed.subject || 'math';
        this.selectedDifficulty = parsed.difficulty || 'random';
        this.taskQuantity = parsed.quantity || 10;
      } catch (e) {
        // Игнорируем ошибки парсинга
      }
    }
  },
  beforeDestroy() {
    // Сохраняем настройки
    localStorage.setItem('last_training_settings', JSON.stringify({
      subject: this.selectedSubject,
      difficulty: this.selectedDifficulty,
      quantity: this.taskQuantity,
      timestamp: Date.now()
    }));
  }
};
</script>

<style scoped>
.task-setup-page {
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
  border-left: 4px solid #4a90e2;
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

.subjects-grid::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
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
  border-color: #4a90e2;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(74, 144, 226, 0.1);
}

.subject-btn.active {
  background: linear-gradient(135deg, #ebf8ff, #bee3f8);
  border-color: #4a90e2;
  box-shadow: 0 5px 15px rgba(74, 144, 226, 0.15);
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
  position: relative;
  overflow: hidden;
}

.diff-btn:hover {
  border-color: #4a90e2;
  transform: translateY(-2px);
}

.diff-btn.selected {
  background: linear-gradient(135deg, #ebf8ff, #e6fffa);
  border-color: #4a90e2;
  box-shadow: 0 5px 15px rgba(74, 144, 226, 0.15);
}

/* Специальный стиль для любой сложности (рандом) - теперь по умолчанию */
.diff-btn.selected[class*="random"] {
  background: linear-gradient(135deg, #f0e7ff, #e9d8fd);
  border-color: #805ad5;
  box-shadow: 0 5px 15px rgba(128, 90, 213, 0.2);
}

.diff-btn.selected[class*="random"] .diff-name {
  color: #6b46c1;
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

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}

/* Количество заданий */
.quantity-wrapper {
  background: #f7fafc;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e2e8f0;
}

.quantity-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 24px;
}

.quantity-btn {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  background: white;
  font-size: 24px;
  font-weight: 600;
  color: #4a90e2;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.quantity-btn:hover {
  background: #4a90e2;
  border-color: #4a90e2;
  color: white;
  transform: scale(1.05);
}

.quantity-btn:active {
  transform: scale(0.95);
}

.quantity-display {
  background: white;
  padding: 8px 28px;
  border-radius: 60px;
  border: 2px solid #e2e8f0;
  min-width: 100px;
  text-align: center;
}

.quantity-number {
  font-size: 36px;
  font-weight: 700;
  color: #2d3748;
}

.preset-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.preset-chip {
  padding: 8px 20px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 60px;
  font-size: 15px;
  font-weight: 600;
  color: #2d3748;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 60px;
  text-align: center;
}

.preset-chip:hover {
  border-color: #4a90e2;
  background: #ebf8ff;
  transform: translateY(-2px);
}

.preset-chip.active {
  background: #4a90e2;
  border-color: #4a90e2;
  color: white;
}

.quantity-hint {
  margin-top: 16px;
  text-align: right;
  font-size: 14px;
  color: #718096;
  font-style: italic;
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
  min-width: 200px;
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
  .task-setup-page {
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
  
  .quantity-number {
    font-size: 32px;
  }
  
  .quantity-btn {
    width: 44px;
    height: 44px;
  }
  
  .preset-chip {
    padding: 6px 16px;
    font-size: 14px;
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
  
  .quantity-wrapper {
    padding: 16px;
  }
  
  .quantity-display {
    padding: 6px 20px;
    min-width: 80px;
  }
  
  .quantity-number {
    font-size: 28px;
  }
  
  .preset-buttons {
    gap: 8px;
  }
  
  .preset-chip {
    padding: 6px 12px;
    font-size: 13px;
    min-width: 50px;
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
  
  .difficulty-options {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .diff-btn {
    width: 180px;
    margin: 5px;
  }
  
  .preset-buttons {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
