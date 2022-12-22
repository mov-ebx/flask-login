<div align="center">
    <h1>Flask Login/Signup</h1>
    <img width="400" src="https://i.giphy.com/media/KsLnm50rkhA6A/giphy.gif">
    <h3>A simple login system in Flask</h3>
    <h5>This is in no way what a modern login system should be. It lacks tons of features such as 2-Factor Authentication</h5>
    <h5>This was my very first time using Flask and this is my first experience in web development, so this code is FAR from perfect. I'm sure I overcomplicated most of it.</h5>
    <h5>Please report vulnerabilities in the <a href="https://github.com/mov-ebx/flask-login/issues">Issues page.</a></h5>

[![Python 3.10](https://img.shields.io/badge/Python-3.10-bluesvg)](https://www.python.org/download/releases/3.0/)
[![GitHub license](https://img.shields.io/badge/license-LGPL%202.1-green)](./LICENSE)
    <a href="https://github.com/mov-ebx">
        <img src="https://gpvc.arturio.dev/mov-ebx">
    </a>
</div>

## How do I use this?

- Make sure you have the [requirements](requirements.txt) installed.
- Run main.py and it will host the website at localhost on port 5000.
- It'll ask you for your SendGrip API key and Email

Don't worry about the database, it'll automatically set it up for you with SQLite.

### What should I modify?

- You should modify the email messages along with the urls sent in the emails to your domain, which can be done in [auth.py](api/auth.py)

## What features does it have?

- Signing in/up
- Email verification
- Password resetting

### What features could be added?

I don't plan on adding these, but I may add them in the future

- 2-Factor Authentication
- Phone number verification

## Credits

- me
- [Ricardo Oliva Alonso](https://codepen.io/ricardoolivaalonso), who made the beautiful login page I stole from their [CodePen](https://codepen.io/ricardoolivaalonso/pen/YzyaRPN)
- the authors of all the packages used
