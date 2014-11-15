# -*- coding: utf-8 -*-
""" agent control
"""

__author__ = "XiaoQian"
__email__ = "xiaoqian@cnnic.cn"
__copyright__ = "Copyright 2007, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-18 10:22:57"

import datetime
from conf.config import Page_Count
from flask import Module, render_template, request, flash, url_for, redirect, Blueprint
from flask.ext.login import current_user, login_required
from app.extensions import db
from app.forms.agent import AgentForm, AddAgentForm, UpdateRemindForm
from app.models import AgentInfo, AgentAccountRecord, DomainPayRecord, DomainPrice
import time,datetime

agent = Blueprint('agent', __name__)

@agent.route('/')
@login_required
def agent_index():
    """to index page.

       Returns:
           to index page
    """
    return render_template('base.html')

@agent.route('/add', methods=['GET', 'POST'])
@login_required
def add_agent():
    """to add agent info page.

       Returns:
           to add agent info page
    """
    form = AddAgentForm()
    domain_prices = DomainPrice.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            # add agent info
            agent_name = form.data['agent_name']
            password = form.data['password']
            comp_name = form.data['comp_name']
            email = form.data['email']
            phone = form.data['phone']
            balance_remind = form.data['balance_remind']
            domain_price_id = request.form['domain_price_id']
            url = form.data['url']
            abuse_email = form.data['abuse_email']
            abuse_phone = form.data['abuse_phone']
            ai = AgentInfo()
            ai.agent_name = agent_name
            ai.password = password
            ai.comp_name = comp_name
            ai.email = email
            ai.phone = phone
            ai.balance_remind = balance_remind
            ai.domain_price_id = domain_price_id
            ai.url = url
            ai.abuse_email = abuse_email
            ai.abuse_phone = abuse_phone
            ai.balance = 0.00
            date_now = datetime.datetime.now()
            ai.update_date = date_now
            ai.creator = current_user.id
            ai.create_date = date_now
            db.session.add(ai)
            db.session.commit()
            flash(u'添加成功')
            return redirect(url_for('agent.query_agent_list', agent_name=agent_name))
    return render_template('/agent/add_agent.html', form=form, domain_prices=domain_prices)

@agent.route('/update/<id>/', methods=['GET', 'POST'])
@login_required
def update_agent(id):
    """to update agent info page.

       Args:
            id: agent_info primary key

       Returns:
           to update agent info page
    """
    # get agent_info object
    agent = AgentInfo.query.get(id)
    form = AgentForm(obj=agent)
    if request.method == 'POST':
        if form.validate_on_submit():
            # update agent info
            form.populate_obj(agent)
            agent.update_date = datetime.datetime.now()
            db.session.commit()
            flash(u'修改成功')
            return redirect(url_for('agent.query_agent_list', agent_name=agent.agent_name))
    return render_template('/agent/update_agent.html', form=form, agent=agent)

@agent.route('/using/<id>/<status>/', methods=['GET', 'POST'])
@login_required
def update_using(id, status):
    """update agent using status.

       Args:
            id: agent_info primary key
            status: using status
       Returns:
           index page url
    """
    # get agent_info object
    agent = AgentInfo.query.get(id)
    if status == 'on':
        agent.status = 1
    elif status == 'off':
        agent.status = 2
    db.session.commit()
    flash(u'状态修改成功')
    return redirect(url_for('agent.query_agent_list', agent_name=agent.agent_name))

@agent.route('/list', methods=['GET', 'POST'])
@agent.route('/list/<int:page>/')
@agent.route('/list/<agent_name>/<int:page>/')
@login_required
def query_agent_list(agent_name='', page=1):
    """to agent account page.
      Args:
            agent_name: agent_info name
            page: page
       Returns:
           to agent account page
    """
    # get agent_info list

    domain_prices = DomainPrice.query.all()
    if request.values:
        agent_name = request.values['agent_name'].strip()
    page_obj = AgentInfo.query.filter(AgentInfo.agent_name.like('%%%s%%' % agent_name))\
        .paginate(page, per_page=Page_Count)
    if agent_name:
        page_url = lambda page: url_for('agent.query_agent_list', agent_name=agent_name, page=page)
    else:
        page_url = lambda page: url_for('agent.query_agent_list', page=page)
    return render_template('/agent/agent_list.html', agent_name=agent_name, page_obj=page_obj, page_url=page_url, domain_prices=domain_prices)

@agent.route('/account', methods=['GET', 'POST'])
@login_required
def query_account():
    """to agent account page.

       Returns:
           to agent account page
    """
    agent_name, sdate, edate, in_amount, out_amount = '', '', '', 0, 0
    if request.values:
        agent_name = request.values['agent_name']
        sdate = request.values['sdate']
        edate = request.values['edate']


        if agent_name and sdate and edate:
            sdate_s = time.strptime(sdate,"%Y-%m-%d")
            sdate_d = datetime.datetime(sdate_s[0],sdate_s[1],sdate_s[2])

            edate_s = time.strptime(edate,"%Y-%m-%d")
            edate_d = datetime.datetime(edate_s[0],edate_s[1],edate_s[2]+1)
            q_agent = AgentInfo.query.filter(AgentInfo.agent_name == agent_name).scalar()
            if not q_agent:
                flash(u'注册商不存在')
            else:
                # get agent account record
                aar_list = AgentAccountRecord.query.filter(AgentAccountRecord.agent_id == q_agent.id,
                                                           AgentAccountRecord.create_date >= sdate_d,
                                                           AgentAccountRecord.create_date <= edate_d).all()

                for aar in aar_list:
                    if aar.operate == 1:
                        in_amount += aar.amount
                    elif aar.operate == 2:
                        out_amount += aar.amount
        else:
            flash(u'请选择查询条件')
    return render_template('/agent/query_account.html', agent_name=agent_name, sdate=sdate, edate=edate,
                           in_amount='%.2f' % in_amount, out_amount='%.2f' % out_amount)

@agent.route('/pay-detail/<int:page>/', methods=['GET', 'POST'])
@agent.route('/pay-detail/<agent_name>/<sdate>/<edate>/<int:page>/', methods=['GET', 'POST'])
@agent.route('/pay-detail', methods=['GET', 'POST'])
@login_required
def query_pay_detail(agent_name='', sdate='', edate='', page=1):
    """to pay detail page.

       Returns:
           to pay detail page
    """
    # get agent_info object
    page_count = 3
    if request.values:
        # get pay detail list
        agent_name = request.values['agent_name']
        sdate = request.values['sdate']
        edate = request.values['edate']
        print agent_name,sdate,edate
    if agent_name and sdate and edate:
        sdate_s = time.strptime(sdate,"%Y-%m-%d")
        sdate_d = datetime.datetime(sdate_s[0],sdate_s[1],sdate_s[2])

        edate_s = time.strptime(edate,"%Y-%m-%d")
        edate_d = datetime.datetime(edate_s[0],edate_s[1],edate_s[2]+1)
        q_agent = AgentInfo.query.filter(AgentInfo.agent_name == agent_name).scalar()
        if not q_agent:
            flash(u'注册商不存在')
        else:
            page_obj = DomainPayRecord.query.filter(DomainPayRecord.agent_id == q_agent.id,
                                                    DomainPayRecord.create_date >= sdate_d,
                                                    DomainPayRecord.create_date <= edate_d)\
                .paginate(page, per_page=page_count)

            if not page_obj.items:
                flash(u'没有消费记录')
            page_url = lambda page: url_for('agent.query_pay_detail',agent_name=agent_name, sdate=sdate,
                                            edate=edate, page=page)
            return render_template('/agent/query_pay_detail.html', agent_name=agent_name, sdate=sdate,
                                   edate=edate, page_obj=page_obj, page_url=page_url)
    else:
        flash(u'请选择查询条件')

    return render_template('/agent/query_pay_detail.html', agent_name=agent_name, sdate=sdate, edate=edate)

@agent.route('/update-remind/<id>/', methods=('GET', 'POST'))
@login_required
def update_remind(id):
    """to update balance remind page.

       Args:
            id: agent_info primary key

       Returns:
           to update balance remind page
    """
    # get agent_info object
    agent = AgentInfo.query.get(id)
    form = UpdateRemindForm(agent_name=agent.agent_name, balance_remind=agent.balance_remind)
    if request.method == 'POST':

        if form.validate_on_submit():

            # operate update
            agent.balance_remind = float(form.balance_remind.data)
            agent.update_date = datetime.datetime.now()
            db.session.commit()
            flash(u'修改成功')

            return redirect(url_for('agent.query_agent_list', agent_name=agent.agent_name))
    return render_template('/agent/update_remind.html', form=form, agent_id=agent.id)

@agent.route('/update-price/<id>/', methods=['GET', 'POST'])
@login_required
def update_price(id):
    """to update price page.

       Args:
            id: agent_info primary key

       Returns:
           to update price page
    """
    # get agent_info object
    agent = AgentInfo.query.get(id)
    price_list = DomainPrice.query.all()
    if request.method == 'POST':
        # update price type
        agent.domain_price_id = request.form['price_id']
        agent.update_date = datetime.datetime.now()
        db.session.commit()
        flash(u'修改成功')
        return redirect(url_for('agent.query_agent_list', agent_name=agent.agent_name))
    return render_template('/agent/update_price.html', agent=agent, price_list=price_list)

@agent.route('/charge/<id>/', methods=['GET', 'POST'])
@login_required
def charge(id):
    """to charge page.

       Args:
            id: agent_info primary key

       Returns:
           to charge page
    """
    # get agent_info object
    agent = AgentInfo.query.get(id)
    amount = 0
    if request.method == 'POST':
        amount = request.form['amount']
        print amount
        if not amount.isdigit():
            flash(u'必须充值整数金额')
        elif int(amount) <= 0:
            flash(u'金额必须大于0')
        else:
            # charge operate, add charge record
            try:
                print "int "
                date_now = datetime.datetime.now()
                agent.balance += int(amount)
                agent.update_date = date_now
                db.session.flush()
                aar = AgentAccountRecord()
                aar.agent_id = agent.id
                aar.amount = int(amount)
                aar.balance = agent.balance
                aar.operate = 1
                aar.record_desc = u'charge by %s' % current_user.username
                aar.creator = current_user.id
                aar.create_date = date_now
                db.session.add(aar)
                db.session.commit()
                flash(u'充值成功，余额：%d元' % agent.balance)
                return redirect(url_for('agent.query_agent_list', agent_name=agent.agent_name))
            except Exception, e:
                print e
                db.session.rollback()
                flash(u'充值失败')
                return redirect(url_for('agent.query_agent_list', agent_name=agent.agent_name))
    return render_template('/agent/charge.html', agent=agent, amount=amount)

@agent.route('/payment/<id>/', methods=['GET', 'POST'])
@login_required
def payment(id):
    """to payment page.

       Args:
            id: agent_info primary key

       Returns:
           to payment page
    """
    # get agent_info object
    agent = AgentInfo.query.get(id)
    amount = 0
    if request.method == 'POST':
        amount = request.form['amount']
        if not amount.isdigit():
            flash(u'必须充值整数金额')
        elif int(amount) <= 0:
            flash(u'金额必须大于0')
        elif int(amount) > agent.balance:
            flash(u'余额不足')
        else:
            # payment operate, add operate record
            try:
                date_now = datetime.datetime.now()
                agent.balance -= int(amount)
                agent.update_date = date_now
                db.session.flush()
                aar = AgentAccountRecord()
                aar.agent_id = agent.id
                aar.amount = int(amount)
                aar.balance = agent.balance
                aar.operate = 2
                aar.record_desc = u'payment by %s' % current_user.username
                aar.creator = current_user.id
                aar.create_date = date_now
                db.session.add(aar)
                db.session.commit()
                flash(u'扣费成功，余额：%d元' % agent.balance)
                return redirect(url_for('agent.query_agent_list', agent_name=agent.agent_name))
            except Exception, e:
                db.session.rollback()
                print e.message
                flash(u'扣费失败')
                return redirect(url_for('agent.query_agent_list', agent_name=agent.agent_name))
    # to web page
    return render_template('/agent/payment.html', agent=agent, amount=amount)
