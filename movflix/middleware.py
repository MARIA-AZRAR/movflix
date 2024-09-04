from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.utils.decorators import sync_and_async_middleware

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        print("i am running before")
        response = self.get_response(request)
        print("I am running after")
        
        return response

@sync_and_async_middleware
def simple_middleware(get_response):
    if iscoroutinefunction(get_response):
        async def middleware(request):
            print("before async")
            response = await get_response(request)
            print("after async")
            return response
    else:
        def middleware(request):
            print("before sync")
            response = get_response(request)
            print("after sync")
            return response
    
    return middleware

class MyAsyncMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        self.is_async = iscoroutinefunction(get_response)
        if iscoroutinefunction(self.get_response):
            print("it is async")
            markcoroutinefunction(self)

    async def __call__(self, request):
        print("before class async")
        response = await self.get_response(request)
        print("after class async")
        return response