[![Donate via PayPal][donate-image]][donate-link]
[![Discord][discord-image]][discord-link]
[![Build][github-ci-image]][github-ci-link]
![License][license-image]
# Sublime Markdown Popups

Sublime Markdown Popups (mdpopups) is a library for Sublime Text plugins.  It utilizes the new plugin API found in ST3
3080+ for generating tooltip popups. It also provides API methods for generating and styling the new phantom elements
introduced in ST3 3118+.  Mdpopups utilizes Python Markdown with a couple of special extensions to convert Markdown to
HTML that can be used to create the popups and/or phantoms.  It also provides a number of other helpful API commands to
aid in creating great tooltips and phantoms.

Mdpopups will use your color scheme to create popups/phantoms that fit your editors look.

![Screenshot](docs/src/markdown/images/tooltips_test.png)

## Features

- Can take Markdown or HTML and create nice looking popup tooltips and phantoms.
- Dynamically creates popup and phantom themes from your current Sublime color scheme.
- Can create syntax highlighted code blocks easily using either Pygments or the built-in Sublime Text syntax highlighter
  automatically in the Markdown environment or outside via API calls.
- Can create color preview boxes via API calls.
- A CSS template environment that allows users to override and tweak the overall look of the tooltip and phantom themes
  to better fit their preferred look.  Using the template filters, users can generically access color scheme colors and
  manipulate them.
- Plugins can extend the current CSS to inject plugin specific class styling.  Extended CSS will be run through the
  template environment.

# Documentation

https://facelessuser.github.io/sublime-markdown-popups

[github-ci-image]: https://github.com/facelessuser/sublime-markdown-popups/workflows/build/badge.svg?branch=master&event=push
[github-ci-link]: https://github.com/facelessuser/sublime-markdown-popups/actions?query=workflow%3Abuild+branch%3Amaster
[discord-image]: https://img.shields.io/discord/678289859768745989?logo=discord&logoColor=aaaaaa&color=mediumpurple&labelColor=333333
[discord-link]: https://discord.gg/TWs8Tgr
[license-image]: https://img.shields.io/badge/license-MIT-blue.svg?labelColor=333333
[donate-image]: https://img.shields.io/badge/Donate-PayPal-3fabd1?logo=paypal
[donate-link]: https://www.paypal.me/facelessuser
