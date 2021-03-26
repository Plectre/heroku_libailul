window.onload = () => {
    var i = 0;
    var slideShowSpeed = 4000;
    var datas = load("/static/datas/bd_datas.json");
    //var url = "https://api.openweathermap.org/data/2.5/weather?q=Bordeaux&lang=fr&appid=73f0cb8d52b1212107a574bf5fc5370e&units=metric"
    var dataWeather;
    var result = JSON.parse(datas)

    var bar_meteo = document.querySelector(".bar-meteo p");
    var card = document.querySelector(".card");
    var mySlide = document.querySelector(".mySlide img");
    var text = document.querySelector(".img-desc");
    //var fadeSource = document.querySelector("#fadeSource");
    //const btnTooglenavBar = document.querySelector(".btn-toogle-minibar")
    //const miniNavBar = document.querySelector(".mini-bar");
    const infoContainer = document.querySelector('#info-container');
    const infoClose = document.querySelector('#info-close');
    //const btn_refresh = document.querySelector("#btn-refresh")
    //btn_refresh.addEventListener('click', ()=>{location.reload()});
    card.addEventListener("mouseenter", listener, false);
    card.addEventListener("mouseout", listener, false);

    // Fermeture de la fiche info
    function closeInfo() {
    infoClose.addEventListener('click', () => {
        infoContainer.classList.add('hidden'),
        false
    });
    }
    function formatDate(timeStamp) {
        var date = new Date(timeStamp * 1000);
        var dateOfTheDay = date.getDate();
        var day = setDay(date.getDay());
        var month = setMonth(date.getMonth())
        var hours = date.getHours();
        var minutes = addZero(date.getMinutes())
        var dateObject = {
            "hours": hours,
            "minutes": minutes,
            "day": day,
            "month": month,
            "dateOfTheDay": dateOfTheDay
        };
        return dateObject;
    }

    function addZero(_minuts) {
        if (_minuts < 10) {
            _minuts = "0" + _minuts
        }
        return _minuts
    }
    var strDay = ["Dimanche", "Lundi", "Mardi", "Mercredi",
        "Jeudi", "Vendredi", "Samedi"
    ]

    function setDay(_day) {
        return strDay[_day];
    }
    var strMonth = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Décembre"
    ]

    function setMonth(month) {
        return strMonth[month];
    }

    function connectError() {
        bar_meteo.innerHTML = "<-- Aucune connexion aux serveurs metéo -->";
    }

    // fetch(url).then(function (response) {
    //     response.text().then(function (txt) {
    //         dataWeather = JSON.parse(txt)

    //         display_meteo_bar(dataWeather)
    //     });
    // }).catch(connectError);

    // function display_meteo_bar(datas) {
    //     var temp = dataWeather.main.temp;
    //     temp = Math.trunc(temp);
    //     var wind = dataWeather.wind.speed;
    //     wind = Math.round(wind * 3.60); //convertion m/s en km/h
    //     var dir = dataWeather.wind.deg;
    //     var clouds = dataWeather.clouds.all
    //     var cloud_desc = dataWeather.weather[0].description;
    //     var pressure = dataWeather.main.pressure;
    //     var time = formatDate(dataWeather.dt);
    //     var sunset = formatDate(dataWeather.sys.sunset);

    //     var meteo = " < " + time.day + " " +
    //         time.dateOfTheDay + " " +
    //         time.month +
    //         " à " + time.hours +
    //         "h" + time.minutes + " -- " +
    //         " Température : " + temp + "°C -- " +
    //         "Vent : " + wind + " km/h" +
    //         " du " + dir + "° -- " +
    //         cloud_desc + " " + clouds + "% -- " +
    //         "Pression : " + pressure + " hPa -- " +
    //         "Couché du soleil : " + sunset.hours + "h" + sunset.minutes +
    //         " > ...Bon vols à tous ! ";

    //     bar_meteo.innerHTML = meteo;
    // }

    // On ecoute les evenements de la souris
    function listener(event) {
        switch (event.type) {
            case "mouseenter":
                //console.log("mouse Enter");
                console.log(window.getComputedStyle(card).getPropertyValue("y"));
                break;
            case "mouseout":
                //console.log("mouse Out");
                break;
        }
    }
    // Fonction de glissement de l'image ...
    function slideShow() {
        if (i < result.images.length) {
            mySlide.src = result.images[i];
            text.innerHTML = result.desc[i]
            i++;
        } else {
            i = 0;
        }
        setTimeout(slideShow, slideShowSpeed);
    }
    // Charge et lit les fichiers json
    function load(file) {
        if (window.XMLHttpRequest) { // Safari
            request = new XMLHttpRequest();
        } else if (window.ActiveXObject) {
            request = new ActiveXObject("Microsoft.XMLHTTP"); //IE Microsoft
        } else {
            return; // Non supporté
        }

        request.open('GET', file, false); // Ouverture du fichier
        request.responseText = "json";
        request.send(null);

        return request.responseText; // renvoi le contenu du fichier
    }

    function toogle_form() {
        var form = document.querySelector("form")
        if (form.style.display === "flex") {
            form.style.display = "none";
        } else {
            form.style.display = "flex";
        }
    };
    
    slideShow()
    closeInfo()
}