
$(document).ready(function () {
    // initialize dashboard services
    var service = Dashboard.core.default();
    // register sample widgets
    Dashboard.samples.default(service);

    // create dashboard view and refresh list
    var dashboard = $('.dashboard-sortable').dashboard({
        dashboardService: service
    }).dashboard("refresh");
    // initialize widget add dialog
    $('h1 .fa.fa-plus-square').dashboardWidgetDialog({
        dashboardService: service,
        addCallback: function(widgetData) {
            dashboard.dashboard("addWidget", widgetData);
        }
    });

});