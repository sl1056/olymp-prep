<template>
    <body>
  <div class="page">
    <!-- Левая колонка с предметами -->
    <div class="sidebar">
      <div class="sidebar-title">ОЛИМПИАДНЫЕ ПРЕДМЕТЫ</div>
      
      <!-- Фильтр по сложности -->
      <div class="difficulty-filter">
        <div class="filter-title">СЛОЖНОСТЬ</div>
        <div class="filter-options">
          <label class="filter-option">
            <input 
              type="checkbox" 
              v-model="selectedDifficulties" 
              value="easy"
            >
            <span class="filter-label">Лёгкая</span>
          </label>
          <label class="filter-option">
            <input 
              type="checkbox" 
              v-model="selectedDifficulties" 
              value="medium"
            >
            <span class="filter-label">Средняя</span>
          </label>
          <label class="filter-option">
            <input 
              type="checkbox" 
              v-model="selectedDifficulties" 
              value="hard"
            >
            <span class="filter-label">Сложная</span>
          </label>
          <label class="filter-option">
            <input 
              type="checkbox" 
              v-model="selectedDifficulties" 
              value="any"
              checked
            >
            <span class="filter-label">Любая</span>
          </label>
        </div>
      </div>
      
      <!-- Сортировка -->
      <div class="sidebar-sorting">
        <div class="sort-title">СОРТИРОВКА</div>
        <div class="sort-options">
          <label class="sort-option">
            <input 
              type="radio" 
              v-model="sortBy" 
              value="number"
              checked
            >
            <span class="sort-label">По номеру</span>
          </label>
          <label class="sort-option">
            <input 
              type="radio" 
              v-model="sortBy" 
              value="difficulty"
            >
            <span class="sort-label">По сложности</span>
          </label>
          <label class="sort-option">
            <input 
              type="radio" 
              v-model="sortBy" 
              value="type"
            >
            <span class="sort-label">По типу</span>
          </label>
        </div>
      </div>
      
      <div class="subjects">
        <div 
          v-for="subject in subjects" 
          :key="subject.id"
          class="subject"
          :class="{ active: activeSubject === subject.id }"
          @click="activeSubject = subject.id"
        >
          <span>{{ subject.name }}</span>
        </div>
      </div>
    </div>

    <!-- Правая колонка с контентом -->
    <div class="content">
      <!-- Верхняя панель -->
      <div class="header">
        <div class="title-section">
          <h1>{{ getSubjectName(activeSubject) }}</h1>
        </div>
        
        <div class="search-section">
          <div class="search-label">ПОИСК ПО НОМЕРУ</div>
          <div class="search-input">
            <input type="number" placeholder="№ задания">
            <button @click="searchTask">ПЕРЕЙТИ</button>
          </div>
        </div>
      </div>

      <!-- Список заданий -->
      <div class="tasks">
        <div class="tasks-list">
          <!-- Отсортированные задания для текущей страницы -->
          <div v-if="currentPageTasks.length > 0">
            <div 
              v-for="task in currentPageTasks" 
              :key="task.id"
              class="task-card"
            >
              <div class="task-header">
                <div class="task-title">
                  <span class="task-number">{{ task.number }}</span>
                  <span :class="['difficulty', task.difficulty]">{{ task.difficultyText }}</span>
                </div>
                <span class="task-type">{{ task.type }}</span>
              </div>
              
              <div class="task-text">
                {{ task.text }}
              </div>
              
              <div class="task-answer">
                <div 
                  class="show-answer-btn" 
                  @click="toggleAnswer(task.id)"
                >
                  {{ showAnswer[task.id] ? 'Свернуть ответ ▲' : 'Показать ответ ▼' }}
                </div>
                
                <div v-if="showAnswer[task.id]" class="answer-content">
                  <div class="answer-title">Ответ:</div>
                  <div class="answer-text">{{ task.answer }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Сообщение если нет заданий -->
          <div v-else class="no-tasks-message">
            <p>Нет заданий, соответствующих выбранным фильтрам</p>
          </div>
        </div>
      </div>

      <!-- Пагинация(типо крутой типо знаю слово такое) -->
      <div class="pagination">
        <button 
          class="page-btn prev" 
          :disabled="currentPage === 1"
          @click="prevPage"
        >
          ← Назад
        </button>
        
        <div class="page-numbers">
          <span 
            v-for="page in totalPages" 
            :key="page"
            class="page-number"
            :class="{ active: page === currentPage }"
            @click="goToPage(page)"
          >
            {{ page }}
          </span>
        </div>
        
        <button 
          class="page-btn next" 
          :disabled="currentPage === totalPages"
          @click="nextPage"
        >
          Вперед →
        </button>
      </div>
    </div>
  </div>
  </body>
</template>

<script>
export default {
  name: 'StudyView',
  
  data() {
    return {
      activeSubject: 'mathematics',
      currentPage: 1,
      selectedDifficulties: ['any'],
      sortBy: 'number',
      showAnswer: {},
      allTasks: [
        {
          id: 'task1',
          number: 'ЗАДАНИЕ №9053',
          difficulty: 'medium',
          difficultyText: 'СРЕДНЯЯ',
          type: 'Тип 1',
          text: 'Определите, атомы каких двух из указанных в ряду элементов имеют на внешнем энергетическом уровне шесть электронов. Запишите в поле ответа номера выбранных элементов.',
          answer: '2, 4',
          originalPage: 1
        },
        {
          id: 'task2',
          number: 'ЗАДАНИЕ №9331',
          difficulty: 'easy',
          difficultyText: 'ЛЁГКАЯ',
          type: 'Тип 2',
          text: 'Из указанных в ряду химических элементов выберите три элемента, которые в Периодической системе химических элементов Д.И. Менделеева находятся в одном периоде. Расположите выбранные элементы в порядке возрастания их неметаллических свойств. Запишите в поле ответа номера выбранных элементов в нужной последовательности.',
          answer: '3, 1, 5',
          originalPage: 1
        },
        {
          id: 'task3',
          number: 'ЗАДАНИЕ №9062',
          difficulty: 'hard',
          difficultyText: 'СЛОЖНАЯ',
          type: 'Тип 1',
          text: 'Определите, атомы каких двух из указанных в ряду элементов имеют на внешнем энергетическом уровне семь электронов. Запишите в поле ответа номера выбранных элементов.',
          answer: '1, 7',
          originalPage: 2
        },
        {
          id: 'task4',
          number: 'ЗАДАНИЕ №9349',
          difficulty: 'medium',
          difficultyText: 'СРЕДНЯЯ',
          type: 'Тип 2',
          text: 'Из указанных в ряду химических элементов выберите три элемента, которые в Периодической системе химических элементов Д.И. Менделеева находятся в одном периоде. Расположите выбранные элементы в порядке возрастания их неметаллических свойств. Запишите в поле ответа номера выбранных элементов в нужной последовательности.',
          answer: '2, 4, 6',
          originalPage: 2
        },
        {
          id: 'task5',
          number: 'ЗАДАНИЕ №101',
          difficulty: 'easy',
          difficultyText: 'ЛЁГКАЯ',
          type: 'Тип 1',
          text: 'Решите уравнение: 3x + 7 = 16. Найдите значение x.',
          answer: 'x = 3',
          originalPage: 3
        },
        {
          id: 'task6',
          number: 'ЗАДАНИЕ №102',
          difficulty: 'medium',
          difficultyText: 'СРЕДНЯЯ',
          type: 'Тип 1',
          text: 'Тело движется со скоростью 10 м/с. Какое расстояние оно пройдет за 5 секунд?',
          answer: '50 метров',
          originalPage: 3
        }
      ]
    }
  },
  
  computed: {
    subjects() {
      return [
        { id: 'mathematics', name: 'МАТЕМАТИКА' },
        { id: 'geometry', name: 'ГЕОМЕТРИЯ' },
        { id: 'discrete_math', name: 'ДИСКРЕТНАЯ МАТЕМАТИКА' },
        { id: 'physics', name: 'ФИЗИКА' },
        { id: 'chemistry', name: 'ХИМИЯ' },
        { id: 'biology', name: 'БИОЛОГИЯ' },
        { id: 'ecology', name: 'ЭКОЛОГИЯ' },
        { id: 'geography', name: 'ГЕОГРАФИЯ' },
        { id: 'astronomy', name: 'АСТРОНОМИЯ' },
        { id: 'russian', name: 'РУССКИЙ ЯЗЫК' },
        { id: 'literature', name: 'ЛИТЕРАТУРА' },
        { id: 'english', name: 'АНГЛИЙСКИЙ ЯЗЫК' },
        { id: 'german', name: 'НЕМЕЦКИЙ ЯЗЫК' },
        { id: 'french', name: 'ФРАНЦУЗСКИЙ ЯЗЫК' },
        { id: 'chinese', name: 'КИТАЙСКИЙ ЯЗЫК' },
        { id: 'spanish', name: 'ИСПАНСКИЙ ЯЗЫК' },
        { id: 'latin', name: 'ЛАТИНСКИЙ ЯЗЫК' },
        { id: 'history', name: 'ИСТОРИЯ' },
        { id: 'social', name: 'ОБЩЕСТВОЗНАНИЕ' },
        { id: 'law', name: 'ПРАВО' },
        { id: 'economics', name: 'ЭКОНОМИКА' },
        { id: 'financial_literacy', name: 'ФИНАНСОВАЯ ГРАМОТНОСТЬ' },
        { id: 'art', name: 'ИСКУССТВО (МХК)' },
        { id: 'technology', name: 'ТЕХНОЛОГИЯ' },
        { id: 'informatics', name: 'ИНФОРМАТИКА' },
        { id: 'robotics', name: 'РОБОТОТЕХНИКА' },
        { id: 'ai', name: 'ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ' },
        { id: 'pe', name: 'ФИЗКУЛЬТУРА' },
        { id: 'obzh', name: 'ОБЖ' }
      ]
    },
    
    // Все отфильтрованные и отсортированные задания
    filteredAndSortedTasks() {
      // Фильтруем задания по сложности
      let filteredTasks = this.allTasks.filter(task => {
        if (this.selectedDifficulties.includes('any')) {
          return true;
        }
        return this.selectedDifficulties.includes(task.difficulty);
      });
      
      // Сортируем задания
      return this.sortTasks(filteredTasks);
    },
    
    // Задания для текущей страницы
    currentPageTasks() {
      const tasksPerPage = 2;
      const startIndex = (this.currentPage - 1) * tasksPerPage;
      const endIndex = startIndex + tasksPerPage;
      
      return this.filteredAndSortedTasks.slice(startIndex, endIndex);
    },
    
    // Общее количество страниц
    totalPages() {
      const tasksPerPage = 2;
      return Math.ceil(this.filteredAndSortedTasks.length / tasksPerPage);
    }
  },
  
  methods: {
    getSubjectName(subjectId) {
      const subject = this.subjects.find(s => s.id === subjectId)
      return subject ? subject.name : 'МАТЕМАТИКА'
    },
    
    searchTask() {
      alert('Поиск задания')
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    },
    
    goToPage(page) {
      this.currentPage = page
    },
    
    toggleAnswer(taskId) {
      this.$set(this.showAnswer, taskId, !this.showAnswer[taskId]);
    },
    
    sortTasks(tasks) {
      if (this.sortBy === 'number') {
        return [...tasks].sort((a, b) => {
          const numA = parseInt(a.number.match(/\d+/)[0]);
          const numB = parseInt(b.number.match(/\d+/)[0]);
          return numA - numB;
        });
      } else if (this.sortBy === 'difficulty') {
        const difficultyOrder = { easy: 1, medium: 2, hard: 3 };
        return [...tasks].sort((a, b) => {
          const diffA = difficultyOrder[a.difficulty];
          const diffB = difficultyOrder[b.difficulty];
          
          if (diffA !== diffB) {
            return diffA - diffB;
          }
          // Если сложность одинаковая, сортируем по номеру
          const numA = parseInt(a.number.match(/\d+/)[0]);
          const numB = parseInt(b.number.match(/\d+/)[0]);
          return numA - numB;
        });
      } else if (this.sortBy === 'type') {
        return [...tasks].sort((a, b) => {
          const typeCompare = a.type.localeCompare(b.type);
          if (typeCompare !== 0) {
            return typeCompare;
          }
          // Если тип одинаковый, сортируем по номеру
          const numA = parseInt(a.number.match(/\d+/)[0]);
          const numB = parseInt(b.number.match(/\d+/)[0]);
          return numA - numB;
        });
      }
      return tasks;
    }
  }
}
</script>

<style scoped>
/* Базовые стили */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.page {
  display: flex;
  min-height: 100vh;
  background: rgb(250, 246, 239);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Скрываем скроллбары */
.page::-webkit-scrollbar,
.sidebar::-webkit-scrollbar,
.content::-webkit-scrollbar,
.subjects::-webkit-scrollbar {
  display: none;
}

.page,
.sidebar,
.content,
.subjects {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

/* ===== ЛЕВАЯ КОЛОНКА - ПРЕДМЕТЫ ===== */
.sidebar {
  width: 300px;
  background: rgb(250, 246, 239);
  padding: 0;
  overflow-y: auto;
  height: 100vh;
  position: sticky;
  top: 0;
}

.sidebar-title {
  background: rgb(250, 246, 239);
  color: #000000;
  padding: 20px;
  font-size: 15px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Фильтр по сложности */
.difficulty-filter {
  padding: 20px;
  background: #ffffff;
  margin: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.filter-title {
  font-size: 13px;
  font-weight: 800;
  color: #1565c0;
  margin-bottom: 15px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.filter-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-option {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s;
}

.filter-option:hover {
  background: #f5f7fa;
}

.filter-option input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.filter-label {
  font-size: 14px;
  font-weight: 500;
  color: #263238;
  cursor: pointer;
}

/* Сортировка в сайдбаре */
.sidebar-sorting {
  padding: 20px;
  background: #ffffff;
  margin: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.sidebar-sorting .sort-title {
  font-size: 13px;
  font-weight: 800;
  color: #1565c0;
  margin-bottom: 15px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.sidebar-sorting .sort-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sidebar-sorting .sort-option {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s;
}

.sidebar-sorting .sort-option:hover {
  background: #f5f7fa;
}

.sidebar-sorting .sort-option input[type="radio"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.sidebar-sorting .sort-label {
  font-size: 14px;
  font-weight: 500;
  color: #263238;
  cursor: pointer;
}

.subjects {
  background-color: rgb(250, 246, 239);
  padding: 15px;
  max-height: calc(100vh - 380px); /* Увеличил высоту для сортировки */
  overflow-y: auto;
}

.subject {
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
  transition: all 0.3s;
  border: 2px solid transparent;
  background: #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.subject:hover {
  border-color: #42a5f5;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.subject.active {
  color: #000000;
  border-color: #1565c0;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
}

/* ===== ПРАВАЯ КОЛОНКА - КОНТЕНТ ===== */
.content {
  background-color: rgb(250, 246, 239);
  flex: 1;
  padding: 35px 45px;
  overflow-y: auto;
}

/* Верхняя панель */
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding: 30px 35px;
  border-radius: 15px;
}

.title-section h1 {
  color: #000000;
  font-size: 32px;
  font-weight: 800;
  margin-bottom: 12px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.search-section {
  width: 350px;
}

.search-label {
  font-size: 13px;
  font-weight: 800;
  color: #1565c0;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-label::before {
  content: "🔍";
  font-size: 16px;
}

.search-input {
  display: flex;
  gap: 12px;
}

.search-input input {
  flex: 1;
  padding: 16px 20px;
  border: 3px solid #b0bec5;
  border-radius: 10px;
  font-size: 16px;
  color: #263238;
  background: #ffffff;
  transition: all 0.3s;
}

.search-input input:focus {
  outline: none;
  border-color: #1e88e5;
  box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.2);
}

.search-input button {
  padding: 16px 28px;
  background: linear-gradient(135deg, #1e88e5, #1565c0);
  color: #ffffff;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.search-input button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 136, 229, 0.4);
}

.search-input button:active {
  transform: translateY(0);
}

/* Список заданий */
.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 60px; /* Увеличил расстояние между заданиями */
}

.task-card {
  background: #ffffff;
  border-radius: 15px;
  padding: 35px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  position: relative;
  overflow: hidden;
  margin-bottom: 10px; /* Дополнительный отступ снизу */
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
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  font-size: 20px;
  font-weight: 900;
  letter-spacing: 0.5px;
  padding: 5px 0;
  border-bottom: 3px solid #000000;
}

.difficulty {
  padding: 10px 22px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 1px;
  border: 3px solid;
}

.difficulty.easy {
  background: #e8f5e9;
  color: #43a047;
  border-color: #43a047;
}

.difficulty.medium {
  background: #fff3e0;
  color: #fb8c00;
  border-color: #fb8c00;
}

.difficulty.hard {
  background: #ffebee;
  color: #e53935;
  border-color: #e53935;
}

.task-type {
  color: #8e24aa;
  font-size: 16px;
  font-weight: 800;
  padding: 10px 22px;
  background: #f3e5f5;
  border-radius: 25px;
  border: 3px solid #8e24aa;
}

.task-text {
  font-size: 17px;
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

.show-answer-btn {
  display: inline-block;
  padding: 12px 24px;
  color: #000000;
  background: transparent;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 8px;
  text-decoration: none;
  border: 2px solid #000000;
}

.show-answer-btn:hover {
  background: #1e88e5;
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 136, 229, 0.2);
}

.answer-content {
  margin-top: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 10px;
  border: 2px solid #cfd8dc;
  animation: fadeIn 0.3s ease;
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

.answer-title {
  font-size: 16px;
  font-weight: 700;
  color: #1565c0;
  margin-bottom: 10px;
}

.answer-text {
  font-size: 18px;
  font-weight: 600;
  color: #263238;
  line-height: 1.6;
}

/* Сообщение при отсутствии заданий */
.no-tasks-message {
  text-align: center;
  padding: 60px;
  background: #ffffff;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.no-tasks-message p {
  font-size: 18px;
  color: #546e7a;
  font-weight: 500;
}

/* Пагинация */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 50px;
  padding: 30px;
  background: #ffffff;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.page-btn {
  padding: 14px 30px;
  border-radius: 10px;
  background: #ffffff;
  font-size: 16px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid #1e88e5;
  color: #1e88e5;
}

.page-btn:hover:not(:disabled) {
  background: #1e88e5;
  color: #ffffff;
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(30, 136, 229, 0.3);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border-color: #b0bec5;
  color: #546e7a;
}

.page-numbers {
  display: flex;
  gap: 10px;
}

.page-number {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 800;
  font-size: 17px;
  background: #ffffff;
  border: 2px solid #1e88e5;
  color: #1e88e5;
  transition: all 0.3s;
}

.page-number:hover {
  background: #42a5f5;
  color: #ffffff;
  transform: translateY(-2px);
}

.page-number.active {
  background: #1e88e5;
  color: #ffffff;
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(30, 136, 229, 0.3);
}

/* Адаптивность */
@media (max-width: 1200px) {
  .page {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
    position: static;
  }
  
  .subjects {
    max-height: none;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 10px;
  }
  
  .content {
    padding: 25px;
  }
  
  .difficulty-filter,
  .sidebar-sorting {
    margin: 10px;
  }
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 25px;
  }
  
  .search-section {
    width: 100%;
  }
  
  .task-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
  
  .pagination {
    flex-direction: column;
    gap: 20px;
  }
  
  .page-numbers {
    order: -1;
  }
}
</style>
