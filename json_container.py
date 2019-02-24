import json


class JsonContainer:

    def __init__(self, container, data=None):
        self.container = container
        if data is None:
            self.data = {}
        else:
            self.data = data

    def load(self):
        try:
            with open(self.container, 'r') as reader:
                self.data = json.load(reader)
                reader.close()
        except json.JSONDecodeError as e:
            print('Error whilst reading ' + repr(self) + '; with exception: ' + str(e))

    def save(self):
        with open(self.container, 'w') as writer:
            json.dump(self.data, writer)
            writer.close()

    # def get_data(self):
    #     return self.json_obj
    #
    # def set_data(self, json_obj):
    #     self.json_obj = json_obj

    def __repr__(self):
        return f'JsonContainer(\'{self.container}\', data={str(self.data)})'

    # def __str__(self):
    #     return repr(self)

    def __len__(self):
        return len(self.data)


def main():
    print('Showing use example for class JsonContainer.')
    json_container_example = JsonContainer('json_container.tmp', data={'Hello': 'World', 'is_cool': True})
    print('Representation: ' + repr(json_container_example))
    print('Saving... ')
    json_container_example.save()
    print('Loading... ')
    json_container_example.load()
    print('Representation: ' + repr(json_container_example))


if __name__ == '__main__':
    main()
