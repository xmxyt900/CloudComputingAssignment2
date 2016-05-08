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
            parse("hash_freq_dr.json", "#drink .vis1");
            parse("term_freq_dr.json", "#drink .vis2");
            parse("time_chart_dr.json", "#drink .vis3");
            parse("sent_time_chart_dr.json", "#drink .vis4");
            break;


        case "neg":
            create_map("geo_data_neg.json", {});
            parse("hash_freq_neg.json", "#neg .vis1");
            parse("term_freq_neg.json", "#neg .vis2");
            parse("time_chart_neg.json", "#neg .vis3");
            break;

	case "pol":
		create_map("geo_data_pol.json",{});
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
            break;

        case "lang":
            create_map("geo_data_lang.json", {"lang":true});
           // parse("hash_freq_prt.json", "#lang .vis1");
            //parse("term_freq_prt.json", "#lang .vis2");
           // parse("time_chart_lang.json", "#lang .vis3");
            //parse("sent_time_chart_lang.json", "#lang .vis4");
            parse("pie_chart_lang.json", "#lang .vis5");
            break;

          default:
          	break;


    }
}

function fullscreen(element) {

    //var  d = document.getElementById('controls').style;
    var d = {};
    var speed = 900;
    if (!isFullscreen) { // MAXIMIZATION

        /*comment to have smooth transition from centre but loose covering the header*/
        //document.getElementById('controls').style.position= "absolute";

        d.width = "20px";
        d.height = "20px";
        //d.left="0%";
        d.top = "0px";
        d.margin = "0 0 0 0";

        $(element).closest("div").animate(d, speed);
        $(element).prop("txt",$(element).html() );
        $(element).html("Back");
        //$(element).closest("div").css('margin-top',"-"+$(element).closest("div.wrapper").css('margin-top'));

        //$(element).closest("div").css('margin-left',"-"+$(element).closest("div.wrapper").css('margin-left'));

        isFullscreen = true;
        $("#footer").hide();
        chart_div = ($(element).closest("div").siblings("div.charts")[0]);
        $(element).closest("div.wrapper").css("z-index", 50);
        $(element).closest("div.wrapper").css("background", "white");


        $(element).closest("div.wrapper").css('margin-top', "0px");
         $(element).closest("div.wrapper").css('margin-left', "0px");
        show_results(chart_div.id);


        $(chart_div).show();
		$("#map").css("margin-top",Math.ceil($("div.single:visible").length/2)*500+"px");

        $("#map").show();
    } else { // MINIMIZATION

        d.width = "270px";
        d.height = "150px";
        // d.position="relative";
        //d.top="+=20px";

        /* comment to have smooth minimze transition but not be placed below header */
        // document.getElementById('controls').style.position= "relative";

        $(element).closest("div").animate(d, 1500);
        $(element).html($(element).prop("txt"));
        $($(element).closest("div").siblings("div.charts")[0]).hide();
        $("#map").hide();

        $(element).closest("div.wrapper").css("z-index", 5);
        $(element).closest("div.wrapper").css("background", "");

        //$(element).closest("div").css('margin-top',"-"+$(element).closest("div").css('margin-top'));

        //$(element).closest("div").css('margin-left',"-"+$(element).closest("div").css('margin-left'));
        $(element).closest("div").css('margin-left', function(index, curValue) {
            return parseInt(curValue, 10) + 40 + Math.floor($(element).closest("div.wrapper").prevAll("div.wrapper").length/3) * 310  + 'px';
        });
        $(element).closest("div.wrapper").css('margin-top', $(element).closest("div.wrapper").prevAll("div.wrapper").length%3 * 170 + 40 + 'px');

        isFullscreen = false;

        $("#footer").show();
    }

}
