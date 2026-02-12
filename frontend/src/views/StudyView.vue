<template>
  <div class="study-page">
    <div class="page-wrapper">
      <!-- Левая панель (оставляем как есть, только меняем классы) -->
      <aside class="navigation-panel">
        <div class="panel-header">
          <h2>ОЛИМПИАДНЫЕ ПРЕДМЕТЫ</h2>
        </div>
        
        <div class="filter-block">
          <h3>СЛОЖНОСТЬ</h3>
          <div class="filter-list">
            <label class="filter-item">
              <input 
                type="checkbox" 
                v-model="selectedDifficulties" 
                value="easy"
              >
              <span>Лёгкая</span>
            </label>
            <label class="filter-item">
              <input 
                type="checkbox" 
                v-model="selectedDifficulties" 
                value="medium"
              >
              <span>Средняя</span>
            </label>
            <label class="filter-item">
              <input 
                type="checkbox" 
                v-model="selectedDifficulties" 
                value="hard"
              >
              <span>Сложная</span>
            </label>
            <label class="filter-item">
              <input 
                type="checkbox" 
                v-model="selectedDifficulties" 
                value="any"
                checked
              >
              <span>Любая</span>
            </label>
          </div>
        </div>
        
        <div class="sort-block">
          <h3>СОРТИРОВКА</h3>
          <div class="sort-list">
            <label class="sort-item">
              <input 
                type="radio" 
                v-model="sortBy" 
                value="number"
                checked
              >
              <span>По номеру</span>
            </label>
            <label class="sort-item">
              <input 
                type="radio" 
                v-model="sortBy" 
                value="difficulty"
              >
              <span>По сложности</span>
            </label>
            <label class="sort-item">
              <input 
                type="radio" 
                v-model="sortBy" 
                value="type"
              >
              <span>По типу</span>
            </label>
          </div>
        </div>
        
        <div class="subject-list">
          <div 
            v-for="subject in subjects" 
            :key="subject.id"
            class="subject-item"
            :class="{ active: activeSubject === subject.id }"
            @click="activeSubject = subject.id"
          >
            {{ subject.name }}
          </div>
        </div>
      </aside>

      <!-- Основной контент -->
      <main class="main-content">
        <!-- ВЕРХНЯЯ ПАНЕЛЬ - полностью из нижнего кода -->
        <div class="content-header">
          <div class="subject-header">
            <button class="back-button" @click="goBack">
              <span class="back-arrow">←</span>
              <span class="back-text">Назад</span>
            </button>
            
            <div class="subject-info">
              <h1>{{ getSubjectName(activeSubject) }}</h1>
            </div>
          </div>
          
          <div class="search-tool">
            <div class="search-label">ПОИСК ПО НОМЕРУ</div>
            <div class="search-box">
              <input 
                type="number" 
                v-model="searchQuery"
                placeholder="№ задания"
                @keyup.enter="searchTask"
                :disabled="isSearching"
              >
              <button @click="searchTask" :disabled="isSearching || !searchQuery">
                {{ isSearching ? 'ПОИСК...' : 'ПЕРЕЙТИ' }}
              </button>
            </div>
            <div v-if="searchError" class="search-error">
              {{ searchError }}
            </div>
          </div>
        </div>

        <!-- Режим поиска - показываем найденное задание (из нижнего кода) -->
        <div v-if="isSearchMode && searchResult" class="search-result-section">
          <div class="section-title">
            <h2>Найденное задание №{{ searchResult.id }}</h2>
            <button class="clear-search-btn" @click="clearSearch">
              × Сбросить поиск
            </button>
          </div>
          
          <div class="task-block">
            <div class="task-head">
              <div class="task-title">
                <span class="task-number">№{{ searchResult.id }}</span>
                <span :class="['difficulty', searchResult.difficulty]">
                  {{ formatDifficulty(searchResult.difficulty) }}
                </span>
              </div>
              <span class="task-type">{{ searchResult.topic }}</span>
            </div>
            
            <div class="task-text">
              {{ searchResult.text }}
            </div>
            
            <div class="answer-section">
              <div class="answer-input-section">
                <div class="answer-label">Введите ваш ответ:</div>
                <input 
                  type="text" 
                  v-model="userAnswers[searchResult.id]"
                  class="answer-input"
                  placeholder="Введите ответ здесь..."
                  @keyup.enter="checkAnswer(searchResult)"
                >
                <button 
                  class="submit-answer-btn" 
                  @click="checkAnswer(searchResult)"
                >
                  Проверить
                </button>
                <div v-if="message[searchResult.id]">
                  <a :style="{ color: message[searchResult.id] === 'Верно!' ? 'green' : 'red', textAlign: 'left' }">
                    {{ message[searchResult.id] }}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Если поиск не дал результатов -->
        <div v-else-if="isSearchMode && !searchResult && !isSearching" class="no-search-results">
          <div class="section-title">
            <h2>Результаты поиска</h2>
            <button @click="clearSearch" class="clear-search-btn">
              × Сбросить поиск
            </button>
          </div>
          <div class="no-results-message">
            <p>Задание с номером {{ searchQuery }} не найдено</p>
          </div>
        </div>

        <!-- Обычный режим (список заданий) -->
        <div v-else class="task-container">
          <div class="task-list">
            <div v-if="isLoading" class="loading-message">
              <p>Загрузка заданий...</p>
            </div>
            
            <div v-else-if="error" class="error-message">
              <p>{{ error }}</p>
              <button @click="getTasks" class="retry-btn">Повторить</button>
            </div>
            
            <div v-else-if="currentPageTasks.length > 0">
              <div 
                v-for="task in currentPageTasks" 
                :key="task.id"
                class="task-block"
              >
                <div class="task-head">
                  <div class="task-title">
                    <span class="task-number">№{{ task.id }}</span>
                    <span :class="['difficulty', task.difficulty]">
                      {{ formatDifficulty(task.difficulty) }}
                    </span>
                  </div>
                  <span class="task-type">{{ task.topic }}</span>
                </div>
                
                <div class="task-text">
                  {{ task.text }}
                </div>
                
                <div class="answer-section">
                  <div class="answer-input-section">
                    <div class="answer-label">Введите ваш ответ:</div>
                    <input 
                      type="text" 
                      v-model="userAnswers[task.id]"
                      class="answer-input"
                      placeholder="Введите ответ здесь..."
                      @keyup.enter="checkAnswer(task)"
                    >
                    <button 
                      class="submit-answer-btn" 
                      @click="checkAnswer(task)"
                    >
                      Проверить
                    </button>
                    <div v-if="message[task.id]">
                      <a :style="{ color: message[task.id] === 'Верно!' ? 'green' : 'red', textAlign: 'left' }">
                        {{ message[task.id] }}
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="no-tasks-message">
              <p>Нет заданий, соответствующих выбранным фильтрам</p>
            </div>
          </div>

          <!-- Пагинация -->
          <div v-if="!isSearchMode && currentPageTasks.length > 0" class="page-controls">
            <button 
              class="nav-btn prev" 
              :disabled="currentPage === 1"
              @click="prevPage"
            >
              ← Назад
            </button>
            
            <div class="page-indicators">
              <span 
                v-for="page in totalPages" 
                :key="page"
                class="page-indicator"
                :class="{ active: page === currentPage }"
                @click="goToPage(page)"
              >
                {{ page }}
              </span>
            </div>
            
            <button 
              class="nav-btn next" 
              :disabled="currentPage === totalPages"
              @click="nextPage"
            >
              Вперед →
            </button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StudyView',
  
  data() {
    return {
      userAnswers: [],
      activeSubject: 'math',
      currentPage: 1,
      selectedDifficulties: ['any'],
      sortBy: 'number',
      allTasks: [],
      isLoading: false,
      error: null,
      message: [],
      
      // Поисковые переменные (из нижнего кода)
      searchQuery: '',
      searchResult: null,
      searchError: '',
      isSearching: false,
      isSearchMode: false
    }
  },
  
  computed: {
    subjects() {
      return [
        { id: 'math', name: 'МАТЕМАТИКА' },
        { id: 'geom', name: 'ГЕОМЕТРИЯ' },
        { id: 'd_math', name: 'ДИСКРЕТНАЯ МАТЕМАТИКА' },
        { id: 'phys', name: 'ФИЗИКА' },
        { id: 'chem', name: 'ХИМИЯ' },
        { id: 'bio', name: 'БИОЛОГИЯ' },
        { id: 'eco', name: 'ЭКОЛОГИЯ' },
        { id: 'geo', name: 'ГЕОГРАФИЯ' },
        { id: 'astro', name: 'АСТРОНОМИЯ' },
        { id: 'rus_lang', name: 'РУССКИЙ ЯЗЫК' },
        { id: 'rus_lit', name: 'ЛИТЕРАТУРА' },
        { id: 'eng_lang', name: 'АНГЛИЙСКИЙ ЯЗЫК' },
        { id: 'ger_lang', name: 'НЕМЕЦКИЙ ЯЗЫК' },
        { id: 'fr_lang', name: 'ФРАНЦУЗСКИЙ ЯЗЫК' },
        { id: 'chi_lang', name: 'КИТАЙСКИЙ ЯЗЫК' },
        { id: 'sp_lang', name: 'ИСПАНСКИЙ ЯЗЫК' },
        { id: 'lat_lang', name: 'ЛАТИНСКИЙ ЯЗЫК' },
        { id: 'hist', name: 'ИСТОРИЯ' },
        { id: 'soc_st', name: 'ОБЩЕСТВОЗНАНИЕ' },
        { id: 'law', name: 'ПРАВО' },
        { id: 'econ', name: 'ЭКОНОМИКА' },
        { id: 'fin_lit', name: 'ФИНАНСОВАЯ ГРАМОТНОСТЬ' },
        { id: 'arts', name: 'ИСКУССТВО (МХК)' },
        { id: 'tech', name: 'ТЕХНОЛОГИЯ' },
        { id: 'inf', name: 'ИНФОРМАТИКА' },
        { id: 'robot', name: 'РОБОТОТЕХНИКА' },
        { id: 'ai', name: 'ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ' },
        { id: 'pe', name: 'ФИЗКУЛЬТУРА' },
        { id: 'obzh', name: 'ОБЖ' }
      ]
    },
    
    filteredTasks() {
      let filtered = this.allTasks.filter(task => {
        if (this.activeSubject && this.activeSubject !== 'all') {
          const taskSubject = (task.subject || '').toString().toLowerCase();
          const activeSubject = this.activeSubject.toString().toLowerCase();

          if (taskSubject !== activeSubject) {
            return false;
          }
        }

        if (this.selectedDifficulties && this.selectedDifficulties.includes('any') || 
            !this.selectedDifficulties || this.selectedDifficulties.length === 0) {
          return true;
        }

        const taskDifficulty = (task.difficulty || 'medium').toString().toLowerCase();
        const hasDifficulty = this.selectedDifficulties.some(diff => 
          diff.toString().toLowerCase() === taskDifficulty
        );

        return hasDifficulty;
      });
  
      return this.sortTasks(filtered);
    },
    
    currentPageTasks() {
      if (this.isSearchMode) return [];
      
      const tasksPerPage = 2;
      const startIndex = (this.currentPage - 1) * tasksPerPage;
      const endIndex = startIndex + tasksPerPage;
      
      return this.filteredTasks.slice(startIndex, endIndex);
    },
    
    totalPages() {
      if (this.isSearchMode) return 0;
      
      const tasksPerPage = 2;
      return Math.ceil(this.filteredTasks.length / tasksPerPage) || 1;
    }
  },

  watch: {
    activeSubject() {
      this.clearSearch();
      this.currentPage = 1;
    },
    selectedDifficulties: {
      handler() {
        this.clearSearch();
        this.currentPage = 1;
      },
      deep: true
    },
    sortBy() {
      this.clearSearch();
      this.currentPage = 1;
    }
  },

  created() {
    this.getTasks();
    
    // Восстанавливаем настройки из localStorage
    const savedConfig = localStorage.getItem('trainingConfig');
    if (savedConfig) {
      try {
        const config = JSON.parse(savedConfig);
        if (config.subject) {
          this.activeSubject = config.subject;
        }
        if (config.difficulty) {
          if (config.difficulty === 'random') {
            this.selectedDifficulties = ['any'];
          } else {
            this.selectedDifficulties = [config.difficulty];
          }
        }
      } catch (e) {
        console.error('Ошибка при восстановлении настроек:', e);
      }
    }
  },
  
  methods: {
    getSubjectName(subjectId) {
      const subject = this.subjects.find(s => s.id === subjectId);
      return subject ? subject.name : 'МАТЕМАТИКА';
    },
    
    formatDifficulty(level) {
      const names = {
        'easy': 'Лёгкая',
        'medium': 'Средняя',
        'hard': 'Сложная'
      };
      return names[level] || level;
    },
    
    goBack() {
      if (window.history.length > 1) {
        this.$router.go(-1);
      } else {
        this.$router.push('/');
      }
    },
    
    // Методы поиска из нижнего кода
    async searchTask() {
      if (!this.searchQuery) {
        this.searchError = 'Введите номер задания';
        return;
      }
      
      const taskNumber = parseInt(this.searchQuery);
      if (isNaN(taskNumber) || taskNumber <= 0) {
        this.searchError = 'Введите корректный номер задания';
        return;
      }
      
      this.isSearching = true;
      this.searchError = '';
      this.isSearchMode = true;
      
      const foundTask = this.allTasks.find(task => task.id === taskNumber);
      
      if (foundTask) {
        this.searchResult = foundTask;
      } else {
        this.searchResult = null;
        this.searchError = `Задание с номером ${taskNumber} не найдено`;
      }
      
      this.isSearching = false;
    },
    
    clearSearch() {
      this.searchQuery = '';
      this.searchResult = null;
      this.searchError = '';
      this.isSearchMode = false;
      this.currentPage = 1;
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.scrollToTop();
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.scrollToTop();
      }
    },
    
    goToPage(page) {
      this.currentPage = page;
      this.scrollToTop();
    },
    
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    async getTasks() {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await axios.get('http://localhost:8000/api/tasks/');
        
        console.log('Полученные задания:', response.data);
        
        if (Array.isArray(response.data)) {
          this.allTasks = response.data;
        } else if (response.data.results) {
          this.allTasks = response.data.results;
        } else if (response.data.tasks) {
          this.allTasks = response.data.tasks;
        } else {
          this.allTasks = [];
        }
        
      } catch (err) {
        console.error('Ошибка при загрузке заданий:', err);
        this.$router.push('/auth');
        this.error = 'Не удалось загрузить задания. Проверьте подключение к серверу.';
      } finally {
        this.isLoading = false;
      }
    },
    
    async checkAnswer(task) {
      try {
        const response = await axios.post('http://localhost:8000/api/submit/', {
          'task_id': task.id,
          'answer': this.userAnswers[task.id],
        });

        console.log('Полученный ответ:', response.data);
        this.message[task.id] = response.data.message;
        
      } catch (err) {
        console.error('Ошибка при отправке ответа:', err);
        this.$router.push('/auth');
      }
    },
    
    sortTasks(tasks) {
      if (!tasks || !Array.isArray(tasks)) {
        return [];
      }
      
      const tasksCopy = [...tasks];
      
      if (this.sortBy === 'number') {
        return tasksCopy.sort((a, b) => a.id - b.id);
      } 
      
      if (this.sortBy === 'difficulty') {
        const order = { easy: 1, medium: 2, hard: 3 };
        return tasksCopy.sort((a, b) => {
          const diffA = order[a.difficulty] || 2;
          const diffB = order[b.difficulty] || 2;
          
          if (diffA !== diffB) {
            return diffA - diffB;
          }
          
          return a.id - b.id;
        });
      } 
      
      if (this.sortBy === 'type') {
        return tasksCopy.sort((a, b) => {
          const typeA = a.topic || '';
          const typeB = b.topic || '';
          const compare = typeA.localeCompare(typeB);
          
          if (compare !== 0) {
            return compare;
          }
          
          return a.id - b.id;
        });
      }
      
      return tasksCopy;
    }
  }
}
</script>

<style scoped>
/* СТИЛИ ПОЛНОСТЬЮ ИЗ НИЖНЕГО КОДА */
.study-page {
  min-height: 100vh;
  background: #FAF6EF;
  font-family: 'Segoe UI', system-ui, sans-serif;
}

.page-wrapper {
  display: flex;
  min-height: 100vh;
  position: relative;
}

/* Левая панель */
.navigation-panel {
  width: 300px;
  background: #FAF6EF;
  padding: 0;
  height: 100vh;
  position: sticky;
  top: 0;
  overflow-y: auto;
  scrollbar-width: none;
}

.navigation-panel::-webkit-scrollbar {
  display: none;
  width: 0;
  height: 0;
}

.panel-header {
  padding: 24px 20px;
}

.panel-header h2 {
  color: #000;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.filter-block,
.sort-block {
  padding: 20px;
  background: #FFF;
  margin: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

.filter-block h3,
.sort-block h3 {
  font-size: 13px;
  font-weight: 800;
  color: #1565C0;
  margin-bottom: 15px;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.filter-list,
.sort-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-item,
.sort-item {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background 0.2s;
}

.filter-item:hover,
.sort-item:hover {
  background: #F5F7FA;
}

.filter-item input[type="checkbox"],
.sort-item input[type="radio"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.filter-item span,
.sort-item span {
  font-size: 14px;
  font-weight: 500;
  color: #263238;
  cursor: pointer;
}

.subject-list {
  padding: 15px;
  max-height: calc(100vh - 380px);
  overflow-y: auto;
  scrollbar-width: none;
}

.subject-list::-webkit-scrollbar {
  display: none;
  width: 0;
  height: 0;
}

.subject-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  margin-bottom: 12px;
  border-radius: 10px;
  cursor: pointer;
  color: #263238;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s;
  border: 2px solid transparent;
  background: #FFF;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

.subject-item:hover {
  border-color: #42A5F5;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

.subject-item.active {
  color: #000;
  border-color: #1565C0;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(30,136,229,0.3);
}

/* Основной контент */
.main-content {
  flex: 1;
  padding: 35px 45px;
  overflow-y: auto;
}

/* ВЕРХНЯЯ ПАНЕЛЬ - стили из нижнего кода */
.content-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding: 30px 35px;
  border-radius: 15px;
}

.subject-header {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px 10px 15px;
  background: transparent;
  border: 2px solid #1E88E5;
  border-radius: 8px;
  color: #1E88E5;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  width: fit-content;
}

.back-button:hover {
  background: #1E88E5;
  color: #FFF;
  transform: translateX(-5px);
  box-shadow: 0 4px 12px rgba(30,136,229,0.3);
}

.back-arrow {
  font-size: 18px;
  font-weight: 900;
}

.back-text {
  letter-spacing: 0.5px;
}

.subject-info h1 {
  color: #000;
  font-size: 32px;
  font-weight: 800;
  margin-bottom: 12px;
}

.search-tool {
  width: 350px;
}

.search-label {
  font-size: 13px;
  font-weight: 800;
  color: #1565C0;
  margin-bottom: 10px;
  letter-spacing: 1.5px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-label::before {
  content: "🔍";
  font-size: 16px;
}

.search-box {
  display: flex;
  gap: 12px;
}

.search-box input {
  flex: 1;
  padding: 16px 20px;
  border: 3px solid #B0BEC5;
  border-radius: 10px;
  font-size: 16px;
  color: #263238;
  background: #FFF;
  transition: all 0.2s;
}

.search-box input:focus {
  outline: none;
  border-color: #1E88E5;
  box-shadow: 0 0 0 3px rgba(30,136,229,0.2);
}

.search-box input:disabled {
  background: #F5F7FA;
  border-color: #CFD8DC;
  cursor: not-allowed;
}

.search-box button {
  padding: 16px 28px;
  background: linear-gradient(135deg, #1E88E5, #1565C0);
  color: #FFF;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 120px;
}

.search-box button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30,136,229,0.4);
}

.search-box button:disabled {
  background: linear-gradient(135deg, #B0BEC5, #90A4AE);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.search-error {
  color: #E53935;
  font-size: 14px;
  margin-top: 8px;
  font-weight: 500;
}

/* Стили для поисковых секций */
.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding: 20px 25px;
  background: #FFF;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.section-title h2 {
  color: #000;
  font-size: 24px;
  font-weight: 800;
}

.clear-search-btn {
  padding: 10px 20px;
  background: #FF5252;
  color: #FFF;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-search-btn:hover {
  background: #E53935;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(229,57,53,0.3);
}

.search-result-section,
.no-search-results {
  margin-bottom: 40px;
  animation: fadeIn 0.5s ease;
}

.no-results-message {
  text-align: center;
  padding: 60px;
  background: #FFF;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.no-results-message p {
  font-size: 18px;
  color: #E53935;
  font-weight: 500;
}

/* Стили для заданий */
.task-list {
  display: flex;
  flex-direction: column;
  gap: 60px;
}

.task-block {
  background: #FFF;
  border-radius: 15px;
  padding: 35px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
  position: relative;
  overflow: hidden;
  margin-bottom: 10px;
}

.task-block::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: white;
}

.task-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 25px;
  border-bottom: 2px solid #CFD8DC;
}

.task-title {
  display: flex;
  align-items: center;
  gap: 20px;
}

.task-number {
  color: #000;
  font-size: 20px;
  font-weight: 900;
  letter-spacing: 0.5px;
  padding: 5px 0;
  border-bottom: 3px solid #000;
}

.difficulty {
  padding: 10px 22px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 900;
  letter-spacing: 1px;
  border: 3px solid;
  text-transform: uppercase;
}

.difficulty.easy {
  background: #E8F5E9;
  color: #43A047;
  border-color: #43A047;
}

.difficulty.medium {
  background: #FFF3E0;
  color: #FB8C00;
  border-color: #FB8C00;
}

.difficulty.hard {
  background: #FFEBEE;
  color: #E53935;
  border-color: #E53935;
}

.task-type {
  color: #8E24AA;
  font-size: 16px;
  font-weight: 800;
  padding: 10px 22px;
  background: #F3E5F5;
  border-radius: 25px;
  border: 3px solid #8E24AA;
}

.task-text {
  font-size: 17px;
  line-height: 1.8;
  color: #263238;
  margin-bottom: 30px;
  padding: 20px;
  background: #F5F7FA;
  border-radius: 12px;
  border: 2px solid #CFD8DC;
  font-weight: 500;
}

/* Стили для ответов (сохраняем из исходного кода) */
.answer-section {
  border-radius: 12px;
  padding: 20px 0;
}

.answer-input-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.answer-label {
  font-size: 16px;
  font-weight: 700;
  color: #1565c0;
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
  cursor: text;
}

.answer-input:focus {
  outline: none;
  border-color: #1e88e5;
  box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.2);
}

.submit-answer-btn {
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
  pointer-events: auto !important;
}

.submit-answer-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 136, 229, 0.4);
}

.submit-answer-btn:active {
  transform: translateY(0);
}

.loading-message,
.error-message,
.no-tasks-message {
  text-align: center;
  padding: 60px;
  background: #ffffff;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.loading-message p,
.error-message p,
.no-tasks-message p {
  font-size: 18px;
  color: #546e7a;
  font-weight: 500;
}

.retry-btn {
  margin-top: 20px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #1e88e5, #1565c0);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 136, 229, 0.4);
}

/* Пагинация из нижнего кода */
.page-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 50px;
  padding: 30px;
  background: #FFF;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.nav-btn {
  padding: 14px 30px;
  border-radius: 10px;
  background: #FFF;
  font-size: 16px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid #1E88E5;
  color: #1E88E5;
}

.nav-btn:hover:not(:disabled) {
  background: #1E88E5;
  color: #FFF;
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(30,136,229,0.3);
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border-color: #B0BEC5;
  color: #546E7A;
}

.page-indicators {
  display: flex;
  gap: 10px;
}

.page-indicator {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 800;
  font-size: 17px;
  background: #FFF;
  border: 2px solid #1E88E5;
  color: #1E88E5;
  transition: all 0.2s;
}

.page-indicator:hover {
  background: #42A5F5;
  color: #FFF;
  transform: translateY(-2px);
}

.page-indicator.active {
  background: #1E88E5;
  color: #FFF;
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(30,136,229,0.3);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Адаптивность */
@media (max-width: 1200px) {
  .page-wrapper {
    flex-direction: column;
  }
  
  .navigation-panel {
    width: 100%;
    height: auto;
    position: static;
  }
  
  .main-content {
    padding: 25px;
  }
  
  .subject-list {
    max-height: none;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 10px;
  }
  
  .filter-block,
  .sort-block {
    margin: 10px;
  }
}

@media (max-width: 768px) {
  .content-header {
    flex-direction: column;
    gap: 25px;
  }
  
  .subject-header {
    width: 100%;
  }
  
  .search-tool {
    width: 100%;
  }
  
  .section-title {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .section-title h2 {
    font-size: 20px;
  }
  
  .task-head {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
  
  .page-controls {
    flex-direction: column;
    gap: 20px;
  }
  
  .page-indicators {
    order: -1;
  }
  
  .answer-input-section {
    flex-direction: column;
  }
  
  .submit-answer-btn {
    align-self: stretch;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .back-button {
    padding: 8px 15px 8px 10px;
    font-size: 14px;
  }
  
  .back-arrow {
    font-size: 16px;
  }
  
  .subject-info h1 {
    font-size: 26px;
  }
  
  .search-box {
    flex-direction: column;
  }
  
  .search-box input,
  .search-box button {
    width: 100%;
  }
}
</style>