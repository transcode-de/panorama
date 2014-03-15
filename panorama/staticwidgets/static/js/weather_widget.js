function weatherWidget() {
    widgets = $('.weather-widget-content');
    widgets.each(function(index, value) {
        $(value).find('.weather-temperature').openWeather({
            city: $(value).data('weatherlocation'),
            placeTarget: $(value).find('.weather-place'),
            units: 'c',
            descriptionTarget: $(value).find('.weather-description'),
            windSpeedTarget: $(value).find('.weather-wind-speed'),
            humidityTarget: $(value).find('.weather-humidity'),
            sunriseTarget: $(value).find('.weather-sunrise'),
            sunsetTarget: $(value).find('.weather-sunset'),
            iconTarget: $(value).find('.weather-icon'),
            customIcons: 'static/img/weather/',
            error: function(message) {
                console.log(message);
            }
        });
    });
}

$(document).ready(function(){
    weatherWidget();
});
