# Sublime Markdown Popups {: .doctitle}
Popup tooltips for Sublime generated with Markdown.

---

## Overview
Sublime Markdown Popups (mdpopups) is a library for Sublime Text plugins.  It utilizes the new plugin API found in ST3 Beta 3080+ for generating tooltip popups.  Mdpopups utilizes Python Markdown with a couple of special extensions to convert Markdown to HTML that can be used to create popups.  It also provides a number of other helpful API commands to aid in creating great tooltips.

Mdpopus provides both a dark and light CSS theme to style your popups, both of which can be overridden or extended.  Mdpopups will determine the brightness of your color scheme when deciding which theme to use.  If desired, a user can map their different color scheme files to custom tooltip CSS themes.

![Screenshot](images/tooltips_test.png)

## Features

- Can take Markdown or HTML and create nice looking popup tooltips.
- Provides a dark and light theme.
- Uses the current Sublime color scheme of a view to create matching tooltip themes.
- Can create syntax highlighed code blocks easily using either Pygments or the built-in Sublime Text syntax highlighter automatically in the Markdown environment or outside via API calls.
- Can create color preview boxes via API calls.
- A CSS template environment that allows users to override and tweak the overall look of the tooltip theme to better fit their preferred look.  Using the template filters, users can generically access color scheme colors and manipulate them.
- Plugins can extend the current CSS to inject plugin specific class styling.  Extended CSS will be run through the template environment.
