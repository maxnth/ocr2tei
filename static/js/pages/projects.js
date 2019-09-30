/* Ajax call to update Project Settings */
$("#save-project-settings").click(function(){
    $.ajax({
       url: "/project_settings/",
       type: "POST",
       data: {"project_name": $("#titleInput").val()},
       dataType: "json",
    }).done(function () {
      $.notify({
          icon: "add_alert",
          message: "Project settings successfully updated."
          },{
              type: 'success',
              timer: 500,
              placement: {
                  from: "top",
                  align: "right"
              }
          });
    });
});

/* Ajax call to update Project Metadata */
$("#save-metadata").click(function() {
    let title_stmt = $("#titleStmt").val();
    let edition_stmt = $("#editionStmt").val();
    let publ_stmt = $("#publicationStmt").val();
    let notes_stmt = $("#notesStmt").val();
    let source_desc = $("#sourceDesc").val();
    let series_stmt = $("#seriesStmt").val();
    let extent = $("#extent").val();

    $.ajax({
        url: "/project_metadata/",
        type: "POST",
        data: {
            "title_stmt": title_stmt, "edition_stmt": edition_stmt, "publ_stmt": publ_stmt, "notes_stmt": notes_stmt,
            "source_desc": source_desc, "series_stmt": series_stmt, "extent": extent
        },
        dataType: "json",
        success: function (data) {
            $.notify({
                icon: "add_alert",
                message: "Metadata successfully updated."
            }, {
                type: 'success',
                timer: 500,
                placement: {
                    from: "top",
                    align: "right"
                }
            });
        }
    })
});

/* Fill form fields if already specified */
$.ajax({
    url: "/project_info",
    type: "GET",
}).done(function (response) {
    if(response.name){
        $("#titleInput").val(response.name);
    }
});

/* Fill form fields if already specified */
$.ajax({
    url: "/project_info",
    type: "GET",
}).done(function (response) {
    if(response["metadata"]){
        let metadata = response["metadata"]

        $("#titleStmt").val(metadata["title_statement"]);
        $("#editionStmt").val(metadata["edition_statement"]);
        $("#publicationStmt").val(metadata["publication_statement"]);
        $("#notesStmt").val(metadata["notes_statement"]);
        $("#sourceDesc").val(metadata["source_description"]);
        $("#seriesStmt").val(metadata["series_statement"]);
        $("#extent").val(metadata["extent"]);
    }
});
