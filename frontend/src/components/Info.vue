<template>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,500&display=swap" rel="stylesheet">
    </head>
    <body>
        <div className="info">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/800px-NASA_logo.svg.png" height="100" width="120">
            <h1>Готовим к олимпиадам<br>по всем предметам в<br>режиме онлайн</h1>
            <p>-выпустили нихуя<br>-подготовили тоже<br>-0 наших учеников стали призерами<br>-0 наших учеников стали участниками<br></p>
        </div>
    </body>
</template>

<script>
export default {
    name: "Info",
}
</script>

<style scoped>

.info {
    width: 731px;
    height: 749px;
    text-align: left;
    font-family: "Inter", Medium;
    margin-left: 20px;
    border: solid;
    border-color: rgb(216, 214, 212);
}
h1 {
    margin-left: 57px;
    font-size: 52px;
    font-weight: 100;
}
p {
    margin-left: 57px;
    font-size: 30px;
    font-weight: 1;
}
img {
    margin-left: 57px;
}
</style>