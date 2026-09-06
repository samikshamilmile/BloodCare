document.addEventListener("DOMContentLoaded", function () {

    const themeButton = document.getElementById("theme");

    // Saved theme load karo
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark");
    } else {
        document.body.classList.remove("dark");
    }

    // Theme toggle
    if (themeButton) {
        themeButton.addEventListener("click", function () {

            document.body.classList.toggle("dark");

            if (document.body.classList.contains("dark")) {
                localStorage.setItem("theme", "dark");

                // Moon → Sun
                themeButton.innerHTML = "☀️";

            } else {
                localStorage.setItem("theme", "light");

                // Sun → Moon
                themeButton.innerHTML = "🌙";
            }
        });

        // Correct icon on page load
        if (document.body.classList.contains("dark")) {
            themeButton.innerHTML = "☀️";
        } else {
            themeButton.innerHTML = "🌙";
        }
    }

});