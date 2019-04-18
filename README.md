# advance-season

Tries to beat the cost of a season ticket by booking lots of advance tickets.

## When to use

This is best used if you want to bulk buy tickets and have a railcard, since this has a significant cost advantage.

## Requirements
* Trainline account
* chromedriver installed on machine and available on PATH
* Python 3
* `pip install -r requirements.txt`

## Instructions
For a series of trips from:

```
York to Leeds
Leaving before 09:00 every morning
Leaving after 18:00 every evening
From 2019-02-11 to 2019-02-15
And your emails is me@myemail.com
```

you would use as follows

```bash
$ python advance_ticket/__init__.py York Leeds 09:00 18:00 2019-02-11 2019-02-15 me@myemail.com
```

After running, a browser window will popup, and the CLI will ask for your trainline password.

Once you've entered it, it will go through the interface and queue up tickets in the basket for every day between those two dates at the same times.

## Caveats & Assumptions

* You will lose some money due to booking through trainline, but it is still *much* cheaper than a season ticket or daily anytime tickets
* In fact for the journey shown it's about £20 cheaper per week which is nearly £1000 a year
* It will use trainline to figure out the best deal.
* There is an option `--young` if you want to add a 16-25 railcard
* Weekend days are skipped by default, but you can incldue them with `-w`
