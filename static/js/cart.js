$(document).ready(function(){
    
    $("#boton_resta").change(function () {
        let precio = $(this).attr("precio")
        let total_actual = $('#total_actual').text().substring(1)
        
        let total = total_actual - precio

        $("#total_actual").html("$"+total)

    });

    $("#boton_suma").change(function () {
        let precio = $(this).attr("precio")
        let total_actual = $('#total_actual').text().substring(1)
        
        let total = total_actual - precio

        $("#total_actual").html("$"+total)

    });

})