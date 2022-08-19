
let selectionID = 'SelectionBox'
let previousLocation = document.getElementById(selectionID).value


/**
 * For the location that has been selected via the selection menu, change the current selection colour back to the
 * default and set the clicked elements colour to the selection colour
 */
function ChangeOnSelectionSelect(selectionColour, defaultColour){
    // Set the last known value to be its default
    document.getElementById(previousLocation).style.fill = defaultColour;

    // Get the newly selected value, assign it as selected, and update previousLocation
    const newValue = document.getElementById(selectionID).value;
    document.getElementById(newValue).style.fill = selectionColour;
    previousLocation = newValue
    return newValue
}


/**
 * Get the original value from the Select container, and set this to the default colour. Then, use the current place's
 * id to select the new polygon on the map and changes it colour to the selection colour
 */
function ChangeOnPolygonSelect(place_id, selectionColour, defaultColour){

    console.log(document.getElementById(selectionID))

    // Set the old value to be default
    const selectionBox = document.getElementById(selectionID);
    document.getElementById(selectionBox.value).style.fill = defaultColour;

    // Set the new value to be blue
    document.getElementById(selectionID).value = place_id;
    document.getElementById(place_id).style.fill = selectionColour;
    previousLocation = place_id;
}


/**
 * Change the colour of a polygon if the user changes the location selection via the selection box. Then, change the
 * href element based on this
 */
function PlaceViaSelect(){

    // Change the polygon selection
    let newValue = ChangeOnSelectionSelect("lightblue", '#A298C4')

    // Assign this to the href button, slicing off the BD- ID linker
    ChangeLocationHref(1, newValue.slice(3))
}


/**
 * Change the value of the selection box when an individual selects a polygon on the map
 * @param place_id id parameter of the selected component
 */
function PlaceViaMap(place_id){

    ChangeOnPolygonSelect(place_id, "lightblue", '#A298C4')

    // Assign this to the href button, slicing off the BD- ID linker
    ChangeLocationHref(1, place_id.slice(3))


}

/**
 * Update the Href of the location selection with the activity
 */
function SelectActivity(){
    // Get the newly selected value and assign it to the href
    ChangeLocationHref(2, document.getElementById('SelectActivity').value.slice(3))

}


/**
 * We cannot directly plug javascript values into a django link, but the link is just a string, and we can adjust the
 * string on the fly. This adjusts a specific element of a link string to be a new value.
 */
function ChangeLocationHref(override_index, replacement_value){

    // Isolate the link button
    let link_button = document.getElementById('LetsGo')

    // Django's url template will create a forward slash link, use this to slice out it's elements
    let href_links = link_button.getAttribute('href').split("/");

    // Skip the first element (as it starts with a forward slash), but for each element, recreate the link. If the
    // override index matches this element (plus 1 as we count starting from words not slashes), then use the
    // replacement_value instead
    let new_link = ""
    for (let link_part_index = 1; link_part_index < href_links.length; link_part_index++ ){
        if (override_index + 1 === link_part_index){
            new_link += "/" + replacement_value
        }
        else {
            new_link += "/" + href_links[link_part_index]
        }
    }

    // Reassign the attribute with the updated value
    link_button.setAttribute('href', new_link)
}


/**
 * Select a given location via the polygon map, then extract it's data link attribute and set the external link a href
 * and text
 */
function LocationViaMap(place_id){

    // Change the selected polygon via the map, and update the selection box
    ChangeOnPolygonSelect(place_id, "lightblue",'#2D2E44');

    // Extract the link from the data attribute data-link
    let externalLink = document.getElementById(place_id).getAttribute('data-link');

    // Conditionally set the external link
    SetExternalLink(externalLink)


}

/**
 * Select the location via the select menu, then extract it's associated polygon data link attribute and set the
 * external link a href and text
 */
function LocationViaSelect(){

    let place_id = ChangeOnSelectionSelect("lightblue",'#2D2E44')

    // Extract the link from the data attribute data-link
    let externalLink = document.getElementById(place_id).getAttribute('data-link');

    // Conditionally set the external link
    SetExternalLink(externalLink)
}


/**
 * Set the external link, conditional on existance.
 */
function SetExternalLink(external_link){
    const link_part = document.getElementById('LocationExternalLink')
    if (external_link === 'None'){
        link_part.innerText = "No external links"
        link_part.removeAttribute("href")
    }
    else {
        link_part.innerText = "More information here"
        link_part.setAttribute("href", external_link)

    }

}