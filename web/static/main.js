console.log("HELLO");			
		$(document).ready(function() {
			console.log( "ready!" );

			$('.album').click(function() {
 					//console.log("clicked");
 					$('#navbarHeader').collapse('hide');
 				});
			$('[data-toggle="tooltip"]').tooltip();  
			
		});
		function onL2SSubmit() {
			console.log("HEYYYYYYY THERE");
			console.log($('#l2s_lake_id').val());
			console.log("HEYYYYYYY THERE..");
			var actionUrl = "/lake_to_site/" + $('#l2s_lake_id').val() + "/";
			$('#forml2s').attr('action', actionUrl);
		}
		function initMap() { 
			console.log("Geo");
			
			
	       // var uluru = {lat: -25.363, lng: 131.044};
	      if( typeof geovar != 'undefined' ) {
	       	console.log(JSON.parse(geovar));
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
	        
	      /* if(typeof geoArrL2S != 'undefined') {
	       	 console.log(JSON.parse(geoArrL2S));
	       	 var geo_l2s = JSON.parse(geoArrL2S);
	       	 //var bounds = new google.maps.LatLngBounds();
	       	 
	       
	       	var mapl2s = new google.maps.Map(document.getElementById('mapl2s'), {
	          zoom: 14,
	          center: new google.maps.LatLng(parseFloat(geo_l2s[0].lat), parseFloat(geo_l2s[0].lng))
	        });
	       	
	       	 for(var i in geo_l2s)
			{
				console.log(geo_l2s[i]);
				var position = new google.maps.LatLng(parseFloat(geo_l2s[i].lat), parseFloat(geo_l2s[i].lng));
				
			    // bounds.extend(position);
			     var marker = new google.maps.Marker({
			          position: position,
			          map: mapl2s,
			          title: geo_l2s[i].title
			        }); 
			    // mapl2s.fitBounds(bounds);
			} 
			// var boundsListener = google.maps.event.addListener((mapl2s), 'bounds_changed', function(event) {
		      //  this.setZoom(14);
		        //google.maps.event.removeListener(boundsListener);
		    //});
	       } */
	        if(typeof geoArrL2S != 'undefined') {
	       	 console.log(JSON.parse(geoArrL2S));
	       	 var geo_l2s = JSON.parse(geoArrL2S);
	       	 var bounds = new google.maps.LatLngBounds();
	       	 var infowindow = new google.maps.InfoWindow(); 
	       
	       	var mapl2s = new google.maps.Map(document.getElementById('mapl2s'), {
	          zoom: 14,
	          center: new google.maps.LatLng(parseFloat(geo_l2s[0].lat), parseFloat(geo_l2s[0].lng))
	        });
	       	 var infoContent = [];

	       	 for(var i in geo_l2s)
			{
				//console.log(geo_l2s[i]);
				var position = new google.maps.LatLng(parseFloat(geo_l2s[i].lat), parseFloat(geo_l2s[i].lng));
				var infoElem = '<div class="info_content">' +
        								'<b>Site ID: </b>'+ geo_l2s[i].title + '<br>' + 
        								'<b>Latitude: </b>'+ geo_l2s[i].lat + '<br>' + 
        								'<b>Longitude: </b>'+ geo_l2s[i].lng + '<br>' + 
        								'<b>Monitoring Location: </b>'+ geo_l2s[i].monitor_loc + '<br>' + 
        								'<b>Inside Lake: </b>'+ geo_l2s[i].inside_lake + '<br>' + 
        								'<b>Distance from shore: </b>'+ geo_l2s[i].dist_shore + ' m<br>' + 
        								'<a href="/site/' + geo_l2s[i].title +'">More...</a>'+    
        							'</div>'

			     infoContent.push(infoElem);
			     var marker = new google.maps.Marker({
			          position: position,
			          map: mapl2s,
			          title: geo_l2s[i].title
			        }); 
			     bounds.extend(marker.position);

			     google.maps.event.addListener(marker, 'click', (function(marker, i) {
				    return function() {
				      //console.log(i);
				      //console.log(infoContent[i]);
				      infowindow.setContent(infoContent[i]);
				      infowindow.open(mapl2s, marker);
				    }
				  })(marker, i));
			    
			} 
			 mapl2s.fitBounds(bounds);
			 //var boundsListener = google.maps.event.addListener(mapl2s, 'bounds_changed', function(event) {
		       // mapl2s.setZoom(14);
		        //google.maps.event.removeListener(boundsListener);
		    //});
		    


	       } 

      }