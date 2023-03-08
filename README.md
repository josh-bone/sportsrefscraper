# sports_reference_scraper
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![Version](https://img.shields.io/pypi/v/sports_reference_scraper)

## Background

[sports-reference.com](https://www.sports-reference.com/) is an online repository containing statistics for many various sports. 

This is _far_ from the first sports-reference scraper. However, on January 1, 2023, sports-reference.com retired their "widgets" feature, which formed the basis of many of existing scrapers. This repository does not use that functionality, so it is the most up-to-date scraper as of my knowledge (in March 2023).

I'm creating this repository _mostly_ to familiarize myself with PyPI packaging and best practices. Feel free to use it in your personal work, research, or passion projects!

## Installation

Assuming you already have [pip](https://pip.pypa.io/en/stable/installation/) installed, run the following from the terminal:

```
pip install sports_reference_scraper
```

### Warning! This isn't _yet_ published on pip as of March 8 2023. See the TestPyPI installation below for a temporary testpypi development build. 

## Example Usage

In your python code, import the necessary class and scrape away!

```python
import datetime as dt
from sports_reference_scraper.games import scrape_shot_chart

# Get the shot chart for Philly 76ers vs. Milwaukee Bucks on March 4, 2023
away = 'PHI'
home = 'MIL'
date = dt.date(2023, 3, 4)
shots = scrape_shot_chart(date, away, home)
```


### Last working TestPyPI installation:

```pip install -i https://test.pypi.org/simple/ sports-reference-scraper==0.1.5```
