from app import create_app
from app.models import db

app = create_app('DevelopmentConfig')








with app.app_context():
        db.create_all() 



app.run(host='0.0.0.0', port=5001, debug=True)    
