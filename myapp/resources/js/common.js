console.log("It works...")

function router(type){
    switch(type){
        case 0:window.location.href = "/registration";//Перенаправление на страницу регистрации
        case 1:window.location.href = "/login";//Перенаправление на страницу авторизации
        default:console.log("Ошибка");
    }
}