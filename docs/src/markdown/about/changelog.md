# Changelog

## 5.1.0

-   **NEW**: Update Marko.
-   **NEW**: Update Pymdown Extensions.
-   **NEW**: Update ColorAide.

## 5.0.3

-   **FIX**: Fix lint issues.
-   **FIX**: Make maintenance easier by moving adjusted import logic for Markdown plugins up into MdPopups main code
    instead of keeping the modifications in the bundled libraries.
-   **CHORE**: Move to wheel releases.

## 5.0.2

-   **FIX**: Provide workaround Sublime quirk when rendering `<li>` tags that start with non-function newlines in.
    This targets the Marko parser specifically.

## 5.0.1

-   **FIX**: Fix some cases where code wrap wasn't respected.

## 5.0.0

-   **NEW**: Update internal, bundled libraries to the latest version.
-   **NEW**: Tweaks to default style.
-   **NEW**: Use default admonition classes that align with GitHub callouts: `note`, `tip`, `warning`, `caution`, and
    `important`. Legacy classes that do not align are still available: `info`, `success`, `error`.
-   **NEW**: Admonitions no longer require the `panel-` prefix (`panel-<name>`) and can now just use the name of the
    admonition to trigger default styling.
-   **NEW**: Add optional CommonMark support via the Marko library using the new frontmatter option `markdown_parser`.

## 4.3.3

-   **CHORE**: Move to wheel releases.

## 4.3.2

-   **FIX**: Avoid calling `sublime.load_binary_resource` when the file doesn't exist as Sublime will sometimes crash
    the Python host instead of throwing a `FileNotFoundError` exception .

## 4.3.1

-   **FIX**: Fixes for Sublime beta using Python 3.13.

## 4.3.0

-   **NEW**: Upgrade internal `coloraide` to version 1.3.
-   **NEW**: Add new color filter called `filters()` which implements filters as stated in
    https://www.w3.org/TR/filter-effects-1/.
-   **FIX**: Small fixes in handling Sublime's color syntax.

## 4.2.2

-   **FIX**: Remove a hack hack related to quote entities.
-   **FIX**: Fix issue related to transient HTML Sheets.

## 4.2.1

-   **FIX**: Fix relative importing of internal `pygments` and `jinja2` packages.

## 4.2.0

-   **NEW**: MdPopups is now self contained and vendors all dependencies.
-   **NEW**: Update internal, default CSS to load from inside `mdpopups` to prepare for Package Control 4.0.

## 4.1.2

-   **FIX**: A few more color related issues.

## 4.1.1

-   **FIX**: Upgrade color library to fix some color related corner cases. Also fix handling of `tmTheme` colors.

## 4.1.0

-   **NEW**: Plugins can now specify a language map in the front matter via `language_map`. The format matches the
    setting with the same name. This allows plugins to specify plugin specific languages that are maybe not good for
    general use.
-   **NEW**: Tweak `<hr>` color.
-   **FIX**: Fix issues with acquiring scheme selection colors.

## 4.0.4

-   **FIX**: Fix failure when displaying a specific debug message.

## 4.0.3

-   **FIX**: Fix stripping of `z` in code.

## 4.0.2

-   **FIX**: A few more fixes related to new color handling library.

## 4.0.1

-   **FIX**: Fixes related to new color handling library.

## 4.0.0

-   **NEW**: Added new `resolve_images` function to allow for processing remote image URLs and downloading the content
    in an HTML buffer.
-   **NEW**: `nl2br` can only be set through `markdown_extensions` via front matter. If passed as a parameter for any
    API function, it will be ignored.
-   **NEW**: `allow_code_wrap` can only be set through the front matter option `allow_code_wrap`. If passed as a
    parameter for any API function (except `syntax_highlight`), it will be ignored.
-   **NEW**: Support latest Markdown and Pymdown Extensions. Must use `markdown.extensions.md_in_html` instead of
    `pymdownx.extrarawhtml`.
-   **NEW**: Better color handling logic.
-   **NEW**: Remove `mdpopups.legacy_color_matcher` option along with legacy color match logic.
-   **FIX**: Fix exception when using Pygments.
-   **FIX**: Fix extra newlines in code blocks.
-   **FIX**: Popups will assign a default background, foreground, and link color. This is to ensure good colors when
    a color scheme assigns unexpected colors via `popup_css`. `popup_css` can override the CSS variables if desired, or
    a user can always specify a custom CSS via settings to change the variables. New CSS variables `--mdpopups-fg`,
    `--mdpopups-bg`, and `--mdpopups-link` have been added to to control these colors.

## 3.7.5

-   **FIX**: Don't strip newlines from content that has `nl2br` disabled.

## 3.7.4

-   **FIX**: Fix plain text syntax highlighting not always being applied correctly as the fallback.
-   **FIX**: Add `JSON/JSON` to highlight mapping.

## 3.7.3

-   **FIX**: Fix issue acquiring font styles like `bold` etc. on latter Sublime builds.

## 3.7.2

-   **FIX**: Add Julia language to highlight list.
-   **FIX**: Add built-in Typescript language to highlight list.

## 3.7.1

-   **FIX**: Fix logic error when using legacy color matcher.

## 3.7.0

-   **NEW**: Add support for `underline` and `glow` in highlighted code blocks.

    Currently Sublime's API has a bug
    (https://github.com/sublimehq/sublime_text/issues/3316) that prevents underline from being detected, you can enable
    the `mdpopups.legacy_color_matcher` to work around this issue until it is fixed. But keep in mind, leg this is not
    required as MdPopups will continue working just fine, just without showing underlines in highlighted code.

    While `glow` support has been added, it will not actually display proper in `minihtml` as `minihtml` cannot yet
    support the CSS `text-shadow` feature that is used to create the glow effect. If/when this support is added to
    Sublime, the glow effect *should* work.

-   **NEW**: Add option `mdpopups.legacy_color_matcher` to enable the legacy color matcher.

## 3.6.2

-   **FIX**: Sublime Text 4 no longer supports `cmd` and `args` in HTML sheets. Additionally, version 4074 will be
    required to get it working.

## 3.6.1

-   **FIX**: Color adjusters with `+` and `-` operator must have a space after the operator.
-   **FIX**: `lightness()` and `saturation()` should not accept numbers, only percentages.
-   **FIX**: Adjustments to match Sublime 4069 which now handles HSL color blending correctly.
-   **FIX**: Handle HSL/HWB if a user uses the 'deg' unit type.
-   **FIX**: Sublime doesn't support them, but support 'rad', 'grad', and 'turn' unit types in case Sublime ever
    supports them in HSL an HWB.

## 3.6.0

-   **NEW**: Add support for parsing `alpha(+value)`, `alpha(-value)`, and `alpha(*value)` in color schemes.
-   **NEW**: Add support for parsing `lightness()` and `saturation()` in color schemes.
-   **NEW**: Add support for `foreground_adjust` properties when parsing color schemes.
-   **NEW**: Add support for parsing blended colors in the HSL and HWB namespace. Blended colors do not always match
    Sublime Text's colors, this is due to a Sublime Text bug: https://github.com/sublimehq/sublime_text/issues/3176.

## 3.5.0

-   **NEW**: Upgrade to handle latest `pymdownx` and `markdown` module.

## 3.4.0

-   **NEW**: Add support for parsing `hwb()` and `alpha()`/`a()` in color schemes.

## 3.3.4

-   **FIX**: Update code highlight languages.

## 3.3.3

-   **FIX**: Fix tab logic inside `st_code_highlight`.
-   **FIX**: Upgrade internal SuperFences to latest.

## 3.3.2

-   **FIX**: Bring extensions up to the latest version.

## 3.3.1

-   **FIX**: Allow `-` in variables names. Write color translations to main scheme object and ensure filtering is done
    after color translations.

## 3.3.0

-   **NEW**: Add `tabs2spaces` to process text and convert tabs to spaces according to tab stops. Use case would include
    formatting text for `syntax_highlight`.

## 3.2.0

-   **NEW**: `pymdownx` and `pyyaml` are now required for use of `mdpopups` (#51).
-   **NEW**: Add support for `.hidden-color-scheme` (#50).

## 3.1.3

-   **FIX**: Create fallback file read for resource race condition.

## 3.1.2

-   **FIX**: Parse legacy `foregroundSelection` properly.

## 3.1.1

-   **FIX**: Color matcher library should only return gradients when one is actually found.

## 3.1.0

-   **NEW**: Handle parsing `.sublime-color-scheme` files with hashed syntax highlighting foreground colors.
-   **FIX**: Rework `*.sublime-color-scheme` merging and ensure `User` package is merged last.

## 3.0.5

-   **FIX**: Parse color schemes with unexpected extensions correctly.

## 3.0.4

-   **FIX**: Support for irregular `.sublime-color-scheme` values.

## 3.0.3

-   **FIX**: `scope2style` wasn't returning background color by default.

## 3.0.2

-   **FIX**: Improved color scheme parsing logic.
-   **FIX**: Fix code background not being correct.

## 3.0.1

-   **FIX**: Update color scheme matcher to latest and fix legacy support issues.

## 3.0.0

-   **NEW**: Support for `.sublime-color-schemes` (which are subject to change).
-   **NEW**: Update `rgba` library.

## 2.2.0

-   **NEW**: Remove deprecations.
-   **NEW**: Update `rgba` library.
-   **NEW**: Expose contrast.
-   **NEW**: Add support for PackageDev settings completions/tooltips/linting.
-   **FIX**: Hide scratch output panel.
-   **FIX**: Increase block code font size to `1rem`.
-   **FIX**: Better YAML stripping logic.
-   **FIX**: More descriptive failure message.

## 2.1.1

-   **FIX**: Strip front matter when `md=False`. Throw it away as we only use the front matter for Markdown.

## 2.1.0

-   **NEW**: Allow adding and configuring extensions via YAML front matter. This feature deprecates `nl2br` function
    parameter which will be removed some time in the future.
-   **NEW**: Allow setting whether block, code tags will allow word wrapping via YAML front matter. This feature
    deprecates the `allow_word_wrap` function parameter which will be removed some time in the future.
-   **NEW**: Expose SuperFences' `custom_fences` feature via YAML front matter.
-   **NEW**: Upgrade internal extensions.
-   **NEW**: Import official `pymdownx` extension if `pymdownx` is installed as a dependency so we can drop internal
    vendored extension copies in the future. This is allowed to be optional for a time until people can update their
    dependencies.
-   **NEW**: Import `pyyaml` extension if `pyyaml` is installed for front matter. This is allowed to be optional for a
    time until people can update their dependencies.
-   **NEW**: `inline-highlight` class in no longer applied to inline code.  Instead `highlight` is applied to both
    inline and block code.

## 2.0

-   **NEW**: Add `kbd` styling and `admontion` styling.
-   **NEW**: New rewritten `default.css`. Adds styling that uses new Sublime CSS features and drops legacy styling for
    old ST versions. No more `base.css`.
-   **NEW**: No longer outputs scope CSS into default CSS. Users must use template to acquire CSS for specific scopes.
    This helps keep the CSS namespace clean. In general, CSS should start using Sublime CSS variables like `--bluish`,
    `--redish` etc.  If a user needs CSS for a scope, they can use the `css` template filter to add the scope's CSS to a
    class of their choice.
-   **NEW**: MdPopups now requires ST 3124+ and all legacy styling and workarounds for ST < 3124 have been dropped.
-   **NEW**: Code blocks are now forced to use a monospace fonts.
-   **NEW**: Legacy `relativesize` template filter has been dropped. Users should use native CSS `rem` units for
    relative sizes.
-   **NEW**: Upgraded `pymdownx` extensions which includes fixes and enhancements. Also abandoned using `CodeHilite` in
    favor of `pymdownx.highlight`.
-   **NEW**: Add option to support wrapping in code blocks.
-   **NEW**: CSS filters are no longer limited to a set list of TextMate or Sublime scopes, and you no longer specify
    the parameters as CSS classes (but MdPopups will be forgiving if you do), but you should specify them as scopes
    (complexity doesn't matter). Also no more specifying multiple scopes separated by commas. Read documentation for
    more info.
-   **NEW**: CSS filter now accepts an `explicit_background` option to return a background only when explicitly defined
    (which is the default). When disabled, the filter will always return a valid background color (which is usually the
    base background).
-   **NEW**: Pygments is no longer the default syntax highlighter.
-   **FIX**: Fix foreground output that was missing semicolon according to spec.
-   **FIX**: Numerous CSS fixes.

## 1.0

-   **NEW**: First release.
