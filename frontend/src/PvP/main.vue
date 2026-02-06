<template>
  <Header />
  <div class="page">
    <div class="header">
      <h1>PVP МАТЧ</h1>
      <p>СРАЖАЙТЕСЬ С ДРУГОМ, РЕШАЯ ОЛИМПИАДНЫЕ ЗАДАНИЯ ПО ВСЕМ ПРЕДМЕТАМ</p>
    </div>

    <div class="cards">
      <div class="card card-create">
        <h2>СОЗДАТЬ МАТЧ</h2>
        <p>Начни новый PvP-бой и пригласи соперника</p>
        <button @click="goToNext">НАЧАТЬ БОЙ</button>
      </div>

      <div class="card card-join">
        <h2>ПРИСОЕДИНИТЬСЯ</h2>
        <p>Войди в матч по ссылке от друга</p>
        <input v-model="matchCode" placeholder="Введите код матча" />
        <button @click="joinMatch">ВОЙТИ В БОЙ</button>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'

export default {
  components: { Header },
  name: "PVPHome",
  
  data() {
    return {
      matchCode: ''
    }
  },

  methods: {
    goToNext() {
      this.$router.push('/pvp/create')
    },
    
    joinMatch() {
      const code = this.matchCode.trim()
      
      if (!code) {
        alert('Введите код матча')
        return
      }
      
      if (code.length < 6) {
        alert('Код матча должен содержать не менее 6 символов')
        return
      }
      
      this.$router.push(`/pvp/join/${code}`)
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: rgb(250, 246, 239);
  min-height: 100vh;
}

.page {
  max-width: 1000px;
  margin: 0 auto;
  margin-top: -8%;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 60px;
}

h1 {
  font-size: 48px;
  color: #1a365d;
  margin-bottom: 16px;
  font-weight: 800;
}

.header p {
  font-size: 20px;
  color: #4a5568;
  line-height: 1.5;
  max-width: 600px;
}

.cards {
  display: flex;
  gap: 40px;
  width: 100%;
  justify-content: center;
}

.card {
  flex: 1;
  min-width: 280px;
  max-width: 400px;
  background: white;
  border-radius: 20px;
  padding: 40px 32px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  border-top: 5px solid;
}

.card-create {
  border-color: #d69e2e;
  background: linear-gradient(to bottom, #fffaf0, #fed7d7);
}

.card-join {
  border-color: #3182ce;
  background: linear-gradient(to bottom, #ebf8ff, #e6fffa);
}

.card h2 {
  font-size: 28px;
  margin-bottom: 16px;
  color: #2d3748;
}

.card p {
  color: #4a5568;
  margin-bottom: 32px;
  line-height: 1.5;
}

.card input {
  width: 100%;
  padding: 14px 18px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 16px;
  margin-bottom: 24px;
  text-align: center;
}

.card-join input {
  border-color: #90cdf4;
}

.card button {
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.card-create button {
  background: #d69e2e;
  color: white;
}

.card-create button:hover {
  background: #b7791f;
}

.card-join button {
  background: #3182ce;
  color: white;
}

.card-join button:hover {
  background: #2c5282;
}

@media (max-width: 768px) {
  .page {
    padding: 30px 16px;
  }
  
  h1 {
    font-size: 36px;
  }
  
  .header p {
    font-size: 18px;
  }
  
  .cards {
    flex-direction: column;
    align-items: center;
    gap: 30px;
  }
}
</style>
