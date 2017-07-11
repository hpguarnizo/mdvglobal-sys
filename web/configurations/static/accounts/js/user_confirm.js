$(document).ready(function(){
        $(".eliminar").click(function(){

             let confirma = confirm("¿Estás seguro que deseas eliminar tu cuenta? Esta será desactivada temporalmente  y eliminada en 10 dias. Si decides volver solo iniciar sesión nuevamente. ");
             if(!confirma){
                return false;
            };
        });
    });