# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, url_for, redirect
from werkzeug import secure_filename
from io import StringIO
import app_module.dao.TruyenDao as TruyenDao
import app_module.dao.ChuongTruyenDao as ChuongTruyenDao


def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1] in set(['txt', 'doc', 'docx'])

def HienThi():
	print("======================")
	if request.method == 'POST':
		print("la post request")
		print(request.form);

		sTieuDeContent = request.form['content'].lower()
		sTieuDeStartWith = request.form['start-with'].lower()
		if not (sTieuDeContent or sTieuDeStartWith):
			sTieuDeContent="chương"
			sTieuDeStartWith="quyển"
		
		print("sTieuDeContent: " + sTieuDeContent);
		print("sTieuDeStartWith: " + sTieuDeStartWith);

		file = request.files['file']

		print("lay file")
		if file and allowed_file(file.filename):
			print("file hop le")
			vTruyen = {}
			vTruyen['manguon'] = "TuFile"
			vTruyen['urlgoc'] = "TuFile"
			vTruyen['ten'] = file.filename
			vTruyen['tenhienthi'] = file.filename
			sMaTruyen = "TuFile_" + file.filename
			vTruyen['matruyen'] = sMaTruyen

			print(vTruyen)
			sTieuDe = ""
			sNoiDung = StringIO()
			filename = secure_filename(file.filename)

			stt = 1
			for line in file.stream:
				lineString = line.decode(encoding='UTF-8')
				lineString = lineString.strip(' \t\n\r');
				if(not lineString):
					continue
				line_lower = lineString.lower()
				if((not sTieuDeContent or sTieuDeContent in line_lower) and (not sTieuDeStartWith or line_lower.startswith(sTieuDeStartWith))):
					if(sTieuDe and sNoiDung.getvalue()):
						vChuong = {}
						vChuong['matruyen'] = sMaTruyen
						vChuong['stt'] = stt
						vChuong['noidung'] = sNoiDung.getvalue()
						vChuong['tieude'] = sTieuDe
						ChuongTruyenDao.insert(vChuong)
						stt = stt + 1
					
					sTieuDe = lineString
					sNoiDung = StringIO()
				else:
					sNoiDung.write(lineString);
					sNoiDung.write("\n");

			if(sTieuDe and sNoiDung.getvalue()):
				vChuong = {}
				vChuong['matruyen'] = sMaTruyen
				vChuong['stt'] = stt
				vChuong['noidung'] = sNoiDung.getvalue()
				vChuong['tieude'] = sTieuDe
				ChuongTruyenDao.insert(vChuong)
			print("ket thuc file")
			vTruyen['sochuong'] = stt - 1
			TruyenDao.insert(vTruyen);
			print("insert truyen thanh cong")

			return redirect(url_for('NhapLieuTuFile', filename=filename))
		else:
			print("file ko hop le")
			return redirect(url_for('NhapLieuTuFile'))

	print("ko phai post, hien thi tu templage")
	return render_template('nhap-lieu-tu-file.html')
