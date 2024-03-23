document.addEventListener('DOMContentLoaded', function() {
    var select = document.querySelector('#id_grade');
    for (var i = 0; i < select.options.length; i++) {
        var option = select.options[i];
        var color = option.text.toLowerCase();
        var dot = document.createElement('span');
        dot.className = 'color-dot color-' + color;
        option.prepend(dot);
    }
});