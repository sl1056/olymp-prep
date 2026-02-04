<template>
  <header class="header">
    <div class="header-content">
      <div class="left-section">
        <img 
          src="@/assets/logo.png"  
          alt="NASA Logo"
          class="logo"
          @click="goToHome"
          style="cursor: pointer;"
        >
        <span class="brand-name" @click="goToHome" style="cursor: pointer;">Vincere</span>
      </div>
      
      <div class="center-section">
        <div class="nav-buttons">
          <button class="nav-btn" @click="goToTraining">Тренинг</button>
          <button class="nav-btn" :class="{ active: $route.path === '/' }" @click="goToHome">Главная</button>
          <button class="nav-btn" @click="goToPvP">PvP</button>
        </div>
      </div>
      
      <div class="right-section">
        <button class="auth-btn" @click="Enter">Войти</button>
      </div>
      
      <button class="mobile-menu-toggle" @click="toggleMobileMenu">
        ☰
      </button>
    </div>
    
    <div class="mobile-menu-overlay" :class="{ 'active': isMobileMenuOpen }" @click="closeMobileMenu">
      <div class="mobile-menu" @click.stop>
        <div class="mobile-menu-header">
          <span class="mobile-brand-name" @click="goToHome" style="cursor: pointer;">Vincere</span>
          <button class="mobile-menu-close" @click="closeMobileMenu">×</button>
        </div>
        <div class="mobile-menu-buttons">

          <button class="mobile-nav-btn" @click="goToTraining">Тренинг</button>
          <button class="mobile-nav-btn" :class="{ active: $route.path === '/' }" @click="goToHome">Главная</button>
          <button class="mobile-nav-btn" @click="goToPvP">PvP</button>
          <button class="mobile-auth-btn" @click="goToProfile">{{ userData?.username || 'Профиль' }}</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: "Header",
  data() {
    return {
      isMobileMenuOpen: false
    };
  },
  mounted() {
    window.addEventListener('resize', this.handleResize);
    this.handleResize();
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    goToHome() {
      this.closeMobileMenu();
      this.$router.push('/');
    },
    
    goToTraining() {
      this.closeMobileMenu();
      this.$router.push('/tasks');
    },
    
    goToPvP() {
      this.closeMobileMenu();
      this.$router.push('/pvp');
    },
    
    goToAuth() {
      this.closeMobileMenu();
      this.$router.push('/auth');
    },
    
    toggleMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen;
    },
    
    closeMobileMenu() {
      this.isMobileMenuOpen = false;
    },
    
    handleResize() {
      if (window.innerWidth > 768 && this.isMobileMenuOpen) {
        this.isMobileMenuOpen = false;
      }
    },
    Enter() {
      location.href='/auth';
    },
    toggleMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen;
    },
    closeMobileMenu() {
      this.isMobileMenuOpen = false;
    },
    handleResize() {
      if (window.innerWidth > 768 && this.isMobileMenuOpen) {
        this.closeMobileMenu();
      }
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

.header {
  width: 100%;
  background-color: rgb(250, 246, 239);
  position: relative;
  height: 100px;
  display: flex;
  align-items: flex-start;
  padding-top: 20px;
}

.header-content {
  width: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 0 40px;
  position: relative;
}

.left-section {
    margin-top: -18px;
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
  padding-top: 10px;
}

.logo {
    border-radius: 100%;
  height: 88px;
  width: 108px;
  object-fit: contain;
  flex-shrink: 0;
}

.brand-name {
  font-family: "Alexandria", sans-serif;
  font-size: 30px;
  font-weight: 400;
  line-height: 1.2;
  white-space: nowrap;
}

.center-section {
  flex: 2;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 15px;
}

.nav-buttons {
  display: flex;
  gap: 100px;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
}

.nav-btn {
  font-family: "Roboto", sans-serif;
  border: none;
  background-color: #7896AA;
  font-size: 26px;
  width: 180px;
  height: 40px;
  border-radius: 60px;
  color: rgb(0, 0, 0);
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  flex-shrink: 0;
}

.nav-btn.active {
  background-color: #7896AA;
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.right-section {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
  padding-top: 15px;
}

.auth-btn {
  font-family: "Anonymous Pro", monospace;
  background-color: rgb(34, 71, 98);
  border: 2px solid rgb(34, 71, 98);
  color: white;
  font-size: 26px;
  width: 140px;
  height: 40px;
  border-radius: 60px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  flex-shrink: 0;
}

.auth-btn:hover {
  background-color: rgb(28, 58, 80);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.mobile-menu-toggle {
  display: none;
  font-size: 32px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px;
  color: #333;
  position: absolute;
  right: 20px;
  top: 40px;
  z-index: 100;
}

.mobile-menu-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.mobile-menu-overlay.active {
  display: block;
  opacity: 1;
}

.mobile-menu {
  position: fixed;
  top: 0;
  right: -300px;
  width: 300px;
  height: 100%;
  background-color: rgb(250, 246, 239);
  padding: 20px;
  display: flex;
  flex-direction: column;
  transition: right 0.3s ease;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
}

.mobile-menu-overlay.active .mobile-menu {
  right: 0;
}

.mobile-menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.mobile-brand-name {
  font-family: "Alexandria", sans-serif;
  font-size: 20px;
  font-weight: 400;
}

.mobile-menu-close {
  font-size: 36px;
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
  line-height: 1;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-menu-buttons {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.mobile-nav-btn,
.mobile-auth-btn {
  width: 100%;
  height: 50px;
  border-radius: 60px;
  border: none;
  font-family: "Roboto", sans-serif;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-nav-btn {
  background-color: #7896AA;
  color: #000;
}

.mobile-auth-btn {
  background-color: rgb(34, 71, 98);
  color: white;
  border-color: rgb(34, 71, 98);
  font-family: "Anonymous Pro", monospace;
  margin-top: 20px;
}

@media (max-width: 1400px) {
  .nav-buttons {
    gap: 80px;
  }
  
  .nav-btn {
    width: 160px;
    font-size: 24px;
  }
  
  .auth-btn {
    width: 130px;
    font-size: 24px;
  }
}

@media (max-width: 1200px) {
  .header-content {
    padding: 0 30px;
  }
  
  .nav-buttons {
    gap: 60px;
  }
  
  .nav-btn {
    width: 140px;
    font-size: 22px;
  }
  
  .auth-btn {
    width: 120px;
    font-size: 22px;
  }
  
  .brand-name {
    font-size: 22px;
  }
  
  .header {
    padding-top: 15px;
  }
  
  .left-section,
  .center-section,
  .right-section {
    padding-top: 15px;
  }
  
  .mobile-menu-toggle {
    top: 35px;
  }
}

@media (max-width: 1024px) {
  .header {
    height: 180px;
    padding-top: 15px;
  }
  
  .header-content {
    padding: 0 20px;
  }
  
  .nav-buttons {
    gap: 50px;
  }
  
  .nav-btn {
    width: 130px;
    height: 38px;
    font-size: 20px;
  }
  
  .auth-btn {
    width: 110px;
    height: 38px;
    font-size: 20px;
  }
  
  .logo {
    height: 75px;
    width: 90px;
  }
  
  .brand-name {
    font-size: 20px;
  }
  
  .left-section,
  .center-section,
  .right-section {
    padding-top: 12px;
  }
  
  .mobile-menu-toggle {
    top: 30px;
  }
}

@media (max-width: 900px) {
  .nav-buttons {
    gap: 40px;
  }
  
  .nav-btn {
    width: 120px;
    font-size: 18px;
  }
  
  .auth-btn {
    width: 100px;
    font-size: 18px;
  }
  
  .header {
    padding-top: 20px;
  }
  
  .left-section,
  .center-section,
  .right-section {
    padding-top: 15px;
  }
}

@media (max-width: 768px) {
  .header {
    height: 150px;
    padding-top: 15px;
  }
  
  .header-content {
    padding: 0 15px;
  }
  
  .center-section,
  .right-section {
    display: none;
  }
  
  .mobile-menu-toggle {
    display: block;
    top: 35px;
  }
  
  .left-section {
    flex: 1;
    padding-top: 5px;
  }
  
  .logo {
    height: 65px;
    width: 80px;
  }
  
  .brand-name {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .header {
    height: 130px;
    padding-top: 10px;
  }
  
  .logo {
    height: 55px;
    width: 70px;
  }
  
  .brand-name {
    font-size: 16px;
  }
  
  .mobile-menu {
    width: 280px;
  }
  
  .mobile-nav-btn,
  .mobile-auth-btn {
    height: 45px;
    font-size: 18px;
  }
  
  .mobile-menu-toggle {
    top: 30px;
  }
}

@media (max-width: 360px) {
  .brand-name {
    font-size: 14px;
  }
  
  .mobile-menu {
    width: 260px;
  }
}

@media (min-width: 1920px) {
  .header {
    height: 220px;
    padding-top: 30px;
  }
  
  .header-content {
    padding: 0 60px;
  }
  
  .nav-buttons {
    gap: 120px;
  }
  
  .nav-btn {
    width: 200px;
    height: 45px;
    font-size: 28px;
  }
  
  .auth-btn {
    width: 160px;
    height: 45px;
    font-size: 28px;
  }
  
  .logo {
    height: 100px;
    width: 120px;
  }
  
  .brand-name {
    font-size: 28px;
  }
  
  .left-section,
  .center-section,
  .right-section {
    padding-top: 20px;
  }
  
  .mobile-menu-toggle {
    top: 50px;
  }
}

@media (prefers-color-scheme: dark) {
  .header {
    background-color: #1a1a1a;
  }
  
  .brand-name,
  .mobile-brand-name {
    color: #ffffff;
  }
  
  .nav-btn {
    background-color: #2c3e50;
    color: #ffffff;
    border-color: #ffffff;
  }
  
  .auth-btn {
    background-color: #1e3a5c;
    border-color: #1e3a5c;
  }
  
  .mobile-menu {
    background-color: #1a1a1a;
  }
  
  .mobile-menu-header {
    border-bottom-color: #333;
  }
}
</style>
