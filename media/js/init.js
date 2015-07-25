

if (window.console) {
    // The console already exists.
} else {
    // Create a dummy console.
    var console = {
	log: function() {},
	warn: function() {},
	error: function() {}
    };
}