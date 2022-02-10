import json,threading,os

from FINDERmaster.code.FINDER_CN import train
from FINDERmaster.code.FINDER_CN.FINDER import FINDER
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from FinderDjango import settings

finder_thread = threading.Thread(target=train.main)
finder_thread.start()


@csrf_exempt
def changeFinderRunning(request):
	'''
	修改FINDER的运行状态
	:param request:
	:return:
	'''
	if request.POST:
		request_data = request.POST
	elif request.GET:
		request_data = request.GET
	else:
		request_data = json.loads(request.body)

	# flag
	flag = request_data["flag"]

	if isinstance(flag, bool):
		settings.FINDER_STOP = flag
	else:
		return HttpResponse(json.dumps({"status": False, "msg": "flag必须为布尔值"}))

	if flag:
		return HttpResponse(json.dumps({"status": True, "msg": "挂起成功"}))

	return HttpResponse(json.dumps({"status": True, "msg": "已继续运行"}))

def get_file_list(file_path):
	dir_list = os.listdir(file_path)
	if not dir_list:
		return
	else:
		dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
		new_list = [name for name in dir_list if name[:6] == "nrange"]
		filename = ".".join(new_list[-1].split(".")[:-1])
		return filename

@csrf_exempt
def GetSolutionForApi(request):
	try:
		if request.POST:
			request_data = request.POST
		elif request.GET:
			request_data = request.GET
		else:
			request_data = json.loads(request.body)

		STEPRATIO = 0.01
		points = request_data["points"]
		edge = request_data["edges"]
		dqn = FINDER()
		file_dir = 'FINDERmaster/code/FINDER_CN/models/Model_powerlaw/'
		MODELFILE = get_file_list(file_dir)
		model_file = file_dir + MODELFILE
		print ('The best model is :%s'%(model_file))
		dqn.LoadModel(model_file)
		solution, time = dqn.EvaluateRealDataForApi(model_file, points, edge, STEPRATIO)
		return HttpResponse(json.dumps({"success": True, "msg": "获取成功", "data": [points[i] for i in solution]}))
	except:
		import traceback
		print(traceback.format_exc())









def heartCheck():
	pass

