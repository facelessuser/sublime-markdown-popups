# User Guide {: .doctitle}
Using and configuring Sublime Markdown Popups.

---

## API Usage
Mdpopups provides a handful of accessible functions.

### show_popup
mdpopups.show_popup
: 
    Accepts Markdown and creates a Sublime popup tooltip.

    | Parameter | Required | Default | Description |
    | --------- | -------- | ------- | ----------- |
    | view | Yes | | A Sublime Text view object. |
    | content | Yes | | Markdown/HTML content to be used to create a tooltip. |
    | md | No | True | Defines whether the content is Markdown and needs to be converterted. |
    | css | No | None | CSS text that should be used instead of loading a theme. |
    | append_css | No | None | CSS to append to the base theme being used. |
    | flags | No | 0 | Flags to pass down to the Sublime Text `view.show_popup` call. |
    | location | No | -1 | Location to show popup in view.  -1 means to show right under the first cursor. |
    | max_width | No | 320 | Maximum width of the popup. |
    | max_height | No | 240 | Maximum height of the popup. |
    | on_navigate | No | None | Callback that receives one variable `href`. |
    | on_hide | No | None | Callback for when teh tooltip is hidden. |

### update_popup
mdpopups.update_popup
: 
    Updates the current existing popup.

    | Parameter | Required | Default | Description |
    | --------- | -------- | ------- | ----------- |
    | view | Yes | | A Sublime Text view object. |
    | content | Yes | | Markdown/HTML content to be used to create a tooltip. |
    | md | No | True | Defines whether the content is Markdown and needs to be converterted. |
    | css | No | None | CSS text that should be used instead of loading a theme. |
    | append_css | No | None | CSS to append to the base theme being used. |

### hide_popup
mdpopups.hide_popup
: 
    Hides the current popup.

    | Parameter | Required | Default | Description |
    | --------- | -------- | ------- | ----------- |
    | view | Yes | | A Sublime Text view object. |

### get_theme
mdpopups.get_theme
: 
    For various reasons, a user may want to manually retrieve the CSS theme to be used, or potential process there own on the fly CSS text. `get_theme` will retrieve the current CSS that will be used, or process and return a user's own css string buffer.  It returns a `PopupTheme` object that contains the stripped CSS content (no carriage returns or comments), the base colors of the theme (foreground and background colors), and the brightness which can be retrieved with `#!python is_dark()` or `#!python is_light()`.

    | Parameter | Required | Default | Description |
    | --------- | -------- | ------- | ----------- |
    | view | Yes | | target view to retrieve view for. |
    | css | No | | A CSS string buffer.  If this is used, `mdpopups` will not calculate a theme to be used. |
    | from_file | No | | When this is set to `True`, the `css` parameter will be treated as a relative file path.  File paths should be in the form `Packages/MyPluginFolder/mytheme.css`. Please use forward slashes. |

    !!! Note "Note"
        CSS content is cached except when using a CSS string buffer.  Up to X number of CSS files are cached at a time for T amount of time where X is 10 and T is 30 minutes by default.  X and T can be changed in the settings file.  If you need to bypass caching, you will have to clear the cache via [`mdpopups.clear_cache`](#clear_cache).

    !!! Note "Under Construction"
        Still working on what colors will be exposed to users.  Working on a way to easily find index and return them.

### clear_cache
mdpopups.clear_cache
: 
    Clears the CSS theme related caches.

### md2html
mdpopups.md2html
: 
    Exposes the markdown to html converter in case it is desired to parse only a section of markdown.  This works well for someone who wants to work directly in HTML, but might want to still syntax highlight some code to insert into the HTML.

    | Parameter | Required | Default | Description |
    | --------- | -------- | ------- | ----------- |
    | markup | Yes | | The markup code to be converted. |

## Global User Settings
All settings for `mdpopups` are placed in Sublime's `Preferences.sublime-settings`.

### mdpopups_debug
Turns on debug mode.  This will dump out all sorts of info to the console.  Such as content before parsing to HTML, final HTML output, etc.  This is more useful for plugin developers.

```js
    "mdpopups_debug": true,
```

### mdpopups_disable
Global kill switch to prevent popups (created by `mdpopups`) from appearing.

```js
    "mdpopups_disable": true,
```

### mdpopups_cache_refresh_time
Control how long a CSS theme file will be in the cache before being refreshed.  Value should be a positive integer greater than 0.  Units are in minutes.  Default is 30.

```js
    "mdpopups_cache_refresh_time": 30,
```

### mdpopups_cache_limit
Control how many CSS theme files will be kept in cache at any given time.  Value should be a positive integer greater than 0.

```js
    "mdpopups_cache_limit": 10
```

### mdpopups_theme_dark
Overrides the default dark theme.  Value should be a relative path pointing to the CSS theme file: `Packages/User/my_dark_theme.css`.  Slashes should be forward slashes.

### mdpopups_theme_light
Overrides the default light theme.  Value should be a relative path pointing to the CSS theme file: `Packages/User/my_light_theme.css`.  Slashes should be forward slashes.

### mdpopups_theme_map
If a specific CSS thee should be paired with a specific color scheme, you can define the mapping in the theme map.  You can specify as many pairings as desired.

```js
    "mdpopups_theme_map":
    {
        "Packages/Theme - Aprosopo/Tomorrow-Morning.tmTheme": "Packages/User/mod_light.css"
    },
```
