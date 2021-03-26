
// meneu accordeon de la page de profil utilisateur
const btn_deploy = document.querySelector(".btn-deploy")

btn_deploy.addEventListener('click', ()=> {
    console.log(btn_deploy);
    const card_menu = document.querySelector('.card-menu:nth-child(2)');
    card_menu.classList.toggle("deploy");
})