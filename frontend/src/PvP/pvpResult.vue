<template>
  <div class="results-page">
    <div class="simple-header">
      <h1 class="header-title">Результаты игры</h1>
      <div class="header-subtitle">Итоги вашей интеллектуальной дуэли</div>
    </div>

    <div class="content">
      <div class="score-container">
        <div class="score-box you">
          <div class="score-header">
            <h3>Вы</h3>
          </div>
          <div class="score-main">
            <div class="score-number">{{ results.yourScore }}</div>
            <div class="score-label">баллов</div>
          </div>
          <div class="score-stats">
            <div class="stat">
              <div class="stat-value">{{ yourPercentage }}%</div>
              <div class="stat-label">Точность</div>
            </div>
            <div class="stat">
              <div class="stat-value">{{ results.yourCorrect }}/{{ results.totalQuestions }}</div>
              <div class="stat-label">Верно</div>
            </div>
          </div>
        </div>

        <div class="vs-box">
          <div class="vs-line"></div>
          <div class="vs-text">VS</div>
          <div class="vs-line"></div>
        </div>

        <div class="score-box opponent">
          <div class="score-header">
            <h3>Соперник</h3>
          </div>
          <div class="score-main">
            <div class="score-number">{{ results.opponentScore }}</div>
            <div class="score-label">баллов</div>
          </div>
          <div class="score-stats">
            <div class="stat">
              <div class="stat-value">{{ opponentPercentage }}%</div>
              <div class="stat-label">Точность</div>
            </div>
            <div class="stat">
              <div class="stat-value">{{ results.opponentCorrect }}/{{ results.totalQuestions }}</div>
              <div class="stat-label">Верно</div>
            </div>
          </div>
        </div>
      </div>

      <div class="result-banner" :class="resultClass">
        <div class="result-text">
          <h2>{{ resultText }}</h2>
          <p>{{ resultSubtitle }}</p>
        </div>
      </div>

      <div class="answers-section">
        <div class="section-title">
          <h2>Ответы</h2>
          <div class="questions-count">{{ results.totalQuestions }} вопросов</div>
        </div>

        <div class="answers-list">
          <div 
            class="answer-item" 
            v-for="(question, index) in questions" 
            :key="question.id"
          >
            <div class="question-info">
              <div class="question-number">Вопрос {{ index + 1 }}</div>
              <div class="question-text">{{ question.text }}</div>
            </div>

            <div class="answers-comparison">
              <div class="answer-row you-answer" :class="{ correct: isUserAnswerCorrect(index), wrong: !isUserAnswerCorrect(index) }">
                <div class="answer-label">Ваш ответ:</div>
                <div class="answer-value">{{ getUserAnswer(index) }}</div>
                <div class="answer-status">
                  {{ isUserAnswerCorrect(index) ? '✓' : '✗' }}
                </div>
              </div>

              <div class="answer-row opponent-answer" :class="{ correct: isOpponentAnswerCorrect(index), wrong: !isOpponentAnswerCorrect(index) }">
                <div class="answer-label">Соперник:</div>
                <div class="answer-value">{{ getOpponentAnswer(index) }}</div>
                <div class="answer-status">
                  {{ isOpponentAnswerCorrect(index) ? '✓' : '✗' }}
                </div>
              </div>

              <div class="correct-answer" v-if="!isUserAnswerCorrect(index) || !isOpponentAnswerCorrect(index)">
                <div class="correct-label">Правильно:</div>
                <div class="correct-value">{{ question.correctAnswer }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="actions">
        <button class="btn retry-btn" @click="retryMatch">
          Играть снова
        </button>
        <button class="btn home-btn" @click="goHome">
          На главную
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameResultsPage',
  
  data() {
    return {
      results: {
        yourScore: 7,
        opponentScore: 5,
        yourCorrect: 7,
        opponentCorrect: 5,
        totalQuestions: 10
      },
      questions: [
        { text: 'Сколько будет 2 + 2?', correctAnswer: '4' },
        { text: 'Столица России?', correctAnswer: 'Москва' },
        { text: 'Сколько планет в Солнечной системе?', correctAnswer: '8' },
        { text: 'Кто написал "Евгений Онегин"?', correctAnswer: 'Пушкин' },
        { text: 'Год основания Москвы?', correctAnswer: '1147' },
        { text: 'Сколько дней в високосном году?', correctAnswer: '366' },
        { text: 'Самый большой океан?', correctAnswer: 'Тихий' },
        { text: 'Химическая формула воды?', correctAnswer: 'H2O' },
        { text: 'Первый космонавт?', correctAnswer: 'Гагарин' },
        { text: 'Самая длинная река в мире?', correctAnswer: 'Нил' }
      ],
      yourAnswers: ['4', 'Москва', '8', 'Толстой', '1147', '366', 'Тихий', 'H2O', 'Гагарин', 'Амазонка'],
      opponentAnswers: ['5', 'Москва', '9', 'Пушкин', '1247', '366', 'Атлантический', 'H2O', 'Леонов', 'Нил']
    };
  },
  
  computed: {
    yourPercentage() {
      return Math.round((this.results.yourCorrect / this.results.totalQuestions) * 100);
    },
    
    opponentPercentage() {
      return Math.round((this.results.opponentCorrect / this.results.totalQuestions) * 100);
    },
    
    matchResult() {
      if (this.results.yourScore > this.results.opponentScore) return 'win';
      if (this.results.yourScore < this.results.opponentScore) return 'lose';
      return 'draw';
    },
    
    resultText() {
      switch (this.matchResult) {
        case 'win': return 'Вы победили!';
        case 'lose': return 'Соперник победил';
        default: return 'Ничья';
      }
    },
    
    resultSubtitle() {
      switch (this.matchResult) {
        case 'win': return 'Отличный результат!';
        case 'lose': return 'Попробуйте еще раз';
        default: return 'Равная игра';
      }
    },
    
    resultClass() {
      return this.matchResult;
    }
  },
  
  methods: {
    getUserAnswer(index) {
      return this.yourAnswers[index] || '—';
    },
    
    getOpponentAnswer(index) {
      return this.opponentAnswers[index] || '—';
    },
    
    isUserAnswerCorrect(index) {
      const userAnswer = this.yourAnswers[index];
      const correctAnswer = this.questions[index].correctAnswer;
      return userAnswer && userAnswer.toLowerCase() === correctAnswer.toLowerCase();
    },
    
    isOpponentAnswerCorrect(index) {
      const opponentAnswer = this.opponentAnswers[index];
      const correctAnswer = this.questions[index].correctAnswer;
      return opponentAnswer && opponentAnswer.toLowerCase() === correctAnswer.toLowerCase();
    },
    
    retryMatch() {
      this.$router.push('/PvP/');
    },
    
    goHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.results-page {
  min-height: 100vh;
  background: rgb(250, 246, 239);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: #4a453a;
  padding-top: 24px;
}

.simple-header {
  text-align: center;
  padding: 20px 24px;
  margin-bottom: 16px;
}

.header-title {
  font-size: 32px;
  font-weight: 700;
  color: #2a5c8c;
  margin: 0 0 8px 0;
  letter-spacing: -0.3px;
}

.header-subtitle {
  font-size: 16px;
  color: #8a857c;
  font-weight: 400;
  max-width: 500px;
  margin: 0 auto;
  line-height: 1.5;
}

.content {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 24px 40px;
}

.score-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 32px;
}

.score-box {
  flex: 1;
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(42, 92, 140, 0.1);
  border: 2px solid;
}

.score-box.you {
  border-color: #2a5c8c;
}

.score-box.opponent {
  border-color: #e74c3c;
}

.score-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.score-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #4a453a;
}

.score-main {
  text-align: center;
  margin-bottom: 20px;
}

.score-number {
  font-size: 48px;
  font-weight: 700;
  color: #2a5c8c;
  line-height: 1;
  margin-bottom: 8px;
}

.score-box.opponent .score-number {
  color: #e74c3c;
}

.score-label {
  font-size: 14px;
  color: #8a857c;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.score-stats {
  display: flex;
  justify-content: space-around;
  padding-top: 16px;
  border-top: 1px solid #eee;
}

.stat {
  text-align: center;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #4a453a;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #8a857c;
}

.vs-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.vs-line {
  width: 1px;
  height: 40px;
  background: #d4cfc5;
}

.vs-text {
  font-size: 16px;
  font-weight: 700;
  color: #e74c3c;
  padding: 8px 16px;
  background: white;
  border-radius: 20px;
  border: 2px solid #e8e2d1;
}

.result-banner {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 12px rgba(42, 92, 140, 0.1);
  border-left: 6px solid;
}

.result-banner.win {
  border-left-color: #4caf50;
  background: linear-gradient(to right, #f1f8e9, white);
}

.result-banner.lose {
  border-left-color: #e74c3c;
  background: linear-gradient(to right, #ffebee, white);
}

.result-banner.draw {
  border-left-color: #ff9800;
  background: linear-gradient(to right, #fff3e0, white);
}

.result-text h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #4a453a;
}

.result-text p {
  margin: 0;
  color: #8a857c;
  font-size: 16px;
}

.answers-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: 0 4px 12px rgba(42, 92, 140, 0.1);
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0ede5;
}

.section-title h2 {
  margin: 0;
  font-size: 22px;
  color: #4a453a;
}

.questions-count {
  font-size: 14px;
  color: #8a857c;
  background: #f5f1e8;
  padding: 6px 12px;
  border-radius: 12px;
}

.answers-list {
  max-height: 500px;
  overflow-y: auto;
  padding-right: 8px;
}

.answer-item {
  background: #f9f7f2;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  border: 1px solid #e8e2d1;
}

.answer-item:last-child {
  margin-bottom: 0;
}

.question-info {
  margin-bottom: 16px;
}

.question-number {
  font-size: 12px;
  font-weight: 600;
  color: #2a5c8c;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.question-text {
  font-size: 16px;
  line-height: 1.5;
  color: #4a453a;
}

.answers-comparison {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.answer-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid;
}

.you-answer {
  background: rgba(42, 92, 140, 0.05);
  border-color: rgba(42, 92, 140, 0.2);
}

.opponent-answer {
  background: rgba(231, 76, 60, 0.05);
  border-color: rgba(231, 76, 60, 0.2);
}

.answer-row.correct {
  background: rgba(76, 175, 80, 0.1);
  border-color: rgba(76, 175, 80, 0.3);
}

.answer-row.wrong {
  background: rgba(244, 67, 54, 0.1);
  border-color: rgba(244, 67, 54, 0.3);
}

.answer-label {
  font-size: 14px;
  color: #8a857c;
  min-width: 80px;
}

.answer-value {
  flex: 1;
  font-size: 15px;
  font-weight: 500;
  color: #4a453a;
}

.answer-status {
  font-size: 18px;
  font-weight: bold;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.answer-row.correct .answer-status {
  color: #4caf50;
}

.answer-row.wrong .answer-status {
  color: #f44336;
}

.correct-answer {
  margin-top: 12px;
  padding: 12px;
  background: rgba(42, 92, 140, 0.08);
  border-radius: 8px;
  border-left: 4px solid #2a5c8c;
}

.correct-label {
  font-size: 12px;
  font-weight: 600;
  color: #2a5c8c;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.correct-value {
  font-size: 15px;
  font-weight: 500;
  color: #4a453a;
}

.actions {
  display: flex;
  gap: 16px;
}

.btn {
  flex: 1;
  padding: 16px 24px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.retry-btn {
  background: #2a5c8c;
  color: white;
}

.retry-btn:hover {
  background: #1d4a73;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(42, 92, 140, 0.3);
}

.home-btn {
  background: white;
  color: #4a453a;
  border: 2px solid #e8e2d1;
}

.home-btn:hover {
  background: #f9f7f2;
  border-color: #d4cfc5;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(139, 115, 85, 0.1);
}

.answers-list::-webkit-scrollbar {
  width: 6px;
}

.answers-list::-webkit-scrollbar-track {
  background: #f5f1e8;
  border-radius: 3px;
}

.answers-list::-webkit-scrollbar-thumb {
  background: #d4cfc5;
  border-radius: 3px;
}

.answers-list::-webkit-scrollbar-thumb:hover {
  background: #8b7355;
}

@media (max-width: 768px) {
  .simple-header {
    padding: 16px 20px;
  }
  
  .header-title {
    font-size: 28px;
  }
  
  .header-subtitle {
    font-size: 15px;
  }
  
  .content {
    padding: 0 16px 32px;
  }
  
  .score-container {
    flex-direction: column;
    gap: 16px;
  }
  
  .vs-box {
    flex-direction: row;
    width: 100%;
  }
  
  .vs-line {
    width: 100%;
    height: 1px;
  }
  
  .vs-text {
    padding: 4px 12px;
  }
  
  .result-banner {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .answer-row {
    flex-wrap: wrap;
  }
  
  .answer-label {
    min-width: 60px;
  }
}

@media (max-width: 480px) {
  .simple-header {
    padding: 12px 16px;
  }
  
  .header-title {
    font-size: 24px;
  }
  
  .header-subtitle {
    font-size: 14px;
  }
  
  .score-number {
    font-size: 40px;
  }
  
  .result-icon {
    font-size: 40px;
  }
  
  .answer-value {
    font-size: 14px;
  }
}
</style>
