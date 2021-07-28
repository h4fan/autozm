# autozm
利用zoomeye api搜索c段ip和端口，存入sqlite进行查询

## 用法

1. 执行`python initdb.py`创建ipport.db
2. 替换autozm.py中的`APIKEY_ZE`
3. 将要查询的ip地址写入`cidr.txt`
4. 运行`python autozm.py`，会将结果存入ipport.db，当出现`getting no result, break`时，说明apikey调用次数用完，ctrl+c结束程序。
5. 利用sqlite打开ipport.db,使用sql查询。

