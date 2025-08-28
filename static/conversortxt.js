  function toggleMenu() {
        document.querySelector('.navbar-links').classList.toggle('active');
    }
            const textarea = document.getElementById("inputText");
            function toUpperCase() {
                textarea.value = textarea.value.toUpperCase();
            }
            function toLowerCase() {
                textarea.value = textarea.value.toLowerCase();
            }
            function toAlternado() {
                let txt = textarea.value;
                let resultado = '';
                let usarMaiusculo = true;
                for (let char of txt) {
                    if (/[a-zA-Z]/.test(char)) {
                        resultado += usarMaiusculo ? char.toUpperCase() : char.toLowerCase();
                        usarMaiusculo = !usarMaiusculo;
                    } else {
                        resultado += char;
                    }
                }
                textarea.value = resultado;
            }
            function inverterTexto() {
                textarea.value = textarea.value.split('').reverse().join('');
            }
function primeiraLetraPalavra() {
    textarea.value = textarea.value
        .toLowerCase()
        .replace(/(^[a-zÀ-ÿ])|(\s+[a-zÀ-ÿ])/g, m => m.toUpperCase());
}
            function primeiraLetraFrase() {
                let txt = textarea.value.toLowerCase();
                textarea.value = txt.charAt(0).toUpperCase() + txt.slice(1);
            }
            function selecionarTexto() {
                textarea.select();
            }
            function removerPontuacaoEAcentos() {
                let texto = textarea.value.normalize('NFD');
                texto = texto.replace(/[\u0300-\u036f]/g, '');
                texto = texto.replace(/[^a-zA-Z0-9\s]/g, '');
                textarea.value = texto;
            }