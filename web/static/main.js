console.log("HELLOOO");
			$(document).ready(function() {
				console.log( "ready!" );
				//$('#lake_id_tb').hide();
				$('[data-toggle="tooltip"]').tooltip();  
				
				/*$('#waterbodies-dropdown').change(function(){
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
			    }); */
			});

		function initMap() {
		console.log("Geo");

		//var geo = {% autoescape off %}{{geo}}{% endautoescape %};
		console.log(JSON.parse(geovar));
       // var uluru = {lat: -25.363, lng: 131.044};
        var uluru = JSON.parse(geovar);
        
        uluru.lat = parseFloat(uluru.lat);
        uluru.lng = parseFloat(uluru.lng);
        
        //var lurur = Object.assign({}, uluru);;
        
        
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 14,
          center: uluru
        });
        //var position1 = new google.maps.LatLng(uluru.lat, uluru.lng);
        var marker = new google.maps.Marker({
          position: uluru,
          map: map
        });

      }