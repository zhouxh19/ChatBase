"""
<指令>你是一名高级数据专家，回答必须类似于以下可以被反序列化的 json 格式，不需要在外层添加任何信息：{"reason": '根据已知信息，我们有三个数据源，即"nation", "orders", 和 "customer"。这些数据源的字段如下：\n - nation：n_nationkey（国家关键字）、n_name（国家名称）、n_regionkey（区域关键字）、n_comment（注释）\n - orders：o_orderkey（订单关键字）、o_custkey（客户关键字）、o_orderstatus（订单状态）、o_totalprice（总价）、o_orderdate（订单日期）、o_orderpriority（订单优先级）、o_clerk（职员）、o_shippriority（发货优先级）、o_comment（注释）\n - customer：c_custkey（客户关键字）、c_name（客户名称）、c_address（地址）、c_nationkey（国家关键字）、c_phone（电话）、c_acctbal（账户余额）、c_mktsegment（市场部分）、c_comment（注释）\n\n为了找出"日本每年的销售额"，我们需要以下步骤：\n 1. 在“nation”数据集中找到代表“日本”的n_nationkey。\n 2. 在“customer”数据集中找到对应的c_custkey，即在哪些客户来自日本。\n 3. 利用这些c_custkey在“orders”数据集中找到所有的订单，并加总o_totalprice', "used_data_paths": ["./multi_source_files/tpch_nation.csv"], "code": '\n def calculate_sales(): \n import pandas as pd \n nations = pd.read_csv("./multi_source_files/tpch_nation.csv", names=["n_nationkey", "n_name", "n_regionkey", "n_comment"]) \n customers = pd.read_csv("./multi_source_files/tpch_customer.csv", names=["c_custkey", "c_name", "c_address", "c_nationkey", "c_phone", "c_acctbal", "c_mktsegment", "c_comment"]) \n orders = pd.read_csv("./multi_source_files/tpch_orders.csv", names=["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate", "o_orderpriority", "o_clerk", "o_shippriority", "o_comment"]) \n japan_key = nations[nations["n_name"]=="Japan"]["n_nationkey"].values[0] \n japan_cust_keys = customers[customers["c_nationkey"]==japan_key]["c_custkey"].unique() \n sales = orders[orders["o_custkey"].isin(japan_cust_keys)]["o_totalprice"].sum() \n return {"column_names": ["Annual Sales"], "data": [[sales]]}'}。需要从已知信息的多个数据源中根据问题使用Python3写出能稳定运行且能计算出问题答案的def代码，且def执行后能返回这样格式的Json数据：{"column_names": ["a", "b"], "data": [[1, "a"],[2, "b"]]}。额外要求如下：1、如果某行的数据为空，则忽略。2、不允许添加编造成分。3、三方库的import放到def中。</指令>
\n<已知信息>[{"path":"./multi_source_files/tpch_nation.csv","header":"n_nationkey, n_name, n_regionkey, n_comment"},{"path":"./multi_source_files/tpch_orders.csv","header":"o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment"},{"path":"./multi_source_files/tpch_customer.csv","header":"c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment"}]</已知信息>
\n<问题>请问日本每年的销售额是多少？</问题>

'<指令>你是一名高级数据专家，任务是从已知信息的多个数据源中根据用户问题，使用Python3写出能稳定运行且能计算出问题答案的def代码，且代码执行后能返回固定Json格式的数据：{"column_names": ["a", "b"], "data": [[1, "a"],[2, "b"]]}。回答生成时需要包含三点：设计理由(理由应详细且合理，100字以内)、使用到的数据源地址、Python执行代码(代码中不需要添加注释)。回答必须类似于以下可以被反序列化的 json 格式：{"reason": "根据已知信息，我们有三个数据源，即"nation", "orders", 和 "customer"。这些数据源的字段如下：\n - nation：n_nationkey（国家关键字）、n_name（国家名称）、n_regionkey（区域关键字）、n_comment（注释）\n - orders：o_orderkey（订单关键字）、o_custkey（客户关键字）、o_orderstatus（订单状态）、o_totalprice（总价）、o_orderdate（订单日期）、o_orderpriority（订单优先级）、o_clerk（职员）、o_shippriority（发货优先级）、o_comment（注释）\n - customer：c_custkey（客户关键字）、c_name（客户名称）、c_address（地址）、c_nationkey（国家关键字）、c_phone（电话）、c_acctbal（账户余额）、c_mktsegment（市场部分）、c_comment（注释）\n\n为了找出"日本每年的销售额"，我们需要以下步骤：\n 1. 在“nation”数据集中找到代表“日本”的n_nationkey。\n 2. 在“customer”数据集中找到对应的c_custkey，即在哪些客户来自日本。\n 3. 利用这些c_custkey在“orders”数据集中找到所有的订单，并加总o_totalprice', "used_data_paths": ["./multi_source_files/tpch_nation.csv"], "code": '\n def calculate_sales(): \n import pandas as pd \n nations = pd.read_csv("./multi_source_files/tpch_nation.csv", names=["n_nationkey", "n_name", "n_regionkey", "n_comment"]) \n customers = pd.read_csv("./multi_source_files/tpch_customer.csv", names=["c_custkey", "c_name", "c_address", "c_nationkey", "c_phone", "c_acctbal", "c_mktsegment", "c_comment"]) \n orders = pd.read_csv("./multi_source_files/tpch_orders.csv", names=["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate", "o_orderpriority", "o_clerk", "o_shippriority", "o_comment"]) \n \n japan_key = nations[nations["n_name"]=="Japan"]["n_nationkey"].values[0] \n japan_cust_keys = customers[customers["c_nationkey"]==japan_key]["c_custkey"].unique() \n sales = orders[orders["o_custkey"].isin(japan_cust_keys)]["o_totalprice"].sum() \n return {"column_names": ["Annual Sales"], "data": [[sales]]}"}。额外要求如下：1、如果某行的数据为空，则忽略。2、不允许添加编造成分。3、三方库的import放到def中。</指令> \n'

{"reason": "", "used_data_paths": ["./multi_source_files/tpch_nation.csv"], "code": "def ..."}

{"reason": '根据已知信息，我们有三个数据源，即"nation", "orders", 和 "customer"。这些数据源的字段如下：\n - nation：n_nationkey（国家关键字）、n_name（国家名称）、n_regionkey（区域关键字）、n_comment（注释）\n - orders：o_orderkey（订单关键字）、o_custkey（客户关键字）、o_orderstatus（订单状态）、o_totalprice（总价）、o_orderdate（订单日期）、o_orderpriority（订单优先级）、o_clerk（职员）、o_shippriority（发货优先级）、o_comment（注释）\n - customer：c_custkey（客户关键字）、c_name（客户名称）、c_address（地址）、c_nationkey（国家关键字）、c_phone（电话）、c_acctbal（账户余额）、c_mktsegment（市场部分）、c_comment（注释）\n\n为了找出"日本每年的销售额"，我们需要以下步骤：\n 1. 在“nation”数据集中找到代表“日本”的n_nationkey。\n 2. 在“customer”数据集中找到对应的c_custkey，即在哪些客户来自日本。\n 3. 利用这些c_custkey在“orders”数据集中找到所有的订单，并加总o_totalprice', "used_data_paths": ["./multi_source_files/tpch_nation.csv"], "code": '\n def calculate_sales(): \n import pandas as pd \n # Load data \n nations = pd.read_csv("./multi_source_files/tpch_nation.csv", names=["n_nationkey", "n_name", "n_regionkey", "n_comment"]) \n customers = pd.read_csv("./multi_source_files/tpch_customer.csv", names=["c_custkey", "c_name", "c_address", "c_nationkey", "c_phone", "c_acctbal", "c_mktsegment", "c_comment"]) \n orders = pd.read_csv("./multi_source_files/tpch_orders.csv", names=["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate", "o_orderpriority", "o_clerk", "o_shippriority", "o_comment"]) \n \n # Find Japan\'s nation key \n japan_key = nations[nations["n_name"]=="Japan"]["n_nationkey"].values[0] \n # Find customer keys of Japanese customers \n japan_cust_keys = customers[customers["c_nationkey"]==japan_key]["c_custkey"].unique() \n # Find all orders from these customers and sum the total price \n sales = orders[orders["o_custkey"].isin(japan_cust_keys)]["o_totalprice"].sum() \n return {"column_names": ["Annual Sales"], "data": [[sales]]}'}

"""
import json
import os
import re
import glob
import time

from configs.file_config import MULTI_SOURCE_FILES_PATH


def extract_method_name(code):
    # 正则表达式匹配方法定义语句，提取方法名
    pattern = r"def\s+(\w+)\s*\("
    match = re.search(pattern, code)
    if match:
        return match.group(1)
    else:
        return None


def execute_code(code):
    try:
        # Execute the code to populate the namespace
        exec(code, globals())
        data = eval(extract_method_name(code) + '()')
        # Filter out special variables
        return {
            "status": True,
            "data": data,
            "msg": "success"
        }
    except Exception as e:
        msg = f"An error occurred: {str(e)}"
        return {
            "status": False,
            "data": [],
            "msg": msg
        }


# def calculate_sales():
#     import pandas as pd
#     house_sales = pd.read_csv("/Volumes/NBDATA/JobProjects/Tsinghua/Data-chat/multi_source_files/北上广深售房数据807-813-202.csv")
#     tianhe_sales = house_sales[house_sales["区县"] == "天河区"]
#     total_sales = tianhe_sales["成交套数"].sum()
#     result = {"column_names": ["House Sales"], "data": [[total_sales]]}
#     return result

def all_file_names(file_paths):
    file_names = []
    for file_path in file_paths:
        # 使用正则表达式提取文件名部分，并去掉文件格式
        match = re.search(r"/([^/]+)\.\w+$", file_path)
        if match and len(match.groups()) >= 1:
            file_names.append(match.group(1))  # 返回匹配到的文件名（不包含格式）
        else:
            file_names.append("")  # 如果没有匹配到文件名，则返回空字符串
    return file_names


def all_files():
    folder_path = MULTI_SOURCE_FILES_PATH
    file_list = os.listdir(folder_path)
    edges = []
    # 获取去掉文件格式的文件名
    file_short_names = [file_name.split('.')[0] for file_name in file_list]
    print('=====:', file_short_names)
    for file_name in file_list:
        file_name = file_name.split('.')[0]
        if '&' in file_name:
            names = file_name.split('&')
            print('===names===:', names)
            for name in names:
                if name in file_short_names:
                    edges.append({"source": name, "target": file_name})

    print('===edges===:', edges)


def rename_keys_in_json(source_file, target_file, key_map):
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list):
        # data = data[:1000]
        new_data = [{key_map.get(key, key): value for key, value in item.items()} for item in data]
    else:
        new_data = {key_map.get(key, key): value for key, value in data.items()}

    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False)


def copy_json_files_to_new_directory(source_directory, target_directory):
    # 使用glob直接找到所有.json文件
    filepaths = glob.glob(os.path.join(source_directory, '*.json'))

    # 创建目标目录（如果不存在）
    os.makedirs(target_directory, exist_ok=True)

    # 使用列表推导式创建文件详情信息, 包含源文件路径和目标文件路径
    files = [{
        "source_file": filepath,
        "target_file": os.path.join(target_directory, os.path.basename(filepath)),
        "base_filename": os.path.splitext(os.path.basename(filepath))[0]
    } for filepath in filepaths]

    return files


def format_data_to_new_file(source_file, target_file):
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        question_data = data.get('question')
        answer_data = data.get('answer')
        new_data = []
        for i, (question, answer) in enumerate(zip(question_data, answer_data)):
            if i < 1000:  # 限制只处理前1000条数据
                new_data.append({"question": question, "answer": answer})
            else:
                print("source_file", source_file)
                break
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False)


def append_answer_to_question(source_file):
    new_data = []
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, list):
            # data = data[:1000]
            for item in data:
                item['original_question'] += ' ' + item['original_answer']
                new_data.append(item)
        with open(source_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False)

def split_json_file(filename, output_dir, items_per_file=2000):

    base_filename = os.path.splitext(os.path.basename(filename))[0]

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 判断数据是否可以被分割，例如数据应该是一个列表
    if not isinstance(data, list):
        raise ValueError("JSON data is not a list")

    os.makedirs(output_dir, exist_ok=True)

    for i in range(0, len(data), items_per_file):
        chunk = data[i:i + items_per_file]
        output_filename = os.path.join(output_dir, f'{base_filename}-{i}.json')

        with open(output_filename, 'w', encoding='utf-8') as output_file:
            json.dump(chunk, output_file, ensure_ascii=False)


def read_pdf_to_text(pdf_file, txt_file):
    from document_loaders import RapidOCRPDFLoader
    loader = RapidOCRPDFLoader(pdf_file)
    docs = loader.load()
    print("docs:", docs)
    text = "".join([doc.page_content for doc in docs])
    # 保存text到txt文件内
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(text)

from celery_app import app

@app.task
def task_run():
    time.sleep(100000)
    print('Task executed.')



if __name__ == '__main__':
    # data = {
    #     "code": "def gen_code():\n    import pandas as pd\n    house_sales = pd.read_csv(\"/Volumes/NBDATA/JobProjects/Tsinghua/Data-chat/multi_source_files/北上广深售房数据807-813-202.csv\")\n    tianhe_sales = house_sales[house_sales[\"区县\"] == \"天河区\"]\n    total_sales = tianhe_sales[\"成交套数\"].sum()\n    return {\"column_names\": [\"House Sales\"], \"data\": [[total_sales]]}\n"
    # }
    #
    # code = data.get('code')
    # print(code)
    #
    # print(execute_code(code))

    source_directory = '/Volumes/NBDATA/JobProjects/Tsinghua/李老师课件资料/ZH/db-qa/content/'
    target_directory = '/Volumes/NBDATA/JobProjects/Tsinghua/李老师课件资料/ZH/db-qa/new_content'
    key_map = {'original_question': 'page_content', 'original_answer': 'llm_content'}
    files = copy_json_files_to_new_directory(source_directory, target_directory)

    for file in files:
        rename_keys_in_json(file.get('source_file'), file.get('target_file'), key_map)

    # filepaths = glob.glob(os.path.join(source_directory, '*.json'))
    # for filepath in filepaths:
    #     append_answer_to_question(filepath)

    # split_json_file("/Volumes/NBDATA/JobProjects/Tsinghua/Dataset(1)/ZH/format-data-large/DBstackExchange.json", '/Volumes/NBDATA/JobProjects/Tsinghua/Dataset(1)/ZH/format-data-large/')

    # read_pdf_to_text("/Volumes/NBDATA/JobProjects/Tsinghua/李老师课件资料/数据库系统概论-第5版_完整版.pdf", "/Volumes/NBDATA/JobProjects/Tsinghua/李老师课件资料/数据库系统概论-第5版.txt")

    # task_run.delay()
