/**
 * author: RaffaDNDM
 * date:   2024-10-15
 */

$.getJSON("https://api.ipify.org?format=json", function(data) {
                
    // Setting text of element P with id gfg
    str_x= data.ip
    
    if(data.ip==$("#office1").html() || data.ip==$("#office2").html() || data.ip==$("#office3").html())
        str_x += " (Office)";
    else
        str_x += " (External)";

    $("#x").html(str_x);
})