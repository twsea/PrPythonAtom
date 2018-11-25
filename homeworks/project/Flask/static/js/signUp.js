/*$(function(){
	$('button').click(function(){
		var title = $('#input_title').val();
		$.ajax({
			url: '/signUpUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});*/

$(function() {
    $('button#calculate').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/signUpUser', {
        title: $('input[name="title_film"]').val(),
      }, function(data) {
        $("#result").text(data.result);
      });
      return false;
    });
  });