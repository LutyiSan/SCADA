//дожидаемся полной загрузки страницы
window.onload = function () {

    //получаем идентификатор элемента
    var a = document.querySelector('#id1');
    //вешаем на него событие
    a.onclick = function () {
        //производим какие-то действия
        a.innerHTML = "<h2>Привет, javascript!</h2><br><h3>Это круто я работаю<h3>";
    }
}