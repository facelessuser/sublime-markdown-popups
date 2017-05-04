## Overview

All settings for `MdPopups` are placed in Sublime's `Preferences.sublime-settings`.  They are applied globally and applied to all popups and phantoms.

## `mdpopups.debug`

Turns on debug mode.  This will dump out all sorts of info to the console.  Content before parsing to HTML, final HTML output, traceback from failures, etc..  This is more useful for plugin developers.  It works by specifying an error level.  `0` or `false` would disable it.  1 would trigger on errors. 2 would trigger on warnings and any level below.  3 would be general info (like HTML output) and any level below.

```js
    "mdpopups.debug": 1,
```

## `mdpopups.disable`

Global kill switch to prevent popups (created by MdPopups) from appearing.

```js
    "mdpopups.disable": true,
```

## `mdpopups.cache_refresh_time`

Control how long a CSS theme file will be in the cache before being refreshed.  Value should be a positive integer greater than 0.  Units are in minutes.  Default is 30.

```js
    "mdpopups.cache_refresh_time": 30,
```

## `mdpopups.cache_limit`

Control how many CSS theme files will be kept in cache at any given time.  Value should be a positive integer greater than or equal to 0.

```js
    "mdpopups.cache_limit": 10
```

## `mdpopups.use_sublime_highlighter`

Controls whether the Pygments or the native Sublime syntax highlighter is used for code highlighting.  This affects code highlighting in Markdown conversion] via and when [md2html](#md2html) and when code is directly processed using [syntax_highlight](#syntax_highlight). To learn more about the syntax highlighter see [Syntax Highlighting](#syntax-highlighting).

```js
    "mdpopups.use_sublime_highlighter": true
```

## `mdpopups.user_css`

Overrides the default CSS theme.  Value should be a relative path pointing to the CSS theme file: `Packages/User/my_custom_theme.css`.  Slashes should be forward slashes. By default, it will point to `Packages/User/mdpopups.css`.  User CSS overrides all CSS: base, default, plugin, etc.

```js
    "mdpopups.use_sublime_highlighter": "Packages/User/mdpopups.css"
```

## `mdpopups.default_formatting`

Controls whether mdpopups default formatting (contained in [`base.css`](https://github.com/facelessuser/sublime-markdown-popups/blob/master/css/base.css)) will be applied or not.

## `mdpopups.default_style`

Controls whether mdpopups default styling (contained in [`default.css`](https://github.com/facelessuser/sublime-markdown-popups/blob/master/css/default.css)) will be applied or not.

## `mdpopups.sublime_user_lang_map`

This is a special setting allowing the mapping of personal syntax languages which are not yet included or will not be included in the official mapping table.  You can either define your own new entry, or use the name of an existing entry to extend language keywords or syntax languages.  When extending, user keywords and languages will be cycled through first.

```js
    'mdpopups.sublime_user_lang_map': {
        "language": (('keywords',), ('MyPackage/MySyntaxLanguage'))
    }
```

**Example**:
```js
'mdpopups.sublime_user_lang_map': {
    'javascript': (('javascript', 'js'), ('JavaScript/JavaScript', 'JavaScriptNext - ES6 Syntax/JavaScriptNext'))
}
```

For a list of all currently supported syntax mappings, see the official [mapping file](https://github.com/facelessuser/sublime-markdown-popups/blob/master/st3/mdpopups/st_mapping.py).

--8<-- "refs.md"
