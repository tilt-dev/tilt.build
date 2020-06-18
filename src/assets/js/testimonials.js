// Interaction for the testimonial list

function testimonialScroll(target) {
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
