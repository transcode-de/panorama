var dashboard_cookieName = "privatdash";

function saveOrder() {
    cookieContent = {};
    $('.widget').each(function (index, value) {
        var self = $(value);
        var widgetID = self.attr('id');
        var column = self.parent().attr('id');
        var index_in_col = self.index();
        var is_collapsed = !self.find('.widget-content').hasClass('in');
        if (!cookieContent[column]) {
            cookieContent[column] = {};
        }
        cookieContent[column][index_in_col] = {
            'widgetID': widgetID, 'is_collapsed': is_collapsed
        };
    });
    $.cookie(dashboard_cookieName, JSON.stringify(cookieContent));
}

function restoreOrder() {
    var dashboard_order = JSON.parse($.cookie(dashboard_cookieName));
    for (var column_id in dashboard_order) {
        var column = $('#' + column_id);
        var column_info = dashboard_order[column_id];
        for (var widget_order in column_info) {
            var widget_information = column_info[widget_order];
            var widget = $('#' + widget_information['widgetID']);
            var is_collapsed = widget_information['is_collapsed'];
            if (is_collapsed) {
                widget.find('.widget-content').removeClass('in');
            }
            column.append(widget);
        }
    }
}

function defaultOrder() {
    $.cookie(dashboard_cookieName, null);
    location.reload();
}

$(document).ready(function () {
    $(document).on("eldarion-ajax:success", function(){
        $('.widget-content').niceScroll();
    });
    $('.column').on('sortstop', function(){
        $('.widget-content').getNiceScroll().resize();
    });


    $('.dashboard-tooltip').tooltip({
        'placement': 'bottom', 'container': 'body'
    });
    $( ".column" ).sortable({
        connectWith: ".column",
        cursor: "move",
        cancel: ".widget-content, .btn",
        delay: 150,
        forceHelperSize: true,
        forcePlaceholderSize: true,
        toleranceType: "pointer",
        stop: function() { saveOrder(); }
    });

    $('.widget-content')
        .on('shown.bs.collapse', function() {
            saveOrder();
        })
        .on('hidden.bs.collapse', function() {
            saveOrder();
        });

    $('#restore-widget-order').click(function () {
        defaultOrder();
    });
    restoreOrder();

});