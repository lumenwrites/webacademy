$(document).ready(function(){

    //Toggle reply
    $('.show-reply').click(function () {
	$('.comment-reply').hide()
	$(this).parent().parent().find('.comment-reply').toggle();
    });
    //cancel
    $('.cancel').click(function () {
	$('.comment-reply').hide()
    });

}); // End document ready
