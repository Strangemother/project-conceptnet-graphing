Initial Layers (preliminary)

The core engine is built on a number of independent layers to produce one larger net. Fundamentally the “core” is the main engine for starting. This will provide the booting structure of mandatory elements:

Data IO through a cache and external requests
Input IO for user interaction and piping messages
Main communication method; passing a usable pipe (or address) into a booting net
Net driver to maintain queued communication between threads and start/stop threads/nets when required

The core will boot an initial thread, at the moment this is defined the “knowledge layer” providing the input of preliminary data for the deeper nets performing abstraction. An operator will feed textual input to the knowledge layer. Currently this is through a simple socket or CLI loop.

The knowledge layer accepts words or sentences to gather all IO data from external inputs and generally populate the given information with more knowledge layer attributes. This is inclusive of other words from the cache and any grammar or spelling corrections before submitting to the next layer for contextualization.

After expansion and normalisation the string is a list of unassociated object, populated with knowledge layer data values; antonyms, synonyms and tokenization of the sentence.
