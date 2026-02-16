<template>
  <div>
    <head>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
      <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Open+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    </head>
    
    <HeaderEnter />
    
    <div class="achievements-page">
      <div class="achievements-header">
        <h1 class="page-title">
          Мои достижения
        </h1>
      </div>

      <div class="achievements-grid">
        <div 
          v-for="item in this.achievementsList" 
          :key="item.id"
          class="achievement-card" 
          :class="{ 'achievement-card-done': item.completed }"
        >
          <div class="card-header">
            <div class="icon-wrapper" :style="{ background: item.bgColor + '20' }">
              <a :class="item.icon" :style="{ color: item.bgColor }">{{ item.icon }}</a>
            </div>
            <div class="status-badge" :class="item.status=='earned' ? 'status-done' : (item.status=='in_progress' ? 'status-working' : 'status-waiting')">
              <i :class="item.status=='earned' ? 'fas fa-check-circle' : (item.status=='in_progress'? 'fas fa-spinner' : 'fas fa-lock')"></i>
              <span>{{ item.status=='earned' ? 'Выполнено' : (item.status=='in_progress' ? 'В процессе' : 'Закрыто') }}</span>
            </div>
          </div>

          <h3 class="achievement-title">{{ item.title }}</h3>
          <p class="achievement-desc">{{ item.description }}</p>

          <div class="progress-section">
            <div class="progress-info">
              <span class="progress-text">
                {{ item.progress.solved }}/{{ item.progress.needed }}
              </span>
              <span class="progress-percent">{{ Math.floor((item.progress.solved / item.progress.needed) * 100) }}%</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ 
                  width: (item.progress.solved / item.progress.needed) * 100 + '%',
                  background: item.completed ? '#06D6A0' : '#4A7B9D'
                }"
              ></div>
            </div>
          </div>

          <div class="card-footer">
            <span class="difficulty-badge" :class="'difficulty-' + item.difficultyLevel">
              <i v-if="item.difficultyLevel === 'Эксперт'" class="fas fa-crown"></i>
              {{ item.difficultyLevel }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderEnter from '@/components/HeaderEnter.vue';
import axios from 'axios';

export default {
  name: 'AchievementsPage',
  components: { HeaderEnter },

  data() {
    return {
      achievementsList: [],
    }
  },

  mounted() {
    this.loadAchievementsData()
    //this.loadSavedProgress()
    
    // тут потом надо будет добавить нормальную обработку ошибок
    console.log('страница загружена')
  },

  methods: {
    async loadAchievementsData() {
        try {
            const token = localStorage.getItem('authToken')
            const response = await axios.get('http://localhost:8000/api/badges/', {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            })
            this.achievementsList = response.data
            console.log(response.data)

        } catch (err) {
            this.errorMessage = err.response?.data?.detail || 'Ошибка';
        } finally {
            this.isLoading = false;
        }
    },

    //loadSavedProgress() {
    //  const savedData = localStorage.getItem('user_achievements_progress')
    //  
    //  if (!savedData) {
    //    return
    //  }
    //  
    //  try {
    //    const parsedData = JSON.parse(savedData)
    //    
    //    for (let i = 0; i < this.achievementsList.length; i++) {
    //      const achievement = this.achievementsList[i]
    //      
    //      for (let j = 0; j < parsedData.length; j++) {
    //        const savedItem = parsedData[j]
    //        
    //        if (achievement.id === savedItem.id) {
    //          // Не перезаписываем выполненные достижения
    //          if (!achievement.completed) {
    //            achievement.currentCount = savedItem.currentCount
    //            achievement.completed = savedItem.completed
    //          }
    //          break
    //        }
    //      }
    //    }
    //    
    //    console.log('прогресс загружен')
    //  } catch (error) {
    //    console.warn('ошибка при загрузке прогресса', error)
    //  }
    //},
//
    //saveProgressToStorage() {
    //  const progressData = []
    //  
    //  for (let i = 0; i < this.achievementsList.length; i++) {
    //    const achievement = this.achievementsList[i]
    //    
    //    progressData.push({
    //      id: achievement.id,
    //      currentCount: achievement.currentCount,
    //      completed: achievement.completed
    //    })
    //  }
    //  
    //  try {
    //    localStorage.setItem(
    //      'user_achievements_progress', 
    //      JSON.stringify(progressData)
    //    )
    //  } catch (error) {
    //    console.warn('ошибка при сохранении прогресса', error)
    //  }
    //}
  },
}
</script>

<style scoped>
.achievements-page {
  background: #FAF6EF;
  min-height: calc(100vh - 100px);
  padding: 40px 30px;
  font-family: 'Open Sans', sans-serif;
}

.achievements-header {
  max-width: 1400px;
  margin: 0 auto 30px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #224762;
  font-family: 'Montserrat', sans-serif;
  letter-spacing: -0.5px;
}

.achievements-grid {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 25px;
}

.achievement-card {
  background: white;
  border-radius: 24px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  border: 1px solid #E8E2D8;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.achievement-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(34, 71, 98, 0.15);
  border-color: #4A7B9D;
}

.achievement-card-done {
  border-left: 6px solid #06D6A0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.status-badge {
  padding: 8px 16px;
  border-radius: 40px;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'Montserrat', sans-serif;
}

.status-done {
  background: #d4edc9;
  color: #1f5e2d;
}

.status-working {
  background: #fff2d9;
  color: #a76100;
}

.status-waiting {
  background: #edf0f5;
  color: #5a6a7c;
}

.achievement-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #224762;
  margin-bottom: 10px;
  font-family: 'Montserrat', sans-serif;
}

.achievement-desc {
  color: #5A6C7D;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 20px;
  min-height: 45px;
  font-family: 'Open Sans', sans-serif;
}

.progress-section {
  margin-bottom: 20px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #224762;
  font-family: 'Montserrat', sans-serif;
}

.progress-text {
  display: flex;
  align-items: center;
  gap: 6px;
}

.progress-bar {
  height: 8px;
  background: #E8E2D8;
  border-radius: 20px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 20px;
  transition: width 0.3s ease;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #F0EBE2;
}

.difficulty-badge {
  padding: 6px 12px;
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'Montserrat', sans-serif;
}

.difficulty-Начинающий {
  background: #E8F5E9;
  color: #2E7D32;
}

.difficulty-Средний {
  background: #FFF3E0;
  color: #F57C00;
}

.difficulty-Сложный {
  background: #FFEBEE;
  color: #C62828;
}

.difficulty-Эксперт {
  background: #F1C40F;
  color: #224762;
}

@media (max-width: 768px) {
  .achievements-page {
    padding: 20px 15px;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .achievement-card {
    padding: 20px;
  }
  
  .achievement-title {
    font-size: 1.2rem;
  }
}
</style>
