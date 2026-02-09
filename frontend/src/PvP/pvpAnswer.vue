<template>
  <div class="task-answer-section">
    <div class="main-container">
      <div class="left-panel">
        <div class="panel-content">
          <div class="player-card you">
            <div class="player-header">
              <div class="avatar-circle">В</div>
              <div class="player-details">
                <div class="player-name">Вы</div>
                <div class="player-score">{{ yourScore }}/10</div>
              </div>
            </div>
            <div class="progress-info">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: yourProgress + '%' }"></div>
              </div>
              <div class="progress-text">{{ yourProgress }}%</div>
            </div>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-icon correct">✓</div>
                <div class="stat-value">{{ answeredCorrectly }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-icon total">?</div>
                <div class="stat-value">{{ answeredQuestions }}/10</div>
              </div>
            </div>
          </div>

          <div class="player-card opponent">
            <div class="player-header">
              <div class="avatar-circle">С</div>
              <div class="player-details">
                <div class="player-name">Соперник</div>
                <div class="player-score">{{ opponentScore }}/10</div>
              </div>
            </div>
            <div class="progress-info">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: opponentProgress + '%' }"></div>
              </div>
              <div class="progress-text">{{ opponentProgress }}%</div>
            </div>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-icon correct">✓</div>
                <div class="stat-value">{{ opponentCorrect }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-icon total">?</div>
                <div class="stat-value">{{ opponentAnswered }}/10</div>
              </div>
            </div>
          </div>

          <div class="questions-card">
            <div class="questions-label">Вопросы</div>
            <div class="questions-grid">
              <div 
                v-for="n in 10" 
                :key="n"
                class="question-number"
                :class="{
                  'current': n === currentQuestion,
                  'answered': answers[n-1]?.answered,
                  'correct': answers[n-1]?.correct
                }"
              >
                {{ n }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="content-area">
        <div class="header-section">
          <div class="task-header">
            <span class="task-number">Вопрос {{ currentQuestion }}</span>
            <div class="score-comparison">
              <span class="score-you">{{ yourScore }}</span>
              <span class="vs">vs</span>
              <span class="score-opponent">{{ opponentScore }}</span>
            </div>
          </div>
        </div>

        <div class="question-section">
          <div class="question-block">
            <div class="question-label">ВОПРОС</div>
            <div class="question-text">{{ getCurrentQuestion() }}</div>
          </div>
        </div>

        <div class="input-section">
          <div class="input-block">
            <div class="input-label">Введите ваш ответ:</div>
            <div class="input-container">
              <input 
                type="text" 
                v-model="currentAnswer"
                placeholder="Введите ответ здесь..."
                class="answer-input"
                :class="{
                  'correct': answers[currentQuestion-1]?.correct,
                  'incorrect': answers[currentQuestion-1]?.answered && !answers[currentQuestion-1]?.correct
                }"
                @keyup.enter="checkAnswer"
                ref="answerInput"
                :disabled="answers[currentQuestion-1]?.answered"
              />
              <button 
                class="check-button"
                @click="checkAnswer"
                :disabled="!currentAnswer.trim() || answers[currentQuestion-1]?.answered"
              >
                {{ answers[currentQuestion-1]?.answered ? 'Отвечено' : 'Проверить' }}
              </button>
            </div>
            <div v-if="answers[currentQuestion-1]?.answered && !answers[currentQuestion-1]?.correct" 
                 class="error-message">
              Правильный ответ: <strong>{{ getCorrectAnswer(currentQuestion) }}</strong>
            </div>
          </div>
        </div>

        <div class="finish-section" v-if="answeredQuestions === 10">
          <button class="finish-button" @click="finishTest">
            Завершить тест
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskAnswer',
  
  data() {
    return {
      currentQuestion: 1,
      currentAnswer: '',
      yourScore: 0,
      opponentScore: 0,
      
      answers: Array(10).fill().map(() => ({ answered: false, correct: false })),
      
      questions: [
        'Сколько будет 2 + 2?',
        'Столица России?',
        'Сколько планет в Солнечной системе?',
        'Кто написал "Евгений Онегин"?',
        'Год основания Москвы?',
        'Сколько дней в високосном году?',
        'Самый большой океан?',
        'Химическая формула воды?',
        'Первый космонавт?',
        'Самая длинная река в мире?'
      ],
      
      correctAnswers: [
        '4', 'Москва', '8', 'Пушкин', '1147', 
        '366', 'Тихий', 'H2O', 'Гагарин', 'Амазонка'
      ]
    }
  },

  async created() {
    await this.startStatusChecking();
  },

  beforeUnmount() {
    // Очищаем интервал при уничтожении компонента
    this.stopStatusChecking();
  },
  
  computed: {
    answeredQuestions() {
      return this.answers.filter(a => a.answered).length
    },
    
    answeredCorrectly() {
      return this.answers.filter(a => a.correct).length
    },
    
    opponentCorrect() {
      // Соперник не получает правильные ответы - всегда 0
      return 0
    },
    
    opponentAnswered() {
      // Соперник не отвечает на вопросы - всегда 0
      return 0
    },
    
    yourProgress() {
      return (this.yourScore / 10) * 100
    },
    
    opponentProgress() {
      // Прогресс соперника всегда 0%
      return 0
    }
  },
  
  methods: {
    getCurrentQuestion() {
      return this.questions[this.currentQuestion - 1]
    },
    
    getCorrectAnswer() {
      return this.correctAnswers[this.currentQuestion - 1]
    },
    
    checkAnswer() {
      if (!this.currentAnswer.trim() || this.answers[this.currentQuestion - 1].answered) return
      
      const isCorrect = this.currentAnswer.trim().toLowerCase() === 
                       this.getCorrectAnswer().toLowerCase()
      
      this.answers[this.currentQuestion - 1] = {
        answer: this.currentAnswer,
        answered: true,
        correct: isCorrect
      }
      
      if (isCorrect) {
        this.yourScore++
      }
      
      if (this.currentQuestion < 10) {
        this.currentQuestion++
        this.currentAnswer = ''
      }
    },
    
    finishTest() {
      this.$router.push('/PvP/result');
    },

    async checkStatus() {
      try {
        // Используем currentMatch.matchCode из ref
        const matchCode = this.currentMatch?.matchCode;
        if (!matchCode) {
          console.error('Match code not found');
          return;
        }
        
        const response = await axios.get(`http://localhost:8000/api/pvp/status/${matchCode}`);
        this.status = response.data.status;
        console.log('Current status:', response.data);
        
        // Если статус показывает, что матч готов, можно перенаправить
        if (response.data.status === 'active') {
          this.stopStatusChecking();
          this.$router.push(`/PvP/answer`);
        }
      } catch (err) {
        console.error('Error checking match status:', err);
      }
    },

    startStatusChecking() {
      // Вызываем сразу один раз
      this.checkStatus();
      
      // Затем устанавливаем интервал на каждую секунду
      this.checkInterval = setInterval(() => {
        this.checkStatus();
      }, 1000);
    },

    stopStatusChecking() {
      if (this.checkInterval) {
        clearInterval(this.checkInterval);
        this.checkInterval = null;
      }
    },
  }
}
</script>

<style scoped>
.task-answer-section {
  min-height: 100vh;
  background: #faf6ef;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.main-container {
  display: flex;
  min-height: 100vh;
  margin: 0;
  padding-left: 0;
}

.left-panel {
  width: 240px;
  padding: 20px 15px;
  position: relative;
  background: white;
  border-right: 1px solid #e8e8e8;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
}

.panel-content {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.player-card {
  padding: 18px;
  border-radius: 12px;
  margin-bottom: 15px;
  background: #fafafa;
  border: 1px solid transparent;
}

.player-card.you {
  border-color: #1565c0;
  border-left: 4px solid #1565c0;
}

.player-card.opponent {
  border-color: #e53935;
  border-left: 4px solid #e53935;
}

.player-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
  color: white;
}

.player-card.you .avatar-circle {
  background: linear-gradient(135deg, #1565c0, #1e88e5);
}

.player-card.opponent .avatar-circle {
  background: linear-gradient(135deg, #e53935, #ef5350);
}

.player-details {
  flex: 1;
}

.player-name {
  font-size: 13px;
  color: #666;
  margin-bottom: 3px;
}

.player-score {
  font-size: 24px;
  font-weight: 800;
}

.player-card.you .player-score {
  color: #1565c0;
}

.player-card.opponent .player-score {
  color: #e53935;
}

.progress-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.progress-bar {
  flex: 1;
  height: 5px;
  background: #e8e8e8;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.player-card.you .progress-fill {
  background: linear-gradient(90deg, #1565c0, #42a5f5);
}

.player-card.opponent .progress-fill {
  background: linear-gradient(90deg, #e53935, #ef5350);
}

.progress-text {
  font-size: 13px;
  font-weight: 600;
  color: #666;
  min-width: 40px;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-icon {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
}

.stat-icon.correct {
  background: #e8f5e9;
  color: #43a047;
}

.stat-icon.total {
  background: #e3f2fd;
  color: #1565c0;
}

.player-card.opponent .stat-icon.total {
  background: #ffebee;
  color: #e53935;
}

.stat-value {
  font-size: 15px;
  font-weight: 700;
  color: #333;
}

.questions-card {
  background: white;
  border-radius: 12px;
  padding: 18px;
  border: 1px solid #e8e8e8;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.questions-label {
  font-size: 14px;
  font-weight: 700;
  color: #1565c0;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.question-number {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: #f5f5f5;
  border: 2px solid #e0e0e0;
  font-size: 14px;
  font-weight: 600;
  color: #666;
  user-select: none;
  cursor: default;
}

.question-number.current {
  background: #1565c0;
  border-color: #1565c0;
  color: white;
  transform: scale(1.1);
  box-shadow: 0 2px 6px rgba(21, 101, 192, 0.3);
}

.question-number.correct {
  background: #e8f5e9;
  border-color: #43a047;
  color: #43a047;
}

.question-number.answered:not(.correct) {
  background: #ffebee;
  border-color: #e53935;
  color: #e53935;
}

.content-area {
  flex: 1;
  padding: 30px 40px;
  display: flex;
  flex-direction: column;
  margin-left: 0;
}

.header-section {
  margin-bottom: 30px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #1565c0;
}

.task-number {
  font-size: 24px;
  font-weight: 700;
  color: #1565c0;
}

.score-comparison {
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  padding: 8px 16px;
  border-radius: 18px;
  border: 2px solid #e8e8e8;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.score-you {
  font-size: 18px;
  font-weight: 700;
  color: #1565c0;
}

.vs {
  font-size: 11px;
  color: #666;
  font-weight: 600;
}

.score-opponent {
  font-size: 18px;
  font-weight: 700;
  color: #e53935;
}

.question-section {
  margin-bottom: 30px;
}

.question-block {
  background: white;
  border-radius: 14px;
  padding: 25px;
  border: 1px solid #e8e8e8;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.question-label {
  font-size: 13px;
  font-weight: 700;
  color: #1565c0;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.question-text {
  font-size: 20px;
  line-height: 1.6;
  color: #333;
  font-weight: 500;
}

.input-section {
  margin-bottom: 25px;
}

.input-block {
  background: white;
  border-radius: 14px;
  padding: 22px;
  border: 1px solid #e8e8e8;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.input-label {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
}

.input-container {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
}

.answer-input {
  flex: 1;
  padding: 16px 20px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  background: white;
  transition: all 0.2s;
}

.answer-input:focus {
  outline: none;
  border-color: #1565c0;
  box-shadow: 0 0 0 3px rgba(21, 101, 192, 0.1);
}

.answer-input.correct {
  border-color: #43a047;
  background: #f1f8e9;
  color: #1b5e20;
}

.answer-input.incorrect {
  border-color: #e53935;
  background: #ffebee;
  color: #b71c1c;
}

.answer-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.check-button {
  padding: 16px 32px;
  background: #1565c0;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 120px;
}

.check-button:hover:not(:disabled) {
  background: #0d47a1;
}

.check-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #e53935;
  font-size: 14px;
  padding: 8px 12px;
  background: #ffebee;
  border-radius: 6px;
  border-left: 4px solid #e53935;
}

.finish-section {
  margin-top: auto;
}

.finish-button {
  width: 100%;
  padding: 18px;
  background: linear-gradient(135deg, #43a047, #2e7d32);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(67, 160, 71, 0.3);
}

.finish-button:hover {
  background: linear-gradient(135deg, #2e7d32, #1b5e20);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(67, 160, 71, 0.4);
}

@media (max-width: 1024px) {
  .main-container {
    flex-direction: column;
  }
  
  .left-panel {
    width: 100%;
    padding: 15px;
    border-right: none;
    border-bottom: 1px solid #e8e8e8;
  }
  
  .panel-content {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    position: static;
  }
  
  .player-card {
    flex: 1;
    min-width: 220px;
    margin-bottom: 0;
  }
  
  .questions-card {
    flex: 0 0 100%;
    margin-top: 0;
  }
  
  .content-area {
    padding: 20px;
    margin-left: 0;
  }
}

@media (max-width: 768px) {
  .panel-content {
    flex-direction: column;
  }
  
  .task-header {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
  
  .input-container {
    flex-direction: column;
  }
  
  .check-button {
    width: 100%;
  }
  
  .questions-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 480px) {
  .player-card {
    min-width: 100%;
  }
  
  .player-header {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
  
  .progress-info {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }
  
  .progress-text {
    text-align: center;
  }
  
  .questions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
