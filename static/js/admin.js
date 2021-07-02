function eliminaGenero(cve, nombre){
    if (window.confirm("Confirma que desea eliminar el género "+nombre+". Esta acción es permanente.")) {
        var ancla = "/delete_genero/"+cve;
        location.href = ancla;
    }
}
function eliminaConsola(cve, nombre){
    if (window.confirm("Confirma que desea eliminar la consola "+nombre+". Esta acción es permanente.")) {
        var ancla = "/delete_consola/"+cve;
        location.href = ancla;
    }
}
function eliminaDesarrolladora(cve, nombre){
    if (window.confirm("Confirma que desea eliminar la desarrolladora "+nombre+". Esta acción es permanente.")) {
        var ancla = "/delete_desarrolladora/"+cve;
        location.href = ancla;
    }
}
function eliminaIdioma(cve, nombre){
    if (window.confirm("Confirma que desea eliminar el idioma "+nombre+". Esta acción es permanente.")) {
        var ancla = "/delete_idioma/"+cve;
        location.href = ancla;
    }
}
function eliminaJuego(cve, nombre){
    if (window.confirm("Confirma que desea eliminar el juego "+nombre+". Esta acción es permanente.")) {
        var ancla = "/delete_juego/"+cve;
        location.href = ancla;
    }
}