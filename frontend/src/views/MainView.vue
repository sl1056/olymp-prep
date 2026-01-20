<script>
    import Header from '@/components/Header.vue';
    import Footer from '@/components/Footer.vue';
    import axios from 'axios';

    export default {
        components: { Header, Footer },
    }
</script>

<template>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Anonymous+Pro:ital,wght@0,400;0,700;1,400;1,700&family=Inter:opsz,wght@14..32,501&display=swap" rel="stylesheet">

        <link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@100..900&display=swap" rel="stylesheet">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        

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

        <!-- Карточки "Почему именно мы?" -->
        <div class="cards-container">
            <h2 class="cards-title">Почему именно мы?</h2>
            <div class="cards-grid">
                <div class="info-card">
                    <i class="card-icon fas fa-chalkboard-teacher"></i>
                    <h3 class="card-title">Инновационный подход</h3>
                    <div class="card-separator"></div>
                    <div class="card-content">
                        <p class="textForCard">Мы создаем уникальную образовательную среду для раскрытия потенциала.</p>
                        <p class="textForCard">Тихо, без лишней суеты и гонки.</p>
                    </div>
                </div>
                <div class="info-card">
                    <i class="card-icon fas fa-book-open"></i>
                    <h3 class="card-title">Широкий выбор материалов</h3>
                    <div class="card-separator"></div>
                    <div class="card-content">
                        <p class="textForCard">У нас много предметов и задач для всестороннего развития.</p>
                        <div class="highlight-card">24 предмета и более 10000 заданий</div>
                    </div>
                </div>
                <div class="info-card">
                    <i class="card-icon fas fa-trophy"></i>
                    <h3 class="card-title">Соревновательный элемент</h3>
                    <div class="card-separator"></div>
                    <div class="card-content">
                        <p class="textForCard">Возможность соревноваться друг с другом в дружеской атмосфере.</p>
                        <div class="highlight-card">Рейтинг и подробная статистика</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="container">
        <section class="courses-section">
            <h2 class="section-title">Олимпиадные предметы</h2>
            <div class="courses-grid">
                <!-- Математические предметы -->
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-calculator"></i></div>
                    <div class="course-name"><a class="href_on_card">Математика</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-shapes"></i></div>
                    <div class="course-name"><a class="href_on_card">Геометрия</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-infinity"></i></div>
                    <div class="course-name"><a class="href_on_card">Дискретная математика</a></div>
                </div>
                
                <!-- Естественные науки -->
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-atom"></i></div>
                    <div class="course-name"><a class="href_on_card">Физика</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-flask"></i></div>
                    <div class="course-name"><a class="href_on_card">Химия</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-dna"></i></div>
                    <div class="course-name"><a class="href_on_card">Биология</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-mountain"></i></div>
                    <div class="course-name"><a class="href_on_card">Экология</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-globe-europe"></i></div>
                    <div class="course-name"><a class="href_on_card">География</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-satellite"></i></div>
                    <div class="course-name"><a class="href_on_card">Астрономия</a></div>
                </div>
                
                <!-- Филология и языки -->
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-language"></i></div>
                    <div class="course-name"><a class="href_on_card">Русский язык</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-book-open"></i></div>
                    <div class="course-name"><a class="href_on_card">Литература</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-globe-americas"></i></div>
                    <div class="course-name"><a class="href_on_card">Английский язык</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-flag"></i></div>
                    <div class="course-name"><a class="href_on_card">Немецкий язык</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-comments"></i></div>
                    <div class="course-name"><a class="href_on_card">Французский язык</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-torii-gate"></i></div>
                    <div class="course-name"><a class="href_on_card">Китайский язык</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-feather-alt"></i></div>
                    <div class="course-name"><a class="href_on_card">Испанский язык</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-scroll"></i></div>
                    <div class="course-name"><a class="href_on_card">Латинский язык</a></div>
                </div>
                
                <!-- Гуманитарные науки -->
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-landmark"></i></div>
                    <div class="course-name"><a class="href_on_card">История</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-users"></i></div>
                    <div class="course-name"><a class="href_on_card">Обществознание</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-balance-scale"></i></div>
                    <div class="course-name"><a class="href_on_card">Право</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-coins"></i></div>
                    <div class="course-name"><a class="href_on_card">Экономика</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-chart-line"></i></div>
                    <div class="course-name"><a class="href_on_card">Финансовая грамотность</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-palette"></i></div>
                    <div class="course-name"><a class="href_on_card">Искусство (МХК)</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fa-solid fa-gears"></i></div>
                    <div class="course-name"><a class="href_on_card">Технология</a></div>
                </div>
                
                <!-- Информатика и технологии -->
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-laptop-code"></i></div>
                    <div class="course-name"><a class="href_on_card">Информатика</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-robot"></i></div>
                    <div class="course-name"><a class="href_on_card">Робототехника</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-brain"></i></div>
                    <div class="course-name"><a class="href_on_card">Искусственный интеллект</a></div>
                </div>
                
                <!-- Другие -->
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-heartbeat"></i></div>
                    <div class="course-name"><a class="href_on_card">Физкультура</a></div>
                </div>
                <div class="course-card">
                    <div class="course-icon"><i class="fas fa-shield-alt"></i></div>
                    <div class="course-name"><a class="href_on_card">ОБЖ</a></div>
                </div>
            </div>
        </section>
        </div>

        <div style="margin-bottom: 80px;"></div>

        <Footer></Footer>
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
    min-height: 0px;
    padding: 50px 20px;
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
}

.highlight {
    background-color: #F8F7FE;
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

.centered-btn:hover {
    background-color: rgb(44, 91, 128);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
    transform: translateY(-3px);
}

.centered-btn:active {
    transform: translateY(1px);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

/* Стили для карточек "Почему именно мы?" */
.cards-container {
    max-width: 1200px;
    margin: 60px auto;
    padding: 0 20px;
}

.cards-title {
    text-align: center;
    color: #2d3748;
    margin-bottom: 50px;
    font-size: 2.5rem;
    font-family: "Alexandria", sans-serif;
    font-weight: 700;
}

.cards-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
}

.info-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 5px 20px rgba(0,0,0,.08);
    padding: 35px;
    text-align: center;
    transition: transform .3s;
    font-family: "Alexandria", sans-serif;
}

.info-card:hover {
    transform: translateY(-5px);
}

.card-icon {
    font-size: 3rem;
    margin-bottom: 25px;
    color: rgb(34, 71, 98);
}

.card-title {
    font-size: 1.6rem;
    color: #2d3748;
    margin-bottom: 20px;
    font-weight: 600;
}

.card-content {
    color: #4a5568;
    line-height: 1.6;
    font-size: 1.1rem;
}

.card-content p {
    margin-bottom: 15px;
}

.highlight-card {
    background: #eef2ff;
    color: rgb(34, 71, 98);
    padding: 8px 16px;
    border-radius: 20px;
    margin: 15px 0;
    display: inline-block;
    font-weight: 600;
    font-size: 1.1rem;
}

.card-separator {
    width: 60px;
    height: 3px;
    background: #e2e8f0;
    margin: 20px auto;
}

.container {
    font-family: "Alexandria", sans-serif;
    font-style: normal;
    max-width: 1200px;
    margin: 0 auto;
    background-color: #F8F7FE;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 100, 0.08);
    overflow: hidden;
}

h1 {
    font-family: "Alexandria", sans-serif;
    font-style: normal;
    font-size: 2.8rem;
    margin-bottom: 10px;
    font-weight: 700;
}

.courses-section {
    padding: 40px;
}

.section-title {
    font-size: 1.8rem;
    color: rgb(0, 0, 0);
    text-align: center;
    margin-bottom: 25px;
    padding-bottom: 10px;
    font-weight: 600;
}

.courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 40px;
}

.course-card {
    background-color: #f0f7ff;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    cursor: pointer;
}

.course-card:hover {
    transform: translateY(-5px);
    border-color: rgb(34, 71, 98);
    box-shadow: 0 8px 20px rgba(26, 109, 255, 0.15);
}

.course-icon {
    font-size: 2.5rem;
    color: rgb(34, 71, 98);
    margin-bottom: 15px;
}

.course-name {
    font-family: "Alexandria", sans-serif;
    font-style: normal;
    font-weight: 600;
    font-size: 1.1rem;
}

.href_on_card {
    font-family: "Alexandria", sans-serif;
    font-style: normal;
    font-size: 20px;
    font-weight: 600;
    text-align: center;
}

.textForCard {
    font-family: "Alexandria", sans-serif;
    font-style: normal;
    font-size: 20px;
    font-weight: 600;
    text-align: center;
}
</style>
