document.getElementsByName('file')[0].oninput = function () {
	var filename = document.getElementsByName('file')[0].files[0].name;
	if (filename.indexOf(".png") == -1 && filename.indexOf(".jpg") == -1 && filename.indexOf(".jpeg") == -1) {
		alert("Upload only image files");
	} else {
		document.getElementById('part1').style.display="none";
		document.getElementById('part3').style.display="block";
	}
}
document.getElementById("logout").onclick= function () {
	localStorage.clear();
	window.location.href="/";
}
document.getElementById("form").style.display ="none";
document.getElementById("add_post").onclick= function () {
	if (document.getElementById("add_p").innerHTML == "remove") {
		document.getElementById("add_p").innerHTML = "add";
		document.getElementById("form").style.display ="none";
	} else {
		document.getElementById("add_p").innerHTML = "remove";
		document.getElementById("form").style.display ="block";
	}
}
if (localStorage.length == 0) {
	window.location.href="/";
}