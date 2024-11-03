document.getElementById('menuButton').addEventListener('click', function() {
    var dropdownMenu = document.getElementById('dropdownMenu');
    dropdownMenu.classList.toggle('show');
});

document.getElementById('menuButton').addEventListener('click', function() {
    this.classList.toggle('rotated');
});