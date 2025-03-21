document.addEventListener("DOMContentLoaded", function() {
    console.log("Script carregado!");

    let form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function() {
            let input = document.querySelector("input[name='guess']");
            if (input && input.value === "") {
                alert("Digite um número para adivinhar!");
                event.preventDefault();
            }
        });
    }
});
