function mostrarContrasena(){
    contrasena=document.getElementById('contra-usu-login');
    if(contrasena.type == 'password'){
        contrasena.type = 'text';
        return false;
    }else{
        contrasena.type = 'password';
        return false;
    }
}
function mostrarContrasenas(){
    contrasena=document.getElementById('contra-usu');
    contrasenaR=document.getElementById('contra-r-usu');
    if(contrasena.type == 'password'){
        contrasena.type = 'text';
        contrasenaR.type = 'text';
        return false;
    }else{
        contrasena.type = 'password';
        contrasenaR.type = 'password';
        return false;
    }
}
function validaContrasenas(){
    contrasena=document.getElementById('contra-usu');
    contrasenaR=document.getElementById('contra-r-usu');
    if(contrasena.value != contrasenaR.value){
        alert("Las contraseñas no coinciden");
        return false;
    }
}
function validaPerfil(){
    miAvatar= document.getElementById('avatar-usu');
    contrasena=document.getElementById('contra-usu');
    contrasenaR=document.getElementById('contra-r-usu');
    var allowedExtensions = /(.jpg|.jpeg|.png)$/i;
    if(contrasena.value != contrasenaR.value){
        alert("Las contraseñas no coinciden");
        return false;
    }
    if(!allowedExtensions.exec(miAvatar.value)){
        alert('Solo se admiten imagenes .jpeg/.jpg/.png');
        miAvatar.value = '';
        return false;
    }
}
function validaFotos(){
    foto1= document.getElementById('foto-juego');
    foto2= document.getElementById('fotodos-juego');
    var allowedExtensions = /(.jpg|.jpeg|.png)$/i;
    if(foto1.value != "" && !allowedExtensions.exec(foto1.value)){
        alert('Solo se admiten imagenes .jpeg/.jpg/.png');
        foto1.value = '';
        return false;
    }
    if(foto2.value != "" && !allowedExtensions.exec(foto2.value)){
        alert('Solo se admiten imagenes .jpeg/.jpg/.png');
        foto2.value = '';
        return false;
    }
}