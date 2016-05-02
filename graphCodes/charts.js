function parse(spec, element) {
  vg.parse.spec(spec, function(chart) { chart({el:element}).update(); });
}
parse("static/js/hash_freq_ng.json", "#vis");
parse("static/js/term_freq_ng.json", "#vis1");

parse("static/js/time_chart_ng.json", "#vis2");