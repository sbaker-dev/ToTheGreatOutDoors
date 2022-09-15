
let loadingCount = 0
let loaded = 0

function setLoadedCount(total){
    loadingCount = total;


}


function updateLoaded(){
    loaded += 1;

    let elem = document.getElementById("progressBar");
    const loadedPercent = (loaded / loadingCount) * 100 + "%";

    elem.style.width = loadedPercent;
    elem.innerHTML = loadedPercent;

    if (loaded === loadingCount){
        let loadingScreen = document.getElementById('LoadingScreen')
        loadingScreen.classList.add('fadeAway')
    }
}




function countLoaded(){

    console.log(loadingCount)
    console.log(loaded)
}