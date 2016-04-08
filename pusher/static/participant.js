function toggleAll(target) {
	var isChecked = $(target).is(":checked");

	var checkboxes = $("input[name$=push][type='checkbox']")

	$(checkboxes).prop('checked', isChecked);
}