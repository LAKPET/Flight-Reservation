const selectBtn = document.getElementById('select-btn');
const text = document.getElementById('text');
const option = document.getElementsByClassName('option');

for (options of option) {
     options.onclick = function () {
        text.innerHTML = this.textContent;
    }
}

