# -*- coding: utf-8 -*-
#########################################################
# python
import os
import sys
import traceback
import logging

# third-party
import json
import urllib

# sjva 공용
from framework import db, scheduler
from framework.job import Job
from framework.util import Util

# 패키지
import system
from .model import ModelSetting

import time
from datetime import datetime

package_name = __name__.split('.')[0]
logger = logging.getLogger(package_name)
#########################################################


class Logic(object):
    db_default = {}

    @staticmethod
    def db_init():
        try:
            for key, value in Logic.db_default.items():
                if db.session.query(ModelSetting).filter_by(key=key).count() == 0:
                    db.session.add(ModelSetting(key, value))
            db.session.commit()
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())

    @staticmethod
    def plugin_load():
        try:
            logger.debug('%s plugin_load', package_name)
            
            try:
                import shutil
                from framework import path_app_root
                db_file = os.path.join(path_app_root, 'data', 'db', '%s.db' % package_name)
                plugin_folder = os.path.join(path_app_root, 'data', 'custom', package_name)
                os.remove(db_file)
                shutil.rmtree(plugin_folder)
            except:
                pass
            
            # Logic.db_init()

            # from plugin import plugin_info
            # Util.save_from_dict_to_json(plugin_info, os.path.join(os.path.dirname(__file__), 'info.json'))
        except Exception as e:
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())

    @staticmethod
    def plugin_unload():
        try:
            logger.debug('%s plugin_unload', package_name)
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())

    @staticmethod
    def setting_save(req):
        try:
            for key, value in req.form.items():
                logger.debug('Key:%s Value:%s', key, value)
                entity = db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
                entity.value = value
            db.session.commit()
            return True                  
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())
            return False

    @staticmethod
    def get_setting_value(key):
        try:
            return db.session.query(ModelSetting).filter_by(key=key).first().value
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())

    ##################################################################
