from pymongo import MongoClient
from app_module.config.Config import *

def getCollectionName():
	return "Truyen";

def getCollection():
	client = MongoClient(MONGO_CONNECTION_TRUYEN);
	db = client[MONGO_CONNECTION_DATABASE_NAME];
	return db[getCollectionName()];

def TimKiem():
	collection = getCollection();
	vResult = collection.find_one();
	return vResult;

def SelectAll():
	collection = getCollection();
	vResult = collection.find();
	lstResult = [];
	for truyen in vResult:
		lstResult.append(truyen["tenhienthi"]);
	return lstResult;

def Count():
	collection = getCollection();
	nCount = collection.count();
	return nCount;

def SelectPhanTrang(nSkip, nLimit):
	collection = getCollection();
	vResult = collection.find({},{"_id":0,"urlgoc":1,"tenhienthi":1,"manguon":1,"sochuong":1,"matruyen":1}).skip(nSkip).limit(nLimit);
	lstResult = [];
	for truyen in vResult:
		lstResult.append(truyen);
	return lstResult;

def CountTheoTuKhoa(sTuKhoa):
	collection = getCollection();
	nCount = collection.count({"$or":[{"tenhienthi":{"$regex":sTuKhoa,"$options":'i'}},{"matruyen":{"$regex":sTuKhoa,"$options":'i'}}]});
	return nCount;

def SelectTheoTuKhoaPhanTrang(sTuKhoa, nSkip, nLimit):
	collection = getCollection();
	vResult = collection.find({"$or":[{"tenhienthi":{"$regex":sTuKhoa,"$options":'i'}},{"matruyen":{"$regex":sTuKhoa,"$options":'i'}}]},{"_id":0,"urlgoc":1,"tenhienthi":1,"manguon":1,"sochuong":1,"matruyen":1}).skip(nSkip).limit(nLimit);
	lstResult = [];
	for truyen in vResult:
		lstResult.append(truyen);
	return lstResult;

def insert(vTruyen):
	collection = getCollection();
	collection.insert_one(vTruyen);

def removeByMaTruyen(sMaTruyen):
	collection = getCollection()
	return collection.delete_one({"matruyen":sMaTruyen}).deleted_count