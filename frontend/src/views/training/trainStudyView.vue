<template>
  <div class="training-page">
    <div class="training-container">
      
      <!-- Шапка -->
      <div class="training-header">
        <div class="subject-info">
          <span class="subject-name">{{ subjectName }}</span>
          <span class="difficulty-badge-header">
            {{ difficultyName }}
          </span>
        </div>
      </div>
      
      <!-- Задания -->
      <div class="tasks-list">
        <div class="task-header">
          <div class="task-title">
            <span class="task-number">{{ taskNumber }}</span>
            <span :class="[
                  'difficulty-badge', 
                  currentTask?.difficulty === 'easy' ? 'easy' : 
                  currentTask?.difficulty === 'medium' ? 'medium' : 'hard'
                ]">{{ currentTask?.difficulty }}</span> 
          </div>
        </div>
        
        <div class="task-text">
          {{ currentTask?.text }}
        </div>
        
        <div class="task-answer">
          <div class="answer-input-section">
            <div class="answer-label">Введите ваш ответ:</div>
            <div 
              class="input-wrapper" 
              :class="{ 
                'saved-border': saved,
                'error-border': error 
              }"
            >
              <input 
                type="text" 
                v-model="answer"
                class="answer-input"
                :placeholder="'Введите ответ здесь...'"
                @keyup.enter="saveTask()"
                @input="error = false"
              >
            </div>
            <div class="action-row">
              <button 
                class="save-answer-btn" 
                @click="saveTask()"
                :disabled="!answer?.trim()"
              >
                Сохранить
              </button>
              <span v-if="error" class="error-message">
                {{ error }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="finish-section">
        <div v-if="error" class="error-banner">
          {{ error }}
        </div>
          <span class="finish-count">{{ taskNumber }}/{{ tasksCount }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios';

export default {
  name: 'TrainingPage',
  
  setup() {
    // Реактивные переменные
    const config = ref(null)
    const currentTask = ref(null)
    const answer = ref('')
    const saved = ref(false)
    const tasksCount = ref(0)
    const taskNumber = ref(0)
    const taskIndex = ref(null)
    const tasks = ref([])
    const subjectName = ref('')
    const difficultyName = ref('')
    const isLoading = ref(false)
    const error = ref('')
    const sessionId = ref(null)
    const results = ref(0)

    // Загружаем конфигурацию при монтировании
    onMounted(() => {
      loadConfig()
    })

    function loadConfig() {
      try {
        const raw = localStorage.getItem('created')
        if (!raw) {
          error.value = 'Настройки не найдены'
          return
        }
        
        const parsed = JSON.parse(raw)
        config.value = parsed
        
        // Инициализируем реактивные переменные из конфига
        sessionId.value = config.value.session_id
        currentTask.value = config.value.task
        tasksCount.value = config.value.total_tasks
        taskNumber.value = config.value.current_task_index
        taskIndex.value = config.value.task.id
        
        // Загружаем названия предмета и сложности
        const subjects = {
          math: 'МАТЕМАТИКА',
          geom: 'ГЕОМЕТРИЯ',
          d_math: "ДИСКРЕТНАЯ МАТЕМАТИКА",
          phys: 'ФИЗИКА',
          chem: 'ХИМИЯ',
          bio: 'БИОЛОГИЯ',
          eco: 'ЭКОЛОГИЯ',
          geo: 'ГЕОГРАФИЯ',
          astro: 'АСТРОНОМИЯ',
          rus_lang: 'РУССКИЙ ЯЗЫК',
          rus_lit: 'ЛИТЕРАТУРА',
          eng_lang: 'АНГЛИЙСКИЙ ЯЗЫК',
          ger_lang: 'НЕМЕЦКИЙ ЯЗЫК',
          fr_lang: 'ФРАНЦУЗСКИЙ ЯЗЫК',
          chi_lang: 'КИТАЙСКИЙ ЯЗЫК',
          sp_lang: 'ИСПАНСКИЙ ЯЗЫК',
          lat_lang: 'ЛАТИНСКИЙ ЯЗЫК',
          hist: 'ИСТОРИЯ',
          soc_st: 'ОБЩЕСТВОЗНАНИЕ',
          law: 'ПРАВО',
          econ: 'ЭКОНОМИКА',
          fin_lit: 'ФИНАНСОВАЯ ГРАМОТНОСТЬ',
          arts: 'ИСКУССТВО (МХК)',
          tech: 'ТЕХНОЛОГИЯ',
          Infinity: 'ИНФОРМАТИКА',
          robot: 'РОБОТОТЕХНИКА',
          ai: 'ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ',
          pe: 'ФИЗКУЛЬТУРА',
          obzh: 'ОБЖ'
        }
        
        const difficulties = {
          easy: 'ЛЁГКАЯ',
          medium: 'СРЕДНЯЯ',
          hard: 'СЛОЖНАЯ',
          random: 'ЛЮБАЯ'
        }

        subjectName.value = subjects[parsed.subject] || 'ПРЕДМЕТ'
        difficultyName.value = difficulties[parsed.difficulty] || 'СРЕДНЯЯ'
        error.value = ''
        
        // Очищаем поле ответа для нового задания
        answer.value = ''
        saved.value = false
        
      } catch (e) {
        error.value = 'Ошибка загрузки настроек'
        console.error(e)
      }
    }

    async function saveTask() {
      if (!answer.value?.trim()) {
        error.value = 'Введите ответ'
        return
      }

      try {
        isLoading.value = true
        error.value = ''
        
        const token = localStorage.getItem('authToken');
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        const response = await axios.post('http://localhost:8000/api/training/submit/', {
            'session_id': sessionId.value,
            'task_id': taskIndex.value,
            'answer': answer.value
        });

        // Получаем новый конфиг из ответа
        const newConfig = response.data
        if (newConfig.message=='Верно!') {
            results.value += 1
            localStorage.setItem('trainingResults', JSON.parse(JSON.stringify(results))._value)
            console.log('Correct: ',JSON.parse(JSON.stringify(results))._value)
        }
        console.log(response.data)
        
        if (newConfig.next_task) {
          // Обновляем конфиг в localStorage
          localStorage.setItem('created', JSON.stringify(newConfig))
          
          // Обновляем все реактивные переменные
          config.value = newConfig
          currentTask.value = newConfig.next_task
          taskNumber.value = newConfig.current_task_index
          taskIndex.value = newConfig.next_task.id
          
          // Очищаем поле ответа и показываем успех
          answer.value = ''
          saved.value = true
          
          // Убираем индикатор сохранения через 2 секунды
          setTimeout(() => {
            saved.value = false
          }, 2000)
        } else {
          // Если нет следующего задания, значит тренировка завершена
          finish()
        }

      } catch (e) {
        error.value = e.response?.data?.error || 'Не удалось сохранить ответ'
        console.error('Save error:', e)
      } finally {
        isLoading.value = false
      }
    }

    async function finish() {
      try {
        localStorage.removeItem('created')
        
        // Перенаправляем на страницу результатов
        window.location.href = '/training/result'
      } catch (e) {
        error.value = 'Не удалось завершить'
        console.error(e)
      }
    }

    const savedCount = computed(() => 
      tasks.value.filter(t => t.saved).length
    )
    
    const hasChanges = computed(() => 
      savedCount.value > 0
    )

    return {
      currentTask,
      answer,
      saved,
      tasksCount,
      taskNumber,
      tasks,
      subjectName,
      difficultyName,
      savedCount,
      hasChanges,
      isLoading,
      error,
      saveTask,
      finish
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.training-page {
  min-height: 100vh;
  background: rgb(250, 246, 239);
  display: flex;
  justify-content: center;
  padding: 40px 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.training-container {
  max-width: 900px;
  width: 100%;
}

/* Шапка */
.training-header {
  background: white;
  border-radius: 15px;
  padding: 25px 35px;
  margin-bottom: 40px;
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

.difficulty-badge-header {
  padding: 12px 28px;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 1px;
  background: #e0e0e0;
  color: #424242;
  border: 3px solid #9e9e9e;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin-bottom: 40px;
}

.task-card {
  background: #ffffff;
  border-radius: 15px;
  padding: 35px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  position: relative;
  overflow: hidden;
}

.task-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: white;
}

.task-header {
  margin-bottom: 30px;
  padding-bottom: 25px;
  border-bottom: 2px solid #cfd8dc;
}

.task-title {
  display: flex;
  align-items: center;
  gap: 20px;
}

.task-number {
  color: #000000;
  font-size: 24px;
  font-weight: 900;
  letter-spacing: 0.5px;
  padding: 5px 0;
  border-bottom: 3px solid #000000;
}

.difficulty-badge {
  padding: 10px 22px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 1px;
  border: 3px solid;
  display: inline-block;
}

.difficulty-badge.easy {
  background: #E8F5E9;
  color: #43A047;
  border-color: #43A047;
}

.difficulty-badge.medium {
  background: #FFF3E0;
  color: #FB8C00;
  border-color: #FB8C00;
}

.difficulty-badge.hard {
  background: #FFEBEE;
  color: #E53935;
  border-color: #E53935;
}

.task-text {
  font-size: 18px;
  line-height: 1.8;
  color: #263238;
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 12px;
  border: 2px solid #cfd8dc;
  font-weight: 500;
}

.task-answer {
  border-radius: 12px;
  padding: 20px 0;
}

.answer-input-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
  position: relative;
}

.answer-label {
  font-size: 16px;
  font-weight: 700;
  color: #1565c0;
}

.input-wrapper {
  display: block;
  width: 100%;
  border-radius: 10px;
  transition: all 0.3s;
}

.input-wrapper.error-border {
  box-shadow: 0 0 0 3px #ffcdd2;
}

.answer-input {
  padding: 16px 20px;
  border: 3px solid #b0bec5;
  border-radius: 10px;
  font-size: 16px;
  color: #263238;
  background: #ffffff;
  transition: all 0.3s;
  font-family: inherit;
  width: 100%;
}

.answer-input:focus {
  outline: none;
  border-color: #1e88e5;
  box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.2);
}

.action-row {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.save-answer-btn {
  padding: 16px 28px;
  background: linear-gradient(135deg, #1e88e5, #1565c0);
  color: #ffffff;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  align-self: flex-start;
}

.save-answer-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 136, 229, 0.4);
}

.save-answer-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.error-message {
  color: #e53935;
  font-size: 14px;
  font-weight: 500;
}

.finish-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  padding: 20px 0;
}

.error-banner {
  background: #ffebee;
  color: #c62828;
  padding: 12px 24px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 15px;
  border: 1px solid #ef9a9a;
}

.finish-btn {
  padding: 18px 50px;
  background: #263238;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  letter-spacing: 1px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.finish-btn:hover:not(:disabled) {
  background: #37474f;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.finish-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.finish-count {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

@media (max-width: 768px) {
  .training-page {
    padding: 20px 15px;
  }
  
  .training-header {
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
  
  .task-card {
    padding: 25px;
  }
  
  .task-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .task-title {
    flex-wrap: wrap;
  }
  
  .save-answer-btn {
    align-self: stretch;
    width: 100%;
  }
  
  .finish-btn {
    width: 100%;
  }
  
  .action-row {
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .training-header {
    padding: 15px 20px;
  }
  
  .subject-name {
    font-size: 22px;
  }
  
  .difficulty-badge-header {
    padding: 10px 20px;
    font-size: 14px;
  }
  
  .task-card {
    padding: 20px;
  }
  
  .task-number {
    font-size: 20px;
  }
  
  .difficulty-badge {
    padding: 8px 16px;
    font-size: 12px;
  }
  
  .task-text {
    font-size: 16px;
    padding: 15px;
  }
  
  .answer-input {
    padding: 14px 16px;
    font-size: 15px;
  }
}
</style>
