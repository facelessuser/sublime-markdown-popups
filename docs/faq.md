## Questions

- **Why don't `#!html <pre>` tags work right?**

    This is because the HTML engine in Sublime treats `#!html <pre>` tags just as a normal block elements; it doesn't treat the content as preformatted.  When MdPopups creates code blocks, it actually specially formats the blocks.  It converts tabs to 4 spaces, and spaces are converted to `#!html &nbsp;` to prevent wrapping.  Lastly, new lines get converted to `#!html <br>` tags.
    {: style="font-style: italic"}

- **Why in code blocks do tabs get converted to 4 spaces?**

    Because I like it that way.  If you are planning on having a snippet of text sent through the syntax highlighter and do not want your tabs to be converted to 4 spaces, you should convert it to the number of spaces you like **before** sending it through the syntax highlighter.
    {: style="font-style: italic"}

- **Why does &lt;insert element&gt; not work, or cause the popup/phantom not to show?**

    Because Sublime's HTML engine is extremely limited.  Though I do not have a complete list of all supported elements, you should keep things basic.  Things like `#!html <table>` will not *currently* work.
    {: style="font-style: italic"}
