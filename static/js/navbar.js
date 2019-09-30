/**
 *  Handles the display and interaction with the loaded project in the navbar
 **/
// ======== Loaded Project =====
function update_current_project(){

    $.ajax({
        url: /project_info/,
        dataType: "json",
        success: function (data) {
            let loaded_project = data["title"];
            if(data["name"]){
                loaded_project= data["name"];
            }

            $("#loaded_project").html('<a class="nav-link" href="#" id="loadedProjectDropdown" ' +
                'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="small material-icons ' +
                'icon-green">fiber_manual_record</i> ' + loaded_project + '</a><div class="dropdown-menu ' +
                'dropdown-menu-right" aria-labelledby="loadedProjectDropdown"><a class="dropdown-item" ' +
                'onclick="close_project()" href="javascript:void(0);">Close Project</a></div>');
        },
        error: function (data) {
            $("#loaded_project").html('<a class="nav-link" href="#" id="noProjectLoaded" ' +
                'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="small material-icons ' +
                'icon-red">fiber_manual_record</i> No Project loaded</a><div class="dropdown-menu ' +
                'dropdown-menu-right" aria-labelledby="noProjectLoaded"><a class="dropdown-item smooth-scroll" ' +
                'href="/#project-table">Load Project</a></div>');
        }
    });
}

// ======= Close Project =====
function close_project(){
    $.ajax({
        method: 'POST',
        url: '/close_project/',
        success: function (data) {
            update_current_project();
            Swal.fire({
                type: 'success',
                title: 'Success!',
                text: "Project successfully closed.",
            })
        },
    });
    update_current_project()
}
