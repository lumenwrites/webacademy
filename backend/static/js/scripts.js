
/* auto open modal */
$(window).on('load', function(){

    $('#submit').modal('show');
});


/* Search autocomplete */
$('#searchbar').typeahead({
    source: [
            "Django",
        "React",
	]
});

$('#searchbar').typeahead()

/* Remember hiding panels */
$(document).ready(function() {
    console.log('Hey!');
    /* Close subscription box and save it as a cookie for 7 days */
    $("#close-subscription-box" ).click(function() {
	console.log("Subscription box closed!");
	Cookies.set('subscription_box_closed', 'yes', { expires: 7 });
    });	

    /* If a cookie isn't set - display the box (it's hidden by default). */
    if (Cookies.get('subscription_box_closed')==null) {
        $('.subscription-box').css("display","block");
    }

    
});


