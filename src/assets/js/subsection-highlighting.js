function highlightSubnav(targetUrl) {
    function activateTarget() {
        document.querySelectorAll(".Docs-subnav-link").forEach(item => {
          if (item.href == targetUrl) {
            item.classList.add("is-active");
            accordionPanel = item.parentNode.parentNode
            sectionHeaderButton = accordionPanel.parentNode.firstElementChild.firstChild
            if (sectionHeaderButton.type == "button" && !!accordionPanel.getAttribute("aria-hidden")) {
                sectionHeaderButton.click()
            }
          } else {
            item.classList.remove("is-active");
          }
        });
    }
    
    // If the active item is not one we clicked, close it first.
    let activeItem = document.querySelector(".Docs-subnav-link.is-active");
    if (activeItem && activeItem.href != targetUrl) {
        activeItem.classList.remove("is-active");
        setTimeout(activateTarget, 300);
    } else {
        activateTarget();
    }
}

highlightSubnav(document.URL)