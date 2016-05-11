var map = null;
var geojson = null;
var shpfile = null
var lang_color = {
    "en": "#FCEC39",
    "fr": "#59FC39",
    "de": "#DE57F9",
    "et": "#831039",
    "es": "#BA761E",
    "und": "#F3EDE5",
    "ja": "#1E070F"
};
var default_color = "#C57DE4";
var lang_processing = false;

function getColor(d) {
    switch (true) {
        case d > 0.50:
            return '#800026';
        case d <= 0.50 && d > 0.25:
            return '#BD0026';

        case d <= 0.25 && d > 0:
            return '#E31A1C';
        case d <= 0 && d > -0.25:
            return '#FC4E2A';
        case d <= -0.25 && d > -0.50:
            return '#FD8D3C';
        case d <= -0.50 && d > -0.75:
            return '#FEB24C';
        case d <= -0.75:
            return '#FED976';
            return '#FFEDA0';

    }
}

function randomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 3,
        dashArray: '',
        fillOpacity: 0.5
    });

    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }
}

function resetHighlight(e) {
    shpfile.resetStyle(e.target);
    var layer = e.target;

    layer.setStyle({
        weight: 1,
        dashArray: '',
        fillOpacity: 0.30
    });
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}


function create_map(file_name, options) {

    lang_processing = false;
    if (options.lang == true) {
        lang_processing = true;
    }
    if (map != undefined || map != null) {
        map.remove();
    }
    map = L.map('map');
    // Load the tile images from OpenStreetMap
    var mytiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    });

    var mytiles2 = L.tileLayer('http://{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright" title="OpenStreetMap" target="_blank">OpenStreetMap</a> contributors | Tiles Courtesy of <a href="http://www.mapquest.com/" title="MapQuest" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png" width="16" height="16">',
        subdomains: ['otile1', 'otile2', 'otile3', 'otile4']
    });

    var mapboxAccessToken = "pk.eyJ1Ijoic2FyYTI5IiwiYSI6ImNpbmdvbmVkbDBidDR1Z2x5NjlyejN3NWQifQ.C26TQRn9wvgvM4kiIeJSsg";
    var mytiles3 = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=' + mapboxAccessToken, {
        id: 'mapbox.light'
    });


    //add suburbs boundaries
    shpfile = new L.Shapefile('vic_postcode.zip', {
        onEachFeature: function(feature, layer) {
            layer.on({
                mouseover: highlightFeature,
                mouseout: resetHighlight
            });

            if (feature.properties) {
                layer.bindPopup(Object.keys(feature.properties).map(function(k) {
                    return k + ": " + feature.properties[k];
                }).join("<br />"), {
                    maxHeight: 200
                });
            }

        }
    });



    shpfile.addTo(map);




    // Initialise an empty map
    default_style = {
        radius: 7,
        fillColor: "red",
        color: "white",
        weight: 1,
        opacity: 1,
        fillOpacity: 1
    };



    // Read the GeoJSON data with jQuery, and create a circleMarker element for each tweet
    // Each tweet will be represented by a nice red dot
    $.getJSON(file_name, function(data) {
        var myStyle = default_style;

        geojson = L.geoJson(data, {
            pointToLayer: function(feature, latlng) {


                if (feature.properties.hasOwnProperty("sent")) {
                    c = getColor(feature.properties.sent)
                } else {
                    if (feature.properties.hasOwnProperty("lang")) {
                        c = lang_color[feature.properties.lang] || default_color
                    }
                }
                myStyle["fillColor"] = c;
                return L.circleMarker(latlng, myStyle);
            }
        });
        geojson.addTo(map)
    });


    //legend
    var legend = L.control({
        position: 'bottomright'
    });
    if (lang_processing) {
        legend.onAdd = function(map) {

            var div = L.DomUtil.create('div', 'info legend');


            // loop through our density intervals and generate a label with a colored square for each interval

            var c_ls = {
                "en": "#FCEC39",
                "fr": "#59FC39",
                "de": "#DE57F9",
                "et": "#831039",
                "es": "#BA761E",
                "und": "#F3EDE5",
                "ja": "#1E070F"
            };

            for (key in c_ls) {
                div.innerHTML +=
                    '<i style="background:' + c_ls[key] + '"></i> ' + key + "<br>";

            }




            return div;
        };
    } else {
        legend.onAdd = function(map) {

            var div = L.DomUtil.create('div', 'info legend');
            grades = [1, 0.50, 0.25, 0, -0.25, -0.50, -0.75];


            for (var i = 0; i < grades.length; i++) {
                div.innerHTML +=
                    '<i style="background:' + getColor(grades[i]) + '"></i> ' +
                    ((grades[i + 1] || grades[i + 1] == 0) ? +grades[i + 1] : '-1') + "    " + grades[i] + "<br>";
            }




            return div;
        };
    }

    legend.addTo(map);


    // Add the tiles to the map, and initialise the view in the middle of Europe
    map.addLayer(mytiles2).setView([-37.77915274, 145.94872684], 9);

}


function parse(spec, element) {
    vg.parse.spec(spec, function(chart) {
        chart({
            el: element
        }).update();
    });
}

var isFullscreen = false;


function show_results(name) {
    switch (name) {

        case "drink":
            create_map("geo_data_dr.json", {});
            // parse("static/js/hash_freq_dr.json", "#drink .vis1");
            parse("term_freq_dr.json", "#drink .vis2");
            parse("time_chart_dr.json", "#drink .vis3");
            parse("sent_time_chart_dr.json", "#drink .vis4");
            break;


        case "neg":
            create_map("geo_data_neg.json", {});
            parse("hash_freq_neg.json", "#neg .vis1");
            parse("term_freq_neg.json", "#neg .vis2");
            parse("time_chart_neg.json", "#neg .vis3");
            parse("sent_time_chart_neg.json", "#neg .vis4");
            break;

        case "pol":
            create_map("geo_data_pol.json", {});
            parse("hash_freq_pol.json", "#pol .vis1");
            parse("term_freq_pol.json", "#pol .vis2");
            parse("time_chart_pol.json", "#pol .vis3");
            parse("sent_time_chart_pol.json", "#pol .vis4");
            break;

        case "prt":
            create_map("geo_data_prt.json", {});
            parse("hash_freq_prt.json", "#prt .vis1");
            parse("term_freq_prt.json", "#prt .vis2");
            parse("time_chart_prt.json", "#prt .vis3");
            parse("sent_time_chart_prt.json", "#prt .vis4");
            parse("pie_chart_prt.json", "#prt .vis5");
            parse("suburb_pie_chart_prt.json", "#prt .vis6");
            break;

        case "lang":
            create_map("geo_data_lang.json", {
                "lang": true
            });
            parse("pie_chart_lang.json", "#lang .vis1");
            parse("suburb_pie_chart_lang.json", "#lang .vis2");
            parse("population_suburb_pie_chart_lang.json", "#lang .vis3");
            break;

        default:
            break;


    }

}

function fullscreen(element) {
    $("#charts_bar").show();
    $(".background-img").hide();
    isFullscreen = true;
    $chart_div = $("#" + $(element).attr("view"));

    $(element).addClass("acive");
    $(".controls2").removeClass("active");
    $("#map").show();
    $("div.wrapper").removeAttr("target");
    show_results($chart_div.attr("id"));
    $chart_div.closest("div.wrapper").show();
    $chart_div.closest("div.wrapper").attr("target", true);

    $chart_div.closest("div.wrapper").siblings(".wrapper").hide();


}


$(document).ready(function() {

    $("#charts_bar").click(function() {
        $("div.wrapper[target=true]").slideToggle("fast", function() {
        });
    });

});
