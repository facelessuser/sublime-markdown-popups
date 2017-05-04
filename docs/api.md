## Dependencies

Your plugin must include the Package Control dependencies listed below. Please read about Package Control's [dependencies][pc-dependencies] to learn more.

```js
{
    "*": {
        ">=3124": [
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

MdPopups uses [Python Markdown][pymd] to parse Markdown and transform it into a popup or phantom (HTML embedded in your file view).  The Markdown environment supports basic Markdown features, but also includes a number of specialty extensions to enhance the environment.  To keep the experience standardized for plugin use, tweaking the Markdown settings is not allowed except for a few things like enabling/disabling `nl2br` etc.

MdPopups includes the following Python Markdown extensions, but some of the features may not be used due to the limitations of Sublime's `minihtml`.

- [attr_list](https://pythonhosted.org/Markdown/extensions/attr_list.html) allows you to add HTML attributes to block and inline elements easily.
- [nl2br](https://pythonhosted.org/Markdown/extensions/nl2br.html) turns new lines into `#!html <br>` tags.
- [def_list](https://pythonhosted.org/Markdown/extensions/definition_lists.html) adds support for definition lists.
- [admonition](https://pythonhosted.org/Markdown/extensions/admonition.html) provides admonition blocks.

MdPopups also includes a couple of 3rd party extensions (some of which have been modified to work better in the Sublime Text environment).

- [superfences](http://facelessuser.github.io/pymdown-extensions/extensions/superfences/) provides support for nested fenced blocks.
- [betterem](http://facelessuser.github.io/pymdown-extensions/extensions/betterem/) is an extension that aims to improve emphasis support in Python Markdown. MdPopups leaves it configured in its default state where underscores are handled intelligently: `_handled_intelligently_` --> _handled_intelligently_ and asterisks can be used to do mid word emphasis: `em*pha*sis` --> em*pha*sis.
- [magiclink](http://facelessuser.github.io/pymdown-extensions/extensions/magiclink/) auto links HTML links.
- [inlinehilite](http://facelessuser.github.io/pymdown-extensions/extensions/inlinehilite/) allows for inline code highlighting: `` `#!python import module` `` --> `#!python import module`.
- [extrarawhtml](http://facelessuser.github.io/pymdown-extensions/extensions/extrarawhtml/) allows you to add `markdown="1"` to block HTML elements to allow content under them to be parsed with Python markdown (inline tags should already have their content parsed).  All this module does is expose this specific functionality from the [Python Markdown's Extra extension](https://pythonhosted.org/Markdown/extensions/extra.html#nested-markdown-inside-html-blocks) as this functionality could not be enabled without including all of the `Extra` extensions other features.  You can read the Python Markdown's Extra extension documentation to learn more about this feature.
- [highlight](http://facelessuser.github.io/pymdown-extensions/extensions/highlight/) controls and configures the highlighting of code blocks.

## Styling

Popups and phantoms are styled with CSS that is fed through the Jinja2 template engine. A default CSS is provided that styles commonly used elements. Plugins can provide CSS to add additional styling for plugin specific purposes. See [CSS Styling](./styling.md) for more info on using the template engine and general styling info.

Plugin developers should avoid overriding the style of existing base classes and elements with plugin injection, but they should use custom plugin classes so that only the specific special elements that must be handled uniquely for the plugin get targeted.  You should use very unique class names (preferably with the plugin's name as part of the class). This way a user can target and override your class styling if desired. There are a couple of ways to approach this.

- It is advised to use the `wrapper_class` option of the `show_popup`, `update_popup`, and `add_phantom` commands to wrap your content in a div with the provided class.  That way the developer can provide CSS to style their specific elements via `#!css .mdpopups .myplugin-wrapper .myclass {}` or simply `#!css .myplugin-wrapper .myclass {}`. This is one of the easiest ways.

- To add classes to inline and some block markdown elements you can use the Python Markdown [attr_list extension syntax](https://pythonhosted.org/Markdown/extensions/attr_list.html).  This will work on inline elements and a number of block elements (though sometimes it can be difficult to target certain kinds of block elements). If all else fails, you can insert raw HTML into your markdown and apply classes directly to the element.

## API Usage

MdPopups provides a number of accessible functions.

### Version

`(int,) mdpopups.version`
: 
    Returns the version of the MdPopups library.  Returns a tuple of integers which represents the major, minor, and patch version.

### Show Popup

`mdpopups.show_popup`
: 
    Accepts Markdown and creates a Sublime popup tooltip.  By default, the built in Sublime syntax highlighter will be used for code highlighting.  Set [`mdpopups.use_sublime_highlighter`](#mdpopupsuse_sublime_highlighter) to `false` in your `Preferences.sublime-settings` file if you would like to use the Pygments syntax highlighter (some setup is required).

    Parameter              | Type                | Required | Default      | Description
    ---------------------- | ------------------- | -------- | ------------ | -----------
    `view`                 | `#!py sublime.View` | Yes      |              | A Sublime Text view object.
    `content`              | `#!py str`          | Yes      |              | Markdown/HTML content to be used to create a tooltip.
    `md`                   | `#!py bool`         | No       | `#!py True`  | Defines whether the content is Markdown and needs to be converted.
    `css`                  | `#!py str`          | No       | `#!py None`  | Additional CSS that will be injected.
    `flags`                | `#!py int`          | No       | `#!py 0`     | Flags to pass down to the Sublime Text `view.show_popup` call.
    `location`             | `#!py int`          | No       | `#!py -1`    | Location to show popup in view.  -1 means to show right under the first cursor.
    `max_width`            | `#!py int`          | No       | `#!py 320`   | Maximum width of the popup.
    `max_height`           | `#!py int`          | No       | `#!py 240`   | Maximum height of the popup.
    `on_navigate`          | `#!py def fn()`     | No       | `#!py None`  | Callback that receives one variable `href`.
    `on_hide`              | `#!py def fn()`     | No       | `#!py None`  | Callback for when the tooltip is hidden.
    `wrapper_class`        | `#!py str`       | No       | `#!py None`  | A string containing the class name you wish wrap your content in.  A `div` will be created with the given class.
    `template_vars`        | `#!py dict`         | No       | `#!py None`  | A dictionary containing template vars.  These can be used in either the CSS or the HTML/Markdown content.
    `template_env_options` | `#!py dict`         | No       | `#!py None`  | A dictionary containing options for the Jinja2 template environment. This **only** applies to the **HTML/Markdown** content. Content plugin vars are found under the object: `plugin`.
    `nl2br`                | `#!py bool`         | No       | `#!py True`  | Determines whether the newline to br Python Markdown extension is enabled or not.
    `allow_code_wrap`      | `#!py bool`         | No       | `#!py False` | Do not convert all the spaces in code blocks to `nbsp` so that wrapping can occur.

### Update Popup

`mdpopups.update_popup`
: 
    Updates the current existing popup.

    Parameter              | Type                | Required | Default      | Description
    ---------------------- | ------------------- | -------- | ------------ | -----------
    `view`                 | `#!py sublime.View` | Yes      |              | A Sublime Text view object.
    `content`              | `#!py str`          | Yes      |              | Markdown/HTML content to be used to create a tooltip.
    `md`                   | `#!py bool`         | No       | `#!py True`  | Defines whether the content is Markdown and needs to be converterted.
    `css`                  | `#!py str`          | No       | `#!py None`  | CSS text that should be used instead of loading a theme.
    `wrapper_class`        | `#!py str`          | No       | `#!py None`  | A string containing the class name you wish wrap your content in.  A `div` will be created with the given class.
    `template_vars`        | `#!py dict`         | No       | `#!py None`  | A dictionary containing template vars.  These can be used in either the CSS or the HTML/Markdown content.
    `template_env_options` | `#!py dict`         | No       | `#!py None`  | A dictionary containing options for the Jinja2 template environment. This **only** applies to the **HTML/Markdown** content. Content plugin vars are found under the object: `plugin`.
    `nl2br`                | `#!py bool`         | No       | `#!py True`  | Determines whether the newline to br Python Markdown extension is enabled or not.
    `allow_code_wrap`      | `#!py bool`         | No       | `#!py False` | Do not convert all the spaces in code blocks to `nbsp` so that wrapping can occur.

### Hide Popup

`mdpopups.hide_popup`
: 
    Hides the current popup.  Included for convenience and consistency.

    Parameter | Type                | Required | Default | Description
    --------- | ------------------- | -------- | ------- | -----------
    `view`    | `#!py sublime.View` | Yes      |         | A Sublime Text view object.


### Is Popup Visible

`bool mdpopups.is_popup_visible`
: 
    Checks if popup is visible in the view. Included for convenience and consistency.

    Parameter | Type                | Required | Default | Description
    --------- | ------------------- | -------- | ------- | -----------
    `view`    | `#!py sublime.View` | Yes      |         | A Sublime Text view object.

### Add Phantom

`int mdpopups.add_phantom`
: 
    Adds a phantom (embedded HTML in the file view) and returns the phantom id.  Returns an integer.
    Accepts Markdown and creates a Sublime phantom (embedded HTML in the file view). By default, the built in Sublime syntax highlighter will be used for code highlighting. Set [`mdpopups.use_sublime_highlighter`](#mdpopupsuse_sublime_highlighter) to `false` in your `Preferences.sublime-settings` file if you would like to use the Pygments syntax highlighter (some setup is required).

    Parameter              | Type                  | Required | Default     | Description
    ---------------------- | --------------------- | -------- | ----------- | -----------
    `view`                 | `#!py sublime.View`   | Yes      |             | A Sublime Text view object.
    `key`                  | `#!py str`            | Yes      |             | A key that is associated with the given phantom.  Multiple phantoms can share the same key, but each phantom will have its own id.
    `region`               | `#!py sublime.Region` | Yes      |             | Region in the view where the phantom should be inserted.
    `content`              | `#!py str`            | Yes      |             | Markdown/HTML content to be used to create a phantom.
    `layout`               | `#!py int`            | Yes      |             | How the HTML content should be inserted.  Acceptable values are: `sublime.LAYOUT_INLINE`, `sublime.LAYOUT_BLOCK`, and `sublime.LAYOUT_BELOW`.
    `md`                   | `#!py bool`           | No       | `#!py True` | Defines whether the content is Markdown and needs to be converterted.
    `css`                  | `#!py str`            | No       | `#!py None` | Additional CSS that will be injected.
    `on_navigate`          | `#!py def fn()`       | No       | `#!py None` | Callback that receives one variable `href`.
    `wrapper_class`        | `#!py str`            | No       | `#!py None` | A string containing the class name you wish wrap your content in.  A `div` will be created with the given class.
    `template_vars`        | `#!py dict`           | No       | `#!py None` | A dictionary containing template vars.  These can be used in either the CSS or the HTML/Markdown content.
    `template_env_options` | `#!py dict`           | No       | `#!py None` | A dictionary containing options for the Jinja2 template environment. This **only** applies to the **HTML/Markdown** content. Content plugin vars are found under the object: `plugin`.
    `nl2br`                | `#!py bool`           | No       | `#!py True` | Determines whether the newline to br Python Markdown extension is enabled or not.
    `allow_code_wrap`      | `#!py bool`           | No       | `#!py False` | Do not convert all the spaces in code blocks to `nbsp` so that wrapping can occur.

### Erase Phantoms

`mdpopups.erase_phantoms`
: 
    Erase all phantoms associated to the given key.  Included for convenience and consistency.

    Parameter | Type                | Required | Default | Description
    --------- | ------------------- | -------- | ------- | -----------
    `view`    | `#!py sublime.View` | Yes      |         | A Sublime Text view object.
    `key`     | `#!py str`          | Yes      |         | A key that is associated with phantoms.  Multiple phantoms can share the same key, but each phantom will have its own id.

### Erase Phantom by ID

`mdpopups.erase_phantom_by_id`
: 
    Erase a single phantom by passing its id.  Included for convenience and consistency.

    Parameter   | Type                | Required | Default | Description
    ----------- | ------------------- | -------- | ------- | -----------
    `view`      | `#!py sublime.View` | Yes      |         | A Sublime Text view object.
    `pid`       | `#!py str`          | Yes      |         | The id associated with a single phantom.  Multiple phantoms can share the same key, but each phantom will have its own id.

### Query Phantom

`[sublime.Region] mdpopups.query_phantom`
: 
    Query the location of a phantom by specifying its id.  A list of `sublime.Region`s will be returned.  If the phantom with the given id is not found, the region will be returned with positions of `(-1, -1)`.  Included for convenience and consistency.

    Parameter | Type                | Required | Default | Description
    --------- | ------------------- | -------- | ------- | -----------
    `view`    | `#!py sublime.View` | Yes      |         | A Sublime Text view object.
    `pid`     | `#!py int`          | Yes      |         | The id associated with a single phantom.  Multiple phantoms can share the same key, but each phantom will have its own id.

### Query Phantoms

`[sublime.Region] mdpopups.query_phantoms`
: 
    Query the location of multiple phantoms by specifying their ids.  A list of `sublime.Region`s will be returned where each index corresponds to the index of ids that was passed in.  If a given phantom id is not found, that region will be returned with positions of `(-1, -1)`.  Included for convenience and consistency.

    Parameter | Type                | Required | Default | Description
    --------- | ------------------- | -------- | ------- | -----------
    `view`    | `#!py sublime.View` | Yes      |         | A Sublime Text view object.
    `pids`    | `#!py [int]`        | Yes      |         | The id associated with a single phantom.  Multiple phantoms can share the same key, but each phantom will have its own id.

### Phantom Class

`mdpopups.Phantoms`
: 
    A phantom object for use with [PhantomSet](#phantomset-class).

    Parameter              | Type                  | Required | Default      | Description
    ---------------------- | --------------------- | -------- | ------------ | -----------
    `region`               | `#!py sublime.Region` | Yes      |              | Region in the view where the phantom should be inserted.
    `content`              | `#!py str`            | Yes      |              | Markdown/HTML content to be used to create a phantom.
    `layout`               | `#!py int`            | Yes      |              | How the HTML content should be inserted.  Acceptable values are: `sublime.LAYOUT_INLINE`, `sublime.LAYOUT_BLOCK`, and `sublime.LAYOUT_BELOW`.
    `md`                   | `#!py bool`           | No       | `#!py True`  | Defines whether the content is Markdown and needs to be converterted.
    `css`                  | `#!py str`            | No       | `#!py None`  | Additional CSS that will be injected.
    `on_navigate`          | `#!py def fn()`       | No       | `#!py None`  | Callback that receives one variable `href`.
    `wrapper_class`        | `#!py str`            | No       | `#!py None`  | A string containing the class name you wish wrap your content in.  A `div` will be created with the given class.
    `template_vars`        | `#!py dict`           | No       | `#!py None`  | A dictionary containing template vars.  These can be used in either the CSS or the HTML/Markdown content.
    `template_env_options` | `#!py dict`           | No       | `#!py None`  | A dictionary containing options for the Jinja2 template environment. This **only** applies to the **HTML/Markdown** content. Content plugin vars are found under the object: `plugin`.
    `nl2br`                | `#!py bool`           | No       | `#!py True`  | Determines whether the newline to br Python Markdown extension is enabled or not.
    `allow_code_wrap`      | `#!py bool`           | No       | `#!py False` | Do not convert all the spaces in code blocks to `nbsp` so that wrapping can occur.

    **Attributes**

    Attribute              | Type                  | Description
    ---------------------- | --------------------- | -----------
    `region`               | `#!py sublime.Region` | Region in the view where the phantom should be inserted.
    `content`              | `#!py str`            | Markdown/HTML content to be used to create a phantom.
    `layout`               | `#!py int`            | How the HTML content should be inserted.  Acceptable values are: `sublime.LAYOUT_INLINE`, `sublime.LAYOUT_BLOCK`, and `sublime.LAYOUT_BELOW`.
    `md`                   | `#!py bool`           | Defines whether the content is Markdown and needs to be converterted.
    `css`                  | `#!py str`            | Additional CSS that will be injected.
    `on_navigate`          | `#!py def fn()`       | Callback that receives one variable `href`.
    `wrapper_class`        | `#!py str`            | A string containing the class name you wish wrap your content in.  A `div` will be created with the given class.
    `template_vars`        | `#!py dict`           | A dictionary containing template vars.  These can be used in either the CSS or the HTML/Markdown content.
    `template_env_options` | `#!py dict`           | A dictionary containing options for the Jinja2 template environment. This **only** applies to the **HTML/Markdown** content. Content plugin vars are found under the object: `plugin`.
    `nl2br`                | `#!py bool`           | Determines whether the newline to br Python Markdown extension is enabled or not.
    `allow_code_wrap`      | `#!py bool`           | No       | `#!py False` | Do not convert all the spaces in code blocks to `nbsp` so that wrapping can occur.

### Phantom Set Class

`mdpopups.PhantomSet`
: 
    A class that allows you to update phantoms under the specified key.

    Parameter | Type                | Required | Default | Description
    --------- | ------------------- | -------- | ------- | -----------
    `view`    | `#!py sublime.View` | Yes      |         | A Sublime Text view object.
    `key`     | `#!py str`          | Yes      |         | The key that should be associated with all related phantoms in the set.

    **Methods**

    `mdpopups.PhantomSet.update`
    : 
        Update all the phantoms in the set with the given phantom list.

        Parameter      | Type                                        | Required | Default | Description
        -------------- | ------------------------------------------- | -------- | ------- | -----------
        `new_phantoms` | [`#!py [mdpopups.Phantom]`](#class-phantom) | Yes      |         | A list of mdpopup phantoms. `sublime.Phantom` will be converted to `mdpopups.Phantom`.

### Clear Cache

`mdpopups.clear_cache`
: 
    Clears the CSS theme related caches.

### Markdown to HTML

`mdpopups.md2html`
: 
    Exposes the Markdown to HTML converter in case it is desired to parse only a section of markdown.  This works well for someone who wants to work directly in HTML, but might want to still have fragments of markdown that they would like to occasionally convert.

    By default, the built in Sublime syntax highlighter will be used for code highlighting. Set [`mdpopups.use_sublime_highlighter`](#mdpopupsuse_sublime_highlighter) to `false` in your `Preferences.sublime-settings` file if you would like to use the Pygments syntax highlighter (some setup is required).

    Parameter              | Type                | Required | Default      | Description
    ---------------------- | ------------------- | -------- | ------------ | -----------
    `view`                 | `#!py sublime.View` | Yes      |              | Sublime text View object.
    `markup`               | `#!py string`       | Yes      |              | The markup code to be converted.
    `template_vars`        | `#!py dict`         | No       | `#!py None`  | A dictionary containing template vars.  These can be used in either the CSS or the HTML/Markdown content.
    `template_env_options` | `#!py dict`         | No       | `#!py None`  | A dictionary containing options for the Jinja2 template environment. This **only** applies to the **HTML/Markdown** content. Content plugin vars are found under the object: `plugin`.
    `nl2br`                | `#!py bool`         | No       | `#!py True`  | Determines whether the newline to br Python Markdown extension is enabled or not.
    `allow_code_wrap`      | `#!py bool`         | No       | `#!py False` | Do not convert all the spaces in code blocks to `nbsp` so that wrapping can occur.

### Color Box

`string mdpopups.color_box`
: 
    Generates a color preview box image encoded in base64 and formated to be inserted right in your your Markdown or HTML code as an `img` tag.

    Parameter     | Type         | Required | Default | Description
    ------------- | ------------ | -------- | ------- | -----------
    `colors`      | `#!py [str]` | Yes      |         | A list of color strings formatted as `#RRGGBBAA` where `R` is the red channel, `G` is the green channel, `B` is the blue channel, and `A` is the alpha channel.
    `border`      | `#!py str`   | Yes      |         | The color for the color box border.  Input is a RGB color formatted as `#RRGGBB`.
    `border2`     | `#!py str`   | No       | `#!py None`  | The optional secondary border color.  This is great if you are going to have it on a light and dark backgrounds.  You can use a double border so the color stands out regardless of the background.  Input is a RGB color formatted as `#RRGGBB`.
    `height`      | `#!py int`   | No       | `#!py 32`    | Height of color box.
    `width`       | `#!py int`   | No       | `#!py 32`    | Width of color box.
    `border_size` | `#!py int`   | No       | `#!py 1`     | Width of the color box border.  If using `border2`, the value should be set to at least 2 to see both colors.
    `check_size`  | `#!py int`   | No       | `#!py 4`     | Size of checkered box squares used for the background of transparent colors.
    `max_colors`  | `#!py int`   | No       | `#!py 5`     | Max number of colors that will be evaluated in the `colors` parameter.  Multiple colors are used to to create palette boxes showing multiple colors lined up horizontally.
    `alpha`       | `#!py bool`  | No       | `#!py False` | Will create color box images with a real alpha channel instead of simulating one with a checkered background.
    `border_map`  | `#!py int`   | No       | `#!py 0xF`   | A mapping of which borders to show.  Where `0x1` is `TOP`, `0x2` is `LEFT`, `0x4` is `BOTTOM`, `0x8` is `RIGHT`.  Map flags can be accessed via `mdpopups.colorbox.TOP` etc.

### Color Box Raw

`bytes mdpopups.color_box`
: 
    Generates a color preview box image and returns the raw byte string of the image.

    Parameter     | Type         | Required | Default      | Description
    ------------- | ------------ | -------- | ------------ | -----------
    `colors`      | `#!py [str]` | Yes      |              | A list of color strings formatted as `#RRGGBBAA` where `R` is the red channel, `G` is the green channel, `B` is the blue channel, and `A` is the alpha channel.
    `border`      | `#!py str`   | Yes      |              | The color for the color box border.  Input is a RGB color formatted as `#RRGGBB`.
    `border2`     | `#!py str`   | No       | `#!py None`  | The optional secondary border color.  This is great if you are going to have it on a light and dark backgrounds.  You can use a double border so the color stands out regardless of the background.  Input is a RGB color formatted as `#RRGGBB`.
    `height`      | `#!py int`   | No       | `#!py 32`    | Height of color box.
    `width`       | `#!py int`   | No       | `#!py 32`    | Width of color box.
    `border_size` | `#!py int`   | No       | `#!py 1`     | Width of the color box border.  If using `border2`, the value should be set to at least 2 to see both colors.
    `check_size`  | `#!py int`   | No       | `#!py 4`     | Size of checkered box squares used for the background of transparent colors.
    `max_colors`  | `#!py int`   | No       | `#!py 5`     | Max number of colors that will be evaluated in the `colors` parameter.  Multiple colors are used to to create palette boxes showing multiple colors lined up horizontally.
    `alpha`       | `#!py bool`  | No       | `#!py False` | Will create color box images with a real alpha channel instead of simulating one with a checkered background.
    `border_map`  | `#!py int`   | No       | `#!py 0xF`   | A mapping of which borders to show.  Where `0x1` is `TOP`, `0x2` is `LEFT`, `0x4` is `BOTTOM`, `0x8` is `RIGHT`.  Map flags can be accessed via `mdpopups.colorbox.TOP` etc.

### Tint

`string mdpopups.tint`
: 
    Takes a either a path to an png or a byte string of a png and tints it with a specific color and returns a string containing the base64 encoded png in an HTML element.

    Parameter | Type             | Required | Default     | Description
    --------- | ---------------- | -------- | ----------- | -----------
    `img`     | `#!py str/bytes` | Yes      |             | Either a string in the form `Packages/Package/resource.png` or a byte string of a png image.
    `color`   | `#!py str`       | Yes      |             | A string in the form of `#RRGGBB` or `#RRGGBBAA` (alpha layer will be stripped and ignored and is only allowed to make it easy to pass in colors from a color scheme).
    `opacity` | `#!py int`       | No       | `#!py 255`  | An integer value between 0 - 255 that specifies the opacity of the tint.
    `height`  | `#!py int`       | No       | `#!py None` | Height that should be specified in the return HTML element.
    `width`   | `#!py int`       | No       | `#!py None` | Width that should be specified in the return HTML element.

### Tint Raw

`bytes mdpopups.tint_raw`
: 
    Takes a either a path to an png or a byte string of a png and tints it with a specific color and returns a byte string of the modified png.

    Parameter | Type             | Required | Default    | Description
    --------- | ---------------- | -------- | ---------- | -----------
    `img`     | `#!py str/bytes` | Yes      |            | Either a string in the form `Packages/Package/resource.png` or a byte string of a png image.
    `color`   | `#!py str`       | Yes      |            | A string in the form of `#RRGGBB` or `#RRGGBBAA` (alpha layer will be stripped and ignored and is only allowed to make it easy to pass in colors from a color scheme).
    `opacity` | `#!py int`       | No       | `#!py 255` | An integer value between 0 - 255 that specifies the opacity of the tint.

### Scope to Style

`dict mdpopups.scope2style`
: 
    Takes a sublime scope (complexity doesn't matter), and guesses the style that would be applied.  While there may be untested corner cases with complex scopes where it fails, in general, it is usually accurate.  The returned dictionary is in the form:

    ```py
    {
        # Colors will be None if not found,
        # though usually, even if the scope has no color
        # it will return the overall theme foreground.
        #
        # Background might be None if using `explicit_background`
        # as it only returns a background if that style specifically
        # defines a background.
        "color": "#RRGGBB",
        "background": "#RRGGBB",
        # Style will usually be either 'bold', 'italic'.
        # Multiple styles may be returned 'bold italic' or an empty string ''.
        "style": 'bold italic'
    }
    ```

    Parameter             | Type                | Required | Default      | Description
    --------------------- | ------------------- | -------- | ------------ | -----------
    `view`                | `#!py sublime.View` | Yes      |              | Sublime text View object so that the correct color scheme will be searched.
    `scope`               | `#!py string`       | Yes      |              | The scope to search for.
    `selected`            | `#!py bool`         | No       | `#!py False` | Whether this scope is in a selected state (selected text).
    `explicit_background` | `#!py bool`         | No       | `#!py False` | Only return a background if one is explicitly defined in the color scheme.

### Syntax Highlight

`mdpopups.syntax_highlight`
: 
    Allows for syntax highlighting outside the Markdown environment.  You can just feed it code directly and give it the language of your choice, and you will be returned a block of HTML that has been syntax highlighted.

    By default, the built in Sublime syntax highlighter will be used for code highlighting. Set [`mdpopups.use_sublime_highlighter`](#mdpopupsuse_sublime_highlighter) to `false` in your `Preferences.sublime-settings` file if you would like to use the Pygments syntax highlighter (some setup is required).

    Parameter         | Type                | Required | Default      | Description
    ----------------- | ------------------- | -------- | ------------ | -----------
    `view`            | `#!py sublime.View` | Yes      |              | Sublime text View object.
    `src`             | `#!py str`          | Yes      |              | The source code to be converted.  No ` ``` ` needed.
    `language`        | `#!py str`          | No       | `#!py None`  | Specifies the language to highlight as.
    `inline`          | `#!py bool`         | No       | `#!py False` | Will return the code formatted for inline display.
    `allow_code_wrap` | `#!py bool`         | No       | `#!py False` | Do not convert all the spaces in code blocks to `nbsp` so that wrapping can occur.

### Get Language From View

`mdpopups.get_language_from_view`
: 
    Allows a user to extract the equivalent language specifier for `mdpopups.syntax_highlight` from a view.  If the language cannot be determined, `None` will be returned.

    Parameter | Type                | Required | Default | Description
    --------- | ------------------- | -------- | ------- | -----------
    `view`    | `#!py sublime.View` | Yes      |         | Sublime text View object.

--8<-- "refs.md"
