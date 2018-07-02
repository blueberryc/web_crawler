爬虫实质上就是模拟浏览器进行HTTP请求的过程。

### HTTP协议是什么？

你浏览的每一个网页都是基于 HTTP 协议呈现的，HTTP 协议是互联网应用中，客户端（浏览器）与服务器之间进行数据通信的一种协议。协议中规定了客户端应该按照什么格式给服务器发送请求，同时也约定了服务端返回的响应结果应该是什么格式。 

HTTP 协议本身是非常简单的。它规定，只能由客户端主动发起请求，服务器接收请求处理后返回响应结果，同时 HTTP 是一种无状态的协议，协议本身不记录客户端的历史请求记录。 

![img](http://mmbiz.qpic.cn/mmbiz_jpg/rO1ibUkmNGMkcw5cSTBtVOThaNzeEhyhaoqOjdvf5k8lL3wYhgWaKicYQ9lI7sKATwib7TrCYJodIwaPksCaJcT7A/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1) 

---

### HTTP请求格式

HTTP 请求由3部分组成，分别是请求行、请求首部、请求体，首部和请求体是可选的，并不是每个请求都需要的。 

![img](http://mmbiz.qpic.cn/mmbiz_jpg/rO1ibUkmNGMkcw5cSTBtVOThaNzeEhyha92nicMMLGiarugYD8gYcvmVibPLEn69ibzz4fibhicTCoJobQmsKCdgzzyaQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1) 

#### 请求行

请求行是每个请求必不可少的部分，它由3部分组成，分别是请求方法（method)、请求URL（URI）、HTTP协议版本，以空格隔开。 

HTTP协议中最常用的请求方法有：GET、POST、PUT、DELETE。GET 方法用于从服务器获取资源，90%的爬虫都是基于GET请求抓取数据。 

#### 请求首部

因为请求行所携带的信息量非常有限，以至于客户端还有很多想向服务器要说的事情不得不放在请求首部（Header），请求首部用于给服务器提供一些额外的信息，比如 User-Agent 用来表明客户端的身份，让服务器知道你是来自浏览器的请求还是爬虫，是来自 Chrome 浏览器还是 FireFox。HTTP/1.1 规定了47种首部字段类型。HTTP首部字段的格式很像 Python 中的字典类型，由键值对组成，中间用冒号隔开。比如： 

```json
User-Agent: Mozilla/5.0
```

因为客户端发送请求时，发送的数据（报文）是由字符串构成的，为了区分请求首部的结尾和请求体的开始，用一个空行来表示，遇到空行时，就表示这是首部的结尾，请求体的开始。 

#### 请求体

请求体是客户端提交给服务器的真正内容，比如用户登录时的需要用的用户名和密码，比如文件上传的数据，比如注册用户信息时提交的表单信息。 

---

### HTTP响应

服务端接收请求并处理后，返回响应内容给客户端，同样地，响应内容也必须遵循固定的格式浏览器才能正确解析。HTTP 响应也由3部分组成，分别是：响应行、响应首部、响应体，与 HTTP 的请求格式是相对应的。 

![img](http://mmbiz.qpic.cn/mmbiz_jpg/rO1ibUkmNGMkcw5cSTBtVOThaNzeEhyhagrBLjdprWsjSqLqZwsP9hMCKuwgO9l95kMqLBQo4ic05IoukK7W5SuQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1) 

其中**状态码**是一个很重要的字段，在我们进行爬虫的爬取时，经常需要靠这一标准来判断我们的请求是否成功。如果状态码是200，说明客户端的请求处理成功，如果是500，说明服务器处理请求的时候出现了异常。404 表示请求的资源在服务器找不到。 

响应体就是我们请求后，服务器给我们返回的内容了。通常是一个HTML网页源码，我们需要对该源码进行进一步的提取来获得我们需要的信息。

