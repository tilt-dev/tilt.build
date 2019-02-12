(function() {
  function $(sel) {
    return document.querySelector(sel)
  }

  let notches = [
    {sel: '.notch--1', rotate: 90, transform: 'translate(568.0799865722656px, 30.780078895390034px) rotate(0deg) translate(-568.0799865722656px, -30.780078895390034px)'},
    {sel: '.notch--2', rotate: -90, transform: 'translate(31.439985513687134px, 30.77007481828332px) rotate(0deg) translate(-31.439985513687134px, -30.77007481828332px)'},
    {sel: '.notch--3', rotate: 90, transform: 'translate(238.06499481201172px, 30.77007481828332px) rotate(0deg) translate(-238.06499481201172px, -30.77007481828332px)'},
    {sel: '.notch--4', rotate: -90, transform: 'translate(405.0400085449219px, 169.33999633789062px) rotate(0deg) translate(-405.0400085449219px, -169.33999633789062px)'}
  ]

  window.addEventListener('scroll', () => {
    let scrollY = window.scrollY
    let scrollMax = document.body.offsetHeight - window.innerHeight
    if (scrollMax <= 0 || !scrollMax) {
      return
    }

    let pct = scrollY / scrollMax
    notches.forEach((notch) => {
      let el = $(notch.sel)
      if (!el) {
        return
      }

      let rotate = notch.rotate * pct
      let newTransform = notch.transform.replace('rotate(0deg)', `rotate(${rotate.toFixed(2)}deg)`)
      el.style.transform = newTransform
    })
  }, {passive: true})
})();
