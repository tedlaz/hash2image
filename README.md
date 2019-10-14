# hash2image

Create images from hashes.

![icon examples](https://imgur.com/CdrpALy.png)

This is an adaptation of Colin Davis' code at [Robohash.org](https://robohash.org/)

## Installation

### 1. Docker

From dockerhub:

```sh
$ docker run -d -p 8099:8099 tedlaz/hash2image
```

or by yourself:

```sh
$ git clone https://github.com/tedlaz/hash2image.git
$ cd hash2image
$ docker build -t hash2image .
$ docker run -d -p 8099:8099 hash2image
```

In either case open your browser at:

```
localhost:8099/"Your text to hash and image"?size=300
```

and you will get a nice image unique for this text.

### 2. Command line

```sh
$ git clone https://github.com/tedlaz/hash2image.git
$ cd hash2image
$ python3 -m venv venv
$ source venv/vin/activate
$ pip install -r requirements.txt
$ python
```

and from python:

```python
import hash2image as hi
hi.hash2image('your text here', 'coats', size=450)
```

and you will get a 450x450 image.

### Possible values for parameter set

- robots (http://localhost:8099/sometext?set=robots)
- monsters (http://localhost:8099/sometext?set=monsters)
- robotfaces (http://localhost:8099/sometext?set=robotfaces)
- cats (http://localhost:8099/sometext?set=cats)
- people (http://localhost:8099/sometext?set=people)
- coats wich is the default set because i created it ;-)

## Image sets and licenses

**Image2hash** comes with six image sets:

- robots by zikri kader under CC-BY-3.0 or CC-BY-4.0 license.
- monsters by Hrvoje Novakovic under CC-BY-3.0 license.
- robot faces by Julian Peter Arias under CC-BY-3.0 license.
- [cats by David Revoy](https://www.peppercarrot.com/en/article391/cat-avatar-generator) under CC-BY-4.0 license.
- [people by Pablo Stanley](https://avataaars.com/), free for personal and commercial use.
- coats of arms, free for personal and commercial use.
