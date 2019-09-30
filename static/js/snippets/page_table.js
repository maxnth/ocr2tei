/**
 *  Load necessary information for the Project Page Overview Datatable via Ajax calls and fill the datatable
 **/
$(document).ready(function() {
    $('#datatable_pages').DataTable({
            "serverSide": true,
            "ajax": '/project_page_list/?format=datatables',
            "columns": [
                {"data": "title"},
                {"targets": -1, "data": "xml", "render": function(data, type, row, meta){
                    if(data) {
                        return "<i class='material-icons icon-green'>check</i>";
                    }else
                        return "<i class='material-icons icon-red'>close</i>";
                    }
                },
                {"targets": -1, "data": "image", "render": function(data, type, row, meta){
                    if(data) {
                        return "<i class='material-icons icon-green'>check</i>";
                    }else
                        return "<i class='material-icons icon-red'>close</i>";
                    }
                },
                {"targets": -1, "data": "output", "render": function(data, type, row, meta){
                    if(data) {
                        return "<i class='material-icons icon-green'>check</i>";
                    }else
                        return "<i class='material-icons icon-red'>close</i>";
                    }
                },
                {"targets": -1, "className": "text-right", "sorting": "false", "data": "title", "render": function(data, type, row, meta){
                    return '<a onclick="load_page(' + "'" + data + "'" + ')" class="btn btn-link btn-info ' +
                        'btn-just-icon open" data-toggle="tooltip" title="Load Page">' +
                        '<i class="material-icons">check</i></a><a onclick="clear_output(' + "'" + data + "'" + ')" ' +
                        'class="btn btn-link btn-just-icon edit" data-toggle="tooltip" title="Clear Output"><i class="material-icons">clear_all</i></a>' +
                        '<a onclick="ask_delete_page(' + "'" + data + "'" + ')" class="btn btn-link btn-danger btn-just-icon remove" data-toggle="tooltip" title="Delete Page">' +
                        '<i class="material-icons">remove</i></a>';
                }},
              ]
        }
    );
});


function reload_pages(){
    $.ajax({
        method: 'GET',
        url: '/project_page_list/?format=datatables'
    });
    $('#datatable_pages').DataTable().ajax.reload();
    $('#reloadTable').toggleClass("hoverSpin");
}


/* Project */
function load_page(project) {
    $.ajax({
        method: 'POST',
        url: '/load_page/' + project,
        data: {project: "project"},
        dataType: "json",
        success: function (data) {
            window.location.href = "/project/page"
        },
        error: function (data) {
            Swal.fire({
              type: "error",
              title: 'Oops...',
              text: "Something went horribly wrong.",
              footer: '<a href>Why do I have this issue?</a>'
            })
        }
    });
}

function clear_output(page) {
    $.ajax({
        method: 'POST',
        url: '/clear_output/' + page,
        data: {project: "project"},
        success: function (data) {
            reload_pages();
            Swal.fire({
              type: "success",
              title: 'Success',
              text: "Output successfully cleared.",
            })
        },
        error: function (data) {
            Swal.fire({
              type: "error",
              title: 'Oops...',
              text: "Output doesn't exist or couldn't be deleted.",
            })
        }
    });
}

function ask_delete_page(page) {
  Swal.fire({
      title: 'Do you really want to remove this page?',
      text: "All files will be permanently removed!",
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.value) {
        delete_page(page);
      }
    })
}

function delete_page(page) {
    $.ajax({
        method: 'POST',
        url: '/delete_page/' + page,
        data: {project: "project"},
        success: function (data) {
            reload_pages();
            Swal.fire({
              type: 'success',
              title: 'Success',
              text: "The page and its files were successfully removed."
            })
        },
        error: function (data) {
            Swal.fire({
              type: "error",
              title: 'Oops...',
              text: "Something went horribly wrong."
            })
        }
    });
}
