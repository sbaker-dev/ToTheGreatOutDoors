/**
 * Parse the Post code from the user, and then add in the map coordinates x and y position. Combine these with the
 * google maps https base link (with directions) to create an external link. Then, open this link.
 */
function GetDirections(){

    let postCode = document.getElementById('PostCode');
    let locationCoordinate = postCode.getAttribute('data-map-x') + ",+" + postCode.getAttribute('data-map-y')
    let directionLink = "https://www.google.com/maps/dir/" + postCode.value + ",United+Kingdom/" + locationCoordinate
    window.open(directionLink)
}