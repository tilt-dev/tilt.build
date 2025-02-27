---
title: Editor Support
layout: docs
sidebar: gettingstarted
---

Whether you're just starting or are a seasoned Tilter, writing `Tiltfile`s should not be tedious.  
We want to make it easy to experiment with your Tiltfile, so you can experience the magic of Tilt's responsiveness with minimal interruptions to your development flow, that includes switching context to look up `Tiltfile` documentation.

We're offering Tiltfile support for [VS Code](https://code.visualstudio.com/) and select IDEs of the [JetBrains suite](https://www.jetbrains.com/products/#type=ide).  
All code is public and open source. We appreciate contributions of all kinds.

## VS Code
The [official `Tiltfile` extension](https://marketplace.visualstudio.com/items?itemName=tilt-dev.Tiltfile) is available at the VS Code marketplace.  
It provides syntax highlighting, autocomplete and signature support for `Tiltfile` functions.

![](assets/img/vscode-extension.gif)

## TextMate bundles
The [tiltfile.tmbundle](https://github.com/tilt-dev/tiltfile.tmbundle) offers syntax highlighting for any IDEs supporting TextMate bundles, like IntelliJ GoLand, PyCharm or WebStorm.

## Emacs

Tilt is compatible with Emacs' `lsp-mode`.

To enable it, install `lsp-mode` and add the following to your `.emacs`:

```
(require 'python-mode)

(define-derived-mode tiltfile-mode
  python-mode "tiltfile"
  "Major mode for Tilt Dev."
  (setq-local case-fold-search nil))

(add-to-list 'auto-mode-alist '("Tiltfile$" . tiltfile-mode))

(with-eval-after-load 'lsp-mode
  (add-to-list 'lsp-language-id-configuration
    '(tiltfile-mode . "tiltfile"))

  (lsp-register-client
    (make-lsp-client :new-connection (lsp-stdio-connection `("tilt" "lsp" "start"))
                     :activation-fn (lsp-activate-on "tiltfile")
                     :server-id 'tilt-lsp)))
```

## Other editors

Tilt embeds its own language server based on Tree Sitter.

https://github.com/tilt-dev/starlark-lsp

To run it locally, run:

```
tilt lsp start
```

Adding Tiltfile support to a new editor usually requires
a few lines of config to start the language server and connect.

