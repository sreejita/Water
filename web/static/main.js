console.log("HELLOOO");
			$(document).ready(function() {
				console.log( "ready!" );
				//$('#lake_id_tb').hide(); 
				$('#lake_name_tb').hide(); 
				$('#area_tb').hide(); 
				$('#waterbodies-dropdown').change(function(){
			        if($('#waterbodies-dropdown').val() == 'lake_id') {
			            $('#lake_id_tb').show(); 
			            $('#lake_name_tb').hide(); 
			            $('#area_tb').hide();
			        } else if($('#waterbodies-dropdown').val() == 'lake_name') {
			            $('#lake_name_tb').show(); 
			            $('#lake_id_tb').hide(); 
			            $('#area_tb').hide();
			        } else {
			        	$('#area_tb').show();
			        	$('#lake_id_tb').hide(); 
			        	$('#lake_name_tb').hide();
			        }
			    });
			});