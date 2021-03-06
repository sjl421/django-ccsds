===Django 源码阅读笔记


> README Of django-ccsds


	Version: django 1.8.16 
	Date: 2016.11.16
	Author: Wayne


最近在参与一个项目－CCSDS，因项目需要，故打算学习django框架，而本仓库的建立是为了跟踪我的django学习历程。如此优秀的框架，如此优秀的代码，当然得拿来好好的研究一番，那么就从阅读源码开始。当然学习django起于源码而不仅仅停留于源码，还会做一些系统的总结，因此学习的大概形式是采用源码＋注释＋总结。

	如有什么不妥的地方，欢迎批评指正，同时也非常欢迎您加入进来，一起阅读源码，一起讨论，一起进步！--- Wayne 2016.11.17

#### Django 安装

这里采取离线安装方式，便于多环境离线部署。
下载离线安装包：[How to get Django](https://www.djangoproject.com/download/ "下载")
 
#### Django 源码学习01：建立Project和App


##### 开始啦！从建立第一个Project 开始说起

 	django: django-admin.py startproject mysite
 	project: manage.py startapp polls


项目（Project） Vs 应用（Apps）

	项目与应用之间有什么不同之处？应用是一个提供功能的 Web 应用 – 例如：一个博客系统、 一个公共记录的数据库或者一个简单的投票系统。项目是针对一个特定的 Web 网站相关的配置和其应用的组合。一个项目可以包含多个应用。 一个应用可以在多个项目中使用。

##### 模型

在Django中编写一个有数据库支持的Web应用的第一步就是定义模型，从本质上讲就是数据库设计及其附加的元数据。

	模型是有关你数据的唯一且明确的数据源。 它包含了你所要存储的数据的基本字段和行为。 Django 遵循 DRY 原则 。 目标是为了只在一个地方定义你的数据模型就可从中自动获取数据。


那么接下来就是为该应用创建对应的数据库架构（create table statements），为Poll和Choice 对象创建Python访问数据库的API。当然在此之前我们需要再次编辑settings.py文件，在INSTALLED_APPS设置中加入'polls'字符，告诉我们的项目已经安装了polls应用。

	Django 应用是“可插拔的”：你可以在多个项目使用一个应用， 你还可以分发应用， 因为它们没有被捆绑到一个给定的 Django 安装环境中。

运行python manage.py sql polls 生成相关的create table sql语句：

	BEGIN;
	CREATE TABLE "polls_poll" (
	    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	    "question" varchar(200) NOT NULL,
	    "pub_date" datetime NOT NULL
	)
	;
	CREATE TABLE "polls_choice" (
	    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	    "poll_id" integer NOT NULL REFERENCES "polls_poll" ("id"),
	    "choice_text" varchar(200) NOT NULL,
	    "votes" integer NOT NULL
	)
	;
	COMMIT;

注意此时，SQL 语句并没有运行，如果你愿意可以直接复制这个语句在数据库命令行中运行，但是Django提供了更简单的方法来执行此SQL。

运行python manage.py syncdb在数据库中创建模型对应的表。syncdb 命令会给在 INSTALLED_APPS 中有但数据库中没有对应表的应用执行 sqlall 操作。


	$ python manage.py syncdb 
	Operations to perform:
	  Synchronize unmigrated apps: staticfiles, polls, messages
	  Apply all migrations: admin, contenttypes, auth, sessions
	Synchronizing apps without migrations:
	  Creating tables...
	    Creating table polls_poll
	    Creating table polls_choice
	    Running deferred SQL...
	  Installing custom SQL...
	Running migrations:
	  No migrations to apply.

syncdb 命令只要你喜欢就可以任意调用， 并且它仅会创建不存在的表。

玩转API

	$ python manage.py shell   
	Python 2.7.12 (default, Jul  1 2016, 15:12:24) 
	Type "copyright", "credits" or "license" for more information.

	IPython 5.1.0 -- An enhanced Interactive Python.
	?         -> Introduction and overview of IPython's features.
	%quickref -> Quick reference.
	help      -> Python's own help system.
	object?   -> Details about 'object', use 'object??' for extra details.

	In [1]: from polls.models import Poll, Choice

	In [2]: Poll.objects.all()
	Out[2]: []

	In [3]: from django.utils import timezone

	In [4]: p = Poll(question="How to read django source code?", pub_date=timezone.now())

	In [5]: p.save
	Out[5]: <bound method Poll.save of <Poll: Poll object>>

	In [6]: p.save()

	In [7]: p.id
	Out[7]: 1

	In [8]: p.question
	Out[8]: 'How to read django source code?'

	In [9]: p.pub_date
	Out[9]: datetime.datetime(2016, 11, 21, 6, 13, 10, 788532, tzinfo=<UTC>)

	In [11]: p.question = 'How to read python web framework django source code?'

	In [12]: p.save()

	In [13]: Poll.objects.all()
	Out[13]: [<Poll: Poll object>]

请注意，第13个命令，objects.all()用以显示数据库中所有的polls，但是其输出这样显示对象是毫无意义的，因此我们需要编辑polls模型并且给Poll和Choice都添加一个unicode()方法来修正此错误。给你的模型添加 unicode() 方法是很重要的， 不仅是让你在命令行下有明确提示， 而且在Django 自动生成的管理界面中也会使用到对象的呈现。

编辑好polls模型，重新生成sql语句，并创建表，然后进入python django shell 使用Poll.objects.all()方法：

	$ python manage.py shell



	In [2]: ls
	db/  manage.py*  mysite/  polls/

	In [3]: from polls.models import Poll, Choice

	In [4]: Poll.objects.all()
	Out[4]: [<Poll: How to read python web framework django source code?>]

	In [5]: 

上面都是些普通的python方法，我们还可以自己添加自定义方法：

	import datetime
	from django.utils import timezone
	# ...
	class Poll(models.Model):
	# ...
		def was_published_recently(self):
			return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


还可以这么玩：

	In [13]: Poll.objects.get(id=1)
	Out[13]: <Poll: How to read python web framework django source code?>

	In [14]: Poll.objects.get(pk=1)
	Out[14]: <Poll: How to read python web framework django source code?>

	In [15]: p = Poll.objects.get(pk=1)

	In [16]: p.was_published_recently
	Out[16]: <bound method Poll.was_published_recently of <Poll: How to read python web framework django source code?>>

	In [17]: p.was_published_recently()
	Out[17]: True

	In [18]: p.choice_set.all()
	Out[18]: []


这么玩：

	python manage.py shell

	Python 2.7.12 (default, Jul  1 2016, 15:12:24) 
	Type "copyright", "credits" or "license" for more information.

	IPython 5.1.0 -- An enhanced Interactive Python.
	?         -> Introduction and overview of IPython's features.
	%quickref -> Quick reference.
	help      -> Python's own help system.
	object?   -> Details about 'object', use 'object??' for extra details.

	In [1]: from polls.models import Poll, Choice

	In [3]: p = Poll.objects.get(id=1)

	In [4]: p.choice_set.create(choice_text='Not much', votes=0)
	Out[4]: <Choice: Not much>

	In [5]: p.choice_set.create(choice_text='The sky', votes=0)
	Out[5]: <Choice: The sky>

	In [6]: p.choice_set.create(choice_text='Just hacking again', votes=0)
	Out[6]: <Choice: Just hacking again>

	....

	In [8]: c = p.choice_set.get(id =3)

	In [9]: c.poll
	Out[9]: <Poll: How to read python web framework django source code?>


还能玩删除：

	In [11]: c = p.choice_set.filter(choice_text__startswith='Just ')

	In [12]: c.delete()


##### 管理你的站点

首先在settings.py中的INSTALLED_APPS 设置安装admin新应用，然后启动开发服务器。

python manage.py runserver

但是如此无法编辑Poll应用，这个时候我们需要告诉管理网站Poll对象要有一个管理页面，在polls页面下创建一个名为admin.py的文件，并添加如下内容：

	from django.contrib import admin
	from polls.models import Poll
	# Register your models here.
	admin.site.register(Poll)

然后再重启开发服务器。

> 通常情况下， 你每次修改过一个文件后开发 服务器都会自动载入， 但是创建一个新文件却不会触发自动载入的逻辑。

此外记得而改下时区，默认为美国时间，改为中国时间。

	# 默认时区为芝加哥时，下面修改为上海时间
	# TIME_ZONE = 'UTC' 
	TIME_ZONE = 'Asia/Shanghai'

##### 编写你的第一个视图

> 在Django应用程序中，视图是一“类”具有特定功能和模板的网页。Django是通过‘URLconfs’从URL获取到视图的。而URLconf是将URL模式（由正则表达式来描述）映射到视图的一种配置。


URL名称的命名空间，修改root URLconf配置中添加命名空间。

为什么要重构代码？

>通常情况下，当你编写一个Django应用时，你会评估下通用视图是否适合解决你的问题，如果是适合你就应该一开始就使用它，而不是进行到一半才重构你的代码。

##### 自动化测试你的应用  Q&A

Q1:什么是自动化测试？
A1:测试是检查你的代码是否正常运行的简单程序。

>不具有测试程序的代码是设计上的错误---Jacob Kaplan-Moss (Django最初的几个开发者之一)

一些开发者遵循测试驱动开发（Test-Driven Development，TDD）,它是一种测试先于编写代码的思想用于指导软件开发。测试驱动开发是敏捷开发中的一项核心实践和技术，也是一种设计方法论。TDD的原理是在开发功能代码之前，先编写单元测试用例代码，测试代码确定需要编写什么产品代码。

应用测试用例按照惯例一般放在该应用的tests.py文件中，测试系统将自动在任何以test开头的文件中查找测试用例。

有时候对测试来说，冗余是件好事，只要你的测试合理的组织，他们就不会变的难以管理。从经验上说，好的做法是：

		1.每个模型或视图具有一个单独的TestClass
		2.为你想测试的每一个情况建立一个单独测试的方法
		3.测试方法的名字可以描述他们的功能

除了一些基本的测试，还有许多非常有用的工具，比如可以使用一个“浏览器框架”例如selenium来测试你的HTML文件在浏览器中真实渲染的样子。这些工具不仅可以让你检查你的Django代码的行为，还能够检查你的JavaScript的行为。他会启动一个浏览器并开始与你的网站进行交互，就像有一个人在操纵一样。Django包含一个LiveServerTestCase来帮助与Selenium这样的工具集成。

发现你的应用中未经测试的代码的一个好方法是检查测试代码的覆盖率。
##### 自定义你的 应用外观
首先在polls中创建static目录，Django将在那里查找静态文件，类似于查找templates。

> Django 的 STATICFILES_FINDERS 设置包含一个查找器列表， 它们知道如何从各种源找到静态文件。
>其中默认的一个是AppDirectoriesFinder,它在每个INSTALLED_APPS下查找“static”子目录，就像刚刚在polls中创建的一样。 
>管理站点也为它的静态文件使用相同的目录结构。

在你刚刚创建的static目录中，创建另外一个目录polls并在它下面创建一个文件style.css。
换句话讲，你的样式表应该位于polls/static/polls/style.css。 
为什么怎么做其实前面关于如何访问模板的路径类似，关键的点就在于静态文件的命名空间，如果有多个应用，都要使用样式但是命名又一样，因此需要告诉Django该使用其中的哪一个，最简单的方法就是为他们添加命名空间。


****
**至此，Django的初步学习到此结束！**
****

#### Django 源码学习02：一个纯粹由Python编写的轻量Ｗeb服务器

 	runserver.py

#### Django 源码学习03：基于正则表达式的URL分派


#### Django 源码学习04：中间件 (Middleware)支持

	允许对请求处理的各个阶段进行干涉

#### Django 源码学习05：视图（Views）模块

	Views模块并不是Django中必须的，但它的存在简化了Django的开发

#### Django 源码学习06：db.models 模块

	Django 的db模块包含models和backends；
	models中定义了与数据库对应的各种fields和生成sql的rules；
	backends里则包含了对mysql、oracle、postgresql、sqlite3的支持。

#### Django 源码学习07：admin.auth模块

	admin.auth是django的权限模块。

#### Django 源码学习08：Session 存储

#### Django 源码学习09：Password 的生成和验证

#### Django 源码学习10：Template (模板)

#### Django 源码学习11：Form (表单)类

#### Django 源码学习12：Django安全机制


