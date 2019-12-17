title: Lessons Learned from Writing a PhD Dissertation in Markdown
thumbnail: https://storage.needpix.com/rsynced_images/papers-576385_1280.png
tags: [Science Writing, LaTeX, Markdown, Make]

#Lessons Learned from Writing a PhD Dissertation in Markdown

When researching ways to write my dissertation, I ended up settling on [Tom Pollard's thesis template](https://github.com/tompollard/phd_thesis_markdown). I was excited at the prospect of avoiding gigantic, unstable word files, being able to break down this massive work into more manageable chunks, and utilizing all the great features of modern text editors to make markhttps://www.needpix.com/photo/286807/papers-stack-heap-documents-business-paperwork-information-stacked-researchdown writing easier (intellisense, code folding, and syntax highlighting, for starters). However, this project was not without its pain points. For anyone else who ends up going this route, I'd like to share some of the ups and downs of this journey.

## The unavoidable behemoth that is LaTeX
I started this project with no desire to learn LaTeX. However, I ended up having to write a decent amount of it by hand. First of all, bear in mind that even though it is a mature technology, [there are still several painful bugs in LaTeX distros](https://tex.stackexchange.com/questions/313768/why-getting-this-error-tlmgr-unknown-directive). First off, here is something that I wish I had earlier: [a guide to installing a stable variant of TeXLive](https://tex.stackexchange.com/questions/1092/how-to-install-vanilla-texlive-on-debian-or-ubuntu). This is by far the most useful installation tutorial I have found for TexLive, helping you to properly install packages with tlmgr and avoid the dreaded [Error 34](https://github.com/tompollard/phd_thesis_markdown/issues). That being said, I was never able to get successful PDF compilation on my Ubuntu machine, I had to switch over to Mac Yosemite to get a PDF that actually had pictures, which are a pretty key part of a scientific thesis...

![](https://thumbs.gfycat.com/ThankfulUnkemptHydatidtapeworm-small.gif)

Worse still, LaTeX error messages are quite cryptic. One of the strangest recurring issues that I found was a [single, 0.5 pt. horizontal line](https://github.com/jgm/pandoc/issues/5801) in a table that broke the entire compilation. Many STEM dissertations tend to use horizontal figures, which are thankfully quite easy to do. First off, in the ```preamble.tex``` file, insert ```\usepackage{rotate}``` and ```\usepackage{pdfpages}``` somewhere before ```\begin{document}```. Then, wherever you need a horizontal figure, replace the traditional markdown syntax with this:

```latex
\begin{landscape}

\begin{sidewaysfigure}
    \hypertarget{fig:LABEL}{%
        \includegraphics{PATH_TO_IMAGE}
        \caption[SHORT_CAPTION]{CAPTION}
        \label{fig:LABEL}
    }
\end{sidewaysfigure}

%Repeat for additional sideways figures

\end{landscape}
```

Here, LABEL is what you'll use to reference this in the main text, using ```@fig:LABEL```. This should take care of your image needs, but images are unfortunately nowhere near as problematic as tables. Note that this will put page numbers on the left side of every page. If you want to have them at the bottom of your page, put this in your preamble:

```latex
\fancypagestyle{sideways}{
\fancyhf{} %Clears the header/footer
\fancyfoot{% Footer
\makebox[\textwidth][r]{% Right
  \rlap{\hspace{.75cm}% Push out of margin by \footskip
    \smash{% Remove vertical height
      \raisebox{4.87in}{% Raise vertically
        \rotatebox{90}{\thepage}}}}}}% Rotate counter-clockwise
\renewcommand{\headrulewidth}{0pt}% No header rule
\renewcommand{\footrulewidth}{0pt}% No footer rule
}
```

Now, just add ```\pagestyle{sideways}``` before ```begin{landscape}``` and ```\pagestyle{plain}``` after ```end{landscape}``` and you'll have page numbers centered at the bottom of your landscape pages.

## Dealing with Large Tables
Just because a table looks nice in markdown doesn't mean it's going to look correct in its PDF form. Often, the text in column headers or cells overlaps, or the spacing between columns doesn't make sense. Thankfully, Pandoc has its own custom  table syntax that allows for line breaks. My recommended workflow to do this is as follows:

1. Create a markdown file _outside_ of the source directory (perhaps in a directory called "bin" or "scratch" for clarity). Let's call it ```tables.md``` for this tutorial
2. Paste your problem tables (in markdown form) into this file
3. Run ```pandoc -t markdown+multiline_tables -o cleaned_tables.md tables.md```
4. Paste the new multi-line tables where the original tables would be in your document

There are some special cases where this won't be sufficient. Even though [there's a great package for figure short captions](https://github.com/martisak/pandoc-shortcaption), there's no such thing for tables as of yet. In your bin/scratch directory, run ```pandoc -H ../styles/preamble.tex -o tables.tex tables.md```. Now, take the LaTeX version of your table, and insert square brackets between ```\caption``` and the curly brace. This can also help with sideways tables, as you just need to wrap the latex table with ```\begin{landscape}``` and ```\end{landscape}```.

## Other Tips
My [fork of the original template](https://github.com/dendrondal/phd_thesis_markdown) uses several other Pandoc filters, including [xnos](https://github.com/tomduck/pandoc-xnos) and [shortcaptions](https://github.com/martisak/pandoc-shortcaption). These cut down on the amount of LaTeX needed. It should be said, however, that I wasn't able to get the autocomplete feature of fignos to work (```+@fig``` and ```*@fig```, respectively). This can be fixed by a simple find and replace, with +@ being replaced with Fig. \@.  This also works for equations and tables, just be mindful that you're using the proper amount of whitespace. Other tips:

- Install a stable version of TexLive (or your distro of choice) EARLY to avoid headaches down the road. 
- Make sure tlmgr works properly to install all your packages. Check ```which tlmgr``` both with and without sudo permissions to make sure its pointing to your install, which is especially important on Debian-based systems.
- Compile early and often. As mentioned previously, there are many strange quirks with PDF compilation.
- Make sure to find you which version of Pandoc you're using (```pandoc --version```). This is especially necessary if you have conda in your PATH, as it installs its own version. My Mac was using 1.1.3, instead of the current 2.7!
- I would highly recommend VSCode as an editor. It has phenomenal markdown syntax highlighting and previews with Markdown All in One, intellisense completion of figure referencing, and very nice cite-while-you-write extensions including Citation Picker for Zotero and Pandoc Citer. It also has version control tools built in for easier merging, and a user-level dictionary where you can put technical words that would originally be flagged by the spell checker (also an extension).

## Conclusions and Caveats
So, the main question one might ask is whether this is all worth it. I would still say yes, despite the major headaches and long nights this caused. First off, Word is in my personal opinion, absolutely terrible. Between the difficulty of things as simple as moving tables and images without messing up your paragraphs, the instability with large documents with tons of images, hogging of RAM, and the potential to completely corrupt your entire dissertation thanks to EndNote (literally happened to me the night before my undergrad thesis submission), I would absolutely not recommend it. I believe [Scrivener](https://www.literatureandlatte.com/scrivener/overview) is a pretty great alternative to Word/OpenOffice/Pages in terms of large, modular documents, but it's not available for Linux, and I'm not sure if it provides the full functionality of this workflow (auto figure/table/equation numbering, Git compatibility, etc.).

All that being said, with the amount of time I spent messing with LaTeX, I probably could have just as easily [written my own Pandoc filters in Python](https://github.com/sergiocorreia/panflute) to emulate some missing functionality with HTML conversion (```\listoffigures``` and short captions in particular), then styled the whole document with CSS. [Prince](https://www.princexml.com/), which can be used as a Pandoc pdf-engine, includes CSS styling. I'm not sure if this would calculate line breaks and image placement as well as Xelatex, but would be worth a try to prevent fonts and horizontal lines breaking a 200 page document. 

To anyone embarking on their dissertation writing journey, I wish you the best, and want to remind you that there is a light at the end of the tunnel!
