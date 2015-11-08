# User Guide {: .doctitle}
Using and configuring Sublime Markdown Popups.

---

## Dependencies
Your plugin must include the following Package Control dependencies:

```js
{
    "*": {
        ">=3000": [
            "pygments",
            "markdown",
            "mdpopups",
            "jinja2",
            "markupsafe"
        ]
    }
}
```

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
    | css | No | None | Additional CSS that will be injected. |
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

### hide_popup
mdpopups.hide_popup
: 
    Hides the current popup.  Included for convenience and consistency.

    | Parameter | Required | Default | Description |
    | --------- | -------- | ------- | ----------- |
    | view | Yes | | A Sublime Text view object. |

### clear_cache
mdpopups.clear_cache
: 
    Clears the CSS theme related caches.

### md2html
mdpopups.md2html
: 
    Exposes the Markdown to HTML converter in case it is desired to parse only a section of markdown.  This works well for someone who wants to work directly in HTML, but might want to still syntax highlight some code to insert into the HTML.

    | Parameter | Required | Default | Description |
    | --------- | -------- | ------- | ----------- |
    | markup | Yes | | The markup code to be converted. |

### syntax_highlight
mdpopups.syntax_highlight
: 
    Allows for syntax highlighting outside the Markdown environment.  You can just feed it code directly and give it the language of choice, and you will be returned a block of HTML that has been syntax highlighted.

    | Parameter | Required | Default | Description |
    | --------- | -------- | ------- | ----------- |
    | markup | Yes | | The markup code to be converted. |
    | lang | No | None | Specifies the language to highlight as. |
    | guess_lang | No | False | If the language passed in does not render, or no language is passed at all, Pygments will attempt to guess the language. |
    | inline | No | False | Will return the code formatted for inline display. |

## Global User Settings
All settings for `mdpopups` are placed in Sublime's `Preferences.sublime-settings`.  They are global and work no for whatever plugin uses the `mdpopups` API.

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
Control how many CSS theme files will be kept in cache at any given time.  Value should be a positive integer greater than or equal to 0.

```js
    "mdpopups_cache_limit": 10
```

### mdpopups_user_css
Overrides the default CSS theme.  Value should be a relative path pointing to the CSS theme file: `Packages/User/my_custom_theme.css`.  Slashes should be forward slashes. By default, it will point to `Packages/User/mdpopups.css`.

## CSS Styling
`mdpopups` was design to give a universal way of displaying and styling tooltips via plugins, but also provide the user an easy way to control the look.

`mdpopups` provides a simple base CSS that styles the basic HTML tags that can be used in the Markdown parser.  On top of that it then parses your current Sublime color scheme and generates CSS that includes styling for all the [standard TextMate scopes](https://manual.macromates.com/en/language_grammars#naming_conventions) (and only those listed scopes) found in your color scheme.  It then uses those scopes via in a default template to highlight your tooltips to match your current color scheme.

Templates are used so that a user can easily tap into all the colors, color filters, and other usefull logic to control their tooltips in one place without having to hard code a specific CSS for a specific color scheme.  Even though a plugin can additionally insert new scopes on demand when calling the popup API, a user can override anything and everything by providing their own [CSS template](#mdpopups_user_css).  The template is fairly powerful and flexible.

### CSS Templates

!!! caution "Under Construction"
    Currently under construction.
