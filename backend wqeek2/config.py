class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Sageyk01!2024@localhost/mechanic_shop'
    debug = True
    
class TestingConfig:
    pass

class ProductionConfig:
    pass