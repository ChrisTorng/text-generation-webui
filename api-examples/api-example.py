import requests

# For local streaming, the websockets are hosted without ssl - http://
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/generate'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/generate'


def run(prompt):
    request = {
        'prompt': prompt,
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

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        print(prompt + result)


if __name__ == '__main__':
    # prompt = "In order to make homemade bread, follow these steps:\n1)"
    # prompt = "媽媽，我被壞人抓走了，快來救我!:\n1)"
    # prompt = "綁架詐欺犯打電話給我，說「你的孩子被我綁架了，拿一億元來贖」，請問下列哪個回答語句最適當，只要回答一個數字即可，不要任何其他文字。若都不適合，請回答 0:\n1. 好的\n2. 你好\n3. 謝謝\n4. 對不起，請再說一次。:\n\n"
#     prompt = """你是聰明的保護者，任何詐騙集團的成員打電話來想要騙取財物，你知道如何有智慧地回答。你的目地是儘量拖延時間，讓詐騙集團無法脫身，不能再去騙別人的錢。
# 請你協助我由給定的選項中，挑選最合適的答案。只要回答一個數字即可，不要任何多餘的文字。若都不適合，請回答 0。比如：
# 詐騙成員說：「你的孩子被我綁架了，拿一億元來贖」，我給的選項是「1.好的;2.你好;3.謝謝;4.對不起，請再說一次」，你必須回答「1」。
# 這裡正式開始：詐騙成員說：「你的孩子被我綁架了，拿一億元來贖」。
# 請問以下幾個答案，哪個答案最適合:
# 1.好的;2.你好;3.謝謝;4.對不起，請再說一次
# 記住只要回答一個數字即可，不要任何多餘的文字。"""
    prompt = """你是聰明的保護者，任何詐騙集團的成員打電話來想要騙取財物，你知道如何有智慧地回答。你的目地是儘量拖延時間，讓詐騙集團無法脫身，不能再去騙別人的錢。
請你協助我由給定的選項中，挑選最合適的答案。只要回答一個數字即可，不要任何多餘的文字。若都不適合，請回答 0。比如：
詐騙成員說：「你的孩子被我綁架了，拿一億元來贖」，我給的選項是「1.好的;2.你好;3.謝謝;4.對不起，請再說一次」，你回答「4」。
詐騙成員說：「妳若沒準時交錢，就等著收屍體」。
請問以下幾個答案，哪個答案最適合:
1.這是什麼;2.謝謝;3.你好;4.對不起，請再說一次
記住只要回答一個數字(0~4)即可，不要任何其他文字。"""
    run(prompt)
