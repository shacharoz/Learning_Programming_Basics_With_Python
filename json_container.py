import json


class JsonContainer:

    #container is our file name
    #initialize the class
    def __init__(self, container, data=None):
        self.container = container
        if data:
            self.data = data
        else:
            self.data = {}

    #loads the database from the file
    def load(self):
        try:
            with open(self.container, 'r') as reader:
                self.data = json.load(reader)
                reader.close()
        except json.JSONDecodeError as e:
            print('Error whilst reading ' + repr(self) + '; with exception: ' + str(e))

    #saves the current data into the file
    def save(self):
        with open(self.container, 'w') as writer:
            json.dump(self.data, writer)
            writer.close()

    #similar to string. great for debug
    def __repr__(self):
        return f'JsonContainer(\'{self.container}\', data={str(self.data)})'

    #prints the class values
    def __str__(self):
        return repr(self)

    #return number of items in json.data
    def __len__(self):
        return len(self.data)


#tests the class
def main():
    print('Showing use example for class JsonContainer.')
    json_container_example = JsonContainer('json_container.ignore', data={'Hello': 'World', 'is_cool': True})
    print('Representation: ' + repr(json_container_example))
    print('Saving... ')
    json_container_example.save()
    print('Loading... ')
    json_container_example.load()
    print('Representation: ' + repr(json_container_example))
    print('Number of items in database: ' + str(len(json_container_example)))


#execute this command when running the file directly
if __name__ == '__main__':
    main()
