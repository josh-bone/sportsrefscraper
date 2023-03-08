# sportsrefscraper
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
![Version](https://img.shields.io/pypi/v/sportsrefscraper)
![Tests](https://github.com/josh-bone/sportsrefscraper/actions/workflows/unit-tests.yml/badge.svg)


## Background

[sports-reference.com](https://www.sports-reference.com/) is an online repository containing statistics for several different sports. The aim of this repository is to maintain an updated web-scraper for this site.

This is _far_ from the first sports-reference scraper. However, on January 1, 2023, [sports-reference.com](https://www.sports-reference.com/) retired their "widgets" feature, which formed the basis of many of existing scrapers. When these broke, I decided to make my own scraper which doesn't use that functionality. This is the most up-to-date scraper as of my knowledge (in March 2023).

I'm creating this repository _mostly_ to familiarize myself with PyPI packaging and best practices. Feel free to use it in your personal work, research, or passion projects!

## Installation

Assuming you already have [pip](https://pip.pypa.io/en/stable/installation/) installed, run the following from the terminal:

```
pip install -i https://test.pypi.org/simple/ sportsrefscraper==0.1.2
```

Because this isn't _yet_ published on pip as of March 8 2023. This is why we have to use the TestPyPI installation above.

### Warning: TestPyPI packages are only hosted temporarily, so if this install doesn't work, just open an issue. I'll publish it on PyPI as soon as someone else starts using this, but until then, I don't want to clog the pipeline.

## Example Usage

In your python code, import the necessary class and scrape away!

```python
import datetime as dt
from sportsrefscraper.games import scrape_shot_chart

# Get the shot chart for Philly 76ers vs. Milwaukee Bucks on March 4, 2023
away = 'PHI'
home = 'MIL'
date = dt.date(2023, 3, 4)
shots = scrape_shot_chart(date, away, home)
```



## Features

<ins>Leagues</ins>:
- [x] NBA
- [ ] MLB
- [ ] NFL

The 'games' submodule has functionality for scraping the following:
- Box Scores
- Shot Charts
- Play-by-play Game Descriptions 

The 'leagues' submodule has functionality for scraping the following:
- Schedule
- Standings 

The 'teams' submodule has functionality for scraping the roster of a team.

## Collaboration

Collaborators are welcome - feel free to submit issues and pull requests at will.

<ins>Our contributors</ins>:

<a href="https://github.com/josh-bone/sportsrefscraper/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=josh-bone/sportsrefscraper" />
</a>
