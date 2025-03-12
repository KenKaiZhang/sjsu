# AutoManual: Constructing Instruction Manuals by LLM Agents via Interactive Environmental Learning

**[Original Paper](https://papers.nips.cc/paper_files/paper/2024/file/0142921fad7ef9192bd87229cdafa9d4-Paper-Conference.pdf)**

## Terms

**episode** : an iteration of the agent doing a task?

**online manner** : real time

**trajectory** results from the Planner

## Abstract

Categorizes environmental knowledge into diverse rules and optimizes them in a n online fashion

- Planner : codes actionable plans based on rules for interacting with environments
- Builder : updates the rules through rule system that facilitates online rule management and essential detail retention
- Formulator : complies rules into human-readable manual

**case-conditioned prompting** : input prompt is adapted based on different cases or conditions

## Introduction

Problem : When navigating through a new environment, agents tend to directly use saved skills as in-context examples, leading to **path dependence**

- agent blindly replicates the paths of previous success, failing to adapt to new scenarios

Solution : AutoManual

1. An observation + task is given to an episode
2. Planner will create free-form code as an actionable plan
3. Planner will use code to interact with the environment
4. Based on trajectory, Builder will update relevant rules 
5. Formulator categorizes the rules according to their application
6. Formulator compiles a Markdown manual

Contributions:

- Adopt actionable code to let Planner interact with environment
- Structured rule system allowing Builder to manage knowledge
- Alternate process between Planner and Builder to optimize rules in an online manner
- Builder is guided by a case-conditioned prompting strategy

## Methods

### Planner

Planner will generate code necessary for curren environmental situation

- system prompts
- current rules
- relevant samples from skill and reflection libraries
- target task
- initial observations

Code outputted will be in 4 segments :

1. Analysis : understanding of the current situation and reflection on previous errors if exist
2. Related Rules : Rules (along with their IDs) that need to be considered in this situation.
3. Overall Plan : general plan to complete the task
4. Code : Python code divided into steps
    - has helpful functions in case of reuse

When Planner interacts with the environment with its code, it will generate a conclusion that will be saved to the skill/reflection library

- Direct success : code is saved as code block in **skill library**
- Indirect success : code is saved as code block along with summary of mistakes that led to error into **skill library**
- Failure : code segment and a conclusion is saved to **reflection library**
    - **conclusion** : why code failed and possible fixes


Code block will be reused based on task type

## Builder

**Rule System** : "knowledge" that will be considered when Planner builds a solution

Each rule contains :

- Rule type :
    - Special Phenomenon
    - Special Mechanism
    - Useful Helper Method
    - Success Process
    - Corrected Error
    - Unsolved Error
- Rule content : rule description and scope of its applications
- Example : example code from trajectory demonstrating rule
- Validation logs : track the rule's application and updates
    - episode
    - rule IDs
    - evolution

A Consolidator agent is used to delete redundant rules when too many rules in Rule System

## Formulator

Rules are categorized based on target scenarios

Each category gets :

- introduction
- summary of rules
- key points
- overall principle that governs the scenario