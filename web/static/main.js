var url = window.location.href;
function submit() {
	var lake_id = document.getElementById('lake_id');
	window.location.replace(url+'site/'+lake_id.value.trim());

}
