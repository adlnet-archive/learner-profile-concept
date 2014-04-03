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

This is a very simple API. It exposes a single root endpoint `/learner/{user}` that sends and receives
JSON documents, where {user} is some unique identifier. It also exposes several sub-endpoints to access
particular parts of the JSON document.


### Example Body

This is an example of the types of data that could be stored in this implementation of the Learner Profile.

```javascript
{
	// store personal information here
	"identity": {
	
		// The ID used in the URL. Auto-populated, immutable, required
		"key": "username",
		
		// additional optional information about the learner
		"givenName": "Joe",      
		"familyName": "Learner",
		"educationLevel": 5,
		
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


### HEAD,GET /learner/{user}

Use these methods to retrieve the document stored for {user}. Supports the `ETag` and `If-None-Match` headers for concurrency
control. The only difference between these two methods is that `HEAD` will not return an actual document, but will still
return the document's ETag. Useful as a cheap way of checking for server-side changes.

#### Arguments
*None*

#### Returns

__200 OK__ (JSON with `GET`, no body with `HEAD`)  
Returns the previously stored document with that user ID.

__304 Not Modified__ (no body)  
If the _If-None-Match_ header is provided and matches the version on the server.

__404 Not Found__ (no body)  
There are no documents associated with that identifier.


### PUT,POST /learner/{user}

Set or update a learner's profile. A `PUT` request will attempt to merge the posted document with the current content of the
learner profile, whereas a `POST` will simply replace it. Supports the `ETag`, `If-Match`, and `If-None-Match` headers for
concurrency control.

#### Arguments
*None*

#### Returns

__200 OK__ (JSON)  
Returns the newly-updated complete document.

__201 Created__ (JSON)  
Returns the newly-created complete document.

__400 Bad Request__ (no body)  
The posted body does not form a valid JSON document.

__412 Precondition Failed__ (no body)  
The server-side content does not match an `If-Match` condition, or does match an `If-None-Match`. No changes are made.

__500 Internal Server Error__ (no body)  
For `PUT` only. Attempt to merge old and new documents failed.


### DELETE /learner/{user}

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
