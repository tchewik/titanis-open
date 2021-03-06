# TITANIS

This Python 3 library provides a tool for complex psycho-emotional analysis of texts in Russian. [API documentation](docs/API.pdf).

## Installation

To install the library and dependencies, run the command:
``sudo apt-get install python-dev build-essential && pip install -U .``

You should also run the docker containers on the same or remote machine with the command:
``docker-compose up -d``

Once you have run this command you can use the tool in your Python script:

```python
>>> from titanis import Titanis
>>>
>>> tt = Titanis(psy_cues=True, psy_cues_normalization='words',
                 psy_dict=True, psy_dict_normalization='abs',
                 syntax=True,
                 discourse=False, discourse_long_texts_only=True,
                 frustration_clf=True)  # use host='remote_host' if the containers are running on a remote server
>>>
>>> text = 'Компьютерные игры могут помочь молодым людям приобрести важные для жизни навыки, хотя в чрезмерном увлечении ими есть и риски.'
>>> result = tt(text)
```
