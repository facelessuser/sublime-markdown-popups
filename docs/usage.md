# User Guide {: .doctitle}
Using and configuring Sublime Markdown Popups.

---

## Dependencies
Your plugin must include the following Package Control dependencies:

```js
{
    "*": {
        ">=3080": [
            "pygments",
            "python-markdown",
            "mdpopups",
            "python-jinja2",
            "markupsafe"
        ]
    }
}
```

## Markdown Support
MdPopups uses [Python Markdown](https://pythonhosted.org/Markdown/) to parse Markdown and transform it into a tooltip.  The Markdown environment supports basic Markdown features, but also includes a number of specialty extensions to enhance the environment.  To keep the experience standardized for plugin use, tweaking the Markdown settings is not allowed.

MdPopups enables the following Python Markdown extensions:

- [attr_list](https://pythonhosted.org/Markdown/extensions/attr_list.html) allows you to add HTML attributes to block and inline elements easily.
- [nl2br](https://pythonhosted.org/Markdown/extensions/nl2br.html) turns new lines int `#!html <br>` tags.
- [def_list](https://pythonhosted.org/Markdown/extensions/definition_lists.html) adds support for definition lists.
- [admonition](https://pythonhosted.org/Markdown/extensions/admonition.html) provides admonition blocks.
- [codehilite](https://pythonhosted.org/Markdown/extensions/code_hilite.html) provides syntax highlighted blocks.

MdPopups also includes a couple 3rd party extensions (some of which have been modified to work better in the Sublime Text environment).

- [superfences](http://facelessuser.github.io/pymdown-extensions/extensions/superfences/) provides support for nested fenced blocks. UML support is disabled.
- [betterem](http://facelessuser.github.io/pymdown-extensions/extensions/betterem/) is extension that aims to improve emphasis support in Python Markdown. MdPopups leaves it configured in its default state where underscores are handled intelligently: `_handled_intelligently_` --> _handled_intelligently_.  Asterisks can be used to do mid word emphasis: `em*pha*sis` --> em*pha*sis.
- [magiclink](http://facelessuser.github.io/pymdown-extensions/extensions/magiclink/) auto links HTML links.
- [inlinehilite](http://facelessuser.github.io/pymdown-extensions/extensions/inlinehilite/) allows for inline code highlighting: `` `#!python import module` `` --> `#!python import module`.

## API Usage
MdPopups provides a handful of accessible functions.

### version
mdpopups.version
: 
    Get the version of the MdPopups library.  Returns a tuple of integers which represents the major, minor, and patch version.

### show_popup
mdpopups.show_popup
: 
    Accepts Markdown and creates a Sublime popup tooltip.  By default, the Pygments syntax highlighter will be used for code highlighting.  Set [`mdpopups.use_sublime_highlighter`](#mdpopupsuse_sublime_highlighter) to `true` in your `Preferences.sublime-settings` file if you would like to use the Sublime syntax highlighter.

    | Parameter | Type | Required | Default | Description |
    | --------- | ---- | -------- | ------- | ----------- |
    | view | sublime.View | Yes | | A Sublime Text view object. |
    | content | string | Yes | | Markdown/HTML content to be used to create a tooltip. |
    | md | bool | No | True | Defines whether the content is Markdown and needs to be converterted. |
    | css | string | No | None | Additional CSS that will be injected. |
    | flags | int | No | 0 | Flags to pass down to the Sublime Text `view.show_popup` call. |
    | location | int | No | -1 | Location to show popup in view.  -1 means to show right under the first cursor. |
    | max_width | int | No | 320 | Maximum width of the popup. |
    | max_height | int | No | 240 | Maximum height of the popup. |
    | on_navigate | function | No | None | Callback that receives one variable `href`. |
    | on_hide | function | No | None | Callback for when the tooltip is hidden. |

!!! caution "Developers Guidelines"
    If injecting your own CSS classes from a plugin, please namespace them by either giving them a very unique name (preferably with the plugin's name as part of the class) or use an additional namespace class (preferably with the plugin's name) and a specific class.  This way a user can target and override your class styling if desired.

    **Example - Unique Class Name**:
    ```css
    .myplugin-myclass { ... }
    ```

    **Example - Namespace Class**:
    ```css
    .myplugin.myclass { ... }
    ```

    Also, do not try to override the style of existing base classes and elements with plugin injection, but use custom plugin classes so that you will only target what your plugin as specifically added special classes to.


## update_popup
mdpopups.update_popup
: 
    Updates the current existing popup.  Set [`mdpopups.use_sublime_highlighter`](#mdpopupsuse_sublime_highlighter) to `true` in your `Preferences.sublime-settings` file if you would like to use the Sublime syntax highlighter.

    | Parameter | Type | Required | Default | Description |
    | --------- | ---- | -------- | ------- | ----------- |
    | view | sublime.View | Yes | | A Sublime Text view object. |
    | content | string | Yes | | Markdown/HTML content to be used to create a tooltip. |
    | md | bool | No | True | Defines whether the content is Markdown and needs to be converterted. |
    | css | string | No | None | CSS text that should be used instead of loading a theme. |

### hide_popup
mdpopups.hide_popup
: 
    Hides the current popup.  Included for convenience and consistency.

    | Parameter | Type | Required | Default | Description |
    | --------- | ---- | -------- | ------- | ----------- |
    | view | sublime.View | Yes | | A Sublime Text view object. |

### clear_cache
mdpopups.clear_cache
: 
    Clears the CSS theme related caches.

### md2html
mdpopups.md2html
: 
    Exposes the Markdown to HTML converter in case it is desired to parse only a section of markdown.  This works well for someone who wants to work directly in HTML, but might want to still have fragments of markdown that they would like to occasionally convert. Code highlighting will use either Pygments or the native Sublime syntax highlighter.  Set [`mdpopups.use_sublime_highlighter`](#mdpopupsuse_sublime_highlighter) to `true` if you want to use the Sublime syntax highlighter.

    | Parameter | Type | Required | Default | Description |
    | --------- | ---- | -------- | ------- | ----------- |
    | view | sublime.View |Yes | | Sublime text View object. |
    | markup | bool | Yes | | The markup code to be converted. |


### color_box
mdpopups.color_box
: 
    Generates a color preview box image encoded in base64 and formated to be inserted right in your your Markdown or HTML code as an `img` tag.

    | Parameter | Type | Required | Default | Description |
    | --------- | ---- | -------- | ------- | ----------- |
    | colors | [string] | Yes | | A list of color strings formatted as `#RRGGBBAA` where `R` is the red channel, `G` is the green channel, `B` is the blue channel, and `A` is the alpha channel. |
    | border | string | Yes | | The color for the color box border.  Input is a RGB color formatted as `#RRGGBB`. |
    | border2 | string | No | None | The optional secondary border color.  This is great if you are going to have it on a light and dark backgrounds.  You can use a double border so the color stands out regardless of the background.  Input is a RGB color formatted as `#RRGGBB`. |
    | height | int | No | 32 | Height of color box. |
    | width | int | No | 32 | Width of color box. |
    | border_size | int | No | 1 | Width of the color box border.  If using `border2`, the value should be set to at least 2 to see both colors. |
    | check_size | int | No | 4 | Size of checkered box squares used for the background of transparent colors. |
    | max_colors | int | No | 5 | Max number of colors that will be evaluated in the `colors` parameter.  Multiple colors are used to to create palette boxes showing multiple colors lined up horizontally. |
    | alpha | bool | No | False | Will create color box images with a real alpha channel instead of simulating one with a checkered background. |
    | border_map | int | No | 0xF | A mapping of which borders to show.  Where `0x1` is `TOP`, `0x2` is `LEFT`, `0x4` is `BOTTOM`, `0x8` is `RIGHT`.  Map flags can be accessed via `mdpopups.colorbox.TOP` etc. |

### syntax_highlight
mdpopups.syntax_highlight
: 
    Allows for syntax highlighting outside the Markdown environment.  You can just feed it code directly and give it the language of your choice, and you will be returned a block of HTML that has been syntax highlighted.  This does not have to be in markdown format.  Just give it plain text to convert to highlighted HTML. `syntax_highlight` will use either Pygments or the native Sublime syntax highlighter.  Set [`mdpopups.use_sublime_highlighter`](#mdpopupsuse_sublime_highlighter) to `true` if you want to use the Sublime syntax highlighter.

    | Parameter | Type |Required | Default | Description |
    | --------- | ---- | ------- | ------- | ----------- |
    | view | sublime.View | Yes | | Sublime text View object. |
    | src | string | Yes | | The source code to be converted.  No ` ``` ` needed. |
    | language | string | No | None | Specifies the language to highlight as. |
    | inline | bool |No | False | Will return the code formatted for inline display. |

## Global User Settings
All settings for `MdPopups` are placed in Sublime's `Preferences.sublime-settings`.  They are global and work no for whatever plugin uses the MdPopups API.

### mdpopups.debug
Turns on debug mode.  This will dump out all sorts of info to the console.  Such as content before parsing to HTML, final HTML output, etc.  This is more useful for plugin developers.

```js
    "mdpopups.debug": true,
```

### mdpopups.disable
Global kill switch to prevent popups (created by MdPopups) from appearing.

```js
    "mdpopups.disable": true,
```

### mdpopups.cache_refresh_time
Control how long a CSS theme file will be in the cache before being refreshed.  Value should be a positive integer greater than 0.  Units are in minutes.  Default is 30.

```js
    "mdpopups.cache_refresh_time": 30,
```

### mdpopups.cache_limit
Control how many CSS theme files will be kept in cache at any given time.  Value should be a positive integer greater than or equal to 0.

```js
    "mdpopups.cache_limit": 10
```

### mdpopups.use_sublime_highlighter
Controls whether the Pygments or the native Sublime syntax highlighter is used for code highlighting.  This affects code highlighting in Markdown conversion] via and when [md2html](#md2html) and when code is directly processed using [syntax_highlight](#syntax_highlight). To learn more about the syntax highlighter see [Syntax Highlighting](#syntax-highlighting).

```js
    "mdpopups.use_sublime_highlighter": true
```

### mdpopups.user_css
Overrides the default CSS theme.  Value should be a relative path pointing to the CSS theme file: `Packages/User/my_custom_theme.css`.  Slashes should be forward slashes. By default, it will point to `Packages/User/mdpopups.css`.

```js
    "mdpopups.use_sublime_highlighter": "Packages/User/mdpopups.css"
```

### mdpopups.sublime_user_lang_map
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

## Syntax Highlighting
MdPopups has two syntax highlighting methods: one is Pygments, the other is Sublimes native syntax highlighters.  When developing a plugin, it is wise to test out both as a syntax mapping may be needed for the Sublime Syntax Highlighter; mappings can be added locally and/or to the main repository via pull requests.

### Pygments
Pygments has a great variety of highlighters out of the box.  It also comes with a number of built-in color schemes that can be used.  Pygments themes are loaded up using the [CSS template](#css-templates).  You can either specify an existing one, paste your own in.  Due to the limitations of the Sublime HTML and CSS engine, you must format your personal Pygments them to work well.

Traditionally Pygments CSS classes are given not only syntax classes applied to each span, but an overall class as assigned to the div wrapper as well.  For instance, a class for whitespace may look like this (where `#!css .highlight` is the div wrapper's class and `#!css .w` i the span's class):

```css
.highlight .w { color: #cccccc } /* Text.Whitespace */
```

But the sublime CSS engine doesn't support parent and child classes like `#!css .highlight .w`; it supports either single or multiple classes on one element like `#!css .class1.class2`.  Because of this, the `#!css .highlight` class must be stripped out.

```css
.w { color: #cccccc } /* Text.Whitespace */
```

MdPopups also needs both classes `#!css .highlgiht` and `#!css .inline-highlight` to be styled with the foreground and background color:

```css
.highlight, .inline-highlight { background-color: #f8f8f8; color: #4d4d4c }
```

**Full Example**:

```css
.highlight, .inline-highlight { background-color: #f8f8f8; color: #4d4d4c }
.c { color: #8e908c; font-style: italic } /* Comment */
.err { color: #c82829 } /* Error */
.k { color: #8959a8; font-weight: bold } /* Keyword */
.l { color: #f5871f } /* Literal */
.n { color: #4d4d4c } /* Name */
.o { color: #3e999f } /* Operator */
.p { color: #4d4d4c } /* Punctuation */
.cm { color: #8e908c; font-style: italic } /* Comment.Multiline */
.cp { color: #8e908c; font-weight: bold } /* Comment.Preproc */
.c1 { color: #8e908c; font-style: italic } /* Comment.Single */
.cs { color: #8e908c; font-style: italic } /* Comment.Special */
.gd { color: #c82829 } /* Generic.Deleted */
.ge { font-style: italic } /* Generic.Emph */
.gh { color: #4d4d4c; font-weight: bold } /* Generic.Heading */
.gi { color: #718c00 } /* Generic.Inserted */
.gp { color: #8e908c; font-weight: bold } /* Generic.Prompt */
.gs { font-weight: bold } /* Generic.Strong */
.gu { color: #3e999f; font-weight: bold } /* Generic.Subheading */
.kc { color: #8959a8; font-weight: bold } /* Keyword.Constant */
.kd { color: #8959a8; font-weight: bold } /* Keyword.Declaration */
.kn { color: #8959a8; font-weight: bold } /* Keyword.Namespace */
.kp { color: #8959a8; font-weight: bold } /* Keyword.Pseudo */
.kr { color: #8959a8; font-weight: bold } /* Keyword.Reserved */
.kt { color: #eab700; font-weight: bold } /* Keyword.Type */
.ld { color: #718c00 } /* Literal.Date */
.m { color: #f5871f } /* Literal.Number */
.s { color: #718c00 } /* Literal.String */
.na { color: #4271ae } /* Name.Attribute */
.nb { color: #4271ae } /* Name.Builtin */
.nc { color: #c82829; font-weight: bold } /* Name.Class */
.no { color: #c82829 } /* Name.Constant */
.nd { color: #3e999f } /* Name.Decorator */
.ni { color: #4d4d4c } /* Name.Entity */
.ne { color: #c82829; font-weight: bold } /* Name.Exception */
.nf { color: #4271ae; font-weight: bold } /* Name.Function */
.nl { color: #4d4d4c } /* Name.Label */
.nn { color: #4d4d4c } /* Name.Namespace */
.nx { color: #4271ae } /* Name.Other */
.py { color: #4d4d4c } /* Name.Property */
.nt { color: #c82829 } /* Name.Tag */
.nv { color: #c82829 } /* Name.Variable */
.ow { color: #3e999f } /* Operator.Word */
.w { color: #4d4d4c } /* Text.Whitespace */
.mb { color: #f5871f } /* Literal.Number.Bin */
.mf { color: #f5871f } /* Literal.Number.Float */
.mh { color: #f5871f } /* Literal.Number.Hex */
.mi { color: #f5871f } /* Literal.Number.Integer */
.mo { color: #f5871f } /* Literal.Number.Oct */
.sb { color: #718c00 } /* Literal.String.Backtick */
.sc { color: #4d4d4c } /* Literal.String.Char */
.sd { color: #8e908c } /* Literal.String.Doc */
.s2 { color: #718c00 } /* Literal.String.Double */
.se { color: #f5871f } /* Literal.String.Escape */
.sh { color: #718c00 } /* Literal.String.Heredoc */
.si { color: #f5871f } /* Literal.String.Interpol */
.sx { color: #718c00 } /* Literal.String.Other */
.sr { color: #718c00 } /* Literal.String.Regex */
.s1 { color: #718c00 } /* Literal.String.Single */
.ss { color: #718c00 } /* Literal.String.Symbol */
.bp { color: #f5871f } /* Name.Builtin.Pseudo */
.vc { color: #c82829 } /* Name.Variable.Class */
.vg { color: #c82829 } /* Name.Variable.Global */
.vi { color: #c82829 } /* Name.Variable.Instance */
.il { color: #f5871f } /* Literal.Number.Integer.Long */
```

### Sublime Syntax Highlighter
MdPopups can also use Sublime's internal syntax highlighter to highlight your code.  The benefit here is that you get code highlighting in your popup that matches your current theme.  The highlighting ability is dependent upon what syntax packages you have installed in Sublime.  It also depends on whether they are enabled and mapped to a language keyword.  Pull requests are welcome to expand and keep the [language mapping](https://github.com/facelessuser/sublime-markdown-popups/blob/master/st3/mdpopups/st_mapping.py) updated.  You can also define in your `Preferences.sublime-settings` file additional mappings to either personal syntax files, or while waiting for your mapping changes to be merged and released.  See [`mdpopups.sublime_user_lang_map`](#mdpopupssublime_user_lang_map) for more info.

In your CSS template it is usually a good idea to generically specify the code wrapper background colors.  With the [CSS templates](#css-templates), this is very easy:

```css+jinja
.highlight, .inline-highlight { {{'.background'|css}} }
```

## CSS Styling
MdPopups was design to give a universal way of displaying and styling tooltips via plugins, but also provide the user an easy way to control the look.

MdPopups provides a simple base CSS that styles the basic HTML tags that can be used in the Markdown parser.  On top of that it then parses your current Sublime color scheme and generates CSS that includes styling for all the [standard TextMate scopes](./textmate_scopes.md) (and only those listed scopes) found in your color scheme.  It then uses those scopes via in a default template to highlight your tooltips to match your current color scheme.

Templates are used so that a user can easily tap into all the colors, color filters, and other usefull logic to control their tooltips in one place without having to hard code a specific CSS for a specific color scheme.  Even though a plugin can additionally insert new scopes on demand when calling the popup API, a user can override anything and everything by providing their own [CSS template](#mdpopupsuser_css).  The template is fairly powerful and flexible.

## CSS Templates
MdPoups provides a [`base.css`](https://github.com/facelessuser/sublime-markdown-popups/blob/master/css/base.css) that formats the general look of the HTML elements (padding, size, etc.).  On top of that, it provides a [`default.css`](https://github.com/facelessuser/sublime-markdown-popups/blob/master/css/default.css) template which applies more superficial styling such as colors, Pygments themes, etc.  It uses the Jinja2 template environment to give direct access to things like color scheme colors, names, and other useful information.  In general, `default.css` should provide most of what everyone **needs**.  But if you **want** greater control, you can create your own CSS template which MdPopups will use instead of `default.css`.

### Template Colors
With the template environment, colors from the current Sublime color scheme can be accessed and manipulated.  Access to the Sublime color scheme styles are done via the `css` filter.

css
: 
    Retrieves the style for a specific TextMate scope from a Sublime color scheme.  By specifying either `.foreground`, `.background`, or anyone of the standard TextMate scopes and then paring it with the `css` filter, all the related styles of the specified scope will be inserted into the css document.

    **Example**:

    This:

    ```css+jinja
    h1, h2, h3, h4, h5, h6 { {{'.comment'|css}} }
    ```

    Might become this:

    ```css+jinja
    h1, h2, h3, h4, h5, h6 { color: #888888, font-style: italic }
    ```

    If you need to get at a specific CSS attribute, you can specify its name in the `css` filter (available attributes are `color`, `background-color`, `font-style`, and `font-weight`).

    This:

    ```css+jinja
    h1, h2, h3, h4, h5, h6 { {{'.comment'|css('color')}} }
    ```

    Would then only include the color:

    ```css+jinja
    h1, h2, h3, h4, h5, h6 { color: #888888 }
    ```

    Some scopes might not have colors assigned to them, so multiple scopes can be defined, and the first one that matches will be used:

    ```css+jinja
    /* If `keyword.operator` is not explicitly used, fallback to `.keyword` */
    h1, h2, h3, h4, h5, h6 { {{'.keyword.operator, .keyword'|css('color')}} }
    ```

If desired you can convert a foreground color to a background color or vice versa.  To convert to a foreground color, you can use the `foreground` filter.  To convert to a background color, you can use the `background` filter.

foreground
: 
    Convert a background to a foreground.

    **Example**:
    ```css+jinja
    body { {{'.background'|css('background-color')|foreground}} }
    ```

background
: 
    Convert a foreground to a background.

    **Example**:
    ```css+jinja
    body { {{'.foreground'|css('color')|background}} }
    ```

### Template Color Filtering
MdPopups also provides a number of color filters within the template environment that can manipulate the colors.  For instance, lets say you had your tooltip is the same color as the view window and it is difficult to see where the tooltip starts and ends.  You can take the color schemes background and apply a brightness filter to it allowing you now see the tooltip clearly.

Here we can make the background of the tooltip darker:

```css+jinja
body { {{'.background'|css('background-color')|brightness(0.9)}} }
```

Color filters take a single color attribute of the form `key: value;`.  So when feeding the filter with CSS, it is advised to specify the attribute in the `css` filter to limit the return to only one attribute as shown above; it may be difficult to tell how many attributes `css` could return without explicitly specifying attribute.  Color filters only take either `color` or `background-color` attributes.

Filters can be chained if more intensity is needed as some filters may clamp the value in one call. Multiple kinds of filters can also be chained together.  These are all the available filters:

brightness
: 
    Shifts brightness either dark or lighter. Brightness is relative to 1 where 1 means no change.  Accepted values are floats that are greater than 0.  Ranges are clamped between 0 and 2.

    **Example - Darken**:
    ```css+jinja
    body { {{'.background'|css('background-color')|brightness(0.9)}} }
    ```

    **Example - Lighten**:
    ```css+jinja
    body { {{'.background'|css('background-color')|brightness(1.1)}} }
    ```

saturation
: 
    Shifts the saturation either to right (saturate) or the left (desaturate).  Saturation is relative to 1 where 1 means no change.  Accepted values are floats that are greater than 0.  Ranges are clamped between 0 and 2.

    **Example - Desaturate**:
    ```css+jinja
    body { {{'.background'|css('background-color')|saturation(0.9)}} }
    ```

    **Example - Saturate**:
    ```css+jinja
    body { {{'.background'|css('background-color')|saturation(1.1)}} }
    ```

grayscale
: 
    Filters all colors to a grayish tone.

    **Example**:
    ```css+jinja
    body { {{'.background'|css('background-color')|grayscale}} }
    ```

sepia
: 
    Filters all colors to a sepia tone.

    **Example**:
    ```css+jinja
    body { {{'.background'|css('background-color')|sepia}} }
    ```

invert
: 
    Inverts a color.

    **Example**:
    ```css+jinja
    body { {{'.background'|css('background-color')|invert}} }
    ```

colorize
: 
    Filters all colors to a shade of the specified hue.  Think grayscale, but instead of gray, you define a non-gray hue.  The values are angular dimensions starting at the red primary at 0°, passing through the green primary at 120° and the blue primary at 240°, and then wrapping back to red at 360°.

    **Example**:
    ```css+jinja
    body { {{'.background'|css('background-color')|colorize(30)}} }
    ```

hue
: 
    Shifts the current hue either to the left or right.  The values are angular dimensions starting at the red primary at 0°, passing through the green primary at 120° and the blue primary at 240°, and then wrapping back to red at 360°.  Values can either be negative to shift left or positive to shift the hue to the right.

    **Example - Left Shift**:
    ```css+jinja
    body { {{'.background'|css('background-color')|hue(-30)}} }
    ```

    **Example - Left Right**:
    ```css+jinja
    body { {{'.background'|css('background-color')|hue(30)}} }
    ```

fade
: 
    Fades a color. Essentially it is like apply transparency to the color allowing the color schemes base background color to show through.

    **Example - Fade 50%**:
    ```css+jinja
    body { {{'.foreground'|css('color')|fade(0.5)}} }
    ```

### Include CSS
The template environment allows for retrieving built-in Pygments CSS or retrieving CSS resources from the Sublime Packages.

pygments
: 
    Retrieve a built-in Pygments color scheme.

    **Example**:
    ```css+jinja
    {{'native'|pygments}}
    ```

getcss
: 
    Retrieve a CSS file from Sublime's `Packages` folder.  CSS retrieved in this manner can include template variables and filters.

    **Example**:
    ```css+jinja
    {{'Packages/User/aprosopo-dark.css'|getcss}}
    ```

## Template Variables
The template environment provides a couple of variables that can be used to conditionally alter the CSS output.  Variables are found under `var`.

var.is_dark | var.is_light
: 
    `is_dark` checks if the color scheme is a dark color scheme.  Alternatively, `is_light` checks if the color scheme is a light color scheme.

    **Example**:
    ```css+jinja
    {% if var.is_light %}
    html{ {{'.background'|css('background-color')|brightness(0.9)}} }
    {% else %}
    html{ {{'.background'|css('background-color')|brightness(1.1)}} }
    {% endif %}
    ```

var.use_pygments
: 
    Checks if the Pygments syntax highlighter is being used.

    **Example**:
    ```css+jinja
    {% if var.use_pygments %}
    {% if var.is_light %}
    {{'default'|pygments}}
    {% else %}
    {{'native'|pygments}}
    {% endif %}
    {% endif %}
    ```

var.color_scheme
: 
    Retrieves the current color schemes name.

    **Example**:
    ```css+jinja
    {% if (
        var.color_scheme in (
            'Packages/Theme - Aprosopo/Tomorrow-Night-Eighties-Stormy.tmTheme',
            'Packages/Theme - Aprosopo/Tomorrow-Morning.tmTheme',
        )
    ) %}
    a { {{'.keyword.operator'|css('color')}} }
    {% else %}
    a { {{'.support.function'|css('color')}} }
    {% endif %}
    ```
