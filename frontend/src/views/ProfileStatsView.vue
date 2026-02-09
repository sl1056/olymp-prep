<template>
  <div class="profile-stats-page">
    <head>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    </head>
    <HeaderEnter />
    
    <div class="container">
      <div class="back-section">
        <button class="back-btn" @click="handleBack">
          <i class="fas fa-arrow-left"></i> Назад к профилю
        </button>
        <h1 class="page-title">Полная статистика</h1>
      </div>

      <div class="user-card">
        <div class="user-header">
          <div class="user-avatar" :style="avatarStyle">
            {{ avatarLetter }}
          </div>
          <div class="user-info">
            <h2 class="username">{{ userData?.username || 'Пользователь' }}</h2>
            <div class="user-id">ID: {{ userId }}</div>
          </div>
        </div>
        <div class="quick-stats">
          <div class="quick-stat">
            <div class="quick-stat-number">{{ totalTests }}</div>
            <div class="quick-stat-label">Всего тестов</div>
          </div>
          <div class="quick-stat">
            <div class="quick-stat-number">{{ correctRate }}%</div>
            <div class="quick-stat-label">Правильных</div>
          </div>
          <div class="quick-stat">
            <div class="quick-stat-number">{{ pvpBattles }}</div>
            <div class="quick-stat-label">PvP сражений</div>
          </div>
        </div>
      </div>

      <div class="charts-container">
        <div class="chart-card">
          <div class="chart-header">
            <h3 class="chart-title">
              <i class="fas fa-book"></i> Распределение по предметам
            </h3>
          </div>
          <div class="chart-wrapper">
            <canvas ref="subjectsChart"></canvas>
          </div>
          <div class="chart-summary">
            <div class="summary-item">
              <span class="summary-label">Лучший предмет:</span>
              <span class="summary-value">{{ bestSubject }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Всего предметов:</span>
              <span class="summary-value">{{ subjectsCount }}</span>
            </div>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <h3 class="chart-title">
              <i class="fas fa-bullseye"></i> Точность по категориям
            </h3>
          </div>
          <div class="chart-content">
            <div class="chart-wrapper pie-wrapper">
              <canvas ref="accuracyChart"></canvas>
            </div>
            <div class="accuracy-details">
              <div v-for="category in accuracyData" :key="category.name" class="accuracy-item">
                <div class="category-name">
                  <span class="color-indicator" :style="{ backgroundColor: category.color }"></span>
                  {{ category.name }}
                </div>
                <div class="accuracy-values">
                  <span class="accuracy-percent">{{ category.value }}%</span>
                  <span class="accuracy-count">{{ category.count }} тестов</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="detailed-stats">
        <h3 class="section-title">
          Подробная статистика по предметам
        </h3>
        <div class="subjects-table">
          <div class="table-header">
            <div class="table-col subject-name">Предмет</div>
            <div class="table-col">Пройдено тестов</div>
            <div class="table-col">Средний балл</div>
            <div class="table-col">Лучший результат</div>
          </div>
          <div v-for="subject in detailedSubjects" :key="subject.name" class="table-row">
            <div class="table-col subject-name">
              {{ subject.name }}
            </div>
            <div class="table-col">{{ subject.tests }}</div>
            <div class="table-col">
              <div class="score-bar">
                <div class="score-fill" :style="{ width: subject.avgScore + '%' }"></div>
                <span class="score-text">{{ subject.avgScore }}%</span>
              </div>
            </div>
            <div class="table-col best-score">{{ subject.bestScore }}%</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import HeaderEnter from '@/components/HeaderEnter.vue'
import axios from 'axios';

export default {
  name: 'ProfileStats',
  
  components: {
    HeaderEnter
  },

  async created() {
    await this.getAnalytics();
  },
  
  setup() {
    const router = useRouter()
    
    const subjectsChart = ref(null)
    const accuracyChart = ref(null)
    const chartInstances = ref([])
    
    const userData = ref({
      username: 'bentalin',
    })
    
    const userId = '2562341'
    
    const totalTests = ref(156)
    const correctRate = ref(85)
    const pvpBattles = ref(181)
    
    const subjectsData = ref({
      labels: ['Математика', 'Информатика', 'Физика', 'Английский язык', 'Химия', 'Биология', 'Физкультура', 'Русский язык'],
      data: [92, 89, 87, 85, 83, 81, 88, 86]
    })
    
    const accuracyData = ref([
      { name: 'Математика', value: 92, count: 28, color: '#FF6B6B' },
      { name: 'Естественные науки', value: 85, count: 32, color: '#4ECDC4' },
      { name: 'Языки', value: 82, count: 35, color: '#06D6A0' },
      { name: 'Гуманитарные', value: 78, count: 25, color: '#FFD166' },
      { name: 'Технические', value: 88, count: 18, color: '#EF476F' }
    ])
    
    const detailedSubjects = ref([
      { name: 'Математика', tests: 25, avgScore: 95, bestScore: 100 },
      { name: 'Геометрия', tests: 15, avgScore: 85, bestScore: 96 },
      { name: 'Дискретная математика', tests: 12, avgScore: 78, bestScore: 90 },
      { name: 'Физика', tests: 22, avgScore: 87, bestScore: 98 },
      { name: 'Химия', tests: 18, avgScore: 83, bestScore: 95 },
      { name: 'Биология', tests: 20, avgScore: 81, bestScore: 94 },
      { name: 'Экология', tests: 10, avgScore: 75, bestScore: 88 },
      { name: 'География', tests: 14, avgScore: 77, bestScore: 92 },
      { name: 'Астрономия', tests: 8, avgScore: 72, bestScore: 85 },
      { name: 'Русский язык', tests: 25, avgScore: 88, bestScore: 97 },
      { name: 'Английский язык', tests: 30, avgScore: 85, bestScore: 99 },
      { name: 'Немецкий язык', tests: 12, avgScore: 76, bestScore: 89 },
      { name: 'Французский язык', tests: 10, avgScore: 74, bestScore: 87 },
      { name: 'Китайский язык', tests: 8, avgScore: 68, bestScore: 82 },
      { name: 'Испанский язык', tests: 9, avgScore: 71, bestScore: 85 },
      { name: 'Латинский язык', tests: 5, avgScore: 65, bestScore: 80 },
      { name: 'Литература', tests: 18, avgScore: 82, bestScore: 95 },
      { name: 'История', tests: 16, avgScore: 79, bestScore: 93 },
      { name: 'Обществознание', tests: 14, avgScore: 76, bestScore: 90 },
      { name: 'Право', tests: 10, avgScore: 73, bestScore: 87 },
      { name: 'Экономика', tests: 15, avgScore: 75, bestScore: 92 },
      { name: 'Финансовая грамотность', tests: 12, avgScore: 80, bestScore: 95 },
      { name: 'Информатика', tests: 24, avgScore: 91, bestScore: 98 },
      { name: 'Робототехника', tests: 10, avgScore: 84, bestScore: 96 },
      { name: 'Искусственный интеллект', tests: 8, avgScore: 86, bestScore: 97 },
      { name: 'Технология', tests: 12, avgScore: 78, bestScore: 91 },
      { name: 'Искусство (МХК)', tests: 10, avgScore: 82, bestScore: 94 },
      { name: 'Физкультура', tests: 15, avgScore: 88, bestScore: 99 },
      { name: 'ОБЖ', tests: 8, avgScore: 85, bestScore: 96 }
    ])
    
    const avatarStyle = computed(() => {
      const colors = {
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
      
      const firstLetter = userData.value.username?.charAt(0)?.toUpperCase() || 'И'
      const colorSet = colors[firstLetter] || colors.default
      
      return {
        background: `linear-gradient(135deg, ${colorSet[0]} 0%, ${colorSet[1]} 100%)`
      }
    })
    
    const avatarLetter = computed(() => {
      return userData.value.username?.charAt(0)?.toUpperCase() || 'И'
    })
    
    const bestSubject = computed(() => {
      const maxIndex = subjectsData.value.data.indexOf(Math.max(...subjectsData.value.data))
      return subjectsData.value.labels[maxIndex]
    })
    
    const subjectsCount = computed(() => detailedSubjects.value.length)
    
    const handleBack = () => {
      router.go(-1)
    }
    
    const loadChartJS = () => {
      return new Promise((resolve, reject) => {
        if (typeof window.Chart !== 'undefined') {
          resolve(window.Chart)
          return
        }
        
        const script = document.createElement('script')
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js'
        script.onload = () => {
          console.log('Chart.js загружен')
          resolve(window.Chart)
        }
        script.onerror = () => {
          console.error('Не удалось загрузить Chart.js')
          reject(new Error('Не удалось загрузить Chart.js'))
        }
        document.head.appendChild(script)
      })
    }
    
    const renderCharts = async () => {
      try {
        const Chart = await loadChartJS()
        
        chartInstances.value.forEach(chart => {
          if (chart && typeof chart.destroy === 'function') {
            chart.destroy()
          }
        })
        chartInstances.value = []
        
        if (subjectsChart.value) {
          const subjectsCtx = subjectsChart.value.getContext('2d')
          const subjectsInstance = new Chart(subjectsCtx, {
            type: 'bar',
            data: {
              labels: subjectsData.value.labels,
              datasets: [{
                label: 'Средний балл',
                data: subjectsData.value.data,
                backgroundColor: [
                  '#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0',
                  '#118AB2', '#9D4EDD', '#EF476F', '#073B4C'
                ],
                borderColor: '#333',
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: { display: false }
              },
              scales: {
                y: {
                  beginAtZero: true,
                  max: 100,
                  ticks: {
                    callback: function(value) {
                      return value + '%'
                    }
                  }
                }
              }
            }
          })
          chartInstances.value.push(subjectsInstance)
        }
        
        if (accuracyChart.value) {
          const accuracyCtx = accuracyChart.value.getContext('2d')
          const accuracyInstance = new Chart(accuracyCtx, {
            type: 'doughnut',
            data: {
              labels: accuracyData.value.map(c => c.name),
              datasets: [{
                data: accuracyData.value.map(c => c.value),
                backgroundColor: accuracyData.value.map(c => c.color),
                borderWidth: 2
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              cutout: '60%',
              plugins: {
                legend: { display: false }
              }
            }
          })
          chartInstances.value.push(accuracyInstance)
        }
        
      } catch (error) {
        console.error('Ошибка отрисовки графиков:', error)
        
        document.querySelectorAll('.chart-wrapper').forEach(wrapper => {
          const fallback = document.createElement('div')
          fallback.className = 'chart-fallback'
          fallback.innerHTML = '<p>⚠️ График временно недоступен</p>'
          wrapper.innerHTML = ''
          wrapper.appendChild(fallback)
        })
      }
    }
    
    onMounted(() => {
      setTimeout(() => {
        renderCharts()
      }, 100)
    })
    
    onUnmounted(() => {
      chartInstances.value.forEach(chart => {
        if (chart && typeof chart.destroy === 'function') {
          chart.destroy()
        }
      })
    })
    
    return {
      subjectsChart,
      accuracyChart,
      userData,
      userId,
      totalTests,
      correctRate,
      pvpBattles,
      subjectsData,
      accuracyData,
      detailedSubjects,
      avatarStyle,
      avatarLetter,
      bestSubject,
      subjectsCount,
      handleBack
    }
  },
  methods: {
    async getAnalytics() {
      try {
        const token = localStorage.getItem('authToken');
        if (token) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            const response = await axios.get('http://localhost:8000/api/analytics/overall/');
            this.userData = response.data;
            console.log(response.data)
        }
      } catch (err) {
          console.error('Ошибка при загрузке статистики пользователя:', err);
          this.userData = null;
      } finally {
          this.isLoading = false;
      }
    },
  }

}
</script>

<style scoped>
.profile-stats-page {
  background: #FAF6EF;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 30px;
}

.back-section {
  margin-bottom: 40px;
  position: relative;
}

.back-btn {
  background: white;
  border: 2px solid #E8E2D8;
  color: #224762;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.back-btn:hover {
  background: #224762;
  color: white;
  transform: translateX(-5px);
}

.page-title {
  font-size: 36px;
  color: #224762;
  font-family: 'Alexandria', sans-serif;
  margin: 0;
}

.user-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 40px;
  box-shadow: 0 10px 30px rgba(34, 71, 98, 0.08);
  border: 1px solid #E8E2D8;
}

.user-header {
  display: flex;
  align-items: center;
  gap: 25px;
  margin-bottom: 30px;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: bold;
  color: white;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.user-info {
  flex: 1;
}

.username {
  font-size: 28px;
  color: #224762;
  margin: 0 0 5px 0;
  font-family: 'Alexandria', sans-serif;
}

.user-id {
  color: #7A8A9B;
  font-size: 14px;
}

.quick-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  padding-top: 20px;
  border-top: 2px solid #F0EBE2;
}

.quick-stat {
  text-align: center;
  padding: 15px;
  border-radius: 12px;
  background: #FAF6EF;
}

.quick-stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #224762;
  font-family: 'Alexandria', sans-serif;
}

.quick-stat-label {
  font-size: 14px;
  color: #7A8A9B;
  margin-top: 5px;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 25px;
  margin-bottom: 40px;
}

.chart-card {
  background: white;
  border-radius: 18px;
  padding: 25px;
  box-shadow: 0 8px 25px rgba(34, 71, 98, 0.08);
  border: 1px solid #E8E2D8;
  display: flex;
  flex-direction: column;
  height: 420px;
  min-height: 420px;
  overflow: hidden;
}

.chart-header {
  margin-bottom: 15px;
}

.chart-title {
  color: #224762;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.chart-title i {
  color: #4A7B9D;
}

.chart-wrapper {
  flex: 1;
  min-height: 250px;
  position: relative;
  width: 100%;
  height: 250px;
  margin: 10px 0;
}

.chart-wrapper canvas {
  width: 100% !important;
  height: 100% !important;
  display: block;
}

.chart-content {
  display: flex;
  flex: 1;
  gap: 20px;
  min-height: 250px;
}

.pie-wrapper {
  flex: 0 0 180px;
  height: 180px;
  margin: auto;
}

.accuracy-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 12px;
}

.accuracy-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: #FAF6EF;
  border-radius: 8px;
}

.category-name {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: #2C3E50;
  font-size: 14px;
}

.color-indicator {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.accuracy-values {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 3px;
}

.accuracy-percent {
  font-size: 16px;
  font-weight: bold;
  color: #224762;
  font-family: 'Alexandria', sans-serif;
}

.accuracy-count {
  font-size: 11px;
  color: #7A8A9B;
}

.chart-summary {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #F0EBE2;
  flex-shrink: 0;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.summary-label {
  font-size: 12px;
  color: #7A8A9B;
}

.summary-value {
  font-size: 16px;
  font-weight: 600;
  color: #224762;
}

.chart-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #7A8A9B;
  text-align: center;
  padding: 20px;
  background: #FAF6EF;
  border-radius: 10px;
  border: 2px dashed #E8E2D8;
}

.chart-fallback p {
  margin: 0;
  font-size: 14px;
  color: '#EF476F';
}

.detailed-stats {
  background: white;
  border-radius: 18px;
  padding: 30px;
  margin-bottom: 40px;
  box-shadow: 0 8px 25px rgba(34, 71, 98, 0.08);
  border: 1px solid #E8E2D8;
}

.section-title {
  color: '#224762';
  font-size: 24px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.subjects-table {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #E8E2D8;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  background: '#224762';
  color: white;
  padding: 18px 20px;
  font-weight: 600;
  font-size: 14px;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  padding: 18px 20px;
  border-bottom: 1px solid #F0EBE2;
  align-items: center;
  transition: background 0.3s ease;
}

.table-row:hover {
  background: #FAF6EF;
}

.table-row:last-child {
  border-bottom: none;
}

.table-col {
  color: #000000;
  padding: 0 10px;
}

.subject-name {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  color: #2C3E50;
}

.score-bar {
  width: 100%;
  height: 24px;
  background: #F0EBE2;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, #3d9cd3, #4e9acd);
  border-radius: 12px;
  transition: width 1s ease;
}

.score-text {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  color: #ffffff;
}

.best-score {
  font-weight: bold;
  color: '#06D6A0';
  font-size: 18px;
}

@media (max-width: 1200px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .chart-card {
    height: 400px;
    min-height: 400px;
  }
}

@media (max-width: 900px) {
  .chart-content {
    flex-direction: column;
  }
  
  .pie-wrapper {
    flex: 0 0 200px;
    height: 200px;
  }
  
  .accuracy-details {
    justify-content: flex-start;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 20px;
  }
  
  .charts-container {
    gap: 20px;
  }
  
  .chart-card {
    padding: 20px;
    height: 380px;
    min-height: 380px;
  }
  
  .chart-wrapper {
    height: 220px;
    min-height: 220px;
  }
  
  .quick-stats {
    grid-template-columns: 1fr;
  }
  
  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: 10px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 28px;
  }
  
  .user-header {
    flex-direction: column;
    text-align: center;
  }
  
  .chart-card {
    height: 360px;
    min-height: 360px;
  }
  
  .chart-wrapper {
    height: 200px;
    min-height: 200px;
  }
}
</style>
