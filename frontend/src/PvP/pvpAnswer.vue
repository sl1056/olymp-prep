<template>
  <div class="task-answer-section">
    <div class="main-container">
      <div class="left-panel">
        <div class="panel-content">
          <div class="player-card you">
            <div class="player-header">
              <div class="avatar-circle">В</div>
              <div class="player-details">
                <div class="player-name">{{ currentUsername || 'Вы' }}</div>
                <div class="player-score">{{ mySubmitted ? 'Ответ отправлен' : 'Отвечаете' }}</div>
              </div>
            </div>
          </div>

          <div class="player-card opponent">
            <div class="player-header">
              <div class="avatar-circle">С</div>
              <div class="player-details">
                <div class="player-name">{{ opponentUsername || 'Соперник' }}</div>
                <div class="player-score">{{ opponentSubmitted ? 'Ответил' : 'Ожидаем ответ' }}</div>
              </div>
            </div>
          </div>

          <div class="questions-card">
            <div class="questions-label">Статус матча</div>
            <div class="status-list">
              <div class="status-line">Код: {{ matchId || '—' }}</div>
              <div class="status-line">Сокет: {{ wsConnected ? 'подключён' : 'отключён' }}</div>
              <div class="status-line">Состояние: {{ matchStatusLabel }}</div>
              <div class="status-line">Вопрос: {{ currentQuestionIndex }}/{{ totalQuestions }}</div>
              <div class="status-line">Счёт: {{ myScore }} : {{ opponentScore }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="content-area">
        <div class="header-section">
          <div class="task-header">
            <span class="task-number">PvP вопрос {{ currentQuestionIndex }}/{{ totalQuestions }}</span>
            <div class="score-comparison">
              <span class="score-you">{{ myScore }}</span>
              <span class="vs">vs</span>
              <span class="score-opponent">{{ opponentScore }}</span>
            </div>
          </div>
        </div>

        <div class="question-section">
          <div class="question-block">
            <div class="question-label">ВОПРОС</div>
            <div class="question-text">{{ taskText || 'Загружаем вопрос...' }}</div>
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
                @keyup.enter="submitAnswer"
                :disabled="isInputDisabled"
              />
              <button
                class="check-button"
                @click="submitAnswer"
                :disabled="!currentAnswer.trim() || isInputDisabled"
              >
                {{ mySubmitted ? 'Ответ отправлен' : 'Отправить' }}
              </button>
            </div>

            <div v-if="serverError" class="error-message">{{ serverError }}</div>
            <div v-if="infoMessage" class="info-message">{{ infoMessage }}</div>
          </div>
        </div>

        <div class="finish-section" v-if="mySubmitted && !finalized">
          <button class="finish-button" disabled>
            Ожидаем ответ соперника...
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TaskAnswer',

  data() {
    return {
      ws: null,
      wsConnected: false,
      statusTimer: null,

      token: '',
      matchId: '',
      currentUserId: null,
      currentUsername: '',
      player1Username: '',
      player2Username: '',
      opponentUsername: '',

      taskText: '',
      currentAnswer: '',
      submittedAnswer: '',

      matchStatus: 'waiting',
      mySubmitted: false,
      opponentSubmitted: false,
      finalized: false,
      currentQuestionIndex: 1,
      totalQuestions: 1,
      myScore: 0,
      opponentScore: 0,

      serverError: '',
      infoMessage: '',
    }
  },

  computed: {
    isInputDisabled() {
      return this.finalized || this.mySubmitted || this.matchStatus !== 'active'
    },

    matchStatusLabel() {
      if (this.matchStatus === 'active') return 'активен'
      if (this.matchStatus === 'finished') return 'завершён'
      if (this.matchStatus === 'cancelled') return 'отменён'
      return 'ожидание'
    }
  },

  async created() {
    await this.initializePage()
  },

  beforeUnmount() {
    this.stopStatusChecking()
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  },

  methods: {
    decodeUserIdFromToken(token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        return Number(payload.user_id)
      } catch {
        return null
      }
    },

    async initializePage() {
      this.token = localStorage.getItem('authToken') || ''
      this.matchId = localStorage.getItem('currentMatchId') || ''

      if (!this.token) {
        this.$router.push('/auth')
        return
      }

      if (!this.matchId) {
        this.$router.push('/PvP')
        return
      }

      this.currentUserId = this.decodeUserIdFromToken(this.token)

      try {
        const [profileResponse, statusResponse] = await Promise.all([
          axios.get('http://localhost:8000/api/auth/profile/', {
            headers: { Authorization: `Bearer ${this.token}` }
          }),
          axios.get(`http://localhost:8000/api/pvp/status/${this.matchId}/`, {
            headers: { Authorization: `Bearer ${this.token}` }
          })
        ])

        this.currentUsername = profileResponse.data.username
        this.applyMatchStatus(statusResponse.data)

        if (this.matchStatus === 'finished') {
          this.saveFallbackResult()
          this.$router.push('/PvP/Result')
          return
        }

        if (this.matchStatus === 'active') {
          this.connectWebSocket()
        } else if (this.matchStatus === 'waiting') {
          this.infoMessage = 'Матч ещё не начался. Ждём второго игрока.'
        }

        this.startStatusChecking()
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.removeItem('authToken')
          this.$router.push('/auth')
          return
        }

        this.serverError = 'Не удалось загрузить данные матча'
      }
    },

    applyMatchStatus(payload) {
      this.matchStatus = payload.status
      this.taskText = payload.task_text || ''
      this.player1Username = payload.player1 || this.player1Username
      this.player2Username = payload.player2 || this.player2Username
      this.currentQuestionIndex = Number(payload.current_question_index || this.currentQuestionIndex || 1)
      this.totalQuestions = Number(payload.questions_count || this.totalQuestions || 1)

      const isPlayer1 = this.currentUsername === payload.player1
      const isPlayer2 = this.currentUsername === payload.player2

      if (isPlayer1) {
        this.opponentUsername = payload.player2 || 'Соперник'
        this.mySubmitted = !!payload.player1_answered
        this.opponentSubmitted = !!payload.player2_answered
        this.myScore = Number(payload.player1_score || 0)
        this.opponentScore = Number(payload.player2_score || 0)
      } else if (isPlayer2) {
        this.opponentUsername = payload.player1 || 'Соперник'
        this.mySubmitted = !!payload.player2_answered
        this.opponentSubmitted = !!payload.player1_answered
        this.myScore = Number(payload.player2_score || 0)
        this.opponentScore = Number(payload.player1_score || 0)
      }

      if (this.matchStatus === 'cancelled') {
        this.infoMessage = 'Матч был отменён.'
        this.stopStatusChecking()
      }
    },

    startStatusChecking() {
      this.stopStatusChecking()
      this.statusTimer = setInterval(async () => {
        try {
          const response = await axios.get(`http://localhost:8000/api/pvp/status/${this.matchId}/`, {
            headers: { Authorization: `Bearer ${this.token}` }
          })

          const prevStatus = this.matchStatus
          this.applyMatchStatus(response.data)

          if (prevStatus !== 'active' && this.matchStatus === 'active' && !this.wsConnected) {
            this.connectWebSocket()
          }

          if (this.matchStatus === 'finished' && !this.finalized) {
            this.finalized = true
            this.infoMessage = 'Матч завершён. Переходим к результатам...'
            this.saveFallbackResult()
            this.$router.push('/PvP/Result')
          }

          if (this.matchStatus === 'cancelled') {
            this.$router.push('/PvP')
          }
        } catch (err) {
          if (err.response?.status === 401) {
            localStorage.removeItem('authToken')
            this.$router.push('/auth')
          }
        }
      }, 3000)
    },

    stopStatusChecking() {
      if (this.statusTimer) {
        clearInterval(this.statusTimer)
        this.statusTimer = null
      }
    },

    connectWebSocket() {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        return
      }

      const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
      const wsUrl = `${wsProtocol}://localhost:8000/ws/pvp/${this.matchId}/?token=${this.token}`

      this.ws = new WebSocket(wsUrl)

      this.ws.onopen = () => {
        this.wsConnected = true
        this.serverError = ''
      }

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          this.handleSocketMessage(data)
        } catch {
          this.serverError = 'Некорректное сообщение от сервера'
        }
      }

      this.ws.onerror = () => {
        this.serverError = 'Ошибка WebSocket-соединения'
      }

      this.ws.onclose = () => {
        this.wsConnected = false
      }
    },

    waitForSocketOpen(timeoutMs = 3000) {
      return new Promise((resolve) => {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          resolve(true)
          return
        }

        this.connectWebSocket()

        const startedAt = Date.now()
        const timer = setInterval(() => {
          if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            clearInterval(timer)
            resolve(true)
            return
          }

          if (Date.now() - startedAt >= timeoutMs) {
            clearInterval(timer)
            resolve(false)
          }
        }, 100)
      })
    },

    handleSocketMessage(data) {
      if (data.error) {
        this.serverError = data.error
        if (data.error !== 'Ответ уже отправлен') {
          this.mySubmitted = false
        }
        return
      }

      if (data.type === 'player_joined') {
        if (data.username && data.username !== this.currentUsername) {
          this.infoMessage = `${data.username} в матче`
        }
        return
      }

      if (data.type === 'opponent_submitted') {
        const submittedUserId = Number(data.user_id)
        if (this.currentUserId && submittedUserId === this.currentUserId) {
          this.mySubmitted = true
        } else {
          this.opponentSubmitted = true
          this.infoMessage = 'Соперник отправил ответ'
        }
        return
      }

      if (data.type === 'next_question' && data.data) {
        const payload = data.data
        this.taskText = payload.task_text || this.taskText
        this.currentQuestionIndex = Number(payload.current_question_index || this.currentQuestionIndex + 1)
        this.totalQuestions = Number(payload.questions_count || this.totalQuestions)
        this.currentAnswer = ''
        this.submittedAnswer = ''
        this.mySubmitted = false
        this.opponentSubmitted = false
        this.serverError = ''
        this.infoMessage = `Новый вопрос ${this.currentQuestionIndex}/${this.totalQuestions}`

        const isPlayer1 = this.currentUsername === this.player1Username
        const isPlayer2 = this.currentUsername === this.player2Username
        if (isPlayer1) {
          this.myScore = Number(payload.player1_score || this.myScore)
          this.opponentScore = Number(payload.player2_score || this.opponentScore)
        } else if (isPlayer2) {
          this.myScore = Number(payload.player2_score || this.myScore)
          this.opponentScore = Number(payload.player1_score || this.opponentScore)
        }
        return
      }

      if (data.type === 'game_over' && data.results) {
        this.finalized = true
        const payload = this.buildResultPayload(data.results)
        localStorage.setItem('pvpLastResult', JSON.stringify(payload))
        this.$router.push('/PvP/Result')
      }
    },

    buildResultPayload(results) {
      const isPlayer1 = this.currentUsername === results.player1_username
      const yourCorrect = isPlayer1 ? !!results.player1_correct : !!results.player2_correct
      const opponentCorrect = isPlayer1 ? !!results.player2_correct : !!results.player1_correct
      const yourScore = Number(isPlayer1 ? results.player1_score : results.player2_score) || 0
      const opponentScore = Number(isPlayer1 ? results.player2_score : results.player1_score) || 0

      const isWin =
        (isPlayer1 && results.winner === 'player1') ||
        (!isPlayer1 && results.winner === 'player2')
      const isLose =
        (isPlayer1 && results.winner === 'player2') ||
        (!isPlayer1 && results.winner === 'player1')

      return {
        match_id: results.match_id,
        current_username: this.currentUsername,
        player1_username: results.player1_username,
        player2_username: results.player2_username,
        player1_new_rating: results.player1_new_rating,
        player2_new_rating: results.player2_new_rating,
        your_score: yourScore,
        opponent_score: opponentScore,
        your_correct: yourCorrect,
        opponent_correct: opponentCorrect,
        total_questions: Number(results.total_questions || this.totalQuestions || 1),
        match_result: isWin ? 'win' : isLose ? 'lose' : 'draw',
        task_text: this.taskText,
        your_answer: this.submittedAnswer || this.currentAnswer.trim() || '—',
        correct_answer: results.correct_answer,
      }
    },

    saveFallbackResult() {
      if (localStorage.getItem('pvpLastResult')) {
        return
      }

      const payload = {
        match_id: this.matchId,
        current_username: this.currentUsername,
        your_score: this.myScore,
        opponent_score: this.opponentScore,
        your_correct: false,
        opponent_correct: false,
        total_questions: this.totalQuestions,
        match_result: 'draw',
        task_text: this.taskText || '—',
        your_answer: this.submittedAnswer || this.currentAnswer.trim() || '—',
        correct_answer: '—',
      }

      localStorage.setItem('pvpLastResult', JSON.stringify(payload))
    },

    async submitAnswer() {
      if (!this.currentAnswer.trim() || this.isInputDisabled) {
        return
      }

      const socketReady = await this.waitForSocketOpen()
      if (!socketReady) {
        this.serverError = 'Нет соединения с сервером. Попробуйте снова.'
        return
      }

      this.serverError = ''
      this.infoMessage = 'Ответ отправлен. Ожидаем соперника...'
      this.submittedAnswer = this.currentAnswer.trim()
      this.mySubmitted = true

      this.ws.send(JSON.stringify({
        command: 'submit_answer',
        answer: this.submittedAnswer,
      }))
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
}

.left-panel {
  width: 280px;
  padding: 20px 15px;
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
  font-size: 14px;
  color: #333;
  margin-bottom: 3px;
  font-weight: 700;
}

.player-score {
  font-size: 13px;
  color: #666;
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
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-line {
  font-size: 13px;
  color: #4a4a4a;
}

.content-area {
  flex: 1;
  padding: 30px 40px;
  display: flex;
  flex-direction: column;
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
}

.score-you,
.score-opponent {
  font-size: 18px;
  font-weight: 700;
}

.score-you {
  color: #1565c0;
}

.score-opponent {
  color: #e53935;
}

.vs {
  font-size: 11px;
  color: #666;
  font-weight: 600;
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
  min-width: 140px;
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
  margin-top: 10px;
}

.info-message {
  color: #1565c0;
  font-size: 14px;
  padding: 8px 12px;
  background: #e3f2fd;
  border-radius: 6px;
  border-left: 4px solid #1565c0;
  margin-top: 10px;
}

.finish-section {
  margin-top: auto;
}

.finish-button {
  width: 100%;
  padding: 18px;
  background: linear-gradient(135deg, #90a4ae, #78909c);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: 700;
  cursor: not-allowed;
}

@media (max-width: 1024px) {
  .main-container {
    flex-direction: column;
  }

  .left-panel {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e8e8e8;
  }

  .panel-content {
    position: static;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
  }

  .content-area {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .panel-content {
    grid-template-columns: 1fr;
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
}
</style>
