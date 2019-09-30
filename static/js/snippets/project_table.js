/**
 *  Load necessary information for the Project Overview Datatable via Ajax calls and fill the datatable
 **/
$(document).ready(function() {
    $('#datatables').DataTable({
            "serverSide": true,
            "ajax": '/project_list/?format=datatables',
            "columns": [
                  {"data": "title"},
                  {"data": "pages"},
                  {"data": "last_edit"},
                  {"targets": -1, "data": "percent_corrected", "render": function(data, type, row, meta){
                    return data + '%';
                   }},
                  {"targets": -1, "className": "text-right", "sorting": "false", "data": "title", "render": function(data, type, row, meta){
                    return '<a onclick="load_project(' + "'" + data + "'" + ')" class="btn btn-link btn-info btn-just-icon open" data-toggle="tooltip" title="Load Project">' +
                        '<i class="material-icons">check</i></a>' +
                        '<a onclick="ask_delete(' + "'" + data + "'" + ')" class="btn btn-link btn-danger btn-just-icon remove" data-toggle="tooltip" title="Delete Project">' +
                        '<i class="material-icons">remove</i></a>';
                   }},
              ]
        }
    );
});

function reload_project(){
    $.ajax({
        method: 'POST',
        url: '/update_projects/'
    });
    $('#datatables').DataTable().ajax.reload();
    $('#reloadTable').toggleClass("hoverSpin");
}

/* Project */
function load_project(project) {
    $.ajax({
        method: 'POST',
        url: '/load_project/' + project,
        data: {project: project},
        dataType: "json",
        success: function (data) {
            update_current_project();
            Swal.fire({
                type: 'success',
                title: 'Success!',
                text: 'Project successfully loaded!' +
                    '',
                footer: '<a href="/project/">Start working on the project.</a>'
            })
        },
        error: function (data) {
            Swal.fire({
                title: 'Do you really want to load this project?',
                text: "Another user is already working on this project. Do you want to load it anyways?",
                type: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Yes, load it!'
            }).then((result) => {
                if (result.value) {
                    force_load_project(project)
                }
            })
        }
    });
}


function force_load_project(project) {
    $.ajax({
        method: 'POST',
        url: '/load_project/' + project + "/1",
        data: {project: "project"},
        dataType: "json",
        success: function (data) {
            update_current_project();
            Swal.fire({
              type: 'success',
              title: 'Success!',
              text: data["message"],
            })
        },
        error: function (data) {
            Swal.fire({
              type: "error",
              title: 'Oops...',
              text: "Something went horribly wrong.",
            })
        }
    });
}

function ask_delete(project) {
  Swal.fire({
      title: 'Do you really want to remove this project?',
      text: "All settings and files will be permanently removed!",
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.value) {
        delete_project(project);
      }
    })
}

function delete_project(project) {
    $.ajax({
        method: 'POST',
        url: '/delete_project/' + project,
        data: {project: "project"},
        success: function (data) {
            reload_project();
            Swal.fire({
              type: 'success',
              title: 'Success',
              text: "The project and its data was successfully removed!",
            })
        },
        error: function (data) {
            Swal.fire({
              type: "error",
              title: 'Oops...',
              text: "Something went horribly wrong.",
            })
        }
    });
}
