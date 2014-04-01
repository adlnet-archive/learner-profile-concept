# Learner Profile Concept

Prototype to provide CRUD services and validation for learner competency information.


## Installation

### Install Riak

[Riak 2.0.0pre20 Download page](http://docs.basho.com/riak/2.0.0pre20/downloads/)

Download the Riak package relevant to your operating system and architecture. Install according to the
instructions.


### Install the prototype

```bash
$ git clone https://github.com/adlnet/learner-profile-concept.git
$ cd learner-profile-concept
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

To leave the virtualenv, run `$ deactivate`.


## Running

```bash
$ cd learner-profile-concept
$ source env/bin/activate
$ python main.py
```


## Usage

This is (for now) a very simple API. It exposes a single endpoint `/profile`, that sends and receives
JSON documents.

### GET /profile

#### Arguments

* *id* - The learner's unique identifier. A SHA1 of a mailto address is recommended, in compliance with
	the xAPI specification.

#### Returns

* `200` - The previously stored document with that ID
* `404` - There are no documents associated with that identifier


### POST /profile

#### Arguments

* *id* - The learner's unique identifier. A SHA1 of a mailto address is recommended, in compliance with
	the xAPI specification.

#### Returns

* `200` - The newly updated document
* `304` - POSTed body was not JSON
* `500` - Server error

