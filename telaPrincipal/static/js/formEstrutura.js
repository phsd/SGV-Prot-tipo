$("#id_id_maquina").change(function () {
  var url = $("#formEstrutura").attr("dataCarregarEstruturasURL");  // get the url of the `load_cities` view
  var idMaquina = $(this).val();  // get the selected country ID from the HTML input
  $.ajax({                       // initialize an AJAX request
    cache: false,
    contentType: "application/json; charset=utf-8",
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
    cache: false,
    contentType: "application/json; charset=utf-8",
    url: url,
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

$.fn.datetimepicker.Constructor.Default = $.extend({}, $.fn.datetimepicker.Constructor.Default, {
  format: 'YYYY-MM-DD HH:mm:ss',
});

$( "#id_prazocorte" ).addClass("form-control-sm");
