/**
 * Created by ltumuhairwe on 7/9/17.
 */
$("#documents a").click(function() {
    addTab($(this));
});

function addTab(link) {
    // hide other tabs
    $("#tabs li").removeClass("current");
    $("#content p").hide();

    // add new tab and related content
    $("#tabs").append("<li class='current'><a class='tab' id='" +
        $(link).attr("rel") + "' href='#'>" + $(link).html() +
        "</a><a href='#' class='remove'>x</a></li>");
    $("#content").append("<p id='" + $(link).attr("rel") + "_content'>" +
        $(link).attr("title") + "</p>");
    // set the newly added tab as curren
    $("#" + $(link).attr("rel") + "_content").show();
    $('#tabs a.tab').live('click', function() {
        // Get the tab name
        var contentname = $(this).attr("id") + "_content";
        // hide all other tabs
        $("#content p").hide();
        $("#tabs li").removeClass("current");
        // show current tab
        $("#" + contentname).show();
        $(this).parent().addClass("current");
    });
    $('#tabs a.remove').live('click', function() {
        // Get the tab name
        var tabid = $(this).parent().find(".tab").attr("id");
        // remove tab and related content
        var contentname = tabid + "_content";
        $("#" + contentname).remove();
        $(this).parent().remove();
    });

    // If tab already exist in the list, return
    if ($("#" + $(link).attr("rel")).length != 0)
        return;

// if there is no current tab and if there are still tabs left, show the first one
    if ($("#tabs li.current").length == 0 && $("#tabs li").length > 0) {
        // find the first tab
        var firsttab = $("#tabs li:first-child");
        firsttab.addClass("current");
        // get its link name and show related content
        var firsttabid = $(firsttab).find("a.tab").attr("id");
        $("#" + firsttabid + "_content").show();}
}




