const messageBtn = document.getElementById('message-btn');
const closeBtn = document.getElementById('close-btn');
const menu = document.getElementById('menu');

messageBtn.addEventListener('click', (event) => {
    menu.classList.remove('hidden');
    menu.classList.add('flex');
    messageBtn.classList.add('hidden');
    event.stopPropagation();
});

closeBtn.addEventListener('click', (event) => {
    menu.classList.add('hidden');
    menu.classList.remove('flex');
    event.stopPropagation();
    messageBtn.classList.remove('hidden');
});

document.addEventListener('click', (event) => {
    if (!menu.contains(event.target) && !messageBtn.contains(event.target)) {
        menu.classList.add('hidden');
        menu.classList.remove('flex');
        messageBtn.classList.remove('hidden');
    }
});