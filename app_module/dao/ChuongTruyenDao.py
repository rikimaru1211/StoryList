from pymongo import MongoClient, ASCENDING
from app_module.config.Config import *

def getCollectionName():
	return "ChuongTruyen"

def getCollection():
	client = MongoClient(MONGO_CONNECTION_TRUYEN)
	db = client[MONGO_CONNECTION_DATABASE_NAME]
	return db[getCollectionName()]

def TimKiem():
	collection = getCollection()
	vResult = collection.find_one()
	return vResult

def SelectByMaTruyen(sMaTruyen):
	collection = getCollection()
	vResult = collection.find({"matruyen":sMaTruyen},{"_id":0,"tieude":1,"noidung":1,"stt":1}).sort('stt', ASCENDING)
	lstResult = []
	for chuong in vResult:
		lstResult.append(chuong)
	return lstResult

def insert(vChuong):
	collection = getCollection()
	collection.insert_one(vChuong)

def removeByMaTruyen(sMaTruyen):
	collection = getCollection()
	return collection.delete_many({"matruyen":sMaTruyen}).deleted_count