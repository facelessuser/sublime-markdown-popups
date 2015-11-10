[![Unix Build Status][travis-image]][travis-link]
![License][license-image]
# Sublime Markdown Popups
Sublime Markdown Popups (mdpopups) is a library for Sublime Text plugins.  It utilizes the new plugin API found in ST3 Beta 3080+ for generating tooltip popups.  Mdpopups utilizes Python Markdown with a couple of special extensions to convert Markdown to HTML that can be used to create popups.  Mdpopups also uses Pygments to allow for both inline and block syntax highlighted code.

Mdpopus provides both a dark and light CSS theme to style your popups, both of which can be overridden or extended.  Mdpopups will determine the brightness of your color scheme when deciding which theme to use.  If desired, a user can map their different color scheme files to custom tooltip CSS themes.

![Screenshot](https://dl.dropboxusercontent.com/u/342698/sublime-markdown-tooltips/early_prototype.png)

## Features

- Can take markdown and create nice looking popup tooltips.
- Provides a dark and light theme.
- Detects color scheme brightness in order to decide whether a light or dark tooltip should be used.
- Allows overriding the default dark and light themes.
- Users can map custom tooltip themes to individual color schemes.
- Plugins can specify or extend the current CSS.
- Markdown can be disabled to use straight HTML.
- Autolinks HTML links (it is up to the plugin to handle the links).
- Allows nested fenced syntax highlighted code blocks and inline blocks via Pygments.

# Documentation

http://facelessuser.github.io/sublime-markdown-popups/

# License
Released under the MIT license.

Copyright (c) 2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[travis-image]: https://img.shields.io/travis/facelessuser/sublime-markdown-popups/master.svg
[travis-link]: https://travis-ci.org/facelessuser/sublime-markdown-popups
[license-image]: https://img.shields.io/badge/license-MIT-blue.svg
