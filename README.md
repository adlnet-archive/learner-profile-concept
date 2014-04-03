# Learner Profile Concept

The goal of this project is to provide a minimal lightweight Web API service for the purpose of storing
Learner Profiles. For the purposes of this project, a Learner Profile contains:

* A learner's personal information (e.g. name, email address)
* A list of a learner's educational goals, expressed as links to [Mozilla Open Badges](http://openbadges.org/)
* A list of a learner's in-progress learning experiences (again, links to badges)
* The learner's current knowledgebase, expressed as a list of Badge Assertions

Though out of the scope of this project, one could also imagine a learner profile containing:
* Learner preferences
* Affective state (interest, boredom, motivation)
* Learner context (hunger, location, on a long car ride, etc.)


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
(env)$ pip install -r requirements.txt
```

To leave the virtualenv, run `$ deactivate`.


## Running

```bash
$ cd learner-profile-concept
$ source env/bin/activate
(env)$ python main.py
```


## Usage

This is a very simple API. It exposes two endpoints: `/api/learner` for creating new learner profiles, and `/api/learner/{userid}`
that sends and receives JSON documents, where {userid} is an identifier chosen during account creation. The API also exposes
several sub-endpoints to access particular parts of the JSON document.

### Endpoint /api/learner

#### POST /api/learner
Create a new learner. Expects a JSON document specifying at least a unique identifier for this user.

##### Arguments
*None*

##### Returns

__201 Created__ (JSON)  
Returns the newly created learner profile. It will likely look something like this:

```javascript
{
	"identity": {
		"userid": "username"
	},
	"badges": {
		"desired": [],
		"inProgress": [],
		"achieved": []
	}
}
```

__400 Bad Request__ (no body)  
The request body is not a valid JSON body, or does not contain the required *userid* field.

__409 Conflict__ (no body)  
The supplied *userid* is already in use by another learner profile. Try again with a different identifier.

##### Example Minimal Request Body

```javascript
{
	"identity": {
		"userid": "username"
	}
}
```


### Endpoint /api/learner/{userid}

#### GET /api/learner/{userid}

Use this method to retrieve the document stored with the given {userid}. Supports the `ETag` and `If-None-Match` headers for
concurrency control.

##### Arguments
*None*

##### Returns

__200 OK__ (JSON)  
Returns the previously stored document with that user ID.

__304 Not Modified__ (no body)  
If the _If-None-Match_ header is provided and matches the version on the server.

__404 Not Found__ (no body)  
There are no documents associated with that identifier.

##### Sample Response Body

```javascript
{
	// store personal information here
	"identity": {
	
		// the ID used in the URL, as supplied during account creation. immutable.
		"userid": "username",
		
		// additional optional information about the learner
		"givenName": "Joe",      
		"familyName": "Learner",
		
		// should store Experience API-style agent identifiers
		"mbox": "mailto:joe.learner@example.com" 
	},
	
	// the learner's competency history and goals
	"badges": {
		
		// badges the learner would like to have
		"desired": [badge1, badge2],
		
		// badges the learner is currently working toward
		"inProgress": [badge1],
		
		// badges the learner has already acquired
		"achieved": [badgeAssertion1, badgeAssertion2]
	}
}
```



#### HEAD /api/learner/{userid}
Same as `GET`, with the exception that it will not return an actual document, but will still return the document's ETag.
Useful as a cheap way of checking for server-side changes.


#### PUT /api/learner/{userid}
Update a learner's profile. Will attempt to merge the posted document with the current content of the learner profile.
Supports the `ETag`, `If-Match`, and `If-None-Match` headers for concurrency control.

##### Arguments
*None*

##### Returns

__200 OK__ (JSON)  
Returns the newly-updated complete document, as if you followed the update with a `GET`.

__400 Bad Request__ (no body)  
The posted body does not form a valid JSON document.

__412 Precondition Failed__ (no body)  
The server-side content does not match an `If-Match` condition, or does match an `If-None-Match`. No changes are made.

__500 Internal Server Error__ (no body)  
Attempt to merge old and new documents failed.


#### POST /api/learner/{userid}

Set a learner's profile, destroying any previous content. Will not allow the *identity.userid* field to be destroyed,
however. Supports the `ETag`, `If-Match`, and `If-None-Match` headers for concurrency control.

##### Arguments
*None*

##### Returns

__200 OK__ (JSON)  
Returns the newly-updated complete document, as if you followed the update with a `GET`.

__400 Bad Request__ (no body)  
The posted body does not form a valid JSON document.

__404 Not Found__ (no body)  
There is no learner with the given *userid*.

__412 Precondition Failed__ (no body)  
The server-side content does not match an `If-Match` condition, or does match an `If-None-Match`. No changes are made.


#### DELETE /api/learner/{userid}

Removes any stored learner profile for this user. Any subsequent `GET`s will return 404. Supports the `If-Match` and
`If-None-Match` headers for concurrency control.

##### Arguments
*None*

##### Returns

__204 No Content__ (no body)  
The profile has been deleted successfully.

__404 Not Found__ (no body)  
There is learner with the given *userid*.

__412 Precondition Failed__ (no body)  
The server-side content does not match an `If-Match` condition, or does match an `If-None-Match`. No changes are made.


### Endpoint /api/learner/{userid}/badges

#### GET /api/learner/{userid}/badges

Use this method to retrieve the badges stored with the given {userid}. Supports the `ETag` and `If-None-Match` headers for concurrency control.

##### Arguments
*None*

##### Returns

__200 OK__ (JSON)  
Returns the user's badges.

__304 Not Modified__ (no body)  
If the _If-None-Match_ header is provided and matches the version on the server.

__404 Not Found__ (no body)  
There are no documents associated with that identifier.

##### Sample Response Body

```javascript
{
	// the learner's competency history and goals
	"badges": {
		
		// badges the learner would like to have
		"desired": [badge1, badge2],
		
		// badges the learner is currently working toward
		"inProgress": [badge1],
		
		// badges the learner has already acquired
		"achieved": [badgeAssertion1, badgeAssertion2]
	}
}
```

#### GET /api/learner/{userid}/badges/achieved

Use this method to retrieve the achieved badges stored with the given {userid}. Supports the `ETag` and `If-None-Match` headers for concurrency control.

##### Arguments
*None*

##### Returns

__200 OK__ (JSON)  
Returns the user's badges.

__304 Not Modified__ (no body)  
If the _If-None-Match_ header is provided and matches the version on the server.

__404 Not Found__ (no body)  
There are no documents associated with that identifier.

##### Sample Response Body

```javascript
{
	// badges the learner has already acquired
	"achieved": [badgeAssertion1, badgeAssertion2]
}
```

#### GET /api/learner/{userid}/badges/achieved/{assertionid}

Use this method to retrieve a user's [badge assertion](https://github.com/mozilla/openbadges-specification/blob/master/Assertion/latest.md). Supports the `ETag` and `If-None-Match` headers for concurrency control.

##### Arguments
*None*

##### Returns

__200 OK__ (JSON)  
Returns the user's badges.

__304 Not Modified__ (no body)  
If the _If-None-Match_ header is provided and matches the version on the server.

__404 Not Found__ (no body)  
There are no documents associated with that identifier.

##### Sample Response Body

```javascript
{
    "userid": "joelearner",
    "recipient": {
        "type": "email",
        "hashed": true,
        "salt": "deadsea",
        "identity": 
    "sha256$c7ef86405ba71b85acd8e2e95166c4b111448089f2e1599f42fe1bba46e865c5"
    },
    "issuedOn": 1359217910,
    "badge": "https://example.org/robotics-badge.json",
    "verify": {
        "type": "hosted",
        "url": "https://example.org/beths-robotics-badge.json"
    }
}
```

#### GET /api/learner/{userid}/badges/inprogress

Use this method to retrieve the badges the given {userid} is working on achieving. Supports the `ETag` and `If-None-Match` headers for concurrency control.

##### Arguments
*None*

##### Returns

__200 OK__ (JSON)  
Returns the user's badges.

__304 Not Modified__ (no body)  
If the _If-None-Match_ header is provided and matches the version on the server.

__404 Not Found__ (no body)  
There are no documents associated with that identifier.

##### Sample Response Body

```javascript
{
	// badges the learner has already acquired
	"inProgress": [badgeAssertion1, badgeAssertion2]
}
```

#### GET /api/learner/{userid}/badges/desired

Use this method to retrieve the badges the given {userid} desires to achieve. Supports the `ETag` and `If-None-Match` headers for concurrency control.

##### Arguments
*None*

##### Returns

__200 OK__ (JSON)  
Returns the user's badges.

__304 Not Modified__ (no body)  
If the _If-None-Match_ header is provided and matches the version on the server.

__404 Not Found__ (no body)  
There are no documents associated with that identifier.

##### Sample Response Body

```javascript
{
	// badges the learner has already acquired
	"desired": [badgeAssertion1, badgeAssertion2]
}
```
