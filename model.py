# -*- coding: utf-8 -*-
#########################################################
# python
import os
import traceback
import json
# third-party

# sjva 공용
from framework.logger import get_logger
from framework import db, app, path_app_root
# 패키지


# 로그
package_name = __name__.split('.')[0]
logger = get_logger(package_name)

if app.config['config']['run_by_real']:
    #dir_name = os.path.dirname(__file__)
    #db_file = os.path.join(dir_name, '%s.db' % package_name)
    db_file = os.path.join(path_app_root, 'data', 'db', '%s.db' % package_name)
    app.config['SQLALCHEMY_BINDS'][package_name] = 'sqlite:///%s' % (db_file)



class ModelSetting(db.Model):
    __tablename__ = 'plugin_%s_setting' % package_name
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    __bind_key__ = package_name

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String, nullable=False)
 
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return repr(self.as_dict())

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


    @staticmethod
    def get(key):
        try:
            return db.session.query(ModelSetting).filter_by(key=key).first().value.strip()
        except Exception as e:
            logger.error('Exception:%s %s', e, key)
            logger.error(traceback.format_exc())

#########################################################

