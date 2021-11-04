// Adapted from
// http://blog.parkermoore.de/2014/08/01/header-anchor-links-in-vanilla-javascript-for-github-pages-and-jekyll/

(function() {
  const eventListener = () => {
    if (document.readyState !== "complete") {
      return
    }

    const links = document.querySelectorAll('.Docs-content h2[id],.Docs-content h3[id]');
    links.forEach(el => {
      // wrap the header contents in a link so that the entire thing is clickable
      const link = document.createElement('a');
      link.href = '#' + el.id;
      link.innerHTML = el.innerHTML;
      el.innerHTML = link.outerHTML;
    })
    document.removeEventListener('readystatechange', eventListener)
  }

  document.addEventListener('readystatechange', eventListener);
})()
