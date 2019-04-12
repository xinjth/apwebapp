import logging; logging.basicConfig(level=logging.INFO)# 设置日志级别
#logging模块来记录我想要的信息,logging相对print来说更好控制输出在哪个地方，怎么输出及控制消息级别来过滤掉那些不需要的信息
import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

def index(request):
#request为aiohttp.web.request实例, 包含http请求的信息, 一般不用自己构造
	return web.Response(body=b'<h1>Awesome</h1>',content_type='text/html')
#web.Response 构造并返回一个response实例, Response类声明为class aiohttp.web.Response(*, status=200, headers=None, content_type=None, body=None, text=None)
@asyncio.coroutine#将generator标记为coroutine类型, coroutine内部可以用yield from调用另一个coroutine
def init(loop):
	app = web.Application(loop=loop)
	#创建web服务器实例 loop: event loop used for processing HTTP requests
	app.router.add_route('GET', '/', index) #为route路径注册处理函数
	srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)	
	#loop.create_server创建一个TCP server;app.make_handler()Creates HTTP protocol factory for handling requests. yield from返回一个创建好的,绑定IP和端口以及http协议簇的监听服务的协程
	logging.info('server started at http://127.0.0.1:9000...')
	return srv

loop = asyncio.get_event_loop() #获取EventLoop:生成一个事件循环实例
loop.run_until_complete(init(loop)) #执行coroutine,行init(loop), run_until_complete: If the argument is a coroutine object, it is wrapped by ensure_future().对loop进行了初始化, 创建了tcp server?
loop.run_forever() #一直运行