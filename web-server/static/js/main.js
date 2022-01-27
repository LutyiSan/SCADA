//дожидаемся полной загрузки страницы
window.onload = function () {

    //получаем идентификатор элемента
    var a = document.querySelector('.create');
    var b = document.querySelector('#center');
    //вешаем на него событие
    a.onmouseover = function () {
        //производим какие-то действия
        console.log(a)
        b.innerHTML = "<h2>Это уже JAVA-SCRIPT</h2>";
        }
       a.onmouseout = function () {
        //производим какие-то действия
        console.log(a)
        b.innerHTML = "<h2>PYTHON+JAVA-SCRIPT захватит МИР!)</h2>";
    }
}