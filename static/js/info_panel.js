var infoPanel = document.getElementById("infoPanel");
var toggleBtn = document.getElementById("toggleBtn");
var isOpen = false;

// Функция для открытия и закрытия информационного окна
function toggleInfoPanel() {
    if (isOpen) {
        infoPanel.style.right = "-370px";  // Закрываем окно
        toggleBtn.classList.remove("btn-danger");
        toggleBtn.classList.add("btn-primary");
        toggleBtn.innerHTML = "i"; // Заменяем текст на крестик
    } else {
        infoPanel.style.right = "0px";  // Открываем окно
        toggleBtn.classList.remove("btn-primary");
        toggleBtn.classList.add("btn-danger");
        toggleBtn.innerHTML = "&times;"; // Заменяем текст на знак инфо
    }
    isOpen = !isOpen;
}

// По клику на кнопку, переключаем состояние окна
toggleBtn.addEventListener("click", toggleInfoPanel);
