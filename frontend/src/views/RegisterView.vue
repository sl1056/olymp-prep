<script>
    import Info from '@/components/Info.vue';
    import axios from 'axios';

    export default {
    components: { Info },
    data() {
        return {
            username: '',
            email: '',
            password: '',
            isLoading: false,
            errorMessage: '',
            successMessage: ''
        }
    },
    methods: {
        async createUser() {
            // Валидация на клиенте
            if (!this.username || !this.email || !this.password) {
                this.errorMessage = 'Все поля обязательны для заполнения';
                return;
            }
            
            if (this.password.length < 6) {
                this.errorMessage = 'Пароль должен содержать минимум 6 символов';
                return;
            }
            
            this.isLoading = true;
            this.errorMessage = '';
            this.successMessage = '';
            
            try {
                const response = await axios.post('http://localhost:8000/api/auth/register/', {
                    "username": this.username,
                    "email": this.email,
                    "password": this.password
                });
                
                // Обработка успешной регистрации
                this.successMessage = 'Регистрация успешна!';
                console.log('Пользователь создан:', response.data);

                this.$router.push('/auth');
                
                // Можно перенаправить пользователя или очистить форму
                // 
                
                // Очистка формы после успешной регистрации
                this.username = '';
                this.email = '';
                this.password = '';
                
            } catch (err) {
                // Обработка ошибок
                if (err.response) {
                    // Сервер ответил с ошибкой
                    if (err.response.data) {
                        this.errorMessage = err.response.data.message || 
                                           JSON.stringify(err.response.data);
                    }
                } else if (err.request) {
                    // Запрос был сделан, но ответа не получено
                    this.errorMessage = 'Ошибка сети. Проверьте подключение к интернету';
                } else {
                    // Ошибка при настройке запроса
                    this.errorMessage = 'Произошла ошибка: ' + err.message;
                }
                console.error('Ошибка регистрации:', err);
            } finally {
                this.isLoading = false;
            }
        }
    }
}
</script>

<template>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Anonymous+Pro:ital,wght@0,400;0,700;1,400;1,700&family=Inter:opsz,wght@14..32,501&display=swap" rel="stylesheet">
    </head>
    <body>
        <div className="app">
            <div className="select">
                <a href="/auth" className="passive">Вход </a> 
                <a href="/register" className="active">Регистрация</a><br>
            </div>
            <div className="input">
                <p>Имя</p><br>
                <input type="text" className="enter" v-model="username"><br>
            </div>
            <div className="input">
                <p>Email</p><br>
                <input type="email" className="enter" v-model="email"><br>
            </div>
            <div className="input">
                <p>Пароль</p><br>
                <input type="password" className="enter" v-model="password"><br><br>
            </div>
            <div>
                <button className="enter_button" @click="createUser">Зарегистрироваться</button>
            </div>
        </div>
        <Info></Info>
    </body>
</template>

<style scoped>
header {
    display: none;
}
</style>
