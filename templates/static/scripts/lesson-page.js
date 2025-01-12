var swiper = new Swiper(".lessonSwiper", {
    spaceBetween: 50,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});



// Run Code Logic
document.getElementById("runButton").addEventListener("click", () => {
    const htmlCode = document.getElementById("htmlCode").value;
    const cssCode = `<style>${document.getElementById("cssCode").value}</style>`;
    const jsCode = `<script>${document.getElementById("jsCode").value}<\/script>`;
    const output = document.getElementById("output").contentWindow.document;

    // Combine HTML, CSS, and JS and render in the iframe
    output.open();
    output.write(htmlCode + cssCode + jsCode);
    output.close();
});