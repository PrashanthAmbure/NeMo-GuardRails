from nemoguardrails.actions import action
from typing import Optional
from nemoguardrails.actions.llm.utils import llm_call
from nemoguardrails.llm.taskmanager import LLMTaskManager
from langchain_core.language_models.llms import BaseLLM

@action()
async def check_input(llm_task_manager: LLMTaskManager, context: Optional[dict] = None, llm: Optional[BaseLLM] = None):
    user_input = context.get("user_message")
    task = 'check_input'

    if user_input:
        prompt = llm_task_manager.render_task_prompt(
            task=task,
            context={
                "user_input": user_input,
            },
        )
        response = await llm_call(
            llm,
            prompt
        )

        print(f"Input self-checking result is: `{response}`.")
    return True if response.lower() == "yes" else False

@action()
async def check_greeting(llm_task_manager: LLMTaskManager, context: Optional[dict] = None, llm: Optional[BaseLLM] = None):
    user_input = context.get("user_message")
    task = 'check_greeting'

    if user_input:
        prompt = llm_task_manager.render_task_prompt(
            task=task,
            context={
                "user_input": user_input,
            },
        )
        response = await llm_call(
            llm,
            prompt
        )

        print(f"Input self-checking result is: `{response}`.")
    return True if response.lower() == "yes" else False
