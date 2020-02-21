# -*- coding: utf-8 -*-
#########################################################
# 고정영역
#########################################################
# python
import os
import sys
import traceback

# third-party
from flask import Blueprint, request, Response, render_template, redirect, jsonify
from flask_login import login_required

# sjva 공용
from framework.logger import get_logger
from framework import app, db, scheduler
from framework.util import Util
from system.logic import SystemLogic
            
# 패키지
from .logic import Logic
from .model import ModelSetting

package_name = __name__.split('.')[0]
logger = get_logger(package_name)

blueprint = Blueprint(package_name, package_name, url_prefix='/%s' %  package_name, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

def plugin_load():
    Logic.plugin_load()

def plugin_unload():
    Logic.plugin_unload()

plugin_info = {
    'version' : '0.0.0.3',
    'name' : 'oraclicker',
    'category_name' : 'custom',
    'icon' : '',
    'developer' : 'starbuck',
    'description' : 'oracle clicker',
    'home' : 'https://github.com/starbuck15/oraclicker',
    'more' : 'https://github.com/starbuck15/oraclicker',
    'zip' : 'https://github.com/starbuck15/oraclicker/archive/master.zip'
}
#########################################################

# 메뉴 구성.
menu = {
    'main' : [package_name, 'Oracliker'],
    'sub' : [
        ['log', '로그']
    ],
    'category' : 'custom',
}

#########################################################
# WEB Menu
#########################################################
@blueprint.route('/')
def home():
    return redirect('/%s/log' % package_name)

@blueprint.route('/<sub>')
@login_required
def detail(sub): 
    if sub == 'log':
        return render_template('log.html', package=package_name)
    return render_template('sample.html', title='%s - %s' % (package_name, sub))

#########################################################
# For UI (보통 웹에서 요청하는 정보에 대한 결과를 리턴한다.)
#########################################################
@blueprint.route('/ajax/<sub>', methods=['GET', 'POST'])
def ajax(sub):
    logger.debug('AJAX %s %s', package_name, sub)
    try:
        if sub == 'setting_save':
            try:
                ret = Logic.setting_save(request)
                return jsonify(ret)
            except Exception as e: 
                logger.error('Exception:%s', e)
                logger.error(traceback.format_exc())

    except Exception as e: 
        logger.error('Exception:%s', e)
        logger.error(traceback.format_exc())
#########################################################
# API
#########################################################
@blueprint.route('/api/<sub>', methods=['GET', 'POST'])
def api(sub):
    logger.debug('api %s %s', package_name, sub)
    
