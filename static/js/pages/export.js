let input_editor;

/* Initial Ajax call to get all pages of the project */
$.ajax({
    url: "/project_page_list/",
    dataType: "json"
}).done(function (response) {
    $.each(response, function (i, obj) {
        if (obj["output"]) {
            $("#exportFiles").append("<input type='checkbox' id='" + obj["title"] + "' class='chkbox' value='" +
                obj["title"] + "'>" + obj["title"] + "<br/>")
        }
    });
});

/* Ace editor for the generated output */
let output_text = "";

/* Ajax call to get user preferences for the Ace editor */
$.ajax({
    url: "/user_info/",
    dataType: "json"
}).done(function (response) {
    var input_editor = ace.edit("editor");
    input_editor.setTheme("ace/theme/" + response["results"][0]["editor_theme"]);
    input_editor.getSession().setMode("ace/mode/xml");
    input_editor.setFontSize("13x");
    input_editor.setAutoScrollEditorIntoView(true);
    input_editor.setPrintMarginColumn(false);
    input_editor.setValue(output_text);
    input_editor.clearSelection();
    input_editor.setOptions({
        maxLines: 60
    });

    $("#btn-save").click(function () {
        let output = input_editor.getValue();

        $.ajax({
            url: "/download_export/",
            type: "POST",
            data: {"output": output},
            success: function () {
                $.notify({
                    icon: "add_alert",
                    message: "File successfully downloaded to the project folder."
                }, {
                    type: 'success',
                    timer: 500,
                    placement: {
                        from: "top",
                        align: "right"
                    }
                });
            }
        });
    });


    $("#btn-generate").click(function () {
        /**
         * Event listener for generating page output
         */
        var pages = [];
        var simple_rules = [];
        var ignore_rules = [];

        $('input.page-check:checkbox:checked').each(function () {
            pages.push($(this).val());
        });

        $('input.simple-check:checkbox:checked').each(function () {
            simple_rules.push($(this).val());
        });

        $('input.ignore-check:checkbox:checked').each(function () {
            ignore_rules.push($(this).val());
        });

        console.log(pages);
        console.log(simple_rules);
        console.log(ignore_rules);

        $.ajax({
            url: "/generate_export/",
            type: "POST",
            dataType: "json",
            data: {"page[]": pages, "simple_rule[]": simple_rules, "ignore_rule[]": ignore_rules},
            success: function (resp) {
                input_editor.setValue(resp["output"]);
            },
            error: function (resp) {
                $.notify({
                    icon: "add_alert",
                    message: "Output couldn't be created."
                }, {
                    type: 'danger',
                    timer: 500,
                    placement: {
                        from: "top",
                        align: "right"
                    }
                });
            }
        });
    });

});

/* Ajax call to build page list */
$.ajax({
    url: "/project_page_list/",
    dataType: "json"
}).done(function (response) {
    $.each(response, function (i, v) {
        $("#page-select-list").append('<li class="list-group-item">' +
            '<div class="checkbox"><label><input class="page-check" type="checkbox" value="' + v["title"] + '"> ' + v["title"] + '</label></div></li>');
    });
});

/* Allow pages checkboxes to be range checked with Shift key */
jQuery(function ($) {
    $('#page-select-list').checkboxes('range', true);
});

/* Saves user selected sizes of the split.js containers in local storage */
function saveUserSizes() {
    localStorage.setItem("splitUserSizes", JSON.stringify([parseFloat(getFlexBasisPercent("#page_image")),
        parseFloat(getFlexBasisPercent("#page_regions")),
        parseFloat(getFlexBasisPercent("#page_code"))]))
}

if (!localStorage.getItem('splitUserSizes')) {
    userSizes = [33, 33, 33]
} else {
    userSizes = JSON.parse(localStorage.getItem("splitUserSizes"));
}

/* Create and manage split.js containers */
splitobj = Split(["#export-select", "#rule-select", "#export-code"], {
    elementStyle: function (dimension, size, gutterSize) {
        $(window).trigger('resize');
        return {'flex-basis': 'calc(' + size + '% - ' + gutterSize + 'px)'}
    },
    gutterStyle: function (dimension, gutterSize) {
        return {'flex-basis': gutterSize + 'px'}
    },
    onDragEnd: function (sizes) {
        localStorage.setItem('splitUserSizes', JSON.stringify(sizes))
    },
    sizes: userSizes,
    minSize: 5,
    gutterSize: 15,
    cursor: 'col-resize'
});

$(".gutter-horizontal").dblclick(function () {
    splitobj.setSizes([33, 33, 33]);
    localStorage.setItem('splitUserSizes', JSON.stringify([33, 33, 33]))
});

$(function () {
    $("#sortable").sortable();
    $("#sortable").disableSelection();
});