var splitobj, output_text, canvas;

function reset_page() {
    /**
     * Destroy all split.js and canvas objects to avoid malfunctions
     */
    if (splitobj) {
        splitobj.destroy();
    }
    if (canvas) {
        canvas.dispose();
    }
}

function getFlexBasisPercent(element) {
    /**
     * Get Flex parameters to save split.js container percentage for cases where the native split.js saving option doesn't
     * work
     * @type {*|jQuery}
     */
    let flexString = $(element).css('flex-basis');
    let percentRegex = /calc\((.+)%.+/g;
    return percentRegex.exec(flexString)[1]
}

function saveUserSizes() {
    /**
     * Saves extracted split.js container percentages in local storage
     */
    localStorage.setItem("splitUserSizes", JSON.stringify([parseFloat(getFlexBasisPercent("#page_image")),
        parseFloat(getFlexBasisPercent("#page_regions")),
        parseFloat(getFlexBasisPercent("#page_code"))]))
}


function input_switch(mode) {
    /**
     * Initiates input mode switch on click
     */
    if (mode === "image") {
        $("#input-canvas-card").css("display", "none");
        $("#input-xml-card").css("display", "block");
    } else if (mode === "xml") {
        $("#input-canvas-card").css("display", "block");
        $("#input-xml-card").css("display", "none");
    }
}


function save_region_options() {
    /**
     * Saves user selected options of the active region on click
     * Ajax sends all parameters to view controller
     * @type {*|jQuery}
     */
    let element = $("#data-rID").text();
    let tei_element = $('#tei-elements').val();
    let ignore_region = "False";

    if ($("#region-ignore-check").is(':checked'))
        ignore_region = "True";

    $.ajax({
        url: "/set_region_tei/",
        type: "POST",
        data: {"rID": element, "TEI": tei_element, "Ignore": ignore_region},
    }).done(function () {
        refresh_page();
        $.notify({
            icon: "add_alert",
            message: "Region settings successfully saved!"

        }, {
            type: 'success',
            timer: 50,
            placement: {
                from: "top",
                align: "right"
            }
        });
    })
}


function save_page_options() {
    /**
     * Saves user selected options of the active region on click
     * Ajax sends all parameters to view controller
     * @type {string}
     */
    let ignore_page = "False";

    if ($("#page-ignore-check").is(':checked')) {
        ignore_page = "True";
    }

    $.ajax({
        url: "/set_page_options/",
        type: "POST",
        data: {"Ignore": ignore_page},
    }).done(function () {
        refresh_page();
        $.notify({
            icon: "add_alert",
            message: "Page settings successfully saved!"

        }, {
            type: 'success',
            timer: 50,
            placement: {
                from: "top",
                align: "right"
            }
        });
    })

}


function switch_page(direction) {
    /**
     * Initializes and handles page switch with Ajax request
     */
    $("#page-loader").show();
    $.ajax({
        url: "/loaded_page/",
        dataType: "json"
    }).done(function (response) {
        saveUserSizes();

        if (direction === "forwards") {
            new_page = response["next"];
        } else if (direction === "backwards") {
            new_page = response["previous"]
        }
        if (new_page) {
            $.ajax({
                url: "/load_page/" + new_page
            }).done(function () {
                refresh_page();
            });
        }
    });
}


function refresh_page() {
    /**
     * Initializes page build up on initial request and page switches
     * Resets everything before loading to avoid malfunctions
     */
    reset_page();

    if (!localStorage.getItem('splitUserSizes')) {
        userSizes = [33, 33, 33]
    } else {
        userSizes = JSON.parse(localStorage.getItem("splitUserSizes"));
    }

    /* Ajax call to get needed page and project information and handle build up in the callback */
    var getProject = $.ajax({
        url: "/loaded_page/",
        dataType: "json"
    });

    getProject.done(function (resp) {
        let btn_next = $("#next-page");
        let btn_prev = $("#previous-page");

        if (resp["next"]) {
            btn_next.css('visibility', 'visible');
        } else {
            btn_next.css('visibility', 'hidden');
        }
        if (resp["previous"]) {
            btn_prev.css('visibility', 'visible');
        } else {
            btn_prev.css('visibility', 'hidden');
        }

        $("#page-title").html(resp["title"]);
        callback(resp);
    });

    function callback(response) {
        /* Build and fill canvas with needed objects */
        let canvas_body = $('#page-canvas-body');
        canvas = new fabric.Canvas('page-canvas');
        canvas.setHeight(canvas_body.height());
        canvas.setWidth(canvas_body.width());
        canvas.hoverCursor = "pointer";

        function resize_canvas() {
            canvas.setHeight(canvas_body.height());
            canvas.setWidth(canvas_body.width());
        }

        var img = fabric.Image.fromURL(response["image"], function (oImg) {

            oImg.evented = false;

            canvas.add(oImg);

            canvas.sendToBack(oImg);

            oImg.setShadow({
                color: 'rgba(0, 0, 0, 0.1)',
                blur: 80,
                offsetX: 100,
                offsetY: 100
            });


        });

        canvas.selection = false;

        /* Fill canvas with regions from Ajax response data */
        $.each($.parseJSON(response["xml_data"]), function (i, v) {
            let readingOrder = i;
            let rID = v["rID"];
            let rType = v["rType"];
            let coords = v["rCoords"];
            let forced_tei = v["comments"];
            let ignored = "False";

            if (forced_tei) {
                let parsed = JSON.parse(forced_tei);

                forced_tei = parsed.forced;
                ignored = parsed.ignore;


                $("#region-ignore-check").prop("checked", true);
                $("#data-tei").html(forced_tei);
            } else {
                forced_tei = "None";
                $("#region-ignore-check").prop("checked", false);
            }

            let temp = new fabric.Polygon(coords,
                {
                    angle: 0,
                    stroke: "#" + ((1 << 24) * Math.random() | 0).toString(16),
                    strokeWidth: 5,
                    fill: 'rgba(0,0,0,0)',
                    hasControls: false,
                    hasBorders: false,
                    lockMovementX: true,
                    lockMovementY: true,
                    title: rID,
                    rType: rType,
                    reading_order: readingOrder,
                    forced: forced_tei,
                    ignored: ignored,
                },
            );

            canvas.add(temp);
        });

        /* Canvas event listeners */
        canvas.on('mouse:wheel', function (opt) {
            var delta = opt.e.deltaY;
            var pointer = canvas.getPointer(opt.e);
            var zoom = canvas.getZoom();
            zoom = zoom - delta / 200;
            if (zoom > 80) zoom = 80;
            if (zoom < 0.1) zoom = 0.1;
            canvas.zoomToPoint({x: opt.e.offsetX, y: opt.e.offsetY}, zoom);
            opt.e.preventDefault();
            opt.e.stopPropagation();
        });

        var panning = false;
        canvas.on('mouse:up', function (e) {
            panning = false;
        });

        canvas.on('mouse:down', function (e) {
            let active;
            if (!canvas.getActiveObject()) {
                panning = true;
                canvas.forEachObject(function (o) {
                    reset_edit_area();
                    o.set({fill: 'rgba(0,0,0,0)'});
                });
            } else {
                canvas.forEachObject(function (o) {
                    reset_edit_area();
                    o.set({fill: 'rgba(0,0,0,0)'});
                });
                active = canvas.getActiveObject();
                active.set({fill: 'rgba(0,0,0,0.2)'});
                select_object_edit_area(active);
            }
        });

        canvas.on('mouse:move', function (e) {
            if (panning && e && e.e) {
                var units = 10;
                var delta = new fabric.Point(e.e.movementX, e.e.movementY);
                canvas.relativePan(delta);
            }
        });

        canvas.zoomToPoint({x: 0, y: 0}, 0.2);
        canvas.renderAll();

        /* Handles display of region settings card after region is selected */
        function reset_edit_area() {
            $("#info-placeholder").css("display", "block");
            $("#info-table").css("display", "none");
        }

        function select_object_edit_area(obj) {
            $("#data-rID").html(obj.title);
            $("#data-rType").html(obj.rType);
            $("#data-ro").html(obj.reading_order);
            $("#data-tei").html(obj.forced);
            $("#info-placeholder").css("display", "none");
            $("#info-table").css("display", "block");
            if (obj.ignored === "True") {
                $("#region-ignore-check").prop("checked", true);
            } else {
                $("#region-ignore-check").prop("checked", false);
            }
        }


        /* Ace output editor */
        let output_text;
        let output_editor;

        if (response["output_text"]) {
            output_text = response["output_text"]
        } else {
            output_text = ""
        }


        $.ajax({
            url: "/user_info/",
            dataType: "json"
        }).done(function (response) {
            output_editor = ace.edit("output_editor");
            output_editor.setTheme("ace/theme/" + response["results"][0]["editor_theme"]);
            output_editor.getSession().setMode("ace/mode/xml");
            output_editor.setFontSize("13x");
            output_editor.setAutoScrollEditorIntoView(true);
            output_editor.setPrintMarginColumn(false);
            output_editor.setValue(output_text);
            output_editor.clearSelection();
            output_editor.setOptions({
                maxLines: 60
            });
        });

        $("#btn-generate").click(function () {
            /**
             * Event listener for generating page output
             */
            $.ajax({
                url: "/generate_page_output/",
                type: "GET",
            }).done(function (response) {
                output_editor.setValue(response["output"]);
            });
        });

        /* Ace input editor */
        let input_text;

        if (response["xml_text"]) {
            input_text = response["xml_text"]
        } else {
            input_text = ""
        }

        $.ajax({
            url: "/user_info/",
            dataType: "json"
        }).done(function (response) {
            var input_editor = ace.edit("input_editor");
            input_editor.setTheme("ace/theme/" + response["results"][0]["editor_theme"]);
            input_editor.getSession().setMode("ace/mode/xml");
            input_editor.setFontSize("13x");
            input_editor.setAutoScrollEditorIntoView(true);
            input_editor.setPrintMarginColumn(false);
            input_editor.setValue(input_text);
            input_editor.clearSelection();
            input_editor.setReadOnly(true);
            input_editor.setOptions({
                maxLines: 60
            });
        });


        $("#btn-save").click(function () {
            let output = output_editor.getValue();

            $.ajax({
                url: "/download_page/",
                type: "POST",
                data: {"output": output},
            }).done(function () {
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
            });
        });

        /* Handle split.js */
        splitobj = Split(["#page_image", "#page_regions", "#page_code"], {
            elementStyle: function (dimension, size, gutterSize) {
                resize_canvas();
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
    }
}

refresh_page();
