import os

import gifos


def main() -> None:
    # Expanded retro terminal GIF for profile README
    t = gifos.Terminal(width=700, height=460, xpad=12, ypad=12)
    t.gen_text(text="Y7X@github:~$ neofetch", row_num=1)
    t.gen_text(text="User: Y7XIFIED", row_num=3)
    t.gen_text(text="Role: Student | Builder", row_num=4)
    t.gen_text(text="OS: Windows-first | Linux via VM", row_num=5)
    t.gen_text(text="IDE: VS Code Insiders", row_num=6)
    t.gen_text(text="Core: JavaScript, React, Next.js, Astro", row_num=7)
    t.gen_text(text="Web: SCSS, CSS, HTML", row_num=8)
    t.gen_text(text="Tooling: npm, Git, GitHub Actions", row_num=9)
    t.gen_text(text="Current Focus: UI engineering + production-ready builds", row_num=10)
    t.gen_text(text="Motto: Random idea -> production ready", row_num=11)
    t.gen_text(text="GitHub: github.com/Y7XIFIED", row_num=12)
    t.gen_text(text="Y7X@github:~$ _", row_num=14)
    t.gen_gif()

    os.makedirs("assets", exist_ok=True)
    if os.path.exists("output.gif"):
        os.replace("output.gif", os.path.join("assets", "readme-terminal.gif"))


if __name__ == "__main__":
    main()
