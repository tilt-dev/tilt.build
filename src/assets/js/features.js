// Interaction for the feature list.

function featureScroll(target) {
  let id = target.getAttribute("data-feature-target");
  if (!id) {
    console.error("missing feature target on element");
    return;
  }

  let el = document.querySelector(
    ".Home2-features-contentItem[data-feature-id='" + id + "']"
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
}
