<script>
    import Info from '@/components/Info.vue';

    export default {
        components: { Info },
        data() {
            return {
                name: '',
                email: '',
                password: '',
                user: [],
            }
        },
        created() {
            axios.get("http://localhost:5173/api/auth/register/")
                .then(response => {
                    this.user = response.data
                })
                .catch(error => {
                    console.error(error) 
                })  
        },
        methods: {
 
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
                <input type="text" className="enter" v-model="name"><br>
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
                <button className="enter_button">Зарегистрироваться</button>
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
