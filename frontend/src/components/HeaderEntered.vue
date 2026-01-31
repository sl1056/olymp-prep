<template>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@100..900&family=Anonymous+Pro:ital,wght@0,400;0,700;1,400;1,700&family=Inter:opsz,wght@14..32,501&display=swap" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@100..900&family=Anonymous+Pro:ital,wght@0,400;0,700;1,400;1,700&family=Inter:opsz,wght@14..32,501&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    </head>
    <header>
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/800px-NASA_logo.svg.png" height="88" width="108">
        <a>sasa and<br>olympiad</a>
        <div className="buttons">
            <button>Предметы</button>
            <button style="background-color: rgb(216, 226, 228);">Меню</button>
            <button>PvP</button>
        </div>
        <h1>{{ userData?.username }}</h1>
        <button className="enter_button" style="float: right;" @click="Enter">{{ userData?.username }}</button>
    </header>
</template>

<script>
import axios from 'axios';

export default {
    name: "HeaderEntered",
    methods: {
        Enter() {
            location.href='/auth';
        }
    },
    async created() {
        await this.getUser();
    },
    async getUser() {
        try {
            // Автоматически добавится заголовок Authorization через interceptor
            const response = await axios.get('http://localhost:8000/api/auth/profile/');
            this.userData = response.data;
        } catch (err) {
            if (err.response && err.response.status === 401) {
                // Токен истек или недействителен
                this.$router.push('/auth');
            }
        } finally {
            this.isLoading = false;
        }
    }
}
</script>

<style scoped>

header {
    display: flex;
    width: 1900px;
    height: 200px;
}
.left {
    text-align: left;
}
.center {
    text-align: center;
    margin-bottom: 100px;
}
h1 {
    font-size: 52px;
    font-weight: 100;
}
a {
    margin-top: 12px;
    margin-left: 120px;
    position: absolute;
    font-size: 25px;
    font-weight: 1;
    font-weight: 400;
    font-family: "Alexandria", normal;
}
button {
    font-family: "Roboto", normal;
    border-color: rgb(0, 0, 0);
    background-color: rgb(255, 255, 255);
    line-height: 0;
    font-size: 26px;
    width: 12%;
    height: 40px;
    box-sizing: border-box;
    border-radius: 60px;
    color: rgb(0, 0, 0);
    letter-spacing: 0.011em;
    margin-left: 100px;
    margin-top: 20px;
}
.buttons {
    text-align: center;
    margin-bottom: 100px;
    width: 1900px;
}
.enter_button {
    margin-right: 10px;
    font-family: "Anonymous Pro", monospace;
    appearance: none;
    border-color: rgb(34, 71, 98);
    background-color: rgb(34, 71, 98);
    line-height: 0;
    font-size: 26px;
    width: 8%;
    height: 40px;
    display: block;
    box-sizing: border-box;
    border-radius: 60px;
    color: white;
    letter-spacing: 0.011em;
    position: center;
}
</style>