$(document).ready(function(){
   alert("aqui");
});

$( "#id_prazocorte" ).addClass("form-control-sm");

$("#id_id_maquina").change(function () {
  alert("aqui");
  var url = $("#formEstrutura").attr("dataCarregarEstruturasURL");  // get the url of the `load_cities` view
  var idMaquina = $(this).val();  // get the selected country ID from the HTML input
  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    data: {
      'id_maquina': idMaquina       // add the country id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#id_id_estruturas").html(data);  // replace the contents of the city input with the data that came from the server
    }
  });
});

$("#id_id_estruturas").change(function () {
  var url = $("#formEstrutura").attr("dataCarregarPrazosEstrutura");  // get the url of the `load_cities` view
  var id_estrutura = $(this).val();  // get the selected country ID from the HTML input
  $.ajax({                       // initialize an AJAX request
    type: "GET",
    url: url,
    timeout: 3000,
    contentType: "application/json; charset=utf-8",
    cache: false,
    data: {
      'id_estrutura': id_estrutura
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      var prazos = JSON.parse(data);
      $.each(prazos, function(i, prazo){
        $("#spanPrazoPadraoCorte").html(prazo.prazopadraocorte);
        $("#spanTotalPrazoCorte").html(Number(prazo.prazopadraocorte) + Number($("#id_prazocorte").val()));
        $("#spanPrazoPadraoCaldSolda").html(prazo.prazopadraocaldsolda);
        $("#spanTotalCaldSolda").html(Number(prazo.prazopadraocaldsolda) + Number($("#id_prazocaldsolda").val()));
        $("#spanPrazoPadraoUsinagem").html(prazo.prazopadraousinagem);
        $("#spanTotalUsinagem").html(Number(prazo.prazopadraousinagem) + Number($("#id_prazousinagem").val()));
        $("#spanPrazoPadraoPintura").html(prazo.prazopadraopintura);
        $("#spanTotalPintura").html(Number(prazo.prazopadraopintura) + Number($("#id_prazopintura").val()));
      });
    }
  });
});

$("#id_prazocorte").change(function () {
  $("#spanTotalPrazoCorte").html(Number($("#spanPrazoPadraoCorte").text()) + Number($(this).val()));
});

  (function($) {
      "use strict";

      jQuery('#vmap').vectorMap({
          map: 'world_en',
          backgroundColor: null,
          color: '#ffffff',
          hoverOpacity: 0.7,
          selectedColor: '#1de9b6',
          enableZoom: true,
          showTooltip: true,
          values: sample_data,
          scaleColors: ['#1de9b6', '#03a9f5'],
          normalizeFunction: 'polynomial'
      });
  })(jQuery);