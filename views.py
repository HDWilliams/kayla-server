from app import app 
from flask import jsonify

@app.route('/')
def home():
  return jsonify({
    'message': 'Hello'
  })

if __name__ == "__main__":
  app.run()