#### pipenv的逻辑

pipenv install的时候有三种逻辑：

- 如果目录下没有Pipfile和Pipfile.lock文件，表示创建一个新的虚拟环境；
- 如果有，表示使用已有的Pipfile和Pipfile.lock文件中的配置创建一个虚拟环境；
- 如果后面带诸如django这一类库名，表示为当前虚拟环境安装第三方库。

#### 安装pipenv

```
pip install pipenv
```

#### 简单使用

进入你的Python项目文件夹：

```
cd your_project
pipenv install
```

生成``pipfile`` 文件 和 ``pipfile.lock`` 文件

#### 安装第三方模块

使用pipenv创建虚拟环境后，**进入pipfile所在目录**，使用install命令安装第三方库。 例如：

```
pipenv install django
```

要卸载某个第三方库：

```
pipenv uninstall beautifulsoup4
```

#### 冻结Pipfile

类似于virtualenv中生成requirements.txt文件。

更新Pipfile.lock来冻结库名称及其版本，以及其依赖关系的列表。需要使用lock参数：

```
pipenv lock
```

如果另一个用户拷贝了你的项目，他们只需要安装Pipenv，然后：

```
pipenv install
```

#### 管理开发环境

通常有一些Python包只在你的开发环境中需要，而不是在生产环境中，例如单元测试包。 Pipenv使用--dev标志区分两个环境。

```
pipenv install --dev django
```

django库现在将只在开发虚拟环境中使用。如果你要在你的生产环境中安装你的项目：

```
pipenv install  # 将不会安装django包
```

如果有一个开发人员将你的项目克隆到自己的开发环境中，他们可以使用--dev标志：

```
pipenv install --dev   # 将会安装django包
```

#### 在虚拟环境中运行命令

使用run参数，提供要运行的命令：

```
pipenv run python manage.py runserver
```

将使用当前虚拟环境关联的Python解释器，执行命令。

简单的执行脚本：

```
pipenv run python your_script.py
```

#### pipenv的选项

```
Options:
  --where             显示项目文件所在路径
  --venv              显示虚拟环境实际文件所在路径
  --py                显示解释器所在路径
  --envs              虚拟环境的选项变量
  --rm                删除当前虚拟环境
  --bare              最小化输出 ??
  --completion        完整输出
  --man               显示帮助页面
  --support           Output diagnostic information for use in GitHub issues.
  --site-packages     显示安装的库
  --python TEXT       指定某个python版本作为虚拟环境的安装源
  --three / --two     Use Python 3/2 when creating virtualenv.
  --clear             Clears caches (pipenv, pip, and pip-tools).
  -v, --verbose       冗长模式
  --pypi-mirror TEXT  指定pip源.
  --version           版本信息.
  -h, --help          帮助信息.


Usage Examples:
   Create a new project using Python 3.7, specifically:
   $ pipenv --python 3.7

   Remove project virtualenv (inferred from current directory):
   $ pipenv --rm

   Install all dependencies for a project (including dev):
   $ pipenv install --dev

   Create a lockfile containing pre-releases:
   $ pipenv lock --pre

   Show a graph of your installed dependencies:
   $ pipenv graph

   Check your installed dependencies for security vulnerabilities:
   $ pipenv check

   Install a local setup.py into your virtual environment/Pipfile:
   $ pipenv install -e .

   Use a lower-level pip command:
   $ pipenv run pip freeze

Commands:
  check      检查安全漏洞.
  clean      卸载所有不在 lock文件 的三方库.
  graph      显示库 及其依赖.
  install    安装虚拟环境 或 三方库
  lock       锁定并更新 pipfile.lock 文件
  open       在编辑器中查看库
  run        在虚拟环境中运行命令
  shell      进入虚拟环境
  sync       安装所有lock文件中的三方库.
  uninstall  卸载一个三方库.
  update     安装三方库的最新版本.
```

