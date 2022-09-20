<!--Hide and show elements for reply button-->

function hideElement(elementID){
    let element = document.getElementById("BT-" + elementID)
    element.classList.add('hidden')

}

function showElement(elementID){
    let element = document.getElementById("H-" + elementID)
    element.classList.remove('hidden')

    hideElement(elementID)
}