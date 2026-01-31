<script>
    import Info from '@/components/Info.vue';
    import axios from 'axios';

    export default {
        components: { Info },
        data() {
            return {
                email: '',
                password: '',
            }
        },
        methods: {
            async createUser() {
                try {
                    const response = await axios.post('http://localhost:8000/api/auth/login/', {
                        "username": this.username,
                        "password": this.password
                    });
                    // Здесь сервер ДОЛЖЕН вернуть токен
                    const token = response.data.access; // или response.data.token

                    // Сохраняем токен
                    localStorage.setItem('authToken', token);

                    // Настраиваем axios для автоматической отправки токена
                    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

                    // Перенаправляем на защищенную страницу
                    this.$router.push('/');
                } catch (err) {
                // обработка ошибок
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
                <a href="/auth" className="active">Вход </a> 
                <a href="/register" className="passive">Регистрация</a><br>
            </div>
            <div className="input">
                <p>Имя</p><br>
                <input type="text" className="enter" v-model="username"><br>
            </div>
            <div className="input">
                <p>Пароль</p><br>
                <input type="password" className="enter" v-model="password"><br><br>
            </div>
            <div className="add">
                <input type="checkbox" id="checkbox"> <a className ="checkboxA">Запомнить меня</a>
                <a href="/forgot" className="forgotten"> Забыли пароль?</a>
            </div>
            <div>
                <button className="enter_button" @click="createUser">Войти</button>
            </div>
        </div>
        <Info></Info>
    </body>
</template>

<style scoped>
Header {
    display: none;
}
</style>
