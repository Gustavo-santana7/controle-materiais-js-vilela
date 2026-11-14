document.addEventListener('DOMContentLoaded', function () {
    const aumentar = document.getElementById('aumentar-fonte');
    const diminuir = document.getElementById('diminuir-fonte');

    let escala = 1;

    const elementos = document.querySelectorAll('body *');

    const tamanhosOriginais = Array.from(elementos).map(function (elemento) {
        return {
            elemento: elemento,
            tamanho: parseFloat(getComputedStyle(elemento).fontSize)
        };
    });

    function aplicarTamanhoFonte() {
        tamanhosOriginais.forEach(function (item) {
            item.elemento.style.fontSize =
                (item.tamanho * escala) + 'px';
        });
    }

    if (aumentar && diminuir) {
        aumentar.addEventListener('click', function () {
            escala = Math.min(1.4, escala + 0.1);
            aplicarTamanhoFonte();
        });

        diminuir.addEventListener('click', function () {
            escala = Math.max(0.8, escala - 0.1);
            aplicarTamanhoFonte();
        });
    }
});