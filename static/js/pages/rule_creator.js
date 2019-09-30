function animate_cards(active){
    if(active === 'simple'){
        $("#simple-rule-card").css("display", "block");
        $("#ignore-rule-card").css("display", "none");
        $("#complex-rule-card").css("display", "none");

    }else if(active === 'ignore'){
        $("#simple-rule-card").css("display", "none");
        $("#ignore-rule-card").css("display", "block");
        $("#complex-rule-card").css("display", "none");

    }else if(active === 'complex'){
        $("#simple-rule-card").css("display", "none");
        $("#ignore-rule-card").css("display", "none");
        $("#complex-rule-card").css("display", "block");

    }
}

function create_simple_rule(){
    let base = $("#page-xml-elements").val();
    let target = $("#tei-elements").val();
    let name = $("#rule-name").val();

    if(name){
        $.ajax({
            url: "/rule/create_rule/simple/",
            type: "POST",
            data: {"name": name, "base": base, "target": target},
            success: function () {
                $.notify({
                  icon: "add_alert",
                  message: "Rule successfully created!"

              },{
                  type: 'success',
                  timer: 500,
                  placement: {
                      from: "top",
                      align: "right"
                  }
              });
            },
            error: function() {
              $.notify({
                  icon: "add_alert",
                  message: "Something went horribly wrong. No rule was created!"

              },{
                  type: 'danger',
                  timer: 500,
                  placement: {
                      from: "top",
                      align: "right"
                  }
              });
            }
        });
    }else{
     $.notify({
      icon: "add_alert",
      message: "Please enter a name for the rule."

          },{
              type: 'warning',
              timer: 500,
              placement: {
                  from: "top",
                  align: "right"
              }
          });
    }

}

function create_ignore_rule(){
    let base = $("#page-xml-elements-ignore").val();
    let name = $("#rule-name-ignore").val();

    if(name){
        $.ajax({
            url: "/rule/create_rule/ignore/",
            type: "POST",
            data: {"name": name, "base": base},
            success: function () {
                $.notify({
                  icon: "add_alert",
                  message: "Rule successfully created!"

              },{
                  type: 'success',
                  timer: 500,
                  placement: {
                      from: "top",
                      align: "right"
                  }
              });
            },
            error: function() {
              $.notify({
                  icon: "add_alert",
                  message: "Something went horribly wrong. No rule was created!"

              },{
                  type: 'danger',
                  timer: 500,
                  placement: {
                      from: "top",
                      align: "right"
                  }
              });
            }
        });
    }else{
     $.notify({
      icon: "add_alert",
      message: "Please enter a name for the rule."

          },{
              type: 'warning',
              timer: 500,
              placement: {
                  from: "top",
                  align: "right"
              }
          });
    }
}