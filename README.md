# TITANIS

This Python library provides a tool for complex psycho-emotional analysis of texts in
Russian. [API documentation](docs/TITANIS%20API.pdf).

## Requirements

- python 3.9
- docker >= 17.06
- docker-compose >= 1.8.0

## Usage

### Server-side

You should run the docker containers on the same or remote machine with the command:
``docker-compose up -d``

### Client-side

To install the library and dependencies, run the command:
``sudo apt-get install python-dev build-essential && pip install -U .``

Once you have run this command you can use the tool in your Python script:

```python
from titanis import Titanis

tt = Titanis(psy_cues=True, psy_cues_normalization='words',
             psy_dict=True, psy_dict_normalization='abs',
             syntax=True,
             discourse=True,
             frustration_clf=True,
             emotive_srl=True)

text = 'Компьютерные игры могут помочь молодым людям приобрести важные для жизни навыки.\
 Хотя в чрезмерном увлечении ими есть и риски.'
result = tt(text)
```
