(function() {
  const eventListener = () => {
    if (document.readyState !== "complete") {
      return
    }

    // Adapted from
    // http://blog.parkermoore.de/2014/08/01/header-anchor-links-in-vanilla-javascript-for-github-pages-and-jekyll/
    // Adds floading header anchors.
    const headerLinks = document.querySelectorAll('.Docs-content h2[id],.Docs-content h3[id]');
    headerLinks.forEach(el => {
      // wrap the header contents in a link so that the entire thing is clickable
      const link = document.createElement('a');
      link.href = '#' + el.id;
      link.innerHTML = el.innerHTML;
      el.innerHTML = link.outerHTML;
    })

    // Add _target=_blank to external links.
    const links = document.querySelectorAll('a')
    links.forEach(el => {
      let href = String(el.href)
      if (href.indexOf('localhost') == -1 &&
          href.indexOf('tilt.dev') == -1 &&
          href.indexOf('github.com/tilt-dev/') == -1) {
        el.target = "_blank"
        el.rel = "noopener noreferrer"
      }
    })

    document.removeEventListener('readystatechange', eventListener)
  }

  document.addEventListener('readystatechange', eventListener);
})()
