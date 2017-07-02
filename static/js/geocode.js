"use strict";


$(function () {
    // Document On Ready

    /* ------------- Map -------------------------- */

    function add_marker(lat, lng) {
        // Adds a single marker to the map and sets the map center there.
        let position = {lat: lat, lng: lng};
        map.setCenter(position);
        let marker = new google.maps.Marker({
            map: map,
            position: position
        });
    }

    /* -------------- Data Entry  ----------------------------- */


    // POSTs the selected stations formdata
    $('#submit-data-glyph').on('click', function (event) {
        event.preventDefault();    // Stop the page from refreshing

        // Captures only selected rows
        let stations = $('.station-entry-row[data-active=enabled]');

        // Array building pattern for stations in the form.
        let data = Object();
        $.each(stations, function (index, station) {
            let fields = $(station).find('input');

            // A single stations object.
            let station_data = Object();
            $.each(fields, function (index, field) {
                let field_name = $(field).attr('name');
                station_data[field_name] = $(field).val();
            });

            // Appends this station to the data Object.
            data[`station_${index}`] = station_data;

        });

        let station_data = {'station_data': data};
        // console.log(station_data);


        // TODO: Rewrite to fetch API
        // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
        $.ajax({
            url: '/calculate',                    // Endpoint
            type: 'POST',
            contentType: 'application/json',      // Important
            data: JSON.stringify(station_data),   // Serialize
            success: function (response) {        // 200
                console.log(response);
                if (response.status === 'success') {
                    add_marker(response.epicenter.lat, response.epicenter.lon);
                }
            },
            error: function (error) {
                console.log(error);
            },
        });  // end .ajax()

    }); // end .on('click')


    /* -------------- Form and UI  ------------------ */


    // Keeps the row data state accurate
    $('.station-entry-row input[type=checkbox]').on('click', function () {
        // Sets the data-active state of the parent row
        let $row = $(this).parents('tr');
        $row.attr('data-active', $row.attr('data-active') === 'enabled' ? 'disabled' : 'enabled');
        $(this).attr('checked', $(this).attr('checked') === 'true' ? 'false' : 'true');
    });


    function update_fields(row, response) {
        console.log(response); // TODO

        let $row = $(row);

        // Parses the Google response data for position data
        let lucky = response.result.results[0];
        let address = lucky.formatted_address;
        let coords = lucky.geometry.location;
        let lat = coords['lat'];
        let lon = coords['lng'];

        /*
         1. Select this rows lat field
         2. Select this rows lon field
         3. Populate
         4. Profit
         */

        $row.find('input[name=name]').val(address);
        $row.find('input[name=latitude]').val(lat);
        $row.find('input[name=longitude]').val(lon);

        add_marker(lat, lon);
    }

    /* -------------- Add And Remove Rows  ------------------ */

    // Add
    $('#add-station-glyph').on('click', function () {
        let $geotable = $('#geodata-table');
        let new_row = $('.station-entry-row:last').clone();
        $geotable.append(new_row);
    });

    // Remove # TODO: Prevent removing too many
    $('#delete-station-glyph').on('click', function () {
        $('.station-entry-row:last').remove();
    });


    /* ----------------- Geocoding -------------------------*/

    $('input.station_address').on('keydown', function (event) {
        if (event.which === 13 | event.keycode === 13) {
            // They pressed return / enter.
            let entry = $(this).val();
            let $row = $(this).parents('tr');

            $.ajax({
                url: '/geocode',
                method: 'POST',
                contentType: 'application/json',      // Important
                data: JSON.stringify({entry: entry}),
                success: function (response) {
                    // Pass to the parsing function
                    update_fields($row, response);
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }

    });
});
