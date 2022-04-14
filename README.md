
<p align="center">
  <img
    width="400"
    src="https://raw.githubusercontent.com/chassing/when-cli/master/media/logo.jpg"
    alt="When CLI"
  />
</p>

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]
[![Black][black-badge]][black-link]
![PyPI - License](https://img.shields.io/pypi/l/when-cli)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/chassing/when-cli/Test?label=tests)
![GitHub Release Date](https://img.shields.io/github/release-date/chassing/when-cli)

# When CLI

<img
  src="https://raw.githubusercontent.com/chassing/when-cli/master/media/example.png"
  alt="Example"
  width="50%"
  align="right"
/>

**when-cli** is a timezone conversion tool. It takes as input a natural time string, can also be a time range, and converts it into different timezone(s) at specific location(s).

- **Local:** Everything runs on your local machine, no internet connection needed
- **Fast:** it's fast! 🚀
- **Easy:** quick to install – start using it in minutes.
- **Customizable:** configure every aspect to your needs.
- **Colorful:** beautiful colors and Emoji 😎 support.

## Installation

You can install **when-cli** from [PyPI](https://pypi.org/project/when-cli/) with `pipx`):

```bash
$ pipx install when-cli
```

or install it with `pip`:
```bash
$ python3 -m pip install when-cli
```

You can also download and use the pre-build binary from the latest [Release](https://github.com/chassing/when-cli/releases).


## Usage

```bash
$ when-cli "7. May 06:00 to May 7th 12:00 in PMI" -l America/Los_Angeles -l klu -l PMI
```
<img
  src="https://raw.githubusercontent.com/chassing/when-cli/master/media/example.png"
  alt="Example"
/>

See [Usage](https://github.com/chassing/when-cli/blob/master/USAGE.md) for more details.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Logo

[vecteezy.com](https://www.vecteezy.com/vector-art/633173-clock-icon-symbol-sign)



[black-badge]:              https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]:               https://github.com/psf/black
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/chassing/when-cli/discussions
[pypi-link]:                https://pypi.org/project/when-cli/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/when-cli
[pypi-version]:             https://badge.fury.io/py/when-cli.svg
