<template>
  <div class="results-page">
    <div class="results-container">
      
      <!-- Шапка с результатами -->
      <div class="results-header">
        <div class="subject-info">
          <span class="subject-name">{{ subject.name }}</span>
          <span class="difficulty-badge" :class="difficulty.id">
            {{ difficulty.name }}
          </span>
        </div>
      </div>

      <!-- Основная статистика -->
      <div class="stats-card">
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-label">Всего заданий</span>
            <span class="stat-value">{{ results.totalTasks }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Сохранено ответов</span>
            <span class="stat-value">{{ results.savedAnswers }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Без ответа</span>
            <span class="stat-value">{{ results.totalTasks - results.savedAnswers }}</span>
          </div>
        </div>
      </div>

      <!-- Прогресс-бар -->
      <div class="progress-section">
        <div class="progress-label">
          <span>Завершено</span>
          <span class="progress-percent">{{ Math.round((results.savedAnswers / results.totalTasks) * 100) }}%</span>
        </div>
        <div class="progress-bar-container">
          <div 
            class="progress-bar" 
            :style="{ width: (results.savedAnswers / results.totalTasks) * 100 + '%' }"
          ></div>
        </div>
      </div>

      <!-- Детальная информация -->
      <div class="details-card">
        <h3 class="details-title">Детали тренировки</h3>
        
        <div class="details-list">
          <div class="detail-row">
            <span class="detail-label">Дата и время:</span>
            <span class="detail-value">{{ formattedDate }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Предмет:</span>
            <span class="detail-value">{{ subject.name }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Уровень сложности:</span>
            <span class="detail-value difficulty-text" :class="difficulty.id">
              {{ difficulty.name }}
            </span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Количество заданий:</span>
            <span class="detail-value">{{ results.totalTasks }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Сохранено ответов:</span>
            <span class="detail-value">{{ results.savedAnswers }}</span>
          </div>
        </div>
      </div>

      <!-- Кнопки действий -->
      <div class="actions-section">
        <button class="again-btn" @click="startNewTraining">
          Новая тренировка
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResultsPage',
  
  data() {
    return {
      results: {
        subject: 'math',
        difficulty: 'medium',
        totalTasks: 0,
        savedAnswers: 0,
        timestamp: null
      },
      
      subjects: {
        math: { id: 'math', name: 'МАТЕМАТИКА', emoji: '📐' },
        physics: { id: 'physics', name: 'ФИЗИКА', emoji: '⚛️' },
        chemistry: { id: 'chemistry', name: 'ХИМИЯ', emoji: '🧪' },
        biology: { id: 'biology', name: 'БИОЛОГИЯ', emoji: '🧬' },
        russian: { id: 'russian', name: 'РУССКИЙ ЯЗЫК', emoji: '📝' },
        english: { id: 'english', name: 'АНГЛИЙСКИЙ ЯЗЫК', emoji: '🇬🇧' },
        history: { id: 'history', name: 'ИСТОРИЯ', emoji: '🏺' },
        informatics: { id: 'informatics', name: 'ИНФОРМАТИКА', emoji: '💻' }
      },
      
      difficultyLevels: {
        easy: { id: 'easy', name: 'ЛЁГКАЯ' },
        medium: { id: 'medium', name: 'СРЕДНЯЯ' },
        hard: { id: 'hard', name: 'СЛОЖНАЯ' }
      }
    }
  },
  
  computed: {
    subject() {
      return this.subjects[this.results.subject] || this.subjects.math
    },
    
    difficulty() {
      return this.difficultyLevels[this.results.difficulty] || this.difficultyLevels.medium
    },
    
    formattedDate() {
      if (!this.results.timestamp) return '—'
      
      const date = new Date(this.results.timestamp)
      const day = date.getDate().toString().padStart(2, '0')
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const year = date.getFullYear()
      const hours = date.getHours().toString().padStart(2, '0')
      const minutes = date.getMinutes().toString().padStart(2, '0')
      
      return `${day}.${month}.${year} ${hours}:${minutes}`
    }
  },
  
  created() {
    this.loadResults()
  },
  
  methods: {
    loadResults() {
      const savedResults = localStorage.getItem('trainingResults')
      if (savedResults) {
        this.results = JSON.parse(savedResults)
      } else {
        // Если нет результатов, перенаправляем на настройки
        this.$router.push('/task-setup')
      }
    },
    
    startNewTraining() {
      this.$router.push('/training/start')
    },
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.results-page {
  min-height: 100vh;
  background: rgb(250, 246, 239);
  display: flex;
  justify-content: center;
  padding: 40px 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.results-container {
  max-width: 700px;
  width: 100%;
}

/* Шапка с предметом и уровнем */
.results-header {
  background: white;
  border-radius: 15px;
  padding: 25px 35px;
  margin-bottom: 30px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.subject-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.subject-name {
  font-size: 28px;
  font-weight: 800;
  color: #000000;
  letter-spacing: 0.5px;
}

.difficulty-badge {
  padding: 12px 28px;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 1px;
  border: 3px solid;
}

.difficulty-badge.easy {
  background: #e8f5e9;
  color: #43a047;
  border-color: #43a047;
}

.difficulty-badge.medium {
  background: #fff3e0;
  color: #fb8c00;
  border-color: #fb8c00;
}

.difficulty-badge.hard {
  background: #ffebee;
  color: #e53935;
  border-color: #e53935;
}

/* Карточка со статистикой */
.stats-card {
  background: white;
  border-radius: 15px;
  padding: 30px 35px;
  margin-bottom: 25px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stat-label {
  font-size: 14px;
  font-weight: 600;
  color: #5f6368;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: 800;
  color: #1e88e5;
}

/* Прогресс-бар */
.progress-section {
  background: white;
  border-radius: 15px;
  padding: 25px 35px;
  margin-bottom: 25px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.progress-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 16px;
  font-weight: 600;
  color: #263238;
}

.progress-percent {
  color: #1e88e5;
  font-weight: 800;
}

.progress-bar-container {
  width: 100%;
  height: 10px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(135deg, #1e88e5, #1565c0);
  border-radius: 10px;
  transition: width 0.3s ease;
}

/* Детальная информация */
.details-card {
  background: white;
  border-radius: 15px;
  padding: 30px 35px;
  margin-bottom: 30px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.details-title {
  font-size: 18px;
  font-weight: 800;
  color: #000000;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #cfd8dc;
}

.details-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.detail-label {
  font-size: 15px;
  font-weight: 600;
  color: #5f6368;
}

.detail-value {
  font-size: 16px;
  font-weight: 600;
  color: #263238;
}

.difficulty-text {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
}

.difficulty-text.easy {
  background: #e8f5e9;
  color: #43a047;
}

.difficulty-text.medium {
  background: #fff3e0;
  color: #fb8c00;
}

.difficulty-text.hard {
  background: #ffebee;
  color: #e53935;
}

/* Кнопки действий */
.actions-section {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.again-btn, .back-btn {
  padding: 16px 32px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  flex: 1;
  max-width: 250px;
}

.again-btn {
  background: linear-gradient(135deg, #1e88e5, #1565c0);
  color: white;
}

.again-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 136, 229, 0.4);
}

.back-btn {
  background: #263238;
  color: white;
}

.back-btn:hover {
  background: #37474f;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Адаптивность */
@media (max-width: 768px) {
  .results-page {
    padding: 20px 15px;
  }
  
  .results-header {
    padding: 20px 25px;
  }
  
  .subject-info {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .subject-name {
    font-size: 24px;
  }
  
  .stats-card,
  .progress-section,
  .details-card {
    padding: 25px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .stat-item {
    flex-direction: row;
    justify-content: space-between;
    padding: 10px 0;
  }
  
  .stat-label {
    margin-bottom: 0;
  }
  
  .actions-section {
    flex-direction: column;
    align-items: center;
  }
  
  .again-btn, .back-btn {
    max-width: none;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .results-header {
    padding: 15px 20px;
  }
  
  .subject-name {
    font-size: 22px;
  }
  
  .difficulty-badge {
    padding: 10px 20px;
    font-size: 14px;
  }
  
  .detail-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
}
</style>
