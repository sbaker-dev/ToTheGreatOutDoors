// Base on https://stackoverflow.com/questions/52576376/how-to-zoom-in-on-a-complex-svg-structure
// This prevents the arrows appearing when you hold down the middle mouse button, so we can just use that for panning
document.body.onmousedown = function(e) { if (e.button === 1) return false; }


const svgImage = document.getElementById("svgImage");
const svgContainer = document.getElementById("svgContainer");
const zoomValue = document.getElementById("zoomValue");
const xPos = document.getElementById("xPos");
const yPos = document.getElementById("yPos");

// TODO: This is dependent on the window size and what your drawing
const xStart = -400
const yStart = -100

// TODO: Given we are going to need to return to pages, we need to have a setter and getter, that sets and gets these
//  values, so that we can return to them
let viewBox = {x: xStart, y: yStart, w: 1200, h: 800};
svgImage.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.w} ${viewBox.h}`);
const svgSize = {w:1200,h:800};
let isPanning = false;
let startPoint = {x: 0, y: 0};
let endPoint = {x: 0, y: 0};
let scale = 1;


let previousLocation = document.getElementById('SelectPlace').value


/**
 * Handle the zoom of the map window
 */
svgContainer.onmousewheel = function(e) {
    e.preventDefault();

    // Scrolling takes a positive value if scrolling down, and a negative if scrolling up. We take the sign so we can
    // scroll exponentially
    const dw = viewBox.w * Math.sign(e.deltaY) * 0.05;
    const dh = viewBox.h * Math.sign(e.deltaY) * 0.05;

    // Create the dx/dy with the mouse offset (to allow for scrolling to where the mouse 'is')
    const dx = dw * e.offsetX / svgSize.w;
    const dy = dh * e.offsetY / svgSize.h;

    // Adjust the viewbox and scale with these updated values
    viewBox = {x:viewBox.x+dx,y:viewBox.y+dy,w:viewBox.w-dw,h:viewBox.h-dh};
    scale = svgSize.w/viewBox.w;

    // Assign this value to the html zoom element
    zoomValue.innerText = `${Math.round(scale*100)/100}`;
    svgImage.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.w} ${viewBox.h}`);
}

/**
 * If a mouse button is pressed down, then we start panning. Set the start point relative to where the mouse currently
 * is
 * @param e Mouse Event
 */
svgContainer.onmousedown = function(e){
    isPanning = true;
    startPoint = {x:e.x,y:e.y};
}


/**
 * If we move the mouse whilst panning, pan the camera
 * @param e Mouse Event
 */
svgContainer.onmousemove = function(e){
    if (isPanning){

        // Invert panning controls due to the polygons requiring inversion
        endPoint = {x:e.x,y:e.y};
        const dx = (startPoint.x - endPoint.x) / scale;
        const dy = (endPoint.y - startPoint.y) / scale;
        const movedViewBox = {x: viewBox.x + dx, y: viewBox.y + dy, w: viewBox.w, h: viewBox.h};

        xPos.innerText = `${Math.round((movedViewBox.x - xStart) * 100) / 100}`;
        yPos.innerText = `${Math.round((movedViewBox.y - yStart) * 100) / 100}`;
        svgImage.setAttribute('viewBox', `${movedViewBox.x} ${movedViewBox.y} ${movedViewBox.w} ${movedViewBox.h}`);

    }
}

/**
 * If we are panning, and the mouse key is lifted up, pan the camera this frame, then set panning to false
 * @param e Mouse Event
 */
svgContainer.onmouseup = function(e){
    if (isPanning){
        endPoint = {x:e.x,y:e.y};
        var dx = (startPoint.x - endPoint.x)/scale;
        var dy = (endPoint.y - startPoint.y)/scale;
        viewBox = {x:viewBox.x+dx,y:viewBox.y+dy,w:viewBox.w,h:viewBox.h};
        svgImage.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.w} ${viewBox.h}`);
        isPanning = false;
    }
}

/**
 * Stop the camera panning if we leave the view box, otherwise the map jumps around
 * @param _ Mouse Event
 */
svgContainer.onmouseleave = function(_){
    isPanning = false;
}

/**
 * Recenter the map to the starting position
 */
function recenter(){
    viewBox = {x: xStart, y: yStart, w: 1200, h: 800};
    svgImage.setAttribute('viewBox', `${xStart} ${yStart} 1200 800`);
    xPos.innerText = `1`;
    yPos.innerText = `1`;
    zoomValue.innerText = `1`;
    startPoint = {x: startPoint.x - startPoint.x, y: startPoint.y - startPoint.y};
    endPoint = {x: endPoint.x - endPoint.x, y: endPoint.y - endPoint.y};
    scale = 1;
    isPanning = false;


}


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