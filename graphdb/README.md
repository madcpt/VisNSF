# Structure

- *conf*文件夹下是janusgraph连接后端的配置文件
- *graphml*文件夹下是导出的网络图
- *processing*文件夹下是处理数据的代码

# How to Use

- 将原始数据处理为[Janusgraph-Utils](https://github.com/IBM/janusgraph-utils)的数据映射格式
  - 数据映射配置文件*schema.json*以及*datamapper.json*已放置在*processed*文件夹下
  - 使用目录下相应代码即可完成映射
  - 具体配置文件格式请参考Janusgraph-Utils文档

- 使用Janusgraph-Utils批量导入

  - 执行以下代码：

    ```shell
    cd /path/to/janusgraph-utils
    
    export JANUSGRAPH_HOME=~/janusgraph
    ./run.sh import /path/to/janusgraph/conf/xxx.properties /path/to/processed /schema.json /path/to/processed/datamapper.json
    ```

    其中`xxx.properties`在*conf*文件夹下

  - 导入完毕后，即可通过Gremlin读取或写入存储在hbase后端的图数据

- 使用Gremlin读取图数据

  - 启动Gremlin Console，并使用命令：

    ```shell
    gremlin> graph = JanusGraphFactory.open('/path/to/janusgraph/conf/xxx.properties')
    ```

    即可加载图数据

  - 当然，我们也可以读取远程服务器上的数据，并进行操作：

    ```shell
    gremlin> :remote connect tinkerpop.server conf/remote.yaml
    gremlin> :> g.V().count()
    ```

    注意在访问服务器时需要使用`:>`

- 将table导入hbase

  - 我们导出了*janus_us*、*janus_cn*、以及*janus_uscn*三个table到同名文件夹下，它们能够通过以下命令重新导入到hbase中：

    ```shell
    $ bin/hbase org.apache.hadoop.hbase.mapreduce.Import <tablename> <inputdir>
    ```

    

  