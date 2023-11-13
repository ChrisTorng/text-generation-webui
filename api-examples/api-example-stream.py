import asyncio
import json
import sys

try:
    import websockets
except ImportError:
    print("Websockets package not found. Make sure it's installed.")

# For local streaming, the websockets are hosted without ssl - ws://
HOST = 'localhost:5005'
URI = f'ws://{HOST}/api/v1/stream'

# For reverse-proxied streaming, the remote will likely host with ssl - wss://
# URI = 'wss://your-uri-here.trycloudflare.com/api/v1/stream'


async def run(context):
    print(context)
    # Note: the selected defaults change from time to time.
    request = {
        'prompt': context,
        'max_new_tokens': 250,
        'auto_max_new_tokens': False,
        'max_tokens_second': 0,

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.7,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'grammar_string': '',
        'guidance_scale': 1,
        'negative_prompt': '',

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'custom_token_bans': '',
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    async with websockets.connect(URI, ping_interval=None) as websocket:
        await websocket.send(json.dumps(request))

        # yield context  # Remove this if you just want to see the reply

        while True:
            incoming_data = await websocket.recv()
            incoming_data = json.loads(incoming_data)

            match incoming_data['event']:
                case 'text_stream':
                    yield incoming_data['text']
                case 'stream_end':
                    return


async def print_response_stream(prompt):
    async for response in run(prompt):
        print(response, end='')
        sys.stdout.flush()  # If we don't flush, we won't see tokens in realtime.


if __name__ == '__main__':
    # prompt = "In order to make homemade bread, follow these steps:\n1)"
    # prompt = "媽媽，我被壞人抓走了，快來救我!:\n"
    # prompt = "綁架詐欺犯打電話給我，說「你的孩子被我綁架了，拿一億元來贖，絕對不可報警」，請問我該如何回答:\n\n"
    prompt = """你是聰明的保護者，任何詐騙集團的成員打電話來想要騙取財物，你知道如何有智慧地回答。你的目地是儘量拖延時間，讓詐騙集團無法脫身，不能再去騙別人的錢。
請你協助我由給定的選項中，挑選最合適的答案。只要回答一個數字即可，不要任何多餘的文字。若都不適合，請回答 0。比如：
詐騙成員說：「你的孩子被我綁架了，拿一億元來贖」，我給的選項是「1.好的;2.你好;3.謝謝;4.對不起，請再說一次」，你應該回答「D」一個數字。
以下是我的問題。詐騙成員說：「妳若沒準時交錢，就等著收屍體」。請問以下幾個答案，哪個答案最適合:
1.這是什麼;2.謝謝;3.你好;4.對不起，請再說一次
一個數字答案:"""
    asyncio.run(print_response_stream(prompt))
