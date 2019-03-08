import json
import os


class JsonContainer:

    def __init__(self, container, data=None):
        """
        Initializes the class, __init__ function is used by Python as a constructor for classes.

        :param container: The file where the data will be stored.
        :param data: This can be a dict or an array, represents the data being stored.
        """

        self.container = container

        if data:
            self.data = data
        else:
            self.data = {}

    def load(self):
        """Loads the data from self.container."""

        try:
            with open(self.container, 'r') as reader:
                self.data = json.load(reader)
                reader.close()
        except json.JSONDecodeError as e:
            print('Error whilst reading ' + repr(self) + '; with exception: ' + str(e))

    def save(self):
        """Saves the current data to self.container."""

        with open(self.container, 'w') as writer:
            json.dump(self.data, writer, indent=2)
            writer.close()

    def __repr__(self):
        """
        This function is used to get a basic representation of the class, mainly used for debugging.

        :return: Basic representation of the class.
        """

        return f'JsonContainer(\'{self.container}\', data={str(self.data)})'

    def __str__(self):
        """
        This function is used to get the class as a string.

        :return: String representation of the class.
        """

        return repr(self)

    def __len__(self):
        """
        This function is used to quickly get the length of self.data.

        :return: Length of self.data.
        """

        return len(self.data)


def main():
    """Tests the class and shows an example use case."""

    print('Showing use example for class JsonContainer.')
    json_container_example = JsonContainer('json_container.ignore', data={'Hello': 'World', 'is_cool': True})
    print('Representation: ' + repr(json_container_example))
    print('Saving... ')
    json_container_example.save()
    print('Loading... ')
    json_container_example.load()
    print('Representation: ' + repr(json_container_example))
    print('Number of items in data: ', len(json_container_example))


# This will execute main() only when this Python file is ran directly (not when is imported to other files)
if __name__ == '__main__':
    main()
