


async function fetchFromJson(place) {
    const response = await fetch(`http://localhost:5000/${place}`)
    const data = await response.json()
    return data
}

async function doAll() {

    const markerName = document.querySelector("input[name = name]")
    const markerDesc = document.querySelector("textarea[name = desc]")
    const markerLat = document.querySelector("input[name = lat]")
    const markerLang = document.querySelector("input[name = lang]")
    const markerIcon = document.querySelector("select[name = icon]")
    const markerId = document.querySelector("input[name = id]")
    const attribNams = document.querySelector("input[name = attribNames]")
    const attribVals = document.querySelector("input[name = attribVals]")
    const clickedArea = document.querySelector("input[name=clicked-area")

    const delMarker = document.querySelector("#delete")
    const deleteBool = document.querySelector("input[name=delete")
    const addMarker = document.querySelector("#add")

    const map = L.map('map').setView([0,0], 3);

    L.tileLayer(`mapTiles/{z}/{x}/{y}.png`, {
        maxZoom: 5,
        minZoom: 0,
        noWrap: true
    }).addTo(map)

    function style() {
        return {
            opacity: 0,
            fillOpacity: 0
        };
    }

    delMarker.addEventListener("click", e => {
        deleteBool.value = "true"
        document.querySelector("form").requestSubmit()

    })

    function findClickedArea(e) {
        var layer = e.target;

        clickedArea.value = layer.feature.properties.name
    }
    async function onEachFeature(feature, layer) {
        layer.on({
            click: findClickedArea
        });
    }

    L.geoJson(await fetchFromJson("getGeoJSON"), {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map)

    async function autoFill(name, description, iconType, lat, lang, attribnam, attribval) {
        markerName.value = name
        markerDesc.innerHTML = description
        markerIcon.value = iconType
        markerLat.value = lat
        markerLang.value = lang
        attribNams.value = attribnam
        attribVals.value = attribval
    }

    var popup = L.popup();

    function onMapClick(e) {
        autoFill("", "", "poiSafeRed", e.latlng["lat"], e.latlng["lng"], "", "")
        delMarker.classList.add("hidden")
        addMarker.innerHTML = "Add"
        popup
            .setLatLng(e.latlng)
            .setContent(
                `<h2>${clickedArea.value}</h2><hr>`+
                `<b>Search this area for ingredients?</b><br>`+
                `<input type="text" placeholder="Set focus?" name="focus"><button id="search-area">Hunt for ingredients</button><br>`
            )
            .openOn(map);

        const search = document.querySelector("#search-area")

        search.addEventListener("click", async (e) => {
            const itemsFound = await fetchFromJson(`getAreaItems?area=${clickedArea.value}&focus=${document.querySelector("input[name=focus]").value}`)
            popup
                .setContent(`<h2>Ingredients found:</h2><hr>${itemsFound.map(item => {
                    return `${item.name}: ${item.value}<br>`
                }).join("")}`)
        })
    }

    map.on('click', onMapClick);

    async function makeMarker(name, description, attribNames, attribValues, iconType, lat, lang, id) {
        const imgSize = iconType.includes("poi") ? 30 : 40
        const iconImg = L.icon({
            iconUrl: `mapStuff/markerTypes/${iconType}.webp`,

            iconSize: [imgSize, imgSize],
            iconAnchor: [imgSize / 2, imgSize],
            popupAnchor: [0, -(imgSize / 2)]
        })

        const marker = L.marker([lat, lang], { icon: iconImg }).addTo(map)
        let attributes = ""
        for (let i = 0; i < attribNames.length; i++) {
            attributes = attributes + `<b>${attribNames[i]}: </b>${attribValues[i]}<br>`
        }
        marker.bindPopup(`<h2>${name}</h2><hr>${description}<br>${attributes}`)
        marker.addEventListener("click", e => {
            autoFill(name, description, iconType, lat, lang, attribNames, attribValues)
            markerId.value = id
            delMarker.classList.remove("hidden")
            addMarker.innerHTML = "Save"
        })
    }

    async function makeAllMarkers() {
        const mapMarkers = await fetchFromJson("getMapMarkers")
        mapMarkers.forEach(marker => {
            makeMarker(marker.name, marker.description, marker.attributes.names, marker.attributes.values, marker.iconType, marker.lat, marker.lang, marker.id)
        });
    }

    makeAllMarkers()
}

doAll()


