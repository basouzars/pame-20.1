class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../data-dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = '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'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    JWT_SECRET_KEY = 'p4m32o2o.i' 