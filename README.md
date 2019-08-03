## Overview
This project is used for inventory calculation for any small business.Business owner can mange their business easily.
They can their daily sales, daily profit, daily return and overall stock of the business.

## Why this project

The purpose of site to get inventory calculation

## Features
* Easy user interface
* Show all product list
* Daily profit and loss calculation
* Daily purchase and sales
* Database backup system and recovery system

## Using library
* flask==1.0.2
* Flask-SQLAlchemy==2.3.2
* WTForms==2.2.1


### Project work flow
![inventory](static/project_look.png)

## Project Structure

      inventory
        ├── app.py
        ├── forms.py
        ├── helper.py
        ├── models.py
        ├── README.md
        ├── requirements.txt
        ├── static
        │   ├── css
        │   │   ├── app.css
        │   │   ├── bootstrap.min.css
        │   │   ├── font-awesome.min.css
        │   ├── js
        │   │   ├── bootstrap.bundle.min.js
        │   │   ├── bootstrap.min.js
        │   │   ├── jquery-1.10.2.js
        │   │   └── jquery-ui.js
        │   └── project_look.png
        ├── templates
        │   ├── backup_message.html
        │   ├── backup_upload.html
        │   ├── base_ex.html
        │   ├── base.html
        │   ├── damage_create.html
        │   ├── damage_list.html
        │   ├── product_create.html
        │   ├── product_list.html
        │   ├── product_update.html
        │   ├── purchase_create.html
        │   ├── purchase_list.html
        │   ├── sales_create.html
        │   ├── sales_list.html
        │   ├── sales_report.html
        │   ├── software_licence.html
        │   ├── stock_out.html
        │   └── top_selling_product_list.html
        └── views.py


## Coding patterns

* **views** *There are views for showing product list, purchase, sales and popular product.*

* **helper** *All type of supporting function are included here *

* **model** *All data model and query call from here by using sqlalchemy.*

* **forms** *There are different type of form are ProductForm, SalesForm, PurchaseForm, DamageForm*


## Prerequisites

To setup the project, you will need the following tools and machine configurations:

#### Run project using docker

- Minimum ubuntu 14.04 server or Minimum windows 7 server
- docker [setup docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- git [setup git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

#### Run project without docker

 - Minimum ubuntu 14.04 server or Minimum windows 7 server
 - git [setup git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
 - pip3 [setup pip3](https://pip.pypa.io/en/stable/installing/)
 - python 3.6 [setup python 3.7](https://www.python.org/doc/)
 - flask 1.0 [setup flask 1.0](http://flask.pocoo.org/docs/1.0/)


## How to run this project without docker

Clone **inventory** from GitLab using,

`git clone https://github.com/inventory.git`

Go to the cloned project directory using,

`cd inventory`


Install **virtualenv** if it's not already installed, by

`pip3 install virtualenv`

Make a virtualenv on project directory, using

`virtualenv .env`

Activate virtualenv.

* For *mac* and *linux*

`source .env/bin/activate`

* For *windows*

You can install *babun* tools for using *mac* and *linux* command.

See in details: http://babun.github.io/

Install the project dependencies in the following command

`pip3 install -r requirements.txt`

Run the project by executing _app.py_ file

`python3 app.py`
