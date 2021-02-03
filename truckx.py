from twisted.web import server, resource
from twisted.internet import reactor, endpoints


def write_in_table(table_name, args):
    pass

def read_from_alarms(ID:int, start_time = -1, end_time = -1):
    pass

def read_from_videos(ID:int):
    pass

class Camera(object):
    def __init__(self, imei_value):
        self.imei = imei_value

    def update_location(self, info:dict):
        write_in_table('LOCATION', [self.imei, info.get('location_time', None), info.get('latitude', None), info.get('longitude', None)])
        return

    def invoke_alarm(self, info:dict):
        write_in_table('ALARMS', [self.imei, info.get('alarm_type', None), info.get('alarm_time', None), info.get('latitude', None), info.get('longitude', None), info.get('file_list', None)])
        return

    def upload_video(self, info:dict):
        write_in_table('VIDEOS', [self.imei, info.get('filename', None), info.get('data', None)])

global B
B = dict() #All camera objects are stored here, replace this with database table in production camera_id(imei), online_camera_object columns

class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        print('received get request')
        print(request.content.read().decode('utf-8'))
    def render_POST(self, request):
        A = dict()
        print(request.args)
        for k, v in request.args.items():
            A[k.decode('utf-8')] = v[0].decode('utf-8')
        print(A)
        t = A.get('type', None)
        if t == 'LOGIN':
            B[A['imei']] = Camera(A['imei'])
            return
        cur_obj = B[A['imei']] #in production cur_obj will be received from database
        if t == 'ALARM':
            cur_obj.invoke_alarm(A)
        elif t == 'LOCATION':
            cur_obj.update_location(A)
        elif not t:
            cur_obj.upload_video(A)
        elif t=='LOGOUT':
            B[A['imei']] = None # camera went offline
            

class AdminUI(object):
    def __init__(self, imei_value):
        self.imei = imei_value

    def get_alarms(self):
        read_from_alarms(self.imei)

    def get_alarms_filter(self, start_time, end_time):
        read_from_alarms(self.imei, start_time, end_time)

    def get_recorded_videos(self):
        read_from_videos(self.imei)

    def send_command(self):
        pass

    
    

site = server.Site(Simple())
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8080)
endpoint.listen(site)
reactor.run()
