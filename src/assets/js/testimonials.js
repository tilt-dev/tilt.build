// Interaction for the testimonial list


// It's not immediately obvious that the testimonial is scrollable.
// Add a little auto-scroller that changes it ever 10s until the user
// discovers the scrollability.
let testimonialScrollTimerId = window.setInterval(function() {
  let nodes = Array.from(document.querySelectorAll('.Home-testimonials-navItem'))
  let navItems = nodes.
      map((node) => {
        let name = node.getAttribute("data-testimonial")
        let selected = node.classList.contains('is-selected')
        return {name: name, selected: selected, node: node}
      }).
      filter((item) => !!item.name)
  let selectedIndex = navItems.findIndex((item) => item.selected)
  let newIndex = (selectedIndex + 1) % navItems.length
  testimonialScrollInternal(navItems[newIndex].node)
}, 8000)

// Click handler
function testimonialScroll(target) {
  window.clearInterval(testimonialScrollTimerId)
  testimonialScrollInternal(target)
}

function testimonialScrollInternal(target) {
  let timon = target.getAttribute("data-testimonial");
  if (!timon) {
    console.error("missing testimonial attr");
    return;
  }

  let timonEl = document.querySelector(
    '.Home-testimonial[data-testimonial="' + timon + '"]'
  );
  if (!timonEl) {
    console.error("missing testimonial el " + timon);
    return;
  }

  let container = timonEl.parentNode;
  container.style.transform = "translate(" + -timonEl.offsetLeft + "px, 0)";

  document.querySelectorAll(".Home-testimonials-navItem").forEach(item => {
    if (item == target) {
      item.classList.add("is-selected");
    } else {
      item.classList.remove("is-selected");
    }
  });
}
