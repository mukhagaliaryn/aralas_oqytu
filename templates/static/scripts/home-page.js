// Swiper
var swiper = new Swiper(".mySwiper", {
    slidesPerView: 1,
    spaceBetween: 8,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        920: {
            slidesPerView: 2,
        },
        1680: {
            slidesPerView: 3,
        },
    },
});


// Calendar
const calendarGrid = document.getElementById('calendar-grid');
const calendarHeader = document.getElementById('month-name');
const prevMonthBtn = document.getElementById('prev-month');
const nextMonthBtn = document.getElementById('next-month');

let currentDate = new Date();

function renderCalendar(date) {
    const year = date.getFullYear();
    const month = date.getMonth();

    // Название месяца
    const monthNames = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ];
    calendarHeader.textContent = `${monthNames[month]} ${year}`;

    // Очистка старых дней
    calendarGrid.innerHTML = '';

    // Получаем первый день и количество дней в месяце
    const firstDayOfMonth = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Заполнение пустых ячеек перед первым днем
    for (let i = 0; i < (firstDayOfMonth || 7) - 1; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.classList.add('day');
        calendarGrid.appendChild(emptyCell);
    }

    // Заполнение дней месяца
    for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement('div');
        dayCell.classList.add('day');
        dayCell.textContent = day;
        dayCell.addEventListener('click', () => {
            alert(`Вы выбрали ${day}-${month + 1}-${year}`);
        });

        // Выделяем текущий день
        const today = new Date();
        if (
            day === today.getDate() &&
            month === today.getMonth() &&
            year === today.getFullYear()
        ) {
            dayCell.classList.add('today');
        }

        calendarGrid.appendChild(dayCell);
    }
}

// Первая загрузка календаря
renderCalendar(currentDate);

// Навигация по месяцам
prevMonthBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar(currentDate);
});

nextMonthBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar(currentDate);
});