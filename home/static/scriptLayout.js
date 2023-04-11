$(document).ready(function(){
    $("#search_field").autocomplete({
        source: "/search",
        minLength: 3
    });
});


