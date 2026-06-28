# VulnoraIQ Desktop Mode (default): runs the web UI and Nora natively on the host
# with GPU; Docker is used only for sandboxed test agents. For the full
# containerised stack instead, use launch-vulnoraiq-docker-lab.* / bootstrap_launch.
from scripts.desktop_launch import main

if __name__ == "__main__":
    main()
