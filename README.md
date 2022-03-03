<p align="center">
  <a href="" rel="noopener">
 <img height=100px src="https://user-images.githubusercontent.com/19360256/156537333-340bcb79-be3e-447a-8bd4-e26a77aff7da.svg" alt="Project logo"></a>
</p>

<h3 align="center">Boozebot</h3>

<div align="center">

<!--   [![Status](https://img.shields.io/badge/status-active-success.svg)]() -->
  [![GitHub Issues](https://img.shields.io/github/issues/curtinrobotics/Boozebot.svg)](https://github.com/curtinrobotics/Boozebot/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/curtinrobotics/Boozebot.svg)](https://github.com/curtinrobotics/Boozebot/pulls)
<!--   [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE) -->

</div>

---

<p align="center"> Boozebot is a drink serving robot developed by the Curtin Robotics Club.
    <br>
</p>

## 📝 Table of Contents

- [About](#about)
- [Env](#env)
  - [Backend](#backend)
  - [Pump](#pump)
- [Built Using](#built_using)
- [Authors](#authors)

## 🧐 About <a name="about"></a>
We had a few goals in mind when developing Boozebot version 3. These were:
 - Serve legal drinks(do not exceed the alcohol limit)
 - Mix complicated Drinks
 - Mix drinks in a quick fashion either equivalent to or faster than an average bartender.
 - Have a mixture of high volume and high accuracy flow rates.
 - Have a simplified backend and user interface for Boozebot.

### Components
#### Hardware
- High-volume liquids
- High-accuracy mixers
- Control unit
- ID card reader
- Cup gantry
- Liquid spouts
- Cup dispenser

#### Software
- User interface & management system
- Pump controller firmware
- Student ID card reader firmware

## 🔧 Environment Setup <a name="env"></a>
### Backend <a name="backend"></a>
#### Prerequisites
1. Install an up-to-date version of Python 3
2. Install pip
3. Install virtualenv (`pip install virtualenv`)

#### Environment Setup
In the Boozebot directory:
```sh
cd Backend
virtualenv venv                   # Initialise virtual environment
source venv/bin/activate          # Activate the virtual environment
pip install -r requirements.txt   # Install dependencies
```

### Pump Controller Firmware <a name="pump"></a>
Cody TODO

## ⛏️ Built Using <a name = "built_using"></a>
- [Tornado](https://www.tornadoweb.org/) - Web Server, WebSocket Implementation, WSGI Host for Flask App
- [Flask](https://flask.palletsprojects.com) - Web Framework for non-WebSocket pages
- [SQLAlchemy](http://www.sqlalchemy.org) - Database Layer

## ✍️ Authors <a name = "authors"></a>
- Thomas Ryan-Galloway (TRG) [@Tomant1](https://github.com/Tomant1) &mdash; Initial Python backend and arduino
- Lachlan Bell (LB) [@lachlanbell](https://github.com/lachlanbell) &mdash; Backend code, ID scanner firmware
- Cody John Dalliston (CJD) [@CodysCodes](https://github.com/CodysCodes) &mdash; Pump controller firmware
- Adrian Tan (AT) [@Adrian-tech-bot](https://github.com/Adrian-tech-bot) &mdash; Backend code

See also the list of [contributors](https://github.com/curtinrobotics/Boozebot/contributors) who participated in this project.
