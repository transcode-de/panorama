$(document).ready(function() {
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
});