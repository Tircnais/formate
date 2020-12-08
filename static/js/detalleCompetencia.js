$("#id_fkcompetence").change(function () {// get the url of the `load_cities` view
    var fkCompetencia = $("#id_fkcompetence").val(); // get the selected country ID from the HTML input
    // var x = document.getElementById("fkcompetence").value; // get the selected country ID from the HTML input
    console.log('id_fkcompetence', fkCompetencia);
    var board_url = "{%  url 'ajaxDetalleComp' %}";
    $.ajax({
    // initialize an AJAX request      
    url: board_url,
    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    type: "POST",
    data: {
    'fkCompetencia': fkCompetencia,
    // add nombCompetencia to the GET parameters
    //'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    // add nombCompetencia id to the GET parameters
    },
    datatype:'json',
    success: function(data) {
        console.log('cambio')
        // `data` is the return of the `load_cities` view function
        var nombArea = document.getElementById("nombre_area");
        var descripcionComp = document.getElementById("descripcion_competencia");
        console.log(data);
        nombArea.innerHTML = data['infoArea'];
        descripcionComp.innerHTML = data['infoCompetencia'];
    }
    });
});