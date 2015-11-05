# Sublime Markdown Popups {: .doctitle}
Popup tooltips for Sublime generated with Markdown.

---

## Overview
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
