$(document).ready(function(){
    $(".glyphicon-filter").on("click", function () {
        // console.log($(".filter-container").css("display"));

        if($(".filter-container").css("display")=="none"){
            $(".filter-container").css({"display":"block"});
            $(".glyphicon-filter").css({"transform":"rotate(180deg)"});

        }else{
            $(".filter-container").css({"display":"none"});
            $(".glyphicon-filter").css({"transform":"rotate(0deg)"});

        }
    })
});