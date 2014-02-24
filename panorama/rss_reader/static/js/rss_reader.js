function mark_as_read() {
    $('.mark-read-link').on('click', function() {
		var self = $(this);
		$.ajax({
			'url': self.data('url'),
			'success': function() {
				self.removeAttr('data-url');
				$(self.data('target')).remove();
				self.removeAttr('data-target');
			}
		});
	});
}

$(document).ready(function() {
	mark_as_read();
	$(document).on("eldarion-ajax:success", mark_as_read);
});