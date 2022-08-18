let previousLocation = document.getElementById('SelectPlace').value

/**
 * Change the colour of a polygon if the user changes the location selection via the selection box.
 */
function SelectViaSelection(){
    // Set the last known value to be its default
    document.getElementById(previousLocation).style.fill = '#A298C4';

    // Get the newly selected value, assign it as selected, and update previousLocation
    const newValue = document.getElementById('SelectPlace').value;
    document.getElementById(newValue).style.fill = "lightblue"
    previousLocation = newValue

    // Assign this to the href button, slicing off the BD- ID linker
    ChangeLocationHref(1, newValue.slice(3))
}


/**
 * Change the value of the selection box when an individual selects a polygon on the map
 * @param place_id id parameter of the selected component
 */
function SelectViaMapLocation(place_id){
    // Set the old value to be blue
    const selectionBox = document.getElementById('SelectPlace');
    document.getElementById(selectionBox.value).style.fill = '#A298C4';

    // Set the new value to be red
    document.getElementById("SelectPlace").value = place_id;
    document.getElementById(place_id).style.fill = "lightblue";
    previousLocation = place_id;

    // Assign this to the href button, slicing off the BD- ID linker
    ChangeLocationHref(1, place_id.slice(3))


}


/**
 * Update the Href of the location selection with the activity
 * @constructor
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
