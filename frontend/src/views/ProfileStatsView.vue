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
            <div class="quick-stat-number">{{ userData?.total_attempts || 0 }}</div>
            <div class="quick-stat-label">Всего тестов</div>
          </div>
          <div class="quick-stat">
            <div class="quick-stat-number">{{ userData?.accuracy_percent || 0 }}%</div>
            <div class="quick-stat-label">Правильных</div>
          </div>
          <div class="quick-stat">
            <div class="quick-stat-number">{{ pvpBattles }}</div>
            <div class="quick-stat-label">PvP сражений</div>
          </div>
        </div>
      </div>

      <div class="charts-container">
        <div class="chart-card full-width">
          <div class="chart-header">
            <h3 class="chart-title">
              <i class="fas fa-chart-pie"></i> Общая статистика по всем предметам
            </h3>
            <div class="chart-subtitle">
              Распределение тестов по предметам с показателями точности
            </div>
          </div>
          
          <div class="chart-content-wrapper">
            <div class="chart-main-area">
              <div class="donut-chart-container">
                <canvas ref="overallChart"></canvas>
                <div class="chart-center-info">
                  <div class="total-tests">{{ totalTestsAllSubjects }}</div>
                  <div class="center-label">Всего тестов</div>
                  <div class="avg-accuracy">{{ avgAccuracy }}%</div>
                  <div class="center-label">Средняя точность</div>
                </div>
              </div>
              
              <div class="chart-legend">
                <div class="legend-header">
                  <span class="legend-title">Предметы</span>
                  <span class="legend-subtitle">Доля от всех тестов</span>
                </div>
                <div class="legend-items-container">
                  <div v-for="(subject, index) in chartData" :key="subject.subject_name" 
                       class="legend-item" @mouseover="highlightSegment(index)" @mouseleave="unhighlightSegment()">
                    <div class="legend-color" :style="{ backgroundColor: subjectColors[index] }"></div>
                    <div class="legend-info">
                      <div class="legend-name">{{ subject.subject_name }}</div>
                      <div class="legend-details">
                        <span class="legend-accuracy">{{ Math.round(subject.accuracy * 100) }}%</span>
                        <span class="legend-count">{{ subject.total_attempts }} тестов</span>
                      </div>
                    </div>
                    <div class="legend-percentage">{{ calculatePercentage(subject) }}%</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="chart-summary-stats">
              <div class="summary-stat">
                <div class="summary-icon">
                  <i class="fas fa-star"></i>
                </div>
                <div class="summary-content">
                  <div class="summary-value">{{ bestSubjectName }}</div>
                  <div class="summary-label">Лучший предмет</div>
                  <div class="summary-extra">Точность: {{ bestSubjectAccuracy }}%</div>
                </div>
              </div>
              
              <div class="summary-stat">
                <div class="summary-icon">
                  <i class="fas fa-bullseye"></i>
                </div>
                <div class="summary-content">
                  <div class="summary-value">{{ subjectsWithHighAccuracy }}</div>
                  <div class="summary-label">Предметы выше 80%</div>
                  <div class="summary-extra">Хорошие результаты</div>
                </div>
              </div>
              
              <div class="summary-stat">
                <div class="summary-icon">
                  <i class="fas fa-books"></i>
                </div>
                <div class="summary-content">
                  <div class="summary-value">{{ chartData.length }}</div>
                  <div class="summary-label">Всего предметов</div>
                  <div class="summary-extra">Активная учебная программа</div>
                </div>
              </div>
              
              <div class="summary-stat">
                <div class="summary-icon">
                  <i class="fas fa-trophy"></i>
                </div>
                <div class="summary-content">
                  <div class="summary-value">{{ mostTestsSubjectName }}</div>
                  <div class="summary-label">Самый изучаемый</div>
                  <div class="summary-extra">{{ mostTestsCount }} тестов</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="detailed-stats">
        <h3 class="section-title">
          <i class="fas fa-list-alt"></i> Подробная статистика по предметам
        </h3>
        
        <div class="subjects-grid">
          <div v-for="subject in chartData" :key="subject.subject_name" class="subject-card">
            <div class="subject-header">
              <div class="subject-icon">
                <i :class="getSubjectIcon(subject.subject_name)"></i>
              </div>
              <div class="subject-title">
                <h4>{{ subject.subject_name }}</h4>
                <span class="subject-tests">{{ subject.total_attempts }} тестов</span>
              </div>
            </div>
            
            <div class="subject-progress">
              <div class="progress-info">
                <span class="progress-label">Точность</span>
                <span class="progress-value">{{ Math.round(subject.accuracy * 100) }}%</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ 
                  width: subject.accuracy * 100 + '%',
                  background: getAccuracyColor(subject.accuracy)
                }"></div>
              </div>
            </div>
            
            <div class="subject-stats">
              <div class="stat-item">
                <div class="stat-icon">
                  <i class="fas fa-check-circle"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ Math.round(subject.accuracy * subject.total_attempts) }}</div>
                  <div class="stat-label">Правильных</div>
                </div>
              </div>
              
              <div class="stat-item">
                <div class="stat-icon">
                  <i class="fas fa-chart-line"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ Math.round(subject.accuracy * 100) }}%</div>
                  <div class="stat-label">Успеваемость</div>
                </div>
              </div>
            </div>
            
            <div class="subject-percentage">
              <div class="percentage-circle" :style="{
                background: `conic-gradient(${getSubjectColor(subject.subject_name)} ${subjectPercentage(subject)}%, #f0f0f0 0%)`
              }">
                <div class="percentage-inner">
                  {{ subjectPercentage(subject) }}%
                </div>
              </div>
              <div class="percentage-label">Доля от всех тестов</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import HeaderEnter from '@/components/HeaderEnter.vue'
import axios from 'axios';

export default {
  name: 'ProfileStats',
  
  components: {
    HeaderEnter
  },

  data() {
    return {
      userData: '',
      colors: []
    }
  },
  
  setup() {
    const router = useRouter()
    
    const overallChart = ref(null)
    const chartInstance = ref(null)
    
    const userData = ref({
      username: 'bentalin',
    })
    
    const userId = '2562341'
    const pvpBattles = ref(0)
    
    const chartData = ref([
      { subject_name: 'Математика', total_attempts: 28, accuracy: 0.92 },
      { subject_name: 'Физика', total_attempts: 22, accuracy: 0.87 },
      { subject_name: 'Химия', total_attempts: 18, accuracy: 0.83 },
      { subject_name: 'Информатика', total_attempts: 24, accuracy: 0.91 },
      { subject_name: 'Биология', total_attempts: 20, accuracy: 0.81 },
      { subject_name: 'Русский язык', total_attempts: 25, accuracy: 0.88 },
      { subject_name: 'Английский язык', total_attempts: 30, accuracy: 0.85 },
      { subject_name: 'Литература', total_attempts: 18, accuracy: 0.82 },
      { subject_name: 'История', total_attempts: 16, accuracy: 0.79 },
      { subject_name: 'География', total_attempts: 14, accuracy: 0.77 },
    ])
    
    // Красивая цветовая палитра для диаграммы
    const subjectColors = [
      '#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2',
      '#9D4EDD', '#FF9E6D', '#073B4C', '#EF476F', '#7209B7',
      '#3A86FF', '#FB5607', '#8338EC', '#FF006E', '#3A86FF'
    ]
    
    const getSubjectIcon = (subjectName) => {
      const icons = {
        'Математика': 'fas fa-calculator',
        'Физика': 'fas fa-atom',
        'Химия': 'fas fa-flask',
        'Информатика': 'fas fa-laptop-code',
        'Биология': 'fas fa-dna',
        'Русский язык': 'fas fa-language',
        'Английский язык': 'fas fa-globe',
        'Литература': 'fas fa-book',
        'История': 'fas fa-landmark',
        'География': 'fas fa-globe-americas',
        'default': 'fas fa-graduation-cap'
      }
      return icons[subjectName] || icons.default
    }
    
    const getAccuracyColor = (accuracy) => {
      if (accuracy >= 0.9) return 'linear-gradient(90deg, #06D6A0, #4ECDC4)'
      if (accuracy >= 0.8) return 'linear-gradient(90deg, #118AB2, #3A86FF)'
      if (accuracy >= 0.7) return 'linear-gradient(90deg, #FFD166, #FF9E6D)'
      return 'linear-gradient(90deg, #EF476F, #FF6B6B)'
    }
    
    const getSubjectColor = (subjectName) => {
      // Простое хеширование для получения цвета
      let hash = 0
      for (let i = 0; i < subjectName.length; i++) {
        hash = subjectName.charCodeAt(i) + ((hash << 5) - hash)
      }
      return subjectColors[Math.abs(hash) % subjectColors.length]
    }
    
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
    
    // Вычисляемые свойства для статистики
    const totalTestsAllSubjects = computed(() => {
      return chartData.value.reduce((sum, subject) => sum + subject.total_attempts, 0)
    })
    
    const avgAccuracy = computed(() => {
      if (chartData.value.length === 0) return 0
      const totalAccuracy = chartData.value.reduce((sum, subject) => 
        sum + (subject.accuracy * subject.total_attempts), 0)
      return Math.round((totalAccuracy / totalTestsAllSubjects.value) * 100)
    })
    
    const bestSubjectName = computed(() => {
      if (chartData.value.length === 0) return 'Нет данных'
      const best = chartData.value.reduce((prev, current) => 
        (prev.accuracy > current.accuracy) ? prev : current
      )
      return best.subject_name
    })
    
    const bestSubjectAccuracy = computed(() => {
      if (chartData.value.length === 0) return 0
      const best = chartData.value.reduce((prev, current) => 
        (prev.accuracy > current.accuracy) ? prev : current
      )
      return Math.round(best.accuracy * 100)
    })
    
    const subjectsWithHighAccuracy = computed(() => {
      return chartData.value.filter(subject => subject.accuracy >= 0.8).length
    })
    
    const mostTestsSubjectName = computed(() => {
      if (chartData.value.length === 0) return 'Нет данных'
      const most = chartData.value.reduce((prev, current) => 
        (prev.total_attempts > current.total_attempts) ? prev : current
      )
      return most.subject_name
    })
    
    const mostTestsCount = computed(() => {
      if (chartData.value.length === 0) return 0
      const most = chartData.value.reduce((prev, current) => 
        (prev.total_attempts > current.total_attempts) ? prev : current
      )
      return most.total_attempts
    })
    
    const calculatePercentage = (subject) => {
      if (totalTestsAllSubjects.value === 0) return 0
      return Math.round((subject.total_attempts / totalTestsAllSubjects.value) * 100)
    }
    
    const subjectPercentage = (subject) => {
      return calculatePercentage(subject)
    }
    
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('authToken')
        if (!token) {
          router.push('/auth')
          return
        }

        const response = await axios.get('http://localhost:8000/api/auth/profile/', {
          headers: {
            'Authorization': `Token ${token}`
          }
        })
        
        userData.value = response.data

      } catch (err) {
        console.error('Ошибка при загрузке данных пользователя:', err)
        router.push('/auth')
      }
    }

    const getAnalytics = async () => {
      try {
        const token = localStorage.getItem('authToken')
        if (!token) {
          router.push('/auth')
          return
        }
        
        console.log(token);

        const response = await axios.get('http://localhost:8000/api/analytics/overall/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        userData.value = response.data;
        console.log(userData.value);

      } catch (err) {
        console.error('Ошибка при загрузке статистики пользователя:', err)
      } 
    }

    const getAnalyticsSubjects = async () => {
      try {
        const token = localStorage.getItem('authToken')
        if (!token) {
          router.push('/auth')
          return
        }
        
        console.log(token);

        const response = await axios.get('http://localhost:8000/api/analytics/subjects/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        chartData.value = response.data;
        console.log('Статистика по предметам:', chartData.value);

        // После получения данных рендерим график
        await nextTick()
        renderChart()

      } catch (err) {
        console.error('Ошибка при загрузке статистики по предметам:', err)
      } 
    }
    
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
    
    const highlightSegment = (index) => {
      if (chartInstance.value) {
        chartInstance.value.setActiveElements([{ datasetIndex: 0, index }])
        chartInstance.value.update()
      }
    }
    
    const unhighlightSegment = () => {
      if (chartInstance.value) {
        chartInstance.value.setActiveElements([])
        chartInstance.value.update()
      }
    }
    
    const renderChart = async () => {
      try {
        const Chart = await loadChartJS()
        
        // Уничтожаем предыдущий график, если он есть
        if (chartInstance.value) {
          chartInstance.value.destroy()
        }
        
        if (!overallChart.value) {
          console.error('Canvas element not found')
          return
        }
        
        const ctx = overallChart.value.getContext('2d')
        
        // Создаем градиенты для каждого сегмента
        const createGradient = (color) => {
          const gradient = ctx.createLinearGradient(0, 0, 0, 400)
          gradient.addColorStop(0, color)
          gradient.addColorStop(1, darkenColor(color, 0.3))
          return gradient
        }
        
        const darkenColor = (color, amount) => {
          let usePound = false
          if (color[0] === "#") {
            color = color.slice(1)
            usePound = true
          }
          
          const num = parseInt(color, 16)
          let r = (num >> 16) + (255 - (num >> 16)) * amount
          let b = ((num >> 8) & 0x00FF) + (255 - ((num >> 8) & 0x00FF)) * amount
          let g = (num & 0x0000FF) + (255 - (num & 0x0000FF)) * amount
          
          r = Math.min(255, Math.max(0, r))
          g = Math.min(255, Math.max(0, g))
          b = Math.min(255, Math.max(0, b))
          
          return (usePound ? "#" : "") + 
            (Math.round(r) | 1 << 8).toString(16).slice(1) +
            (Math.round(g) | 1 << 8).toString(16).slice(1) +
            (Math.round(b) | 1 << 8).toString(16).slice(1)
        }
        
        // Подготавливаем данные для графика
        const labels = chartData.value.map(s => s.subject_name)
        const data = chartData.value.map(s => s.total_attempts)
        const backgroundColors = chartData.value.map((_, index) => 
          createGradient(subjectColors[index % subjectColors.length])
        )
        const hoverColors = chartData.value.map((_, index) => 
          darkenColor(subjectColors[index % subjectColors.length], 0.2)
        )
        
        chartInstance.value = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: labels,
            datasets: [{
              data: data,
              backgroundColor: backgroundColors,
              borderColor: '#fff',
              borderWidth: 3,
              hoverBackgroundColor: hoverColors,
              hoverBorderColor: '#224762',
              hoverBorderWidth: 4,
              hoverOffset: 10
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    const subject = chartData.value[context.dataIndex]
                    const percentage = calculatePercentage(subject)
                    return [
                      `${subject.subject_name}`,
                      `Точность: ${Math.round(subject.accuracy * 100)}%`
                    ]
                  }
                },
                backgroundColor: 'rgba(34, 71, 98, 0.9)',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: '#06D6A0',
                borderWidth: 1,
                padding: 12,
                displayColors: false
              }
            },
            animation: {
              animateScale: true,
              animateRotate: true,
              duration: 1500,
              easing: 'easeOutQuart'
            },
            interaction: {
              intersect: false,
              mode: 'index'
            }
          }
        })
        
        console.log('График успешно отрисован')
        
      } catch (error) {
        console.error('Ошибка отрисовки графика:', error)
        
        // Fallback
        if (overallChart.value) {
          overallChart.value.parentElement.innerHTML = `
            <div class="chart-fallback">
              <i class="fas fa-chart-pie fa-3x"></i>
              <p>График временно недоступен</p>
              <p>Данные по предметам загружены</p>
            </div>
          `
        }
      }
    }
    
    onMounted(() => {
      getAnalytics()
      getAnalyticsSubjects()
    })
    
    onUnmounted(() => {
      if (chartInstance.value) {
        chartInstance.value.destroy()
      }
    })
    
    return {
      overallChart,
      userData,
      userId,
      pvpBattles,
      chartData,
      subjectColors,
      avatarStyle,
      avatarLetter,
      totalTestsAllSubjects,
      avgAccuracy,
      bestSubjectName,
      bestSubjectAccuracy,
      subjectsWithHighAccuracy,
      mostTestsSubjectName,
      mostTestsCount,
      getSubjectIcon,
      getAccuracyColor,
      getSubjectColor,
      calculatePercentage,
      subjectPercentage,
      highlightSegment,
      unhighlightSegment,
      handleBack
    }
  },
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
  transition: transform 0.3s ease;
}

.quick-stat:hover {
  transform: translateY(-5px);
  background: #F0EBE2;
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
  margin-bottom: 40px;
}

.chart-card.full-width {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(34, 71, 98, 0.08);
  border: 1px solid #E8E2D8;
}

.chart-header {
  margin-bottom: 30px;
}

.chart-title {
  color: #224762;
  font-size: 24px;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 8px 0;
}

.chart-title i {
  color: #FF6B6B;
}

.chart-subtitle {
  color: #7A8A9B;
  font-size: 14px;
}

.chart-content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.chart-main-area {
  display: flex;
  gap: 40px;
  align-items: center;
  min-height: 300px;
}

.donut-chart-container {
  position: relative;
  width: 300px;
  height: 300px;
  flex-shrink: 0;
}

.chart-center-info {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 1;
}

.total-tests {
  font-size: 32px;
  font-weight: bold;
  color: #224762;
  font-family: 'Alexandria', sans-serif;
}

.center-label {
  font-size: 12px;
  color: #7A8A9B;
  margin: 2px 0;
}

.avg-accuracy {
  font-size: 18px;
  font-weight: 600;
  color: #06D6A0;
  margin-top: 8px;
}

.chart-legend {
  flex: 1;
  background: #FAF6EF;
  border-radius: 12px;
  padding: 20px;
  max-height: 300px;
  overflow-y: auto;
}

.legend-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #E8E2D8;
}

.legend-title {
  font-weight: 600;
  color: #224762;
}

.legend-subtitle {
  font-size: 12px;
  color: #7A8A9B;
}

.legend-items-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.legend-item:hover {
  background: white;
  transform: translateX(5px);
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  flex-shrink: 0;
}

.legend-info {
  flex: 1;
}

.legend-name {
  font-weight: 600;
  color: #2C3E50;
  font-size: 14px;
  margin-bottom: 2px;
}

.legend-details {
  display: flex;
  gap: 10px;
  font-size: 12px;
}

.legend-accuracy {
  color: #06D6A0;
  font-weight: 600;
}

.legend-count {
  color: #7A8A9B;
}

.legend-percentage {
  font-weight: bold;
  color: #224762;
  font-size: 16px;
}

.chart-summary-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.summary-stat {
  background: #FAF6EF;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  gap: 15px;
  align-items: center;
  transition: all 0.3s ease;
}

.summary-stat:hover {
  background: #F0EBE2;
  transform: translateY(-3px);
}

.summary-icon {
  width: 50px;
  height: 50px;
  background: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #224762;
}

.summary-content {
  flex: 1;
}

.summary-value {
  font-size: 18px;
  font-weight: bold;
  color: #224762;
  margin-bottom: 4px;
}

.summary-label {
  font-size: 12px;
  color: #7A8A9B;
  margin-bottom: 2px;
}

.summary-extra {
  font-size: 10px;
  color: #06D6A0;
  font-weight: 600;
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
  color: #224762;
  font-size: 24px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.subject-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #E8E2D8;
  transition: all 0.3s ease;
}

.subject-card:hover {
  box-shadow: 0 8px 25px rgba(34, 71, 98, 0.1);
  transform: translateY(-5px);
  border-color: #118AB2;
}

.subject-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.subject-icon {
  width: 40px;
  height: 40px;
  background: #FAF6EF;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #224762;
}

.subject-title h4 {
  margin: 0;
  font-size: 16px;
  color: #224762;
  font-weight: 600;
}

.subject-tests {
  font-size: 12px;
  color: #7A8A9B;
}

.subject-progress {
  margin-bottom: 20px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.progress-label {
  font-size: 12px;
  color: #7A8A9B;
}

.progress-value {
  font-size: 14px;
  font-weight: 600;
  color: #224762;
}

.progress-bar {
  height: 8px;
  background: #F0EBE2;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 1.5s ease;
}

.subject-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  gap: 10px;
  align-items: center;
}

.stat-icon {
  width: 32px;
  height: 32px;
  background: #FAF6EF;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #224762;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 16px;
  font-weight: bold;
  color: #224762;
  margin-bottom: 2px;
}

.stat-label {
  font-size: 10px;
  color: #7A8A9B;
}
</style>