# beamer-to-ltx-talk
Converts from beamer to the new ltx-talk format for LaTeX presentations.

This script is distributed under the GNU GPL v3.0 License. Read it at https://www.gnu.org/licenses/gpl-3.0.en.html.
It is provided as is, with no warranty.

The beamer LaTeX document class, used for presentations, is incompatible with the LaTeX tagging project, so cannot produce accessible PDFs (see [the LaTeX tagging project site](https://latex3.github.io/tagging-project/) for more info). I was unable to find a script that converted beamer documents to ltx-talk documents (which are tagging compatible), hence this script.
It works for my own admittedly basic purposes, so I hope it can at least serve as a reasonable starting point for others'.

It handles the \secname and \subsecname commands with new \currentSection and \currentSubsection commands. 
It also comments out theme commands, so if you want to use a theme you will need to do that manually.

The syntax to run it is python beamer-to-ltxtalk-auto.py <oldfilepath>.tex -o <newfilepath>.tex.

Regards,
Kit
