/**
 * Get webapp status informations for the information cards on the Dashboard
 **/
let amount_pages = 0;

$.ajax({
    url: "/project_list",
    method: "GET",
}).done(function (response) {
    $.each(response["results"], function(i,v){
            amount_pages += parseInt(v["pages"]);
    });
    $("#AmountPages").html(amount_pages);
});

