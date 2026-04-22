import os

import gifos


def main() -> None:
    # Minimal retro terminal GIF for profile README
    t = gifos.Terminal(width=700, height=360, xpad=12, ypad=12)
    t.gen_text(text="Y7X@github:~$ neofetch", row_num=1)
    t.gen_text(text="OS: Every OS (Linux via VM)", row_num=3)
    t.gen_text(text="Role: Student", row_num=4)
    t.gen_text(text="IDE: VS Code Insiders", row_num=5)
    t.gen_text(text="Stack: Astro, React, Next.js, SCSS, CSS", row_num=6)
    t.gen_text(text="Tooling: npm", row_num=7)
    t.gen_text(text="Motto: Random idea -> production ready", row_num=8)
    t.gen_text(text="Y7X@github:~$ _", row_num=10)
    t.gen_gif()

    os.makedirs("assets", exist_ok=True)
    if os.path.exists("output.gif"):
        os.replace("output.gif", os.path.join("assets", "readme-terminal.gif"))


if __name__ == "__main__":
    main()

