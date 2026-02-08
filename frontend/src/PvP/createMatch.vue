<template>
  <div class="match-settings-page">
    <div class="settings-header">
      <h1>НАСТРОЙКИ МАТЧА</h1>
      <p>Настройте параметры перед началом PvP-боя</p>
    </div>

    <div class="settings-container">
      <div class="setting-section">
        <h2>ПРЕДМЕТ</h2>
        <div class="subjects-grid">
          <button 
            v-for="subject in subjectList" 
            :key="subject.id"
            :class="['subject-card', { active: selectedSubjectId === subject.id }]"
            @click="handleSubjectSelect(subject.id)"
          >
            <span class="subject-icon">{{ subject.icon }}</span>
            <span class="subject-name">{{ subject.name }}</span>
          </button>
        </div>
      </div>

      <div class="setting-section">
        <h2>СЛОЖНОСТЬ</h2>
        <div class="difficulty-grid">
          <button 
            v-for="level in difficultyOptions" 
            :key="level.id"
            :class="['difficulty-card', { active: selectedDifficultyLevel === level.id }]"
            @click="handleDifficultySelect(level.id)"
          >
            <span class="difficulty-name">{{ level.name }}</span>
            <span class="difficulty-desc">{{ level.description }}</span>
          </button>
        </div>
      </div>

      <div class="setting-section">
        <h2>ВЫБЕРИТЕ</h2>
        <div class="options-grid">
          <div class="option-item">
            <label class="option-label">
              <input type="checkbox" v-model="matchSettings.timerEnabled" />
              <span class="option-text">Таймер на ответ</span>
            </label>
          </div>
          <div class="option-item">
            <label class="option-label">
              <input type="checkbox" v-model="matchSettings.showHints" />
              <span class="option-text">Подсказки</span>
            </label>
          </div>
          <div class="option-item">
            <label class="option-label">
              <input type="checkbox" v-model="matchSettings.randomOrder" />
              <span class="option-text">Случайный порядок</span>
            </label>
          </div>
          <div class="option-item">
            <label class="option-label">
              <input type="checkbox" v-model="matchSettings.privateMatch" />
              <span class="option-text">Закрытый матч</span>
            </label>
          </div>
        </div>
      </div>

      <div class="actions-section">
        <button class="back-button" @click="handleBack">
          ← НАЗАД
        </button>
        <button class="start-button" @click="handleStartMatch">
          НАЧАТЬ МАТЧ
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MatchSettings',
  
  data() {
    return {
      selectedSubjectId: 'math',
      selectedDifficultyLevel: 'medium',
      matchSettings: {
        timerEnabled: true,
        showHints: false,
        randomOrder: true,
        privateMatch: false
      },
      subjectList: [
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
      ],
      difficultyOptions: [
        { id: 'easy', name: 'Лёгкая', description: 'Для новичков' },
        { id: 'medium', name: 'Средняя', description: 'Базовый уровень' },
        { id: 'hard', name: 'Сложная', description: 'Олимпиадный уровень' },
      ]
    }
  },
  
  methods: {
    handleSubjectSelect(subjectId) {
      this.selectedSubjectId = subjectId
    },
    
    handleDifficultySelect(difficultyId) {
      this.selectedDifficultyLevel = difficultyId
    },
    
    handleBack() {
      this.$router.back()
    },
    
    handleStartMatch() {
      const matchData = {
        subject: this.selectedSubjectId,
        difficulty: this.selectedDifficultyLevel,
        settings: this.matchSettings
      }
      
      console.log('Настройки матча:', matchData)
      this.$router.push('/PvP/create/wait')
    }
  }
}
</script>

<style>
.match-settings-page {
  min-height: 100vh;
  background: rgb(250, 246, 239);
  padding: 40px 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.settings-header {
  text-align: center;
  margin-bottom: 50px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.settings-header h1 {
  font-size: 42px;
  color: #1a365d;
  margin-bottom: 16px;
  font-weight: 800;
  letter-spacing: 1px;
}

.settings-header p {
  font-size: 18px;
  color: #4a5568;
  line-height: 1.5;
}

.settings-container {
  max-width: 1100px;
  margin: 0 auto;
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
}

.setting-section {
  margin-bottom: 50px;
}

.setting-section h2 {
  font-size: 28px;
  color: #2d3748;
  margin-bottom: 25px;
  font-weight: 700;
  border-left: 4px solid #3182ce;
  padding-left: 15px;
}

.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 15px;
  max-height: 500px;
  overflow-y: auto;
  padding: 10px;
  margin-bottom: 10px;
}

.subject-card {
  background: #f7fafc;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 120px;
  justify-content: center;
}

.subject-card:hover {
  transform: translateY(-3px);
  border-color: #3182ce;
  box-shadow: 0 8px 20px rgba(49, 130, 206, 0.15);
}

.subject-card.active {
  background: linear-gradient(135deg, #ebf8ff, #e6fffa);
  border-color: #3182ce;
  box-shadow: 0 8px 20px rgba(49, 130, 206, 0.2);
}

.subject-card.active:nth-child(odd) {
  background: linear-gradient(135deg, #ebf8ff, #d6f5ff);
}

.subject-icon {
  font-size: 32px;
  margin-bottom: 10px;
  display: block;
  min-height: 40px;
  display: flex;
  align-items: center;
}

.subject-name {
  font-size: 14px;
  font-weight: 600;
  color: #2d3748;
  text-align: center;
  line-height: 1.3;
}

.difficulty-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.difficulty-card {
  background: #f7fafc;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 25px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.difficulty-card:hover {
  transform: translateY(-3px);
  border-color: #3182ce;
  box-shadow: 0 8px 20px rgba(49, 130, 206, 0.15);
}

.difficulty-card.active {
  background: linear-gradient(135deg, #ebf8ff, #e6fffa);
  border-color: #3182ce;
  box-shadow: 0 8px 20px rgba(49, 130, 206, 0.2);
}

.difficulty-name {
  font-size: 20px;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 8px;
}

.difficulty-desc {
  font-size: 14px;
  color: #718096;
  text-align: center;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.option-item {
  background: #f7fafc;
  border-radius: 12px;
  padding: 20px;
}

.option-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.option-label input {
  width: 20px;
  height: 20px;
  margin-right: 12px;
  cursor: pointer;
  accent-color: #3182ce;
}

.option-text {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
}

.actions-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 50px;
  padding-top: 30px;
  border-top: 1px solid #e2e8f0;
}

.back-button {
  background: #edf2f7;
  border: 2px solid #cbd5e0;
  border-radius: 12px;
  padding: 16px 30px;
  font-size: 16px;
  font-weight: 600;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button:hover {
  background: #e2e8f0;
  border-color: #a0aec0;
}

.start-button {
  background: #4a90e2;
  border: none;
  border-radius: 12px;
  padding: 18px 40px;
  font-size: 18px;
  font-weight: 700;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
}

.start-button:hover {
  background: #417fc7;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(74, 144, 226, 0.3);
}

@media (max-width: 768px) {
  .match-settings-page {
    padding: 20px 15px;
  }
  
  .settings-header h1 {
    font-size: 32px;
  }
  
  .settings-container {
    padding: 25px 20px;
  }
  
  .setting-section h2 {
    font-size: 24px;
  }
  
  .subjects-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
    max-height: 400px;
  }
  
  .subject-card {
    padding: 15px 10px;
    min-height: 100px;
  }
  
  .subject-icon {
    font-size: 28px;
  }
  
  .subject-name {
    font-size: 13px;
  }
  
  .difficulty-grid,
  .options-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-section {
    flex-direction: column;
    gap: 20px;
  }
  
  .back-button,
  .start-button {
    width: 100%;
  }
}
</style>
