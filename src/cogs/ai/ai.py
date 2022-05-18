import random
import asyncio

import torch
import discord
from discord.ext import commands
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "microsoft/DialoGPT-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

async def generate_bot_responses(text: str) -> list[str]:
    return_choices = []

    # 1
    input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
    bot_input_ids = input_ids
    chat_history_ids = model.generate(
        input_ids,
        max_length=6942,
        pad_token_id=tokenizer.eos_token_id,
    )
    output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return_choices.append(output)

    # # 2
    # bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1)
    # chat_history_ids = model.generate(
    #     bot_input_ids,
    #     max_length=6942,
    #     num_beams=3,
    #     early_stopping=True,
    #     pad_token_id=tokenizer.eos_token_id
    # )
    # output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    # return_choices.append(output)

    # # 3
    # bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1)
    # chat_history_ids = model.generate(
    #     bot_input_ids,
    #     max_length=6942,
    #     do_sample=True,
    #     top_k=0,
    #     pad_token_id=tokenizer.eos_token_id
    # )
    # output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    # return_choices.append(output)

    # # 4
    # bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1)
    # chat_history_ids = model.generate(
    #     bot_input_ids,
    #     max_length=6942,
    #     do_sample=True,
    #     top_k=0,
    #     temperature=0.75,
    #     pad_token_id=tokenizer.eos_token_id
    # )
    # output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    # return_choices.append(output)

    # # 5
    # bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1)
    # # generate a bot response
    # chat_history_ids = model.generate(
    #     bot_input_ids,
    #     max_length=6942,
    #     do_sample=True,
    #     top_k=100,
    #     temperature=0.75,
    #     pad_token_id=tokenizer.eos_token_id
    # )
    # output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    # return_choices.append(output)

    # # 6
    # bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1)
    # chat_history_ids = model.generate(
    #     bot_input_ids,
    #     max_length=6942,
    #     do_sample=True,
    #     top_p=0.95,
    #     top_k=0,
    #     temperature=0.75,
    #     pad_token_id=tokenizer.eos_token_id
    # )
    # output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    # return_choices.append(output)

    return return_choices



async def get_response(text):
    choices = await generate_bot_responses(text)
    choice = random.choice(choices) 
    return choice
    


class AI(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.slash_command(name="ai-test", description="Try using the ")
    async def ai_test(self, ctx, *, text: str):
        await ctx.defer()
        choice = await get_response(text)
        await ctx.respond(f"You: {text}\nWhy: {choice}")


def setup(client):
    client.add_cog(AI(client))

