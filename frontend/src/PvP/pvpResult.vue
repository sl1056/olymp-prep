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
            <div class="player-icon">👤</div>
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
            <div class="player-icon">⚡</div>
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
        <div class="result-icon">{{ resultIcon }}</div>
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
    const gameResults = {
      playerScore: 7,
      rivalScore: 6,
      playerRightAnswers: 7,
      rivalRightAnswers: 6,
      questionsCount: 10
    };
    
    const quizData = [
      { id: 1, questionText: 'Сколько будет 2 + 2?', rightAnswer: '4' },
      { id: 2, questionText: 'Столица России?', rightAnswer: 'Москва' },
      { id: 3, questionText: 'Сколько планет в Солнечной системе?', rightAnswer: '8' },
      { id: 4, questionText: 'Кто написал "Евгений Онегин"?', rightAnswer: 'Пушкин' },
      { id: 5, questionText: 'Год основания Москвы?', rightAnswer: '1147' },
      { id: 6, questionText: 'Сколько дней в високосном году?', rightAnswer: '366' },
      { id: 7, questionText: 'Самый большой океан?', rightAnswer: 'Тихий' },
      { id: 8, questionText: 'Химическая формула воды?', rightAnswer: 'H2O' },
      { id: 9, questionText: 'Первый космонавт?', rightAnswer: 'Гагарин' },
      { id: 10, questionText: 'Самая длинная река в мире?', rightAnswer: 'Нил' }
    ];
    
    const playerAnswers = ['4', 'Москва', '8', 'Пушкин', '1147', '366', 'Тихий', 'H2O', 'Гагарин', 'Амазонка'];
    const rivalAnswers = ['4', 'Москва', '9', 'Пушкин', '1147', '365', 'Атлантический', 'H2O', 'Гагарин', 'Нил'];
    
    return {
      gameResults,
      quizData,
      playerAnswers,
      rivalAnswers,
      isLoading: false
    };
  },
  
  computed: {
    results() {
      return {
        yourScore: this.gameResults.playerScore,
        opponentScore: this.gameResults.rivalScore,
        yourCorrect: this.gameResults.playerRightAnswers,
        opponentCorrect: this.gameResults.rivalRightAnswers,
        totalQuestions: this.gameResults.questionsCount
      };
    },
    
    questions() {
      return this.quizData.map(q => ({
        id: q.id,
        text: q.questionText,
        correctAnswer: q.rightAnswer
      }));
    },
    
    yourPercentage() {
      const correct = this.gameResults.playerRightAnswers;
      const total = this.gameResults.questionsCount;
      return total > 0 ? Math.floor((correct / total) * 100) : 0;
    },
    
    opponentPercentage() {
      const correct = this.gameResults.rivalRightAnswers;
      const total = this.gameResults.questionsCount;
      return total > 0 ? Math.floor((correct / total) * 100) : 0;
    },
    
    matchResult() {
      const player = this.gameResults.playerScore;
      const rival = this.gameResults.rivalScore;
      
      if (player > rival) return 'win';
      if (player < rival) return 'lose';
      return 'draw';
    },
    
    resultClass() {
      return this.matchResult;
    },
    
    resultText() {
      if (this.matchResult === 'win') return 'Вы победили!';
      if (this.matchResult === 'lose') return 'Соперник победил';
      return 'Ничья';
    },
    
    resultSubtitle() {
      if (this.matchResult === 'win') return 'Отличный результат!';
      if (this.matchResult === 'lose') return 'Попробуйте еще раз';
      return 'Равная игра';
    },
    
    resultIcon() {
      if (this.matchResult === 'win') return '🏆';
      if (this.matchResult === 'lose') return '🎯';
      return '🤝';
    }
  },
  
  methods: {
    getUserAnswer(index) {
      if (index < 0 || index >= this.playerAnswers.length) return '—';
      const answer = this.playerAnswers[index];
      return answer && answer.trim() !== '' ? answer : '—';
    },
    
    getOpponentAnswer(index) {
      if (index < 0 || index >= this.rivalAnswers.length) return '—';
      const answer = this.rivalAnswers[index];
      return answer && answer.trim() !== '' ? answer : '—';
    },
    
    checkAnswerCorrectness(userAnswer, correctAnswer) {
      if (!userAnswer || userAnswer === '—') return false;
      return userAnswer.trim().toLowerCase() === correctAnswer.trim().toLowerCase();
    },
    
    isUserAnswerCorrect(index) {
      if (index < 0 || index >= this.quizData.length) return false;
      const userAnswer = this.getUserAnswer(index);
      const correctAnswer = this.quizData[index].rightAnswer;
      return this.checkAnswerCorrectness(userAnswer, correctAnswer);
    },
    
    isOpponentAnswerCorrect(index) {
      if (index < 0 || index >= this.quizData.length) return false;
      const opponentAnswer = this.getOpponentAnswer(index);
      const correctAnswer = this.quizData[index].rightAnswer;
      return this.checkAnswerCorrectness(opponentAnswer, correctAnswer);
    },
    
    async retryMatch() {
      this.isLoading = true;
      try {
        await new Promise(resolve => setTimeout(resolve, 300));
        this.$router.push('/PvP/');
      } catch (error) {
        console.error('Ошибка при переходе:', error);
      } finally {
        this.isLoading = false;
      }
    },
    
    goHome() {
      this.saveToHistory();
      this.$router.push('/');
    },
    
    saveToHistory() {
      const historyItem = {
        date: new Date().toLocaleString(),
        score: `${this.gameResults.playerScore}:${this.gameResults.rivalScore}`,
        result: this.matchResult
      };
      
      try {
        console.log('Сохранено в историю:', historyItem);
      } catch (e) {
      }
    }
  },
  
  mounted() {
    const params = this.$route.params;
    if (params && params.results) {
      try {
        const parsed = JSON.parse(params.results);
        Object.assign(this.gameResults, {
          playerScore: parsed.yourScore || 0,
          rivalScore: parsed.opponentScore || 0,
          playerRightAnswers: parsed.yourCorrect || 0,
          rivalRightAnswers: parsed.opponentCorrect || 0,
          questionsCount: parsed.totalQuestions || 10
        });
      } catch (e) {
      }
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

.player-icon {
  font-size: 24px;
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

.result-icon {
  font-size: 48px;
  flex-shrink: 0;
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
