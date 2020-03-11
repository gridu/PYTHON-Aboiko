from application import create_app

production_configs = 'settings.Config'
app = create_app(production_configs)


if __name__ == "__main__":
    app.run(debug=True)
