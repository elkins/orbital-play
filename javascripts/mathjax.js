window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*",
    processHtmlClass: "arithmatex"
  }
};

document.addEventListener("DOMContentLoaded", function() {
  if (typeof MathJax !== 'undefined') {
    MathJax.typesetPromise();
  }
});

// For MkDocs Material instant loading
if (typeof app !== 'undefined') {
  app.document$.subscribe(function() {
    if (typeof MathJax !== 'undefined') {
      MathJax.typesetPromise();
    }
  });
}
