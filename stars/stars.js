let fetch = require("node-fetch");

function humanizeNumber(count) {
  if (count < 1000) {
    return count;
  }

  if (count < 10000) {
    return (count / 1000).toFixed(1) + "k";
  }

  return (count / 1000).toFixed(0) + "k";
}

fetch("https://api.github.com/repos/tilt-dev/tilt")
  .then(res => res.json())
  .then(obj => obj.stargazers_count)
  .then(stars => {
    console.log(humanizeNumber(stars));
  });
