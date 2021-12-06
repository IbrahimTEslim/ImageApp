from django.conf import settings
from django.contrib.auth import SESSION_KEY
# from .sessions import session_manegment
from django.http import HttpResponse
from django.contrib.sessions.models import Session

class CheckSession:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self,request,view_func,args,kwargs):
        # path = request.path_info
        # print(path)

        # print('\n\n')
        # for k in request.META:
        #     print(k,"\n")
        # print(request.headers['Cookie'][0:10],"\n")
        # print(type(request.headers['Cookie']),"\n")
        # print(request.headers['test'],"\n")
        # print(type(request.headers['test']),"\n")
        # print(request.META['HTTP_COOKIE'],"\n\n")
        # print(type(request.META['HTTP_COOKIE']),"\n")

        # if request.headers['Cookie'][0:10] != 'Session_id':
        #     print('first fail')
        #     return HttpResponse("to Login page too ;p")

        # print("\n\nSe:\n",request.META['HTTP_COOKIE'][11:])
        # if request.META['HTTP_COOKIE'][11:] not in settings.SE.sessions_ids:
        #     print('sec fail')
        #     return HttpResponse("Nope, to Login page firt :p")
        # print(type(request.COOKIES))
        # print("\n\n",request.path,"\n\n")
        if request.path == '/user/login' or request.path =='/user/register':
            return None
       
        if request.session is not None and request.session._session_key is not None:
            try:
                session = Session.objects.get(pk = request.session._session_key)
            except Session.DoesNotExist:
                print(request.session.items())
                return HttpResponse("You have session id but naaah - now i don't have it\ngo to login")
            if session is not None:
                return None
        else:
            return HttpResponse("Catched you in the middle of the ware, go to login")
        
