---
slug: "vscode-extension"
date: 2022-05-03
author: siegs
layout: blog
title: A VS Code Extension for Tiltfiles
image: /assets/images/vscode-extension/gears.jpg
image_caption: 'Plastic Gear Lot from <a href="https://www.pexels.com/photo/assorted-color-plastic-gear-lot-1476320/">Dan Cristian Pădureț</a>'
subtitle: Improve Tiltfile authoring when working in VS Code
description: Stop switching between code and documentation and use our VS Code Extension to write your Tiltfiles!
tags:
- tiltfile
- devtools
- vscode
---

If you use [Visual Studio Code][code], are new to Tilt and have been spending a lot of time switching between writing your `Tiltfile` and reading our [`Tiltfile` API Reference][docs], stop! Go [install our new `Tiltfile` extension][install] and let us help you write `Tiltfile`s more easily! And if you're not a fan of VS Code, stay to learn about the components we used to build the extension. (You might be able to re-use what we built into Tilt to drive a `Tiltfile` extension in your own editor!)

Our `Tiltfile` extension is [available in the Visual Studio marketplace][install], and can also be found in the Extensions sidebar inside VS Code. The extension requires you to have Tilt installed already; make sure you're using [the latest release][upgrade] to ensure you have all the features available.

## Syntax Highlighting

`Tiltfile`s are based on [Starlark][starlark], a dialect of Python. The extension automatically highlights Starlark thanks to a TextMate bundle derived from [Bazel's VS Code Extension][Bazel] and [Magic Python][].

You can also use [our TextMate bundle for syntax highlighting with other IDEs that support it][tmbundle].

## Completion and Signature Help

A major reason for using an IDE like VS Code is to help you write code faster and more correctly with context-aware hints. The `Tiltfile` extension adds symbol completion for [Starlark builtin functions and methods][starlark], [Tilt builtins][docs], and any variables or functions you define in your `Tiltfile`s. The documentation shown in pop-ups is sourced from the same code that generates [our API docs][docs].

When you type the opening parenthesis (`(`) of a function or method, the extension gives help on the parameters to that function:

![Signature Help][imgsighelp]

The extension has some basic type inference that will show only methods for Starlark strings, lists, or dictionaries when available, otherwise methods on all types will be presented.

![Method Completion][imgmethods]

## Hover and Go to Definition

When you hover your cursor over a variable, function or method, the extension displays a documentation pop-up:

![Hover Documentation][imghover]

You can also type F12 ("Go to Definition") with the cursor on (almost) any symbol and jump to the definition of it. (Symbols for which you can't jump are Starlark/Tilt builtins and Tilt extensions. The latter can be fixed and [has an issue open that you can follow][refext].)

## Load Statements

The extension is aware of Starlark load statements in your `Tiltfile`s and makes the symbols you declare available for completion, signature help, and hover. It also can warn you about errors in your
load statements:

![Load Statements with errors][imgload]

## Live Errors

The extension detects when you have Tilt running, checks for any runtime errors in your Tiltfile, and underlines them. Since Tilt automatically re-runs your Tiltfile on change, this means you can edit your Tiltfile, hit save, and see errors right away, without leaving VS Code:

![Live errors][imgerrors]

Finally, you may have noticed the "🌐 Tilt" bit in the status bar in the bottom right of VS Code. Click on it to open the Tilt UI in your browser.

# A Language Server

Underneath the hood of the `Tiltfile` extension is a [Language Server Protocol (LSP)][lsp] implementation built into Tilt. While the [extension code itself][vscode-tilt] is fairly thin, the bulk of the functionality is provided by the language server, most of which is provided by the [starlark-lsp][] package. [Milas investigated][spec] different ways of building a language extension and analyzing Starlark code, and we settled on building a language server in Go using the [go.lsp.dev](https://go.lsp.dev/) and [Tree sitter][] libraries. Writing the LSP in Go allows us to embed starlark-lsp directly into Tilt, which makes for easy distribution. We ended up using Tree Sitter's Python grammar to parse Starlark, which allows us to define [builtins and their documentation in Python stub files][tilt-api-stubs] that are parsed by starlark-lsp when the language server initializes.

Having a `Tiltfile` language server means that implementing a Tilt extension in your editor of choice should not be difficult. Editors like [Sublime Text][sublimelsp], [Vim][vimlsp] and [Emacs][emacslsp] already have LSP client packages available, so it's a matter of configuring a new language with a language server that runs the command `tilt lsp start`.

We also wrote [starlark-lsp][] to be Tilt-agnostic, so if you have some other Starlark-based application and want to build a language server extension for it, feel free to use or extend it for that purpose!

# Let's Hear It

If you have ideas for the `Tiltfile` VS Code extension or the Starlark LSP server, let us know by [filing an issue][vscode-issue] or [contributing some code][contribute]! Enjoy!


[code]: https://code.visualstudio.com/
[docs]: {{site.docsurl}}/api.html
[install]: https://marketplace.visualstudio.com/items?itemName=tilt-dev.tiltfile
[upgrade]: {{site.docsurl}}/upgrade.html

[starlark]: https://github.com/bazelbuild/starlark/blob/master/spec.md

[Bazel]: https://github.com/bazelbuild/vscode-bazel
[Magic Python]: https://github.com/MagicStack/MagicPython
[tmbundle]: https://github.com/tilt-dev/tiltfile.tmbundle

[refext]: https://github.com/tilt-dev/vscode-tilt/issues/28

[imgsighelp]: {{site.blogurl}}/assets/images/vscode-extension/signature-help.gif
[imgmethods]: {{site.blogurl}}/assets/images/vscode-extension/methods.gif
[imghover]: {{site.blogurl}}/assets/images/vscode-extension/hover.png
[imgload]: {{site.blogurl}}/assets/images/vscode-extension/load.png
[imgerrors]: {{site.blogurl}}/assets/images/vscode-extension/live-errors.gif

[lsp]: https://code.visualstudio.com/api/language-extensions/language-server-extension-guide
[vscode-tilt]: https://github.com/tilt-dev/vscode-tilt/tree/main/src
[Tree sitter]: https://tree-sitter.github.io/tree-sitter/

[sublimelsp]: https://github.com/sublimelsp
[vimlsp]: https://github.com/mattn/vim-lsp-settings
[emacslsp]: https://emacs-lsp.github.io/lsp-mode/

[spec]: https://github.com/tilt-dev/tilt.specs/blob/master/ide_extensions.md
[starlark-lsp]: https://github.com/tilt-dev/starlark-lsp
[tilt-api-stubs]: https://github.com/tilt-dev/tilt/tree/master/internal/tiltfile/api

[vscode-issue]: https://github.com/tilt-dev/vscode-tilt/issues/new
[contribute]: https://github.com/tilt-dev/vscode-tilt/blob/main/CONTRIBUTING.md
