function update_editor_theme(selection) {
    /**
     * Get user selected theme and update preference in user model via Ajax
     */
    $.ajax({
        url: "/change_editor_theme/",
        type: "POST",
        data: {"theme": selection.value},
        success: function () {
            $.notify({
                icon: "add_alert",
                message: "Your editor theme was updated."

            }, {
                type: 'success',
                timer: 500,
                placement: {
                    from: "top",
                    align: "right"
                }
            });
        },
        error: function () {
            $.notify({
                icon: "add_alert",
                message: "Your editor theme couldn't be updated."

            }, {
                type: 'danger',
                timer: 500,
                placement: {
                    from: "top",
                    align: "right"
                }
            });
        }
    })
}