from website import create_app

# creating instance for create_app() function
app = create_app()

if __name__ == '__main__':
    # to start the server
    app.run(debug = True)