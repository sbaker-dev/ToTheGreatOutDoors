

let lastTravelLocation = ""

function ChangeSelected(place_id){

    if (lastTravelLocation !== ""){
            document.getElementById(lastTravelLocation).style.fill = '#2D2E44';

    }


    // Split the ID on the dollar sign to get an array with name, category, and (Optional) external link
    const place_id_values = place_id.split("$");

    // Set the name and category
    document.getElementById('LocationName').innerText = place_id_values[0]
    document.getElementById('LocationCategory').innerText = "Location Type:" + place_id_values[1]

    // Conditionally set the external link
    SetExternalLink(place_id_values[2])

    // Set the selected to the selection colour
    document.getElementById(place_id).style.fill = "lightblue";
    lastTravelLocation = place_id

}


function SetExternalLink(external_link){
    const link_part = document.getElementById('LocationExternalLink')
    if (external_link === 'None'){
        link_part.innerText = "Sorry, no external link known"
        link_part.removeAttribute("href")
    }
    else {
        link_part.innerText = "More information here"
        link_part.setAttribute("href", external_link)

    }

}