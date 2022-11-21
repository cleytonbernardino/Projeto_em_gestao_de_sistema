// alert('Isso é apenas um rascunho da tela, não era nem para ser encontrado :)')

(function(){
    const menu = document.querySelector("#input-menu");
    const searchBar = document.querySelector(".search-bar");
    const btnFechar = document.querySelector(".close");
    const btnAbrir = document.querySelector(".open");
    const menuHidden = document.querySelector('#hidden-menu')

    btnFechar.addEventListener('click', () => {
        searchBar.setAttribute('style', 'width: fit-content');
        menuHidden.setAttribute('style', 'display: none;')
        btnAbrir.setAttribute('class', 'open')   
        btnFechar.setAttribute('class', 'close hidden')
    })

    btnAbrir.addEventListener('click', () => {
        searchBar.setAttribute('style', 'width: 30rem;');
        menuHidden.setAttribute('style', 'display: block;')
        btnFechar.setAttribute('class', 'close')
        btnAbrir.setAttribute('class', 'open hidden')  
    })
})()