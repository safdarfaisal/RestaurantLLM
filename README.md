# RestaurantLLM
A proof of concept for an FSM based model of a restaurant reception system

![FSM model](https://github.com/safdarfaisal/RestaurantLLM/assets/56080226/1d743a28-92e1-4e4e-89fd-a08dbf372b5f)

## Quick Start

The PoC uses the Gemma system of models and is configured to run on a CPU. 

It uses the following libraries
 - transitions
 - transformers
 - torch

Installing these libraries should be enough to run the PoC itself, the model is 5 gigabytes in size and is installed during runtime when run for the first time.

It currently has a fixed input as it was meant to show the initial decision flow being decided using an intent analyser.
