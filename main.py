from transitions import Machine, State

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

hf_access_token  = "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"

tokenizer = AutoTokenizer.from_pretrained("google/gemma-1.1-2b-it", token = hf_access_token)
model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-1.1-2b-it",
    torch_dtype=torch.bfloat16,
    token = hf_access_token
    )


def get_response_from_user():
    return input()

system_prompt = "You are a professional receptionist"

def call_llm(prompt : str, secondary_prompt : str = "") -> str:
    # user_input = get_response_from_user()
    user_input = "Are there seats available?"
    prompt = prompt + user_input
    inputs = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(inputs, max_new_tokens=150)
    val = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    print(val)
    val = str(val).replace(prompt,"")
    return val

import re

def parse_keywords(response : str) -> str:
    m = re.search('\*([^*]+)\*', response)
    return str(m).lower()

class Diagram:
    diagramStates = [
        State(name='start'),
        State(name='introduction', on_enter=['introduction']), 
        State(name='enquiry', on_enter=['enquiry']), 
        State(name='reserve', on_enter=['reserve']), 
        State(name='escalate', on_enter=['escalate']), 
        State(name='complete', on_enter=['complete']) 
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=Diagram.diagramStates, initial='start')
        self.machine.add_transition('move_to_introduction', 'start', 'introduction')
        self.machine.add_transition('move_to_reserve', 'introduction', 'reserve')
        self.machine.add_transition('move_to_enquiry', 'introduction', 'enquiry')
        self.machine.add_transition('escalate', 'introduction', 'escalate')
        self.machine.add_transition('escalate', 'enquiry', 'escalate')
        self.machine.add_transition('escalate', 'reserve', 'escalate')
        self.machine.add_transition('complete', 'reserve', 'complete')
        self.machine.add_transition('complete', 'enquiry', 'complete')
        self.move_to_introduction()

    def introduction(self):
        print('intro reached')
        prompt = """Determine if the response provided is a request for a reservation or if it is an enquiry. If it is a reservation, end with *reserve*. If it is an enquiry, end with *enquiry*. """
        output_val = call_llm(prompt=prompt)
        keyword = parse_keywords(output_val)
        if "enquiry" in keyword:
            self.move_to_enquiry()
        else:
            if "reserve" in keyword:
                self.move_to_reserve()
            else:
                self.escalate()
    def reserve(self):
        print("reservation process ... ...")
        self.complete()
    def enquiry(self):  
        print("enquiry process ... ...")
        self.complete()
    def escalate(self):
        print("issue escalated")
    def complete(self):
        print("contact completed")

# actionState = ActionableStates()
# diagramStates = [
#     State(name='Start'),
#     State(name='Introduction', on_enter=['introduction']), 
#     State(name='Enquiry'), 
#     State(name='Reserve'), 
#     State(name='Escalate'), 
#     State(name='Complete') 
#     ]

diagram = Diagram()
