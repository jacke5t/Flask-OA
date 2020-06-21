
数据库操作步骤
    1.init命令，初始化，创建迁移文件目录，只需要执行一次
        python main.py db init
    2.migrate生成迁移文件，将模型中的变更生成对应文件
        python main.py db migrate
    3.upgrade命令，执行迁移文件，将生成的迁移文件执行，达到同步表结构的效果
        python main.py db upgrade