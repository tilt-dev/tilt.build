// Interaction for the feature list.

function featureScroll(target) {
  let id = target.getAttribute("data-feature-target");
  if (!id) {
    console.error("missing feature target on element");
    return;
  }

  let el = document.querySelector(
    ".js-featuresContentItem[data-feature-id='" + id + "']"
  );
  if (!el) {
    console.error("missing feature element " + id);
    return;
  }

  let scrollingEl = el.parentNode;
  scrollingEl.scroll({
    top: el.offsetTop,
    behavior: "smooth"
  });

  function activateTarget() {
    document.querySelectorAll(".js-featuresNavItemButton").forEach(button => {
      let item = button.parentNode;
      if (button == target) {
        item.classList.toggle("is-active");
      } else {
        item.classList.remove("is-active");
      }
    });
  }

  // If the active item is not one we clicked, close it first.
  let activeItem = document.querySelector(".js-featuresNavItem.is-active");
  if (activeItem && activeItem != target.parentNode) {
    activeItem.classList.remove("is-active");
    setTimeout(activateTarget, 300);
  } else {
    activateTarget();
  }
}
