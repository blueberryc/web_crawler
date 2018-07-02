Python 提供了很多模块来支持 HTTP 协议的网络编程，urllib、urllib2、urllib3、httplib、httplib2，都是和 HTTP 相关的模块，看名字觉得很反人类，更糟糕的是这些模块在 Python2 与 Python3 中有很大的差异，如果业务代码要同时兼容 2 和 3，写起来会让人崩溃。幸运地是，繁荣的 Python 社区给开发者带来了一个非常惊艳的 HTTP 库 requests，一个真正给人用的HTTP库。 

requests 实现了 HTTP 协议中绝大部分功能，它提供的功能包括 Keep-Alive、连接池、Cookie持久化、内容自动解压、HTTP代理、SSL认证、连接超时、Session等很多特性，最重要的是它同时兼容 python2 和 python3。 

### 快速入门

![](http://pax93mwix.bkt.clouddn.com/18-6-28/5024627.jpg)

requests的get()函数用一个网页的URL作为参数，然后返回一个Response对象。Response 对象是 对 HTTP 协议中服务端返回给浏览器的响应数据的封装，响应的中的主要元素包括：状态码、原因短语、响应首部、响应体等等，这些属性都封装在Response 对象中。 

![](http://pax93mwix.bkt.clouddn.com/18-6-28/55762411.jpg)

requests 除了支持 GET 请求外，还支持 HTTP 规范中的其它所有方法，包括 POST、PUT、DELTET、HEADT、OPTIONS方法。 

```powershell
>>> r = requests.post('http://httpbin.org/post', data = {'key':'value'})
>>> r = requests.put('http://httpbin.org/put', data = {'key':'value'})
>>> r = requests.delete('http://httpbin.org/delete')
>>> r = requests.head('http://httpbin.org/get')
>>> r = requests.options('http://httpbin.org/get')
```

#### 构建请求查询参数

很多URL都带有很长一串参数，我们称这些参数为URL的查询参数，用”?”附加在URL链接后面，多个参数之间用”&”隔开 ，比如：http://fav.foofish.net/?p=4&s=20 ，现在你可以用字典来构建查询参数： 

```powershell
>>> args = {"p": 4, "s": 20}
>>> response = requests.get("http://fav.foofish.net", params = args)
>>> response.url
'http://fav.foofish.net/?p=4&s=2'
```



#### 构建请求首部Headers

requests 可以很简单地指定请求首部字段 Headers，比如有时要指定 User-Agent 伪装成浏览器发送请求，以此来蒙骗服务器。直接传递一个字典对象给参数 headers 即可。 

```powershell
>>> r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
```



#### 构建POST请求数据

requests 可以非常灵活地构建 POST 请求需要的数据，如果服务器要求发送的数据是表单数据，则可以指定关键字参数 data，如果要求传递 json 格式字符串参数，则可以使用json关键字参数，参数的值都可以字典的形式传过去。 

作为表单数据传输给服务器

```powershell
>>> payload = {'key1': 'value1', 'key2': 'value2'}
>>> r = requests.post("http://httpbin.org/post", data=payload)
```

作为json格式的字符串格式传输给服务器

```powershell
>>> import json
>>> url = 'http://httpbin.org/post'
>>> payload = {'some': 'data'}
>>> r = requests.post(url, json=payload)
```



#### Response中的响应体

HTTP返回的响应消息中很重要的一部分内容是响应体，响应体在 requests 中处理非常灵活，与响应体相关的属性有：content、text、json()。 

1. content 是 byte 类型，适合直接将内容保存到文件系统或者传输到网络中 
2. text 是 str 类型，比如一个普通的 HTML 页面，需要对文本进一步分析时，使用 text 
3. 如果使用第三方开放平台或者API接口爬取数据时，返回的内容是json格式的数据时，那么可以直接使用json()方法返回一个经过json.loads()处理后的对象 

```cmd
# content
>>> r = requests.get("https://pic1.zhimg.com/v2-2e92ebadb4a967829dcd7d05908ccab0_b.jpg")
>>> type(r.content)
<class 'bytes'>
# 另存为 test.jpg
>>> with open("test.jpg", "wb") as f:
...     f.write(r.content)

# text
>>> r = requests.get("https://foofish.net/understand-http.html")
>>> type(r.text)
<class 'str'>
>>> re.compile('xxx').findall(r.text)

# json
>>> r = requests.get('https://www.v2ex.com/api/topics/hot.json')
>>> r.json()
[{'id': 352833, 'title': '在长沙，父母同住...'
```

---

#### 代理设置

当爬虫频繁地对服务器进行抓取内容时，很容易被服务器屏蔽掉，因此要想继续顺利的进行爬取数据，使用代理是明智的选择。如果你想爬取墙外的数据，同样设置代理可以解决问题，requests 完美支持代理。 

```python
import requests

proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}
requests.get('http://example.org', proxies=proxies)
```

---

#### 超时设置

requests 发送请求时，默认请求下线程一直阻塞，直到有响应返回才处理后面的逻辑。如果遇到服务器没有响应的情况时，问题就变得很严重了，它将导致整个应用程序一直处于阻塞状态而没法处理其他请求。 正确的方式的是给每个请求显示地指定一个超时时间。 

```cmd
>>> import requests
>>> r = requests.get("http://www.google.coma")
'...一直阻塞中'

>>> r = requests.get("http://www.google.coma", timeout=5)
'5秒后报错'
Traceback (most recent call last):
socket.timeout: timed out
```

---

#### Session

在[爬虫系列学习（1）：快速理解HTTP协议](https://segmentfault.com/n/1330000015413249)中介绍过HTTP协议是一中无状态的协议，为了维持客户端与服务器之间的通信状态，使用 Cookie 技术使之保持双方的通信状态。 

有些网页是需要登录才能进行爬虫操作的，而**登录的原理**就是浏览器首次通过用户名密码登录之后，服务器给客户端发送一个随机的Cookie，下次浏览器请求其它页面时，就把刚才的 cookie 随着请求一起发送给服务器，这样服务器就知道该用户已经是登录用户。 

```python
import requests
# 构建会话
session  = requests.Session()
#　登录url
session.post(login_url, data={username, password})
#　登录后才能访问的url
r = session.get(home_url)
session.close()
```

构建一个session会话之后，客户端第一次发起请求登录账户，服务器自动把cookie信息保存在session对象中，发起第二次请求时requests 自动把session中的cookie信息发送给服务器，使之保持通信状态。 