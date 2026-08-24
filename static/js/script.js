// 🔍 SEARCH
function searchPlaces() {
    let input = document.getElementById("search").value.toLowerCase();
    let cards = document.getElementsByClassName("card");

    for (let i = 0; i < cards.length; i++) {
        let text = cards[i].innerText.toLowerCase();
        cards[i].style.display = text.includes(input) ? "flex" : "none";
    }
}

// 🎯 FILTER
function filterCategory(category) {
    let sections = document.querySelectorAll(".category");

    sections.forEach(sec => {
        if (category === "all" || sec.dataset.category === category) {
           sec.style.display = "flex";
        } else {
            sec.style.display = "none";
        }
    });
}