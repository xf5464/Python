https://pypi.python.org/pypi/svn 上下载的不是全的，没有update
去https://github.com/dsoprea/PySvn下载下来，然后复制svn文件夹到Python35\Lib\site-packages或者打包成whl再安装
如果你先去python.org下载whl安装，再安装github上下载编好的whl，尝试了下文件不会改，所以直接把svn文件夹复制到site-packages下就可以。