<template>
  <div class="study-page">
    <div class="page-wrapper">
      <aside class="navigation-panel">
        <div class="panel-header">
          <h2>ОЛИМПИАДНЫЕ ПРЕДМЕТЫ</h2>
        </div>
        
        <div class="filter-block">
          <h3>СЛОЖНОСТЬ</h3>
          <div class="filter-list">
            <label class="filter-item">
              <input type="checkbox" v-model="selectedDifficulties" value="easy">
              <span>Лёгкая</span>
            </label>
            <label class="filter-item">
              <input type="checkbox" v-model="selectedDifficulties" value="medium">
              <span>Средняя</span>
            </label>
            <label class="filter-item">
              <input type="checkbox" v-model="selectedDifficulties" value="hard">
              <span>Сложная</span>
            </label>
            <label class="filter-item">
              <input type="checkbox" v-model="selectedDifficulties" value="any" checked>
              <span>Любая</span>
            </label>
          </div>
        </div>
        
        <div class="sort-block">
          <h3>СОРТИРОВКА</h3>
          <div class="sort-list">
            <label class="sort-item">
              <input type="radio" v-model="sortMethod" value="number" checked>
              <span>По номеру</span>
            </label>
            <label class="sort-item">
              <input type="radio" v-model="sortMethod" value="difficulty">
              <span>По сложности</span>
            </label>
            <label class="sort-item">
              <input type="radio" v-model="sortMethod" value="type">
              <span>По типу</span>
            </label>
          </div>
        </div>
        
        <div class="subject-list">
          <div 
            v-for="item in subjectList" 
            :key="item.id"
            class="subject-item"
            :class="{ active: currentSubject === item.id }"
            @click="currentSubject = item.id"
          >
            {{ item.name }}
          </div>
        </div>
      </aside>

      <main class="main-content">
        <div class="content-header">
          <div class="subject-header">
            <button class="back-button" @click="goBack">
              <span class="back-arrow">←</span>
              <span class="back-text">Назад</span>
            </button>
            
            <div class="subject-info">
              <h1>{{ getCurrentSubjectName() }}</h1>
            </div>
          </div>
          
          <div class="search-tool">
            <div class="search-label">ПОИСК ПО НОМЕРУ</div>
            <div class="search-box">
              <input 
                type="number" 
                v-model="searchTaskNumber" 
                placeholder="№ задания"
                @keyup.enter="findTask"
                :disabled="isSearching"
              >
              <button @click="findTask" :disabled="isSearching || !searchTaskNumber">
                {{ isSearching ? 'ПОИСК...' : 'ПЕРЕЙТИ' }}
              </button>
            </div>
            <div v-if="searchError" class="search-error">
              {{ searchError }}
            </div>
          </div>
        </div>

        <!-- Режим поиска - показываем найденное задание -->
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
                <span class="task-id">№{{ searchResult.id }}</span>
                <span :class="['difficulty-mark', searchResult.difficulty]">
                  {{ formatDifficulty(searchResult.difficulty) }}
                </span>
              </div>
              <span class="task-category">{{ searchResult.topic }}</span>
            </div>
            
            <div class="task-description">
              {{ searchResult.text }}
            </div>
            
            <div class="answer-section">
              <div 
                class="toggle-answer" 
                @click="toggleAnswerVisibility(searchResult.id)"
              >
                {{ answerVisible[searchResult.id] ? 'Свернуть ответ ▲' : 'Показать ответ ▼' }}
              </div>
              
              <div v-if="answerVisible[searchResult.id]" class="answer-block">
                <div class="answer-label">Ответ:</div>
                <div class="answer-value">{{ searchResult.correct_answer || searchResult.answer || 'Ответ не указан' }}</div>
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
            <p>Задание с номером {{ searchTaskNumber }} не найдено</p>
          </div>
        </div>

        <!-- Обычный режим (список заданий) -->
        <div v-else class="task-container">
          <div class="task-list">
            <div v-if="tasksOnPage.length > 0">
              <div 
                v-for="item in tasksOnPage" 
                :key="item.id"
                class="task-block"
              >
                <div class="task-head">
                  <div class="task-title">
                    <span class="task-id">№{{ item.id }}</span>
                    <span :class="['difficulty-mark', item.difficulty]">
                      {{ formatDifficulty(item.difficulty) }}
                    </span>
                  </div>
                  <span class="task-category">{{ item.topic }}</span>
                </div>
                
                <div class="task-description">
                  {{ item.text }}
                </div>
                
                <div class="answer-section">
                  <div 
                    class="toggle-answer" 
                    @click="toggleAnswerVisibility(item.id)"
                  >
                    {{ answerVisible[item.id] ? 'Свернуть ответ ▲' : 'Показать ответ ▼' }}
                  </div>
                  
                  <div v-if="answerVisible[item.id]" class="answer-block">
                    <div class="answer-label">Ответ:</div>
                    <div class="answer-value">{{ item.correct_answer || item.answer || 'Ответ не указан' }}</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else-if="!isSearching" class="empty-list">
              <p>Нет заданий, соответствующих выбранным фильтрам</p>
            </div>
          </div>

          <!-- Пагинация только в обычном режиме -->
          <div v-if="!isSearchMode && tasksOnPage.length > 0" class="page-controls">
            <button 
              class="nav-btn prev" 
              :disabled="currentPageNumber === 1"
              @click="goToPrevPage"
            >
              ← Назад
            </button>
            
            <div class="page-indicators">
              <span 
                v-for="page in totalPageCount" 
                :key="page"
                class="page-indicator"
                :class="{ active: page === currentPageNumber }"
                @click="selectPage(page)"
              >
                {{ page }}
              </span>
            </div>
            
            <button 
              class="nav-btn next" 
              :disabled="currentPageNumber === totalPageCount"
              @click="goToNextPage"
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
  name: 'StudyPage',
  
  data() {
    return {
      currentSubject: 'math',
      currentPageNumber: 1,
      selectedDifficulties: ['any'],
      sortMethod: 'number',
      answerVisible: {},
      taskCollection: [],
      loading: false,
      fetchError: null,
      
      // Поисковые переменные
      searchTaskNumber: '',
      searchResult: null,
      searchError: '',
      isSearching: false,
      isSearchMode: false
    }
  },
  
  computed: {
    subjectList() {
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
      let result = this.taskCollection.filter(task => {
        if (this.currentSubject && this.currentSubject !== 'all') {
          const taskSubject = (task.subject || '').toString().toLowerCase();
          if (taskSubject !== this.currentSubject) {
            return false;
          }
        }

        if (this.selectedDifficulties.includes('any') || !this.selectedDifficulties.length) {
          return true;
        }

        const taskDifficulty = (task.difficulty || 'medium').toString().toLowerCase();
        return this.selectedDifficulties.some(diff => 
          diff.toString().toLowerCase() === taskDifficulty
        );
      });
  
      return this.applySorting(result);
    },
    
    tasksOnPage() {
      if (this.isSearchMode) return [];
      
      const perPage = 2;
      const start = (this.currentPageNumber - 1) * perPage;
      const end = start + perPage;
      
      return this.filteredTasks.slice(start, end);
    },
    
    totalPageCount() {
      if (this.isSearchMode) return 0;
      
      const perPage = 2;
      return Math.ceil(this.filteredTasks.length / perPage) || 1;
    }
  },
  
  watch: {
    currentSubject() {
      this.clearSearch();
      this.currentPageNumber = 1;
    },
    
    selectedDifficulties() {
      this.clearSearch();
      this.currentPageNumber = 1;
    },
    
    sortMethod() {
      this.clearSearch();
      this.currentPageNumber = 1;
    }
  },
  
  created() {
    this.loadTasks();
  },
  
  methods: {
    async loadTasks() {
      this.loading = true;
      this.fetchError = null;
      
      try {
        const result = await axios.get('http://localhost:8000/api/tasks/');
        
        let tasks = [];
        if (Array.isArray(result.data)) {
          tasks = result.data;
        } else if (result.data.results) {
          tasks = result.data.results;
        } else if (result.data.tasks) {
          tasks = result.data.tasks;
        } else {
          tasks = [];
        }
        
        // Нормализация данных - чтобы работало и с answer, и с correct_answer
        this.taskCollection = tasks.map(task => ({
          ...task,
          // Приводим к единому формату
          correct_answer: task.correct_answer || task.answer || 'Ответ не указан',
          answer: task.answer || task.correct_answer || 'Ответ не указан'
        }));
        
      } catch (err) {
        console.error('Ошибка при загрузке заданий:', err);
        this.fetchError = 'Не удалось загрузить задания. Проверьте подключение к серверу.';
        this.taskCollection = [];
      } finally {
        this.loading = false;
      }
    },

    formatDifficulty(level) {
      const names = {
        'easy': 'Лёгкая',
        'medium': 'Средняя',
        'hard': 'Сложная'
      };
      return names[level] || level;
    },
    
    getCurrentSubjectName() {
      const subject = this.subjectList.find(s => s.id === this.currentSubject);
      return subject ? subject.name : 'МАТЕМАТИКА';
    },
    
    async findTask() {
      if (!this.searchTaskNumber) {
        this.searchError = 'Введите номер задания';
        return;
      }
      
      const taskNumber = parseInt(this.searchTaskNumber);
      if (isNaN(taskNumber) || taskNumber <= 0) {
        this.searchError = 'Введите корректный номер задания';
        return;
      }
      
      this.isSearching = true;
      this.searchError = '';
      this.isSearchMode = true;
      
      // Ищем в загруженных заданиях
      const foundTask = this.taskCollection.find(task => task.id === taskNumber);
      
      if (foundTask) {
        this.searchResult = foundTask;
      } else {
        this.searchResult = null;
        this.searchError = `Задание с номером ${taskNumber} не найдено`;
      }
      
      this.isSearching = false;
    },
    
    clearSearch() {
      this.searchTaskNumber = '';
      this.searchResult = null;
      this.searchError = '';
      this.isSearchMode = false;
      this.currentPageNumber = 1;
    },
    
    goBack() {
      if (window.history.length > 1) {
        this.$router.go(-1);
      } else {
        this.$router.push('/');
      }
    },
    
    goToPrevPage() {
      if (this.currentPageNumber > 1) {
        this.currentPageNumber--;
        this.scrollToTop();
      }
    },
    
    goToNextPage() {
      if (this.currentPageNumber < this.totalPageCount) {
        this.currentPageNumber++;
        this.scrollToTop();
      }
    },
    
    selectPage(page) {
      this.currentPageNumber = page;
      this.scrollToTop();
    },
    
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    
    toggleAnswerVisibility(taskId) {
      this.answerVisible[taskId] = !this.answerVisible[taskId];
      // Принудительное обновление
      this.answerVisible = { ...this.answerVisible };
    },
    
    applySorting(tasks) {
      if (!tasks || !Array.isArray(tasks)) {
        return [];
      }
      
      const tasksCopy = [...tasks];
      
      if (this.sortMethod === 'number') {
        return tasksCopy.sort((a, b) => a.id - b.id);
      } 
      
      if (this.sortMethod === 'difficulty') {
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
      
      if (this.sortMethod === 'type') {
        return tasksCopy.sort((a, b) => {
          const typeA = a.type || '';
          const typeB = b.type || '';
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

.main-content {
  flex: 1;
  padding: 35px 45px;
  overflow-y: auto;
}

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

.search-error {
  color: #E53935;
  font-size: 14px;
  margin-top: 8px;
  font-weight: 500;
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

/* Общие стили */
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

.search-result-section {
  margin-bottom: 40px;
  animation: fadeIn 0.5s ease;
}

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
  margin-bottom: 20px;
}

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

.task-id {
  color: #000;
  font-size: 20px;
  font-weight: 900;
  letter-spacing: 0.5px;
  padding: 5px 0;
  border-bottom: 3px solid #000;
}

.difficulty-mark {
  padding: 10px 22px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 900;
  letter-spacing: 1px;
  border: 3px solid;
  text-transform: uppercase;
}

.difficulty-mark.easy {
  background: #E8F5E9;
  color: #43A047;
  border-color: #43A047;
}

.difficulty-mark.medium {
  background: #FFF3E0;
  color: #FB8C00;
  border-color: #FB8C00;
}

.difficulty-mark.hard {
  background: #FFEBEE;
  color: #E53935;
  border-color: #E53935;
}

.task-category {
  color: #8E24AA;
  font-size: 16px;
  font-weight: 800;
  padding: 10px 22px;
  background: #F3E5F5;
  border-radius: 25px;
  border: 3px solid #8E24AA;
}

.task-description {
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

.answer-section {
  border-radius: 12px;
  padding: 20px 0;
}

.toggle-answer {
  display: inline-block;
  padding: 12px 24px;
  color: #000;
  background: transparent;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 8px;
  border: 2px solid #000;
}

.toggle-answer:hover {
  background: #1E88E5;
  color: #FFF;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30,136,229,0.2);
}

.answer-block {
  margin-top: 20px;
  padding: 20px;
  background: #F5F7FA;
  border-radius: 10px;
  border: 2px solid #CFD8DC;
  animation: fadeIn 0.3s ease;
}

.answer-label {
  font-size: 16px;
  font-weight: 700;
  color: #1565C0;
  margin-bottom: 10px;
}

.answer-value {
  font-size: 18px;
  font-weight: 600;
  color: #263238;
  line-height: 1.6;
}

.empty-list {
  text-align: center;
  padding: 60px;
  background: #FFF;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.empty-list p {
  font-size: 18px;
  color: #546E7A;
  font-weight: 500;
}

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
  cursor: default;
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

@media (max-width: 1200px) {
  .page-wrapper {
    flex-direction: column;
  }
  
  .navigation-panel {
    width: 100%;
    height: auto;
    position: static;
    scrollbar-width: none;
  }
  
  .navigation-panel::-webkit-scrollbar {
    display: none;
    width: 0;
    height: 0;
  }
  
  .main-content {
    padding: 25px;
  }
  
  .subject-list {
    max-height: none;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 10px;
    overflow-y: visible;
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
