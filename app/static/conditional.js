//Copyright 2015 Pareto Software, LLC, released under an MIT license: http://opensource.org/licenses/MIT
$( document ).ready(function() {
		//var episode_ok=false;
		//Inputs that determine what fields to show
		var episode = $('#live_form input:radio[name=episode]');			
		
		//Wrappers for all fields
		var toilet_parent = $('#live_form #episode_toilet');
		var leakage = $('#live_form textarea[name="episode_leakage"]').parent();
    var urgency_parent = $('#live_form #urgency');
    var bristol_parent = $('#live_form #bristol');
		var button = $('#live_form button[name="submit"]').parent();

    var rest=urgency_parent.add(bristol_parent).add(button);
  	var all=toilet_parent.add(leakage).add(rest);

		episode.change(function(){
			var value=this.value;				
			all.addClass('form_group_hidden'); //hide everything and reveal as needed
			if (value == 'toilet'){
				toilet_parent.removeClass('form_group_hidden');
        rest.removeClass('form_group_hidden');
        $('#regular-slider').get(0).slick.setPosition();
			}
			else if (value == 'leakage'){
				leakage.removeClass('form_group_hidden');
        rest.removeClass('form_group_hidden');
        $('#regular-slider').get(0).slick.setPosition();
			}		

		});	
	
		
});
