'use strict';

(function() {
  let lastScrollY = -1
  let lastScrollDownTime = 0
  let timer = 0

  function $(sel) {
    return document.querySelector(sel)
  }

  function onTimer() {
    $('.dotSpinner').classList.remove('is-active')
  }

  window.addEventListener('scroll', () => {
    let curScrollY = window.scrollY
    let isDownwards = lastScrollY != -1 && curScrollY > lastScrollY
    if (isDownwards) {
      let dot = $('.dotSpinner')
      if (dot) {
        dot.classList.add('is-active')
        lastScrollDownTime = Date.now()
        clearTimeout(timer)
        timer = setTimeout(onTimer, 200)
      }
    }
    lastScrollY = curScrollY
  }, {'passive': true})
})()
