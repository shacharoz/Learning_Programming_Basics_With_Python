import sys; sys.dont_write_bytecode = True

from app import app as application

if __name__ == '__main__':
    application.run(debug=True, port=80)
