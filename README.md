# pip-cache

A simple script that allows prefix-based searching of a locally cached copy of
all available PyPi packages, a la `apt-cache pkgnames`. The cache is created and
updated manually by calling `pip-cache update`, in the spirit of
`apt-get update`.

The cache is stored in `$XDG_DATA_HOME/pip-cache/all-packages.txt`, where
`$XDG_DATA_HOME` is usually `~/.local/share` on Linux systems.

Used in [`pip-bash-completion`](https://github.com/brunobeltran/pip-bash-completion).
