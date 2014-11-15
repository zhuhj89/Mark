# -*- coding: utf-8 -*-
"""
  the flow manage view
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-9-01"

from flask import Blueprint, render_template,request,url_for,jsonify,Module
from app.models.flow import Flow
from app.models.flow_node import FlowNode
from app.models.flow_link import FlowLink
from app.models.flow_node_auditer import FlowNodeAuditer
from app.models.role_info import RoleInfo
from app.models.user_info import UserInfo
from app.extensions import db
import json
from sqlalchemy import and_
from sqlalchemy.orm import  eagerload
import datetime

flow = Blueprint('flow', __name__)

@flow.route('/show')
@flow.route('/show/<flow_id>')
def show_flow(flow_id=''):
    print "*"*100
    print flow_id
    flow = None
    if flow_id:
        flow = Flow.query.get(flow_id)
    return render_template('/flow/flow_show.html', flow=flow)

@flow.route('/save', methods=['GET', 'POST'])
def save_flow():

    if request.method == 'POST':

        flow_id = request.form['flow_id']
        flow_name = request.form['flow_name']
        flow_desc = request.form['flow_desc']

        if flow_id is None or flow_id == '':
            flow = Flow()
            flow_node = FlowNode()
            flow.flow_desc = flow_desc
            flow.flow_name = flow_name
            flow.flow_code = '001'
            db.session.add(flow)
            db.session.flush()
            flow_node.flow_id = flow.flow_id
            flow_node.flow_node_name = '流程开始'
            flow_node.flag = '1'
            db.session.add(flow_node)
        else:
            flow = Flow.query.get(flow_id)
            flow.flow_name = flow_name
            flow.flow_desc = flow_desc
            db.session.merge(flow)
        db.session.commit()

    return 'save ok'


# @mod.route('/select', methods=['GET', 'POST'])
# def slect_flow():
#     if request.method == 'GET':
#         flow_list = Flow.query.all()
#         return render_template('/flow/select_flow.html', flow_list=flow_list)
#
# @mod.route('/select_node_show')
# def select_node_show():
#
#     flow_id = request.args.get("flow_id")
#     if flow_id != '':
#
#         flow_nodes = FlowNode.query.filter(FlowNode.flow_id == flow_id).order_by(FlowNode.flow_node_id).all()
#         return render_template('/flow/save_node.html', flow_nodes=flow_nodes, flow_id=flow_id)

@flow.route('/save_node', methods=['GET', 'POST'])
def save_flow_node():
    if request.method == 'GET':
        conn = db.engine.connect()
        nodes_result = conn.execute("select b.flow_name, a.flow_node_id, a.flow_node_name  \
                        from flow_node a,flow b where a.flow_id=b.flow_id ORDER BY a.flow_id,a.flow_node_id")
        return render_template('/flow/save_node.html', nodes=nodes_result)
    if request.method == 'POST':

        p_node_id = request.form['previous_node']
        p_node = FlowNode.query.get(p_node_id)

        node = FlowNode()
        node.flow_id = p_node.flow_id
        node.flow_node_name = request.form['node_name']
        node.flow_node_desc = request.form['node_desc']
        node.flag = '0'
        db.session.add(node)
        db.session.flush()

        flow_link = FlowLink()
        flow_link.flow_id = p_node.flow_id
        flow_link.previous_node_id = request.form['previous_node']
        flow_link.next_node_id = node.flow_node_id
        db.session.add(flow_link)
        db.session.commit()
        return "save ok"


@flow.route('/save_node_audter', methods=['GET', 'POST'])
def save_node_auditer():

    if request.method == 'GET':
        conn = db.engine.connect()
        nodes_result = conn.execute("select b.flow_name, a.flow_node_id, a.flow_node_name  \
                        from flow_node a,flow b where a.flow_id=b.flow_id ORDER BY a.flow_id,a.flow_node_id")
        users = UserInfo.query.filter(UserInfo.role_id == 1).all()
        print users
        return render_template("/flow/save_node_auditer.html", nodes=nodes_result, users=users)
    if request.method == 'POST':
        dict_form = dict(request.form)
        for user_id in dict_form['user_ids']:

            node_auditer = FlowNodeAuditer()
            node_auditer.user_id = user_id
            node_auditer.flow_node_id = request.form['flow_node_id']
            db.session.add(node_auditer)
            db.session.commit()
        return 'save node auditer ok'










