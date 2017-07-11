  $(document).ready(function(){

    categoria();
    tipo();
    fecha();

    $("#id_categoria").change(categoria);

    function categoria(){
        if($("#id_categoria").val()==="2"){
            $("#ciudad").addClass("sr-only");
            $("#direccion").addClass("sr-only");
            $("#cupo").addClass("sr-only");
            $("#pais").addClass("sr-only");
            $("#provincia").addClass("sr-only");
            $(".presencial").prop("required",false);
        }else{
            $("#ciudad").removeClass("sr-only");
            $("#direccion").removeClass("sr-only");
            $("#cupo").removeClass("sr-only");
            $("#pais").removeClass("sr-only");
            $("#provincia").removeClass("sr-only");
            $(".presencial").prop("required",true);
        }
    };

    $("#id_tipo_evento").change(tipo);

    function tipo(){
        if($("#id_tipo_evento").val()==="2"){
            $("#id_precio").prop("required",false);
            $("#precio").addClass("sr-only");
        }else{
            $("#precio").removeClass("sr-only");
            $("#id_precio").prop("required",false);
        }
    }

    $("#id_fecha").change(fecha);

    function fecha(){
        let fecha_string = $("#id_fecha").val().split("/");
        let fecha_ingresada = new Date()
        fecha_ingresada.setYear(parseInt(fecha_string[2]));
        fecha_ingresada.setMonth(parseInt(fecha_string[1])-1);
        fecha_ingresada.setDate(parseInt(fecha_string[0]));

        let fecha_actual = new Date();

        if(fecha_ingresada<=fecha_actual){
            $("#id_fecha").val("");
            alert("La fecha ingresada debe ser posterior a hoy");
        }
    }

    $('#data_1 .input-group.date').datepicker({
        todayBtn: "linked",
        keyboardNavigation: false,
        forceParse: false,
        calendarWeeks: true,
        autoclose: true,
        language: "es",
        format: "dd/mm/yyyy"
    });

    let form = document.getElementById('form');
    
    function mifuncion(event) {
        // Evitamos que el formulario se envíe
      event.preventDefault();
      
      // Si el form no es valido
      if (form.checkValidity()) {
        let texto = $("#id_nombre").val() + "\n" + $("#id_fecha").val() + "\n" + $("#id_categoria option:selected").html() + "\n";
        if($("#id_categoria").val()==="1"){
            texto += $("select[name=ciudad] option:selected").html()+ " " + $("select[name=provincia] option:selected").html() + " " + $("select[name=pais] option:selected").html() + "\n" +
                     $("#id_cupo").val() + " asistentes \n"; 
        }
        texto += $("select[name=tipo_evento] option:selected").html() + "\n";
        if($("#id_tipo_evento").val()==="1"){
            texto += $("#id_precio").val() + " ARS";
        }
      
        swal({
            title: "Nuevo evento",
            text: texto,
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
        }, function () {
            $("#btn").click()
        });
        return false;
      
      }
      return false;
      
    }
  });
