
import re
import argparse
import sys

# This LaTeX block redefines \section and \subsection so they automatically 
# update the \currentSection and \currentSubsection variables when used.
AUTO_UPDATE_PREAMBLE = r"""
% --- Auto-injected by conversion script ---
\newcommand{\currentSection}{}
\newcommand{\currentSubsection}{}

% Save original commands
\let\oldsection\section
\let\oldsubsection\subsection

% Redefine \section to update \currentSection and reset \currentSubsection
\renewcommand{\section}[1]{%
    \renewcommand{\currentSection}{#1}%
    \renewcommand{\currentSubsection}{}%
    \oldsection{#1}%
}

% Redefine \subsection to update \currentSubsection
\renewcommand{\subsection}[1]{%
    \renewcommand{\currentSubsection}{#1}%
    \oldsubsection{#1}%
}
% ------------------------------------------
"""

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert Beamer to ltx-talk with automatic section variable tracking."
    )
    parser.add_argument("input_file", help="Path to the input .tex file")
    parser.add_argument("-o", "--output", help="Path to the output .tex file (optional)")
    return parser.parse_args()

def transform_frames(text):
    """
    Transforms \begin{frame}{Title} -> \begin{frame} \frametitle{Title}
    Uses multiline mode to handle cases where braces might be spaced out.
    """
    # Pattern looks for:
    # \begin{frame}
    # Optional [...]
    # {Title}
    pattern = re.compile(r'\\begin\{frame\}(?P<opts>\[.*?\])?\s*\{(?P<title>.*?)\}', re.DOTALL)
    
    def replacement(match):
        opts = match.group('opts')
        title = match.group('title')
        
        # Build the new string
        if opts:
            return f"\\begin{{frame}}{opts}\n\\frametitle{{{title}}}"
        else:
            return f"\\begin{{frame}}\n\\frametitle{{{title}}}"

    return pattern.sub(replacement, text)

def process_file(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Change Document Class to ltx-talk
        # Replaces \documentclass[...]{...} with \documentclass{ltx-talk}
        content = re.sub(
            r'\\documentclass(\[.*?\])?\{.*?\}', 
            r'\\documentclass{ltx-talk}', 
            content, 
            count=1
        )

        # 2. Inject the Auto-Update Preamble
        # We insert this immediately after the new \documentclass{ltx-talk}
        if r'\documentclass{ltx-talk}' in content:
            content = content.replace(
                r'\documentclass{ltx-talk}', 
                '\\DocumentMetadata{tagging = on, lang = en}' + '\n' + r'\documentclass{ltx-talk}' + '\n' + AUTO_UPDATE_PREAMBLE
            )
        else:
            # Fallback if no documentclass found (e.g. partial file), prepend it
            content = AUTO_UPDATE_PREAMBLE + content

        # 3. Variable Substitution
        # Replace legacy beamer commands with our new variables
        content = content.replace(r'\secname', r'\currentSection')
        content = content.replace(r'\subsecname', r'\currentSubsection')
		# 4. Theme Commenting 
		# Comment out theme line
        content = content.replace(r'\usetheme', r'%\usetheme')
        # 5. Replace Titlepage with Maketitle
        content = content.replace(r'\titlepage', r'\maketitle')
        # 6. Transform Frame Syntax
        content = transform_frames(content)

        # 7. Write Output
        target = output_path if output_path else input_path.replace('.tex', '_ltxtalk.tex')
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Conversion complete. Saved to: {target}")

    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    args = parse_arguments()
    process_file(args.input_file, args.output)