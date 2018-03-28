from flask import render_template, request
from app_module.control.Pagination import Pagination
import app_module.dao.TruyenDao as TruyenDao

PAGE_SIZE = 10
def HienThi(page):
	tukhoa = request.args.get('tukhoa')
	nFirstRow = (page - 1) * PAGE_SIZE
	print('tukhoa: %r' % tukhoa)
	count = 0
	lstTruyen = []
	try:
		if not tukhoa:
			count = TruyenDao.Count()
			lstTruyen = TruyenDao.SelectPhanTrang(nFirstRow, PAGE_SIZE)
		else:
			count = TruyenDao.CountTheoTuKhoa(tukhoa)
			lstTruyen = TruyenDao.SelectTheoTuKhoaPhanTrang(tukhoa, nFirstRow, PAGE_SIZE)
		print('count: %r' % count)
		if not lstTruyen and page != 1:
			abort(404)
		stt=nFirstRow+1;
		for vTruyen in lstTruyen:
			vTruyen["stt"] = stt
			stt+=1
	except Exception as e:
		print('Exception: %r' % e)
	pagination = Pagination(page, PAGE_SIZE, count)
	return render_template('danh-sach-truyen.html', pagination=pagination, lstTruyen=lstTruyen)