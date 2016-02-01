$(function() {
    $("a.close[close-href]").click(function (e) {
            e.preventDefault();
            $.post($(this).attr("close-href"), "", function () {
            });
        }
    );
});

