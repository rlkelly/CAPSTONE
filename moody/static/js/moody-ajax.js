/**
 * Created by leif on 22/10/2014.
 */
	$(document).ready(function() {

		// JQuery code to be added in here.

        $('#likes').click(function(){
	        var catid;
	        artid = $(this).attr("data-artid");
	         $.get('/rango/like_category/', {art_id: artid}, function(data){
	                   $('#like_count').html(data);
	                   $('#likes').hide();
	               });
	    });



        	$('#suggestion').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/moody/suggest_artist/', {suggestion: query}, function(data){
                 $('#arts').html(data);
		});
	});

	});
