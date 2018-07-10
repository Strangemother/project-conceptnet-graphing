# Intonation and peak detection

I called this the Startrek lift as it's exactly the aim for this part of the project. Todays audio equipment and software is excellent at detecting voices in a loud environment. I remember testing Google voice search in a rock concert and was pleasantly surprised by the accuracy.

In the case of the turbo-lift it has the ability to understand _when_ it's being referred to rather than simply hearing "hot words". This allows someone to _said_ words during a conversation without affecting the lifts functionality. So how is this done? I asked myself.

Firstly I feel this can be achieved without ML - or perhaps 16 nodes and 4 layers is totally enough. I think I've seen; much of this can be done with simple audio processing of existing technologies and FFT peak fiddling.


To note some of the 'detection' requirements - based upon the Turbo lift.

+ Understand flat commands without prompt... "Deck four"
+ Capture with hot word "Computer go to deck six"
+ Hotword include "halt [lift]", "stop",



### Capture on

+ intonation gaps
+ paused hotwords
+ hotword wait?


Noting some citations from the program and general day to day of the talking to computer, certain pattern from an operator (human speech) to detect direct communication. Some are unavailable in the current architecture but we'll cover them anyway.

For the research, we'll only consider the turbo-lift - but this as application a range of general interactive places.

    Input: User Speech
        OP, Operator, User, Human
    Output: Text to Speech
        CTX (context machine), machine, system, computer
    Focus Result: Graphing Results
        Generated result objects

We'll focus on speech strings, or Temporal String graphs - a mud of words without grammar.

    ... and then I left about midnight hello computer floor three please and I said to him I'll see you later at two near the top...

In this case half-way through a conversation the CTX is addressed as 'computer'. Cleaned up:

    .... [and then I left about midnight] "hello computer, *floor three* please" [and I said to ...

The unnecessary content in brackets; the real action "floor three" could be detected via 'hot-word' _floor_, but the remaining content container "two" and "the top". They are also acceptable hot words

Our cases focus on this type of input.


## Initial and direct.

Initially entering the _turbo lift_ alone a user will state the intent and stay silent. This is the best case, as it's easy to extrapolate.


    [computer] floor three
    deck six [please]
    forty third floor


Any combination of the above. Through silence before and after - The system operation can focus on floor graphs.
Sound detection is done through a hardware level and simple TTS Stream as temporal strings provide input.


## Pause Direct

In our main case above the user has another conversation as they enter and after a brief moment they pause the conversation and communicate directly to the system. This occurs with two people entering or one person personal (on a phone for example).

For this the capture by initial and direct may not occur as there will be no pause in the temporal stream. However the operator may pause for a longer period before addressing another entity

    [I prepared for a winter trip to] floor 8 [alaska whilst listening to pink floyd]


_As a helper (I find this silly to) I find saying this out-loud to a pseudo device. You'll easily here your pitch and intonation change when referencing a 'computer' than communicating to another._

When referring to a third-party - external to the current conversation or context - a person tends to pause for a longer period than their average breath.

In a study by Donders Institute[1] we find the average response time for a breath is less than a second. Anything over that is a context switch and we can conceptualize from this[2]. This is of course a gross over-simplification but for now it'll serve.

    I prepared for a winter trip to [pause > 1s] floor 8 [pause*B > 1s] alaska ...

The initial pause delay should be equated from the last X seconds median of pauses within the ^initial contact. Therefore a more accurate average of the current context pausing can be used.

The second pause requires more than half a second[2] [3]; at which point a user will continue their own conversation.


A user will pause, speak, pause and continue with a pitch and intonation change.  Detecting a volume and pitch change - and potentially a _direction_ the system can extrapolate a temporal stream for graphing; "floor three"


### Direct

A user may directly refer to the system before a command. this is easier to monitor through hot-words: "computer floor three". However someone may mention those words through general conversation.

Combining Pause Direct with the intonation detection should serve well-enough. The hot-word "computer" (or any associated graph) the system and assert the immediate string "floor three".


### Noisy Environments

In areas with a lot of background noise the same Capture and Pause Direct, procedures work. With ambient level detection the system can assess the average volume of a general converation or background. General noise is about 75db. Monitoring anything above this for Pause Direct should work. Mostly relying upon volumn change for a simple statement greater than 10db of the average.




Breathing in Conversation: an Unwritten History
Marcin Włodarczak, Mattias Heldner
Department of Linguistics
Stockholm University
Stockholm, Sweden
{wlodarczak,heldner}@ling.su.se

Jens Edlund
Speech, Music and Hearing
KTH Royal Institute of Techonology
Stockholm, Sweden
edlund@speech.kth.se

https://www.diva-portal.org/smash/get/diva2:892585/FULLTEXT01.pdf



[1] https://www.frontiersin.org/articles/10.3389/fpsyg.2015.00284/full#h4
[1.b] https://www.frontiersin.org/articles/10.3389/fpsyg.2015.00284/full#h5

    ORIGINAL RESEARCH ARTICLE
    Front. Psychol., 12 March 2015 | https://doi.org/10.3389/fpsyg.2015.00284
    Breathing for answering: the time course of response planning in conversation
    Francisco Torreira1, Sara Bögels1 and Stephen C. Levinson1,2
    1Language and Cognition Department, Max Planck Institute for Psycholinguistics, Nijmegen, Netherlands
    2Donders Institute for Brain, Cognition and Behaviour, Radboud University, Nijmegen, Netherlands



[2] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4240966/

    Philos Trans R Soc Lond B Biol Sci. 2014 Dec 19; 369(1658): 20130399.
    doi:  10.1098/rstb.2013.0399
    PMCID: PMC4240966
    PMID: 25385777
    Take a breath and take the turn: how breathing meets turns in spontaneous dialogue
    Amélie Rochet-Capellan1 and Susanne Fuchs2



[3] http://www.speech.kth.se/prod/publications/files/3418.pdf

    Pauses, gaps and overlaps in conversations
    Mattias Heldner , Jens Edlund
    KTH Speech, Music and Hearing, Lindstedtsvagen 24, SE-100 44 Stockholm, Sweden



http://www.aclweb.org/anthology/W96-0418

    Matchmaking: dialogue modelling and speech generation meet*
    Brigitte Grote
    FAW Ulm
    Germany
    Eli Hagen
    GMD/IPSI, Darmstadt and
    Technical University of Darmstadt
    Germany
    Elke Teich
    University of tile Saarland
    Department of Applied Linguistics, Translation and Interpretation
    Germany



https://www.frontiersin.org/articles/10.3389/fpsyg.2012.00376/full#h4

Prediction of turn-ends based on anticipation of upcoming words
Lilla Magyari1* and J. P. de Ruiter2
1Language and Cognition Department, Max Planck Institute for Psycholinguistics, Nijmegen, Netherlands
2Faculty of Linguistics and Literary Studies, University of Bielefeld, Bielefeld, Germany
