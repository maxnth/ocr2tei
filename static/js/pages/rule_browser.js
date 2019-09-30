const get_simple_rules = $.ajax({
    url: "/rules/simple_rules/",
    type: "GET",
    dataType: "JSON",
});

get_simple_rules.done(function (response) {
    if(response["results"]){
        $("#rule-list").html("<h3>Simple rules</h3>");
        $.each(response["results"], function (k, v) {
            $("#rule-list").append("<div class='card rule-info-card'><div class='card-header card-header-primary' " +
                "data-header-animation='true'>" +
                "<h4 class='card-title'>" + v["name"] + "</h4></div><div class='card-body'>This rule converts<b>" +
                " " + v["base"] + "</b> to <b>" + v["target"] + "</b></div></div>")
        })
    }
    get_ignore_rules();
});

function get_ignore_rules() {
    $.ajax({
        url: "/rules/ignore_rules/",
        type: "GET",
        dataType: "JSON",
    }).done(function (response) {
        if (response["results"]) {
            $("#rule-list").append("<hr><h3>Ignore rules</h3>");
            $.each(response["results"], function (k, v) {
                $("#rule-list").append("<div class='card rule-info-card'><div class='card-header card-header-info'>" +
                    "<h4 class='card-title'>" + v["name"] + "</h4></div><div class='card-body'>This rule ignores" +
                    " <b>" + v["base"] + "</div></div>")
            })
        }
    });
}

function delete_rule(mode, rule){
    $.ajax({
        url: "/rule/delete_rule/",
        type: "POST",
        data: {"mode": mode, "name": rule}
    }).done(function () {
                window.location.reload();
    });
}