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

This is a very simple API. It exposes two endpoints: `/api/learner` for creating new learner profiles, and `/api/learner/{user}`
that sends and receives JSON documents, where {user} is a predetermined identifier. It also exposes several sub-endpoints to access
particular parts of the JSON document.


### POST /api/learner
Create a new learner. Expects a JSON document specifying at least a unique identifier for this user

#### Arguments
*None*

#### Returns

__201 Created__

__400 Bad Request__

__409 Conflict__

#### Sample Minimal Request Body

```javascript
{
	"identity": {
		"key": "username"
	}
}
```

### GET /api/learner/{user}

Use this method to retrieve the document stored with the key {user}. Supports the `ETag` and `If-None-Match` headers for
concurrency control.

#### Arguments
*None*

#### Returns

__200 OK__ (JSON)  
Returns the previously stored document with that user ID.

__304 Not Modified__ (no body)  
If the _If-None-Match_ header is provided and matches the version on the server.

__404 Not Found__ (no body)  
There are no documents associated with that identifier.

#### Sample Response Body

```javascript
{
	// store personal information here
	"identity": {
	
		// the ID used in the URL, as supplied during account creation. immutable.
		"key": "username",
		
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

### HEAD /api/learner/{user}
Same as `GET`, with the exception that it will not return an actual document, but will still return the document's ETag.
Useful as a cheap way of checking for server-side changes.


### PUT /api/learner/{user}
Update a learner's profile. Will attempt to merge the posted document with the current content of the learner profile.
Supports the `ETag`, `If-Match`, and `If-None-Match` headers for concurrency control.

#### Arguments
*None*

#### Returns

__200 OK__ (JSON)  
Returns the newly-updated complete document, as if you followed the update with a `GET`.

__400 Bad Request__ (no body)  
The posted body does not form a valid JSON document.

__412 Precondition Failed__ (no body)  
The server-side content does not match an `If-Match` condition, or does match an `If-None-Match`. No changes are made.

__500 Internal Server Error__ (no body)  
Attempt to merge old and new documents failed.


### POST /api/learner/{user}

Set a learner's profile, destroying any previous content. Will not destroy the `key` field however. Supports the `ETag`,
`If-Match`, and `If-None-Match` headers for concurrency control.

#### Arguments
*None*

#### Returns

__200 OK__ (JSON)  
Returns the newly-updated complete document, as if you followed the update with a `GET`.

__400 Bad Request__ (no body)  
The posted body does not form a valid JSON document.

__412 Precondition Failed__ (no body)  
The server-side content does not match an `If-Match` condition, or does match an `If-None-Match`. No changes are made.


### DELETE /api/learner/{user}

Removes any stored learner profile for this user. Any subsequent `GET`s will return 404. Supports the `If-Match` and
`If-None-Match` headers for concurrency control.

#### Arguments
*None*

#### Returns

__204 No Content__ (no body)  
The document has been deleted successfully.

__404 Not Found__ (no body)  
There is no database entry for the provided username.

__412 Precondition Failed__ (no body)  
The server-side content does not match an `If-Match` condition, or does match an `If-None-Match`. No changes are made.
