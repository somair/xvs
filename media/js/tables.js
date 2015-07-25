var dt;
var tid;
var entity;

function update_selected() {
  var action_button = $("#action_button");
  var checked_count = dt.rows(".selected").data().length;
  var volunteers_plural = entity + ((checked_count == 1) ? "" : "s");
  var button_label = "Perform this action with " + checked_count + " " + volunteers_plural;

  action_button.attr('value', button_label);

  if (checked_count > 0) {
    action_button.attr('disabled', null);
  } else {
    action_button.attr('disabled', true);
  }
}

function select_all() {
  dt.rows().nodes().each(function (el) {
    $(el).addClass('selected');
  });
  update_selected();
}

function select_visible() {
  $(tid + " tr").addClass('selected');
  update_selected();
}

function select_none() {
  dt.rows().nodes().each(function (el) {
    $(el).removeClass('selected');
  });
  update_selected();
}

function get_selected_ids() {
  var vids = [];

  dt.rows().nodes().each(function (el) {
    var elq = $(el);

    if (elq.hasClass("selected")) {
      var vid = elq.attr('id').substring(1);
      vids.push(vid);
    }

  });

  return vids;
}

function set_ids() {
  var vids = get_selected_ids();
  var vids_str = vids.join(",");
  $("#action_ids").attr("value", vids_str);
}

function set_up_table(ent, cols) {
  tid = "#" + ent + "_table";
  entity = ent;
  dt = $(tid).DataTable({
    "stateSave": true,
    "pageLength": 100
  });
}

function make_selectable() {
  $(tid + ' tbody').on( 'click', 'tr', function () {
    $(this).toggleClass('selected');
    update_selected();
  });

  update_selected();
}