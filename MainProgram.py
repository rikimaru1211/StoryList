#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, url_for, Response, redirect, flash
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from werkzeug import secure_filename
from app_module.control.Pagination import Pagination
from app_module.control.Form import CustomForm
from io import BytesIO
import app_module.web.DanhSachTruyenPage as DanhSachTruyenPage
import app_module.web.NhapLieuTuFilePage as NhapLieuTuFilePage
import app_module.dao.TruyenDao as TruyenDao
import app_module.dao.ChuongTruyenDao as ChuongTruyenDao
import app_module.utils.EpubFunction as EpubFunction

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route('/')
@app.route('/index.html')
def Home():
	return render_template('index.html')

@app.route('/test/')
def Test_Select():
	arrKetQua = TruyenDao.SelectAll()
	sKetQua = "KetQua:<br/>"
	sKetQua += "<br/>".join(arrKetQua)
	return sKetQua


PAGE_SIZE = 10
@app.route('/danh-sach-truyen/', methods=['GET'])
@app.route('/danh-sach-truyen/<int:page>', methods=['GET'])
def DanhSachTruyen(page = 1):
	return DanhSachTruyenPage.HienThi(page)


@app.route('/lay-du-lieu-tu-web', methods=['GET', 'POST'])
def LayDuLieuTuWeb():
	# form = RegistrationForm(request.form)
	form = CustomForm(request.form)
	form.createFields()
	username = TextField('Username', [validators.Length(min=4, max=25)])
	form.addField(username);
	email = TextField('Email Address', [validators.Length(min=6, max=35)])
	form.addField(email);
	if request.method == 'POST' and form.validate():
		user = User(form.username.data, form.email.data)
		db_session.add(user)
		flash('Thanks for registering')
		return redirect(url_for('login'))
	return render_template('lay-du-lieu-tu-web.html', form=form)


@app.route('/nhap-lieu-tu-file/', methods=['GET', 'POST'])
def NhapLieuTuFile():
	return NhapLieuTuFilePage.HienThi()


@app.route('/download-txt/<matruyen>')
def DownloadTXT(matruyen):
	lstChuong = ChuongTruyenDao.SelectByMaTruyen(matruyen)

	sNoiDungFile = ''.join(["%s\n%s\n\n" % (vChuong["tieude"], vChuong["noidung"]) for vChuong in lstChuong])

	# We need to modify the response, so the first thing we 
	# need to do is create a response out of the CSV string
	response = Response(sNoiDungFile, mimetype='text/plain')
	# This is the key: Set the right header for the response
	# to be downloaded, instead of just printed on the browser
	response.headers["Content-Disposition"] = "attachment; filename="+matruyen+".txt"
	return response

@app.route('/download-epub/<matruyen>')
def DownloadEPUB(matruyen):
	lstChuong = ChuongTruyenDao.SelectByMaTruyen(matruyen)

	outFile = BytesIO()

	EpubFunction.CreateEpubFile(matruyen, lstChuong, outFile)

	response = Response(outFile.getvalue(), mimetype='application/x-zip-compressed')
	response.headers["Content-Disposition"] = "attachment; filename="+matruyen+".epub"
	return response

@app.route('/delete/<matruyen>')
def DeleteTruyen(matruyen):
	ChuongTruyenDao.removeByMaTruyen(matruyen)
	TruyenDao.removeByMaTruyen(matruyen)
	return  DanhSachTruyenPage.HienThi(1)


def url_for_other_page(page):
	queryString = request.query_string.decode(encoding='UTF-8')
	args = request.view_args.copy()
	args['page'] = page
	return ''.join([ url_for(request.endpoint, **args), "?" , queryString ])
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

if __name__ == '__main__':
    app.run(debug=True)