[![Donate via PayPal][donate-image]][donate-link]
[![Discord][discord-image]][discord-link]
[![Build][github-ci-image]][github-ci-link]
![License][license-image]
# Sublime Markdown Popups

Sublime Markdown Popups (mdpopups) is a library for Sublime Text plugins.  It utilizes the new plugin API found in ST3 Beta 3080+ for generating tooltip popups. It also provides API methods for generating and styling the new phantom elements introduced in ST3 Beta 3118+.  Mdpopups utilizes Python Markdown with a couple of special extensions to convert Markdown to HTML that can be used to create the popups and/or phantoms.  It also provides a number of other helpful API commands to aid in creating great tooltips and phantoms.

Mdpopups will use your color scheme to create popups/phantoms that fit your editors look.

![Screenshot](docs/src/markdown/images/tooltips_test.png)

## Features

- Can take Markdown or HTML and create nice looking popup tooltips and phantoms.
- Dynamically creates popup and phantom themes from your current Sublime color scheme.
- Can create syntax highlighted code blocks easily using either Pygments or the built-in Sublime Text syntax highlighter automatically in the Markdown environment or outside via API calls.
- Can create color preview boxes via API calls.
- A CSS template environment that allows users to override and tweak the overall look of the tooltip and phantom themes to better fit their preferred look.  Using the template filters, users can generically access color scheme colors and manipulate them.
- Plugins can extend the current CSS to inject plugin specific class styling.  Extended CSS will be run through the template environment.

# Documentation

https://facelessuser.github.io/sublime-markdown-popups

# License
Released under the MIT license.

Copyright (c) 2015 - 2020 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[github-ci-image]: https://github.com/facelessuser/sublime-markdown-popups/workflows/build/badge.svg?branch=master&event=push
[github-ci-link]: https://github.com/facelessuser/sublime-markdown-popups/actions?query=workflow%3Abuild+branch%3Amaster
[discord-image]: https://img.shields.io/discord/678289859768745989?logo=discord&logoColor=aaaaaa&color=mediumpurple&labelColor=333333
[discord-link]: https://discord.gg/TWs8Tgr
[license-image]: https://img.shields.io/badge/license-MIT-blue.svg?labelColor=333333
[donate-image]: https://img.shields.io/badge/Donate-PayPal-3fabd1?logo=paypal
[donate-link]: https://www.paypal.me/facelessuser
