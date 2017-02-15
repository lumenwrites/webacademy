
/* auto open modal */
$(window).on('load', function(){
    /* $('#submit').modal('show');*/
});


/* Search autocomplete */
$('#searchbar').typeahead({
    source: [
            "Django",
        "React",
	]
});

$('#searchbar').typeahead()


$(document).ready(function() {
    /* Remember hiding panels */
    /* Close subscription box and save it as a cookie for 7 days */
    $("#close-subscription-box" ).click(function() {
	console.log("Subscription box closed!");
	Cookies.set('subscription_box_closed', 'yes', { expires: 7 });
    });	

    /* If a cookie isn't set - display the box (it's hidden by default). */
    if (Cookies.get('subscription_box_closed')==null) {
        $('.subscription-box').css("display","block");
    }



    /* Filtering */
    
    $('.dropdown-menu').on('click', 'a', function(e) {
	e.preventDefault();
	/* Grab the value */
	var value = $(this).attr('href');
	var filter = $(this).parent().parent().attr('id');
	/* Add the value to GET request */
	var url = $.query.set(filter, value);
	/* If the value is set back to default - remove it. */
	if (value == 'all') {
	    url = $.query.REMOVE(filter);	    
	}
	/* Go to the url */
	window.location = url;
    });


    
});



/* Search */
$('#search-form').submit(function(event){
    /* Custom get request */
    event.preventDefault();
    event.stopPropagation();

    var query = $('#searchbar').val(); 

    var posttype = [];
    /* Grab post type */

    if (query){
	var query = '?query=' + query;
    } else {
	var query = ""
    }
    
    if (query && posttype > 0){
	/* If there's a query, add posttype at the end */
	var posttype = '&posttype=' + posttype;
    } else if (posttype) {
	/* If not - just filter by posttype. proabbly category first. */
	var posttype = '?posttype=' + posttype;	
    } else {
	var posttype = ""
    }
    /* Send the get request */
    window.location = action + query + hubs;
});


