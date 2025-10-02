
# NeMo Guardrails Custom Actions

This repository demonstrates how to implement **custom actions** in [NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/latest/getting-started/overview.html). Actions allow you to define asynchronous Python functions that can be invoked by your conversational AI flows to perform tasks such as input validation, greeting checks, or any custom logic you need.

## What Are Actions?

In NeMo Guardrails, **actions** are Python functions decorated with `@action()` that can:

- Execute custom logic asynchronously.
- Access the conversation context.
- Interact with an LLM if needed.
- Return a value that can influence the flow of the conversation.

Actions are typically used in **flows** defined in `colang` or `config.yml` to validate user inputs, check conditions, or call external APIs.

## Implementation Example

This project includes two example actions:

### 1. `check_input`

Validates user input based on a self-check task defined in your prompts.

```python
@action()
async def check_input(llm_task_manager, context=None, llm=None):
    user_input = context.get("user_message")
    task = 'check_input'

    if user_input:
        prompt = llm_task_manager.render_task_prompt(
            task=task,
            context={"user_input": user_input},
        )
        response = await llm_call(llm, prompt)
        print(f"Input self-checking result is: `{response}`.")
    return True if response.lower() == "yes" else False
```

### 2. `check_greeting`

Checks whether the user input is a greeting.

```python
@action()
async def check_greeting(llm_task_manager, context=None, llm=None):
    user_input = context.get("user_message")
    task = 'check_greeting'

    if user_input:
        prompt = llm_task_manager.render_task_prompt(
            task=task,
            context={"user_input": user_input},
        )
        response = await llm_call(llm, prompt)
        print(f"Greeting self-checking result is: `{response}`.")
    return True if response.lower() == "yes" else False
```

## How Actions Are Used

1. Actions are imported into your `rails` configuration and registered with `@action()`.
2. In your `colang` flows or `config.yml`, you can call these actions with:

```colang
define flow check input
  $allowed = execute check_input
  if not $allowed
    bot refuse to respond
    stop
```

3. The result of an action (`True` or `False`) can control the conversation flow, enabling dynamic and intelligent responses.

## Files in This Project

- `actions.py` – Contains all custom actions.
- `config.yml` – Configuration for your NeMo Guardrails setup.
- `prompts.yml` – Contains prompts used for LLM self-checking tasks.
- `rails.co` – Flow definitions connecting actions with the conversation.
