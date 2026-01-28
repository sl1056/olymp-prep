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
                        "email": this.email,
                        "password": this.password
                    });
                } catch (err) {}
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
                <p>Email</p><br>
                <input type="email" className="enter" v-model="email"><br>
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
