<template>
    <div class="info-page">
        <button class="vincere-button home-button" @click="goToHome">
            <svg class="home-icon" viewBox="0 0 24 24">
                <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
            </svg>
            <span class="button-text">На главную</span>
        </button>
        
        <div class="info-container">
            <div class="info-card">
                <div class="logo-section">
                    <img src="@/assets/logo.png" 
                         alt="NASA Logo" class="nasa-logo">
                </div>
                <div class="content-section">
                    <h1 class="title">
                        Готовим к олимпиадам<br>
                        по всем предметам в<br>
                        <span class="highlight">режиме онлайн</span>
                    </h1>
                    <div class="features-list">
                        <div class="feature-item">
                            <span class="feature-marker">-</span>
                            <span class="feature-text">выпустили 1000 учеников</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-marker">-</span>
                            <span class="feature-text">подготовили 30000 учеников</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-marker">-</span>
                            <span class="feature-text">20+ наших учеников стали призерами</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-marker">-</span>
                            <span class="feature-text">2500+ наших учеников стали участниками</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Info",

    methods: {
        goToHome() {
            this.$router.push('/');
        },
    }
}
</script>

<style scoped>
.info-page {
    position: relative;
    min-height: 100vh;
    background-color: #FAF6EF;
    padding-top: 20px;
}

.info-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
    position: relative;
}

/* Надо придумать что-то с кнопкой */
.vincere-button.home-button {
    font-family: "Alexandria", sans-serif;
    background-color: #224762;
    color: white;
    border: none;
    padding: 12px 25px 12px 20px;
    border-radius: 50px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 6px 20px rgba(34, 71, 98, 0.25);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    position: absolute;
    top: 20px;
    right: 20px;
    z-index: 100;
    display: flex;
    align-items: center;
    gap: 10px;
    border: 2px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
}

.home-icon {
    width: 20px;
    height: 20px;
    fill: white;
    transition: transform 0.3s ease;
}

.button-text {
    position: relative;
    z-index: 2;
}


.vincere-button.home-button:hover {
    background-color: #1B3A50;
    transform: translateY(-1px) scale(1.05);
}


@media (max-width: 768px) {
    .vincere-button.home-button {
        position: fixed;
        top: 15px;
        right: 15px;
        padding: 10px 20px 10px 16px;
        font-size: 14px;
        letter-spacing: 0.5px;
        gap: 8px;
        border-radius: 40px;
        box-shadow: 0 4px 15px rgba(34, 71, 98, 0.25);
        z-index: 1001;
    }
    
    .home-icon {
        width: 18px;
        height: 18px;
    }
    
    .info-container {
        padding-top: 70px;
    }
    
    .vincere-button.home-button:active {
        transform: scale(0.95);
    }
    
    .vincere-button.home-button:hover {
        transform: translateY(-2px);
    }
}

@media (max-width: 480px) {
    .vincere-button.home-button {
        top: 10px;
        right: 10px;
        padding: 8px 16px 8px 12px;
        font-size: 12px;
        gap: 6px;
    }
    
    .home-icon {
        width: 16px;
        height: 16px;
    }
    
    .button-text {
        display: none;
    }
    
    .vincere-button.home-button {
        width: 45px;
        height: 45px;
        padding: 0;
        justify-content: center;
        border-radius: 50%;
    }
    
    .home-icon {
        width: 20px;
        height: 20px;
    }
    
    .info-container {
        padding-top: 60px;
    }
}

.info-card {
    width: 100%;
    max-width: 731px;
    height: 749px;
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 24px;
    padding: 40px;
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.08),
        0 8px 16px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
        
    border: 1px solid rgba(0, 0, 0, 0.06);
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    margin-top: 20px;
}

.info-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #4a90e2, #63b3ed, #90cdf4);
    border-radius: 24px 24px 0 0;
}

.logo-section {
    margin-bottom: 30px;
    text-align: center;
}

.nasa-logo {
    height: 80px;
    width: auto;
    filter: drop-shadow(0 6px 12px rgba(74, 144, 226, 0.2));
    border-radius: 90%;
}

.content-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-top: 10px;
}

.title {
    font-family: 'Inter', sans-serif;
    font-size: 42px;
    font-weight: 600;
    line-height: 1.3;
    margin-bottom: 40px;
    color: #1a202c;
    letter-spacing: -0.5px;
    margin-top: 0;
}

.highlight {
    color: #1e88e5;
    position: relative;
    display: inline-block;
}

.highlight::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #4a90e2, #63b3ed);
    border-radius: 2px;
    opacity: 0.7;
}

.features-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.feature-item {
    display: flex;
    align-items: center;
    padding: 12px 18px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 12px;
    border: 1px solid rgba(0, 0, 0, 0.04);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.feature-marker {
    font-size: 28px;
    color: #4a90e2;
    font-weight: 700;
    margin-right: 15px;
    min-width: 20px;
}

.feature-text {
    font-family: 'Inter', sans-serif;
    font-size: 20px;
    font-weight: 500;
    color: #2d3748;
    line-height: 1.4;
}

@media (max-width: 768px) {
    .info-card {
        height: auto;
        padding: 25px;
        margin: 15px;
        margin-top: 10px;
    }
    
    .title {
        font-size: 32px;
        margin-bottom: 30px;
    }
    
    .feature-text {
        font-size: 18px;
    }
    
    .feature-marker {
        font-size: 24px;
        margin-right: 12px;
    }
    
    .logo-section {
        margin-bottom: 20px;
    }
    
    .nasa-logo {
        height: 70px;
    }
}

@media (max-width: 480px) {
    .title {
        font-size: 26px;
    }
    
    .feature-text {
        font-size: 16px;
    }
    
    .info-card {
        padding: 20px;
    }
    
    .info-container {
        padding: 20px 10px;
    }
    
    .feature-item {
        padding: 10px 15px;
    }
}
</style>
