define(['jquery', 'pubsub', 'app/urlmanager', 'superselect'], function($, pubsub, urlManager, SuperSelect) {

    'use strict';

    // Populate selector and prepare its publisher
    $.getJSON(window.API_URL + '/info')
        .done(function(response_data) {
            var existingYears = response_data.data.years
            var yearSelector = $("#year-selector")
            for (var i = 0; i < existingYears.length; ++i) {
                var year = existingYears[i];
                var item = '<option value="' + year + '">' + year + '</option>';
                yearSelector.append(item)
            }

            // // -----------SUPER STYLED SELECT------------------------------------------
            // // Iterate over each select element
            // $('#year-selector').each(function() {
            //     var yearSelector = new SuperSelect($(this));

            //     // // Subscribe to year change
            //     // pubsub.subscribe("year.changed", function(event, data) {
            //     //     yearSelector.setValue(data.value);
            //     // });

            //     yearSelector.on('change', function(e, value) {
            //         pubsub.publish('year.changed', {
            //             value: [value]
            //         });
            //         /* alert($this.val()); Uncomment this for demonstration! */
            //     });

            // });
            // // ------------------------------------------------------------------------


            // Subscribe to year change
            pubsub.subscribe("year.changed", function(event, data) {
                $("#year-selector").val(data.value)
            })

            // Set current year
            var currentYear = urlManager.getParam('year')
            // if (!currentYear) currentYear = new Date().getFullYear()
            yearSelector.val(currentYear)
        });

    // Publish year change
    $("#year-selector").change(function(e) {
        pubsub.publish('year.changed', {value: e.target.value})
    })
});
