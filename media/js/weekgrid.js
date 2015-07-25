function DivCheckbox(shadow) {
    var that = this;

    // The <select> that we are replacing.
    var shadow = shadow;
    // The current state of the checkbox.
    var state = shadow.val() == "True";

    this.div = $("<div class='checkbox off'>not available</div>");
    this.div.click(function(){
	// Toggle the state
	that.set(!that.get());
    })

    // Accessors.
    this.set = function (new_state) {
	state = new_state;
	if (state) {
	    that.div.addClass("on");
	    that.div.removeClass("off");
	    that.div.html("available!");
	    shadow.val("True");
	} else {
	    that.div.addClass("off");
	    that.div.removeClass("on");
	    that.div.html("not available");
	    shadow.val("False");
	}
    }
    this.get = function () {
	return state;
    }

    // Update the dom object to reflect the initial state.
    this.set(state);
}

$(function(){
    // Make weekgrids more pretty.
    // Find all selects
    $(".weekgrid_widget select").each(function(i){
	// Create div checkboxs to replace them.
	var dc = new DivCheckbox($(this));
	dc.div.insertAfter($(this));
	console.log(["Inserting", dc]);
    });
    // Update the weekgrid class to reflect that we've prettified it.
    $(".weekgrid_widget").addClass("pretty");
    console.log("Weekgridding done.");
});
