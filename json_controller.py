import json

with open('test.txt', 'w') as writer:
    json.dump({'hello': 'world'}, writer)
    writer.close()

with open('test.txt', 'r') as reader:
    print(json.load(reader))
    reader.close()