function switchTab(tabName, reload = false) {
	// Hide all tabs
	var tabs = document.getElementsByClassName('tab');
	for (var i = 0; i < tabs.length; i++) {
		tabs[i].style.display = 'none';
	}

	// Show the selected tab
	document.getElementById(tabName).style.display = 'block';

	window.history.replaceState(null, '', window.location.pathname);


	window.history.replaceState(null, null, "?tab=" + tabName);
	
	if (reload) {
		window.location.reload();
	}
	window.location.search = urlParams;
    }

function createTag() {
	let tag_name = prompt("Напишите название тэга");

	if (tag_name != null) {
		var create_form = document.getElementById("create_new_tag_form");

		var input_name = document.createElement("input");
		input_name.name = "name";
		input_name.value = tag_name;

		create_form.appendChild(input_name);

		create_form.submit();

	}
}
