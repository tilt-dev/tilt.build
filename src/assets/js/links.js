// Adapted from
// http://blog.parkermoore.de/2014/08/01/header-anchor-links-in-vanilla-javascript-for-github-pages-and-jekyll/

(function() {
  var anchorForId = function (id) {
    var anchor = document.createElement("a");
    anchor.className = "permalink";
    anchor.href      = "#" + id;
    anchor.innerHTML = "►";
    return anchor;
  };

  document.onreadystatechange = function () {
    if (this.readyState === "complete") {
      let links = Array.from(document.querySelectorAll('.docsContent h2[id],.docsContent h3[id]'))
      links.forEach((el) => el.insertBefore(anchorForId(el.id), el.firstChild))
    }
  };
})()
