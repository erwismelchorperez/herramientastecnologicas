from app import create_app
# comando apra inicar en servidor local
# gunicorn --bind 0.0.0.0:5000 run:app

"""
    estos son los comandos para iniciarlo de manera local
    
    flask run --host=0.0.0.0 --port=5001 --debug
"""
app = create_app()

print(app.url_map)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
    