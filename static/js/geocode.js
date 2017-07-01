"use strict";


$(function () {
    // Document On Ready


    $('#submit-data-glyph').on('click', function (event) {
        event.preventDefault();
        let stations = $('.station-entry-row[data-active=enabled]');

        // Array building pattern for three stations.
        let data = {};
        $.each(stations, function (index, station) {
            let fields = $(station).find('input');
            let station_data = {};
            $.each(fields, function (index, field) {
                let field_name = $(field).attr('name');
                station_data[field_name] = $(field).val();
            });
            data[`station_${index}`] = station_data;

        });

        let station_data = {'station_data': data};
        console.log(station_data);

        $.ajax({
            url: '/calculate',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(station_data),
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            },
        });
    });

    // Keeps the row data state accurate
    $('.station-entry-row input[type=checkbox]').on('click', function () {
        // Sets the data-active state of the parent row
        let $row = $(this).parents('tr');
        $row.attr('data-active', $row.attr('data-active') === 'enabled' ? 'disabled' : 'enabled')
    });


    // Add And Remove Rows

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

    // Geocoding Below
    // $('input#encode').on('click', function () {
    //     $.ajax({
    //         url: `${$SCRIPT_ROOT}/calculate`,
    //         method: 'POST',
    //         data: {
    //             station_address: $('input[name="station_address"]').val()
    //         },
    //         success: function (response) {
    //             console.log(response);
    //             $("#seismic_station").text(response.seismic_station);
    //         },
    //         error: function (error) {
    //             console.log(error);
    //         }
    //     });
    //
    //
    // });
});
