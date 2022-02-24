function createHttpRequestor() {
    var xmlhttpRequestor;
    if (window.XMLHttpRequest) {
        //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
        xmlhttpRequestor = new XMLHttpRequest();
    } else {
        // IE6, IE5 浏览器执行代码
        xmlhttpRequestor = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlhttpRequestor
}
// response handler
function createYoubikeResponseTable(jsonData, search_query) {

    var table = "<tr><th>Station Number</th><th>Address</th><th>Bike Number</th></tr>";
    for (i = 0; i < jsonData.length; i++) {
        if (jsonData[i].sarea == search_query || jsonData[i].ar.includes(search_query)) {
            table += "<tr><td>" + jsonData[i].sna.replace('YouBike2.0_', '') + "</td><td>" + jsonData[i].ar + "</td><td>" + jsonData[i].sbi + "</td></tr>";
        }
    }
    document.getElementById("youbikeSearchResultTable").innerHTML = table;
}

// search youbike stations location api
function searchYoubike(inputEleName, sucessCallback) {
    var xmlhttp = createHttpRequestor()
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            let youbikeData = JSON.parse(this.responseText);
            let search_query = inputEleName.value
            sucessCallback(youbikeData, search_query)
        }
    }
    xmlhttp.open("GET", "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json", true);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send();
}

// youbike query hint
function showHint(str) {
    if (str.length == 0) {
        document.getElementById("youbikeSearchHint").innerHTML = "";
        return;
    }

    var xmlhttp = createHttpRequestor()
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var result = xmlhttp.responseText
            document.getElementById("youbikeSearchHint").innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "./search_hint/" + str, true);
    xmlhttp.send();
}