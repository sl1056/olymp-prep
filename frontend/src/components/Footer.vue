<template>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@100..900&family=Anonymous+Pro:ital,wght@0,400;0,700;1,400;1,700&family=Inter:opsz,wght@14..32,501&display=swap" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@100..900&family=Anonymous+Pro:ital,wght@0,400;0,700;1,400;1,700&family=Inter:opsz,wght@14..32,501&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    </head>
    <footer>
        <div class="footer-container">
            <div class="footer-content">
                <div class="contact-info">
                    <div class="footer-item">
                        <i class="fas fa-phone-alt"></i>
                        <span class="footer-text">8-800-555-35-35</span>
                    </div>
                    
                    <div class="footer-item">
                        <i class="fas fa-envelope"></i>
                        <span class="footer-text">pomoshi.net@mail.ru</span>
                    </div>
                    
                    <div class="footer-item">
                        <i class="fab fa-github"></i>
                        <a href="https://github.com/sl1056/olymp-prep" target="_blank" class="footer-text github-link">GitHub</a>
                    </div>
                </div>
                
                <div class="footer-bottom">
                    <p class="copyright">© 2026 Vincere. Все права защищены.</p>
                    <p class="tagline">Подготовка к олимпиадам онлайн</p>
                </div>
            </div>
        </div>
    </footer>
</template>

<script>
export default {
    name: "Footer",
}
</script>

<style scoped>
footer {
    width: 100%;
    background-color: rgb(38, 38, 38);
    margin-top: auto;
}

.footer-container {
    max-width: 1881px;
    margin: 0 auto;
    padding: 0 20px;
}

.footer-content {
    padding: 50px 0 30px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 40px;
}

.contact-info {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 80px;
    width: 100%;
}

.footer-item {
    display: flex;
    align-items: center;
    gap: 15px;
    min-height: 40px;
}

.footer-item i {
    font-size: 24px;
    color: #7896AA;
    width: 30px;
    text-align: center;
}

.footer-text {
    font-size: 24px;
    font-family: "Anonymous Pro", monospace;
    color: aliceblue;
    line-height: 1;
    display: inline-block;
    vertical-align: middle;
}

.github-link {
    text-decoration: none;
    color: aliceblue;
    transition: all 0.3s ease;
}

.github-link:hover {
    color: #7896AA;
    transform: translateY(-2px);
}

.footer-bottom {
    text-align: center;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 25px;
    width: 100%;
    margin-top: 20px;
}

.copyright {
    font-family: "Inter", sans-serif;
    font-size: 16px;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 10px;
}

.tagline {
    font-family: "Alexandria", sans-serif;
    font-size: 18px;
    color: rgba(255, 255, 255, 0.8);
    font-weight: 300;
}

@media (max-width: 1024px) {
    .footer-content {
        padding: 40px 0 25px;
        gap: 35px;
    }
    
    .contact-info {
        gap: 60px;
    }
    
    .footer-text {
        font-size: 22px;
    }
    
    .footer-item i {
        font-size: 22px;
        width: 28px;
    }
    
    .footer-item {
        gap: 12px;
    }
}

@media (max-width: 768px) {
    .footer-content {
        padding: 35px 0 20px;
        gap: 30px;
    }
    
    .contact-info {
        gap: 40px;
        flex-direction: column;
    }
    
    .footer-item {
        min-height: auto;
        justify-content: center;
    }
    
    .footer-text {
        font-size: 20px;
    }
    
    .footer-item i {
        font-size: 20px;
        width: 26px;
    }
    
    .copyright {
        font-size: 15px;
    }
    
    .tagline {
        font-size: 17px;
    }
}

@media (max-width: 480px) {
    .footer-container {
        padding: 0 15px;
    }
    
    .footer-content {
        padding: 30px 0 20px;
        gap: 25px;
    }
    
    .contact-info {
        gap: 25px;
    }
    
    .footer-text {
        font-size: 18px;
    }
    
    .footer-item i {
        font-size: 18px;
        width: 24px;
    }
    
    .footer-item {
        gap: 10px;
    }
    
    .footer-bottom {
        padding-top: 20px;
        margin-top: 15px;
    }
    
    .copyright {
        font-size: 14px;
        margin-bottom: 8px;
    }
    
    .tagline {
        font-size: 16px;
    }
}

@media (max-width: 360px) {
    .footer-text {
        font-size: 16px;
    }
    
    .footer-item i {
        font-size: 16px;
        width: 22px;
    }
    
    .copyright {
        font-size: 13px;
    }
    
    .tagline {
        font-size: 15px;
    }
}

@media (min-width: 1921px) {
    .footer-container {
        max-width: 1800px;
    }
    
    .footer-content {
        padding: 60px 0 40px;
        gap: 45px;
    }
    
    .contact-info {
        gap: 100px;
    }
    
    .footer-text {
        font-size: 26px;
    }
    
    .footer-item i {
        font-size: 26px;
        width: 32px;
    }
    
    .copyright {
        font-size: 18px;
    }
    
    .tagline {
        font-size: 20px;
    }
}
</style>
