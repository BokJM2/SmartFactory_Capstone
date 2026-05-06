import json

total = 0
for id in range(1, 56):
    with open(f'../../outputs/gpt35/{id}.json', 'r', encoding='utf-8') as file:
        question = json.load(file)
        total += int(question["tokens"]["total_tokens"])
print(total)
