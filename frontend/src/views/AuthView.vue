<template>
    <div class="auth-page">
        <div class="container">
            <div class="left-panel">
                <Info />
            </div>
            <div class="right-panel">
                <div class="auth-card">
                    <div class="auth-header">
                        <h2>Добро пожаловать</h2>
                        <p>Войдите в свой аккаунт</p>
                    </div>
                    
                    <div class="tab-switcher">
                        <router-link to="/auth" :class="['tab', $route.path === '/auth' ? 'active' : '']">
                            Вход
                        </router-link>
                        <router-link to="/register" :class="['tab', $route.path === '/register' ? 'active' : '']">
                            Регистрация
                        </router-link>
                        <div class="tab-indicator"></div>
                    </div>
                    
                    <form @submit.prevent="createUser" class="auth-form">
                        <div class="form-group">
                            <label for="username">Имя пользователя</label>
                            <input 
                                type="text" 
                                id="username" 
                                v-model="username"
                                placeholder="Введите имя пользователя"
                                required
                            >
                            <div class="input-icon">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                                    <circle cx="12" cy="7" r="4"/>
                                </svg>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label for="password">Пароль</label>
                            <input 
                                type="password" 
                                id="password" 
                                v-model="password"
                                placeholder="Введите пароль"
                                required
                            >
                            <div class="input-icon">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                                </svg>
                            </div>
                        </div>
                        
                        <div class="form-options">
                            <label class="checkbox-label">
                                <input type="checkbox" id="remember">
                                <span class="checkmark"></span>
                                Запомнить меня
                            </label>
                            <router-link to="/forgot" class="forgot-link">
                                Забыли пароль?
                            </router-link>
                        </div>
                        
                        <button type="submit" class="submit-btn" :disabled="isLoading">
                            <span v-if="isLoading">
                                <svg class="spinner" viewBox="0 0 50 50">
                                    <circle cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
                                </svg>
                            </span>
                            <span v-else>Войти</span>
                        </button>
                        
                        <div v-if="errorMessage" class="error-message">
                            {{ errorMessage }}
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Info from '@/components/Info.vue';
import axios from 'axios';

export default {
    name: 'AuthView',
    components: { Info },
    data() {
        return {
            username: '',
            password: '',
            isLoading: false,
            errorMessage: ''
        }
    },
    methods: {
        async createUser() {
            this.isLoading = true;
            this.errorMessage = '';
            
            try {
                const response = await axios.post('http://localhost:8000/api/auth/login/', {
                    username: this.username,
                    password: this.password
                });
                
                const token = response.data.access;
                localStorage.setItem('authToken', token);
                axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                
                this.$router.push('/');
            } catch (err) {
                this.errorMessage = err.response?.data?.detail || 
                                  'Неверное имя пользователя или пароль';
            } finally {
                this.isLoading = false;
            }
        }
    }
}
</script>

<style scoped>
.auth-page {
    min-height: 100vh;
    background: rgb(250, 246, 239);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    font-family: 'Inter', sans-serif;
}

.container {
    display: flex;
    max-width: 1400px;
    width: 100%;
    gap: 40px;
    align-items: center;
    justify-content: center;
}

.left-panel {
    flex: 1;
    max-width: 731px;
}

.right-panel {
    flex: 1;
    max-width: 480px;
}

.auth-card {
    background: white;
    border-radius: 24px;
    padding: 50px;
    box-shadow: 
        0 20px 60px rgba(0, 0, 0, 0.1),
        0 0 40px rgba(74, 144, 226, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.auth-header {
    text-align: center;
    margin-bottom: 40px;
}

.auth-header h2 {
    font-size: 32px;
    font-weight: 700;
    color: #1a202c;
    margin-bottom: 10px;
}

.auth-header p {
    font-size: 16px;
    color: #718096;
    font-weight: 400;
}

.tab-switcher {
    display: flex;
    background: #f7fafc;
    border-radius: 12px;
    padding: 4px;
    margin-bottom: 40px;
    position: relative;
}

.tab {
    flex: 1;
    padding: 14px 20px;
    text-align: center;
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
    color: #718096;
    border-radius: 8px;
    transition: all 0.3s ease;
    position: relative;
    z-index: 1;
}

.tab.active {
    color: #4a90e2;
    background: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.tab-indicator {
    position: absolute;
    transition: all 0.3s ease;
}

.auth-form {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.form-group {
    margin-right: 15%;
    position: relative;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: #4a5568;
    font-size: 14px;
}

.form-group input {
    width: 100%;
    padding: 16px 20px 16px 50px;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    font-size: 16px;
    font-family: 'Inter', sans-serif;
    transition: all 0.3s ease;
    background: #f8fafc;
}

.form-group input:focus {
    outline: none;
    border-color: #4a90e2;
    background: white;
    box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.input-icon {
    margin-top: 3.5%;
    position: absolute;
    left: 20px;
    top: 42px;
    transform: translateY(-50%);
    color: #a0aec0;
}

.form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 10px 0;
}

.checkbox-label {
    display: flex;
    align-items: center;
    cursor: pointer;
    font-size: 14px;
    color: #4a5568;
    user-select: none;
}

.checkbox-label input {
    display: none;
}

.checkmark {
    width: 20px;
    height: 20px;
    border: 2px solid #e2e8f0;
    border-radius: 6px;
    margin-right: 10px;
    position: relative;
    transition: all 0.3s ease;
}

.checkbox-label input:checked + .checkmark {
    background: #4a90e2;
    border-color: #4a90e2;
}

.checkbox-label input:checked + .checkmark::after {
    content: '✓';
    position: absolute;
    color: white;
    font-size: 14px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.forgot-link {
    color: #4a90e2;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    transition: color 0.3s ease;
}

.forgot-link:hover {
    color: #2c5282;
    text-decoration: underline;
}

.submit-btn {
    background: #1763a5;
    color: white;
    border: none;
    padding: 18px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 10px;
    position: relative;
    overflow: hidden;
}

.submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(74, 144, 226, 0.3);
}

.submit-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.spinner {
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite;
}

.spinner circle {
    stroke: white;
    stroke-linecap: round;
    stroke-dasharray: 90, 150;
    stroke-dashoffset: 0;
    animation: dash 1.5s ease-in-out infinite;
}

.error-message {
    background: #fed7d7;
    color: #c53030;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 14px;
    margin-top: 10px;
    text-align: center;
    border: 1px solid #fc8181;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes dash {
    0% { stroke-dasharray: 1, 150; stroke-dashoffset: 0; }
    50% { stroke-dasharray: 90, 150; stroke-dashoffset: -35; }
    100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124; }
}

@media (max-width: 1024px) {
    .container {
        flex-direction: column;
        gap: 30px;
    }
    
    .left-panel,
    .right-panel {
        max-width: 100%;
        width: 100%;
    }
    
    .auth-card {
        padding: 40px 30px;
    }
}

@media (max-width: 640px) {
    .auth-card {
        padding: 30px 20px;
    }
    
    .auth-header h2 {
        font-size: 28px;
    }
    
    .form-options {
        flex-direction: column;
        gap: 15px;
        align-items: flex-start;
    }
}
</style>
