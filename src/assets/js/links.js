// Adapted from
// http://blog.parkermoore.de/2014/08/01/header-anchor-links-in-vanilla-javascript-for-github-pages-and-jekyll/

(function() {
  document.onreadystatechange = function () {
    if (this.readyState === "complete") {
      const links = Array.from(document.querySelectorAll('.docsContent h2[id],.docsContent h3[id]'));
      links.forEach(el => {
        // wrap the header contents in a link so that the entire thing is clickable
        const link = document.createElement('a');
        link.href = '#' + el.id;
        link.innerHTML = el.innerHTML;
        el.innerHTML = link.outerHTML;
      })
    }
  };
})()
