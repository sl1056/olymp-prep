<script>
    import Header from '@/components/Header.vue';
    import axios from 'axios';

    export default {
        components: { Header },
    }
</script>

<template>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Anonymous+Pro:ital,wght@0,400;0,700;1,400;1,700&family=Inter:opsz,wght@14..32,501&display=swap" rel="stylesheet">

        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@100..900&display=swap" rel="stylesheet">
    </head>
    <body>
        <Header></Header>
        {{ this.user }}       
        <p class="text1">Платформа для подготовки <br> к олимпиадам <br>sasa and olympiad</p>
        <h5>мы подготавливаем школьников 5-11 класса, для участия в олимпиадах</h5>

        <div class="button-container">
            <a href="ТУТ БУДЕТ ССЫЛКА" target="_blank">
                <button class="centered-btn">
                    Начать решать
                </button>
            </a>
        </div>

       <div class="content">
            <div class="highlight">
                <p class="text2">Наша цель — не просто занятия, а ваш результат: <br>
            диплом, льготы при поступлении в вуз, развитие <br>мышления</p>
            </div>                    
        </div>

    </body>

</template>

<style scoped>

body {
    background-color: rgb(250, 246, 239);
    margin: 0;
    padding: 0;
    width: 100vw;
    max-width: 100%;
    overflow-x: hidden;
    
    min-height: 100vh;
}

.content {
            min-height: 1500px;
            padding: 50px 20px;
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
        }

.highlight {
            background-color: #E0DFE1;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
            border-left: 4px solid rgb(34, 71, 98);
        }

.text1 {
    text-align: center;

    font-family: "Alexandria", sans-serif;
    font-style: normal;
    font-size: 85px;

    margin-top: -100px;
}

.text2 {
    text-align: center;

    font-family: "Alexandria", sans-serif;
    font-style: normal;
    font-size: 30px;
    font-weight: 300;

}

h5 {
    font-family: "Alexandria", sans-serif;
    font-style: normal;
    font-size: 20px;
    font-weight: 500;
    text-align: center;
}

 .button-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 50px 20;
            padding: 20px;
        }
        
        /* Стили для кнопки */
        .centered-btn {
            background-color: rgb(34, 71, 98);
            color: white;
            border: none;
            padding: 18px 40px;
            border-radius: 90px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Эффекты при наведении */
        .centered-btn:hover {
            background-color: rgb(44, 91, 128);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
            transform: translateY(-3px);
        }
        
        /* Эффект при нажатии */
        .centered-btn:active {
            transform: translateY(1px);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        }

</style>
