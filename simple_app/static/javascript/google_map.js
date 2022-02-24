'use strict';

/** Hide a DOM element. */
function hideElement(el) {
    el.style.display = 'none';
}

/** Show a DOM element that has been hidden. */
function showElement(el) {
    el.style.display = 'block';
}

function mapStationsToMarker(googleMapObj, station) {
    let marker = new google.maps.Marker({
        position: new google.maps.LatLng({
            'lat': parseFloat(station.lat),
            'lng': parseFloat(station.lng)
        }),
        title: station.ar,
        map: googleMapObj,
    });
    return marker;
}

function mapStationsToLocationResult(station) {
    return {
        "title": station.sna.replace('YouBike2.0_', ''),
        "address1": station.ar,
        "coords": {
            'lat': parseFloat(station.lat),
            'lng': parseFloat(station.lng)
        },
        // "placeId": "ChIJQRJ5VmypQjQRwvCsSW8Y3UQ"  // how to get this ?
    }
}

const youbikeStationLocations = function(callback) {
    var xmlhttp = createHttpRequestor()
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    }
    xmlhttp.open("GET", "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json", true);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send();
}

function searchResultHandler(locator, address, location) {
    // search locations
    if (locator.searchLocationMarker) {
        locator.searchLocationMarker.setMap(null); // clear marker
    }
    if (!location) {
        locator.searchLocation = null;
        return;
    }
    locator.searchLocation = {
        'address': address,
        'location': location
    };
    locator.searchLocationMarker = new google.maps.Marker({
        icon: { // https://developers.google.com/maps/documentation/javascript/reference/marker#MarkerLabel
            path: "M 12,2 C 8.1340068,2 5,5.1340068 5,9 c 0,5.25 7,13 7,13 0,0 7,-7.75 7,-13 0,-3.8659932 -3.134007,-7 -7,-7 z",
            anchor: new google.maps.Point(12, 17),
            fillOpacity: 1,
            fillColor: '#FFFFFF',
            strokeWeight: 2,
            strokeColor: "green",
            scale: 2,
            labelOrigin: new google.maps.Point(12, 9)
        },
        position: location,
        map: locator.map,
        title: address
    });
    locator.map.panTo(locator.searchLocation.location)

    // clear youbike station markers
    if (locator.markers && locator.markers.length >= 0) {
        locator.markers.forEach(element => {
            element.setMap(null)
        });
    }
    // mark stations
    let nearStations = locator.nearEnoughStations(locator.youbikeStations);
    locator.markers = nearStations.map(element => mapStationsToMarker(locator.map, element));
    if (locator.markers) {
        // marker click callback
        locator.markers.forEach(function(element, index) {
            element.addListener('click', function() {
                locator.selectResultItemCallback(index, false, true);
            })
        });
        // new results
        locator.locations = nearStations.map(mapStationsToLocationResult);
    }
    // update data
    const addressParts = address.split(' ');
    locator.userCountry = addressParts[addressParts.length - 1];
    locator.updateBounds(); // if you want to zoom out the map 
    locator.renderResultsList();
    locator.updateTravelTimes();
    locator.clearDirections();
}


/** Search youbike locations  **/
function initializeYoubikeSearchInput(locator) {
    const geocoder = locator.geocoder;
    const youbikeGeocodeCache = new Map();
    const searchInputEl = document.getElementById('youbike-search-input');
    const searchButtonEl = document.getElementById('youbike-search-button');

    const geocodeSearch = function(query) {
        if (!query) {
            return;
        }

        if (youbikeGeocodeCache.has(query)) {
            const cacheResult = youbikeGeocodeCache.get(query)
            searchResultHandler(locator, cacheResult.formatted_address, cacheResult.location);
            return;
        }
        const request = {
            address: query,
            bounds: locator.map.getBounds()
        };

        geocoder.geocode(request, function(results, status) {
            if (status === 'OK') {
                if (results.length > 0) {
                    const result = results[0];
                    youbikeGeocodeCache.set(query, result);
                    searchResultHandler(locator, result.formatted_address, result.location);
                }
            }
        });
    };

    // Set up geocoding on the search input.
    searchButtonEl.addEventListener('click', function() {
        geocodeSearch(searchInputEl.value.trim());
    });

    // Initialize Autocomplete.
    initializeSearchInputAutocomplete(
        locator, searchInputEl, geocodeSearch, searchResultHandler);
}

/** Add Autocomplete to the search input. */
function initializeSearchInputAutocomplete(
    locator, searchInputEl, fallbackSearch, searchLocationUpdater) {
    // Set up Autocomplete on the search input. Bias results to map viewport.
    const autocomplete = new google.maps.places.Autocomplete(searchInputEl, {
        types: ['geocode'],
        fields: ['place_id', 'formatted_address', 'geometry.location']
    });
    autocomplete.bindTo('bounds', locator.map);
    autocomplete.addListener('place_changed', function() {
        const placeResult = autocomplete.getPlace();
        if (!placeResult.geometry) {
            // Hitting 'Enter' without selecting a suggestion will result in a
            // placeResult with only the text input value as the 'name' field.
            fallbackSearch(placeResult.name);
            return;
        }
        searchLocationUpdater(
            locator, placeResult.formatted_address, placeResult.geometry.location);
    });
}

/** Initialize Distance Matrix for the locator. */
function initializeDistanceMatrix(locator) {
    const distanceMatrixService = new google.maps.DistanceMatrixService();

    // Annotate travel times to the selected location using Distance Matrix.
    locator.updateTravelTimes = function() {
        if (!locator.searchLocation) return;

        const units = (locator.userCountry === 'USA') ?
            google.maps.UnitSystem.IMPERIAL :
            google.maps.UnitSystem.METRIC;
        const request = {
            origins: [locator.searchLocation.location],
            destinations: locator.locations.map(function(x) {
                return x.coords;
            }),
            travelMode: google.maps.TravelMode.DRIVING,
            unitSystem: units,
        };
        const callback = function(response, status) {
            if (status === 'OK') {
                const distances = response.rows[0].elements;
                for (let i = 0; i < distances.length; i++) {
                    const distResult = distances[i];
                    let travelDistanceText, travelDistanceValue;
                    if (distResult.status === 'OK') {
                        travelDistanceText = distResult.distance.text;
                        travelDistanceValue = distResult.distance.value;
                    }
                    const location = locator.locations[i];
                    location.travelDistanceText = travelDistanceText;
                    location.travelDistanceValue = travelDistanceValue;
                }

                // Re-render the results list, in case the ordering has changed.
                locator.renderResultsList();
            }
        };
        distanceMatrixService.getDistanceMatrix(request, callback);
    };
}

/** Initialize Directions service for the locator. */
function initializeDirections(locator) {
    const directionsCache = new Map();
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer({
        suppressMarkers: true,
    });

    // Update directions displayed from the search location to
    // the selected location on the map.
    locator.updateDirections = function() {
        if (!locator.searchLocation || (locator.selectedLocationIdx == null)) {
            return;
        }
        const cacheKey = JSON.stringify(
            [locator.searchLocation.location, locator.selectedLocationIdx]);
        if (directionsCache.has(cacheKey)) {
            const directions = directionsCache.get(cacheKey);
            directionsRenderer.setMap(locator.map);
            directionsRenderer.setDirections(directions);
            return;
        }
        const request = {
            origin: locator.searchLocation.location,
            destination: locator.locations[locator.selectedLocationIdx].coords,
            travelMode: google.maps.TravelMode.WALKING
        };
        directionsService.route(request, function(response, status) {
            if (status === 'OK') {
                directionsRenderer.setMap(locator.map);
                directionsRenderer.setDirections(response);
                directionsCache.set(cacheKey, response);
            }
        });
    };

    locator.clearDirections = function() {
        directionsRenderer.setMap(null);
    };
}

/** Initialize Place Details service and UI for the locator. */
function initializeDetails(locator) {
    const panelDetailsEl = document.getElementById('locations-panel-details');
    const detailsService = new google.maps.places.PlacesService(locator.map);

    const detailsTemplate = Handlebars.compile(
        document.getElementById('locator-details-tmpl').innerHTML);

    const renderDetails = function(context) {
        panelDetailsEl.innerHTML = detailsTemplate(context);
        panelDetailsEl.querySelector('.back-button')
            .addEventListener('click', hideDetails);
    };

    const hideDetails = function() {
        showElement(locator.panelListEl);
        hideElement(panelDetailsEl);
    };

    locator.showDetails = function(locationIndex) {
        const location = locator.locations[locationIndex];
        const context = {
            location
        };

        // Helper function to create a fixed-size array.
        const initArray = function(arraySize) {
            const array = [];
            while (array.length < arraySize) {
                array.push(0);
            }
            return array;
        };

        if (location.placeId) {
            const request = {
                placeId: location.placeId,
                fields: [
                    'formatted_phone_number', 'website', 'opening_hours', 'url',
                    'utc_offset_minutes', 'price_level', 'rating', 'user_ratings_total'
                ]
            };
            detailsService.getDetails(request, function(place, status) {
                if (status == google.maps.places.PlacesServiceStatus.OK) {
                    if (place.opening_hours) {
                        const daysHours =
                            place.opening_hours.weekday_text.map(e => e.split(/\:\s+/))
                            .map(e => ({
                                'days': e[0].substr(0, 3),
                                'hours': e[1]
                            }));

                        for (let i = 1; i < daysHours.length; i++) {
                            if (daysHours[i - 1].hours === daysHours[i].hours) {
                                if (daysHours[i - 1].days.indexOf('-') !== -1) {
                                    daysHours[i - 1].days =
                                        daysHours[i - 1].days.replace(/\w+$/, daysHours[i].days);
                                } else {
                                    daysHours[i - 1].days += ' - ' + daysHours[i].days;
                                }
                                daysHours.splice(i--, 1);
                            }
                        }
                        place.openingHoursSummary = daysHours;
                    }
                    if (place.rating) {
                        const starsOutOfTen = Math.round(2 * place.rating);
                        const fullStars = Math.floor(starsOutOfTen / 2);
                        const halfStars = fullStars !== starsOutOfTen / 2 ? 1 : 0;
                        const emptyStars = 5 - fullStars - halfStars;

                        // Express stars as arrays to make iterating in Handlebars easy.
                        place.fullStarIcons = initArray(fullStars);
                        place.halfStarIcons = initArray(halfStars);
                        place.emptyStarIcons = initArray(emptyStars);
                    }
                    if (place.price_level) {
                        place.dollarSigns = initArray(place.price_level);
                    }
                    if (place.website) {
                        const url = new URL(place.website);
                        place.websiteDomain = url.hostname;
                    }

                    context.place = place;
                    renderDetails(context);
                }
            });
        }
        renderDetails(context);
        hideElement(locator.panelListEl);
        showElement(panelDetailsEl);
    };
}