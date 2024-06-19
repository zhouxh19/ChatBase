# 按照 500 个字符长度截断段落
import re
from typing import List

import tiktoken
from langchain.text_splitter import CharacterTextSplitter
from torch import nn
from transformers import AutoTokenizer, AutoModel
import torch
from angle_emb import AnglE, Prompts

device = "cpu"
tokenizer = AutoTokenizer.from_pretrained("WhereIsAI/UAE-Large-V1")
emb_model = AutoModel.from_pretrained("WhereIsAI/UAE-Large-V1").to(device)
angle = AnglE.from_pretrained('WhereIsAI/UAE-Large-V1', pooling_strategy='cls').to(device)
model_path = "text_splitter/uae_partition_mlp_training20000_epoch10_balanced.pth"  # 指定保存路径

def num_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-4-0125-preview")
    num_tokens = len(encoding.encode(text))
    return num_tokens


def encode_text(text):
    vec = angle.encode({'text': text}, prompt=Prompts.C)
    return vec.flatten()


class MLPClassifier(nn.Module):
    def __init__(self, input_dim):
        super(MLPClassifier, self).__init__()
        self.fc1 = nn.Linear(input_dim * 4, 512)  # 假设input_dim是单个编码的维度
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(512, 1)

    def forward(self, x1, x2):
        diff = torch.abs(x1 - x2)
        product = x1 * x2
        features = torch.cat([x1, x2, diff, product], dim=-1)
        # print(features.shape)
        x = self.fc1(features)
        x = self.relu(x)
        x = self.fc2(x)
        return torch.sigmoid(x)


def split_article(article, max_tokens=360):
    parts = []
    start = 0
    punctuations = ".!?"

    while start < len(article):
        end = start

        while end < len(article):
            if num_tokens(article[start:end]) > max_tokens:
                break
            end += 1

        if end >= len(article):
            parts.append(article[start:])
            break

        last_punctuation = 0
        for i in range(end - 1, start - 1, -1):
            if article[i] in punctuations:
                last_punctuation = i
                break

        if last_punctuation > start:
            parts.append(article[start:last_punctuation + 1])
            start = last_punctuation + 1
        else:
            parts.append(article[start:end])
            start = end
    return parts


def mlp_article_partition(article):  # 输入是长 context  输出分好段的元组
    model = MLPClassifier(input_dim=1024).to(device)  # input_dim
    # Load the model weights
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    truncated_paragraphs = split_article(article)
    new_paragraphs = []
    embeddings = []
    split_tokens = [".", "?", "!"]

    for text in truncated_paragraphs:
        subtexts = re.split('(?<={})'.format('|'.join(map(re.escape, split_tokens))), text)

        current_paragraph = subtexts[0]
        for i in range(1, len(subtexts)):
            text1 = current_paragraph
            text2 = subtexts[i]
            encoded_text1 = tokenizer(text1, return_tensors='pt',
                                      max_length=512, truncation=True, padding='max_length').to(device)
            encoded_text2 = tokenizer(text2, return_tensors='pt',
                                      max_length=512, truncation=True, padding='max_length').to(device)
            embedding1 = emb_model(**encoded_text1).pooler_output
            embedding2 = emb_model(**encoded_text2).pooler_output
            outputs = model(embedding1, embedding2)
            predicted = outputs > 0.5  # adjusted threshold   # 越小就越倾向于切分为更多的子段
            # print(outputs)

            # 如果预测结果为0，将当前段落添加到new_paragraphs列表并开始新的段落
            if predicted.item() == 1:
                new_paragraphs.append(current_paragraph)
                current_paragraph = text2
            # 如果预测结果为1，将text2添加到当前段落
            else:
                current_paragraph += text2

        # 确保最后一个段落被添加
        new_paragraphs.append(current_paragraph)

    # 获取每个段落的嵌入并将其添加到嵌入列表中
    for para in new_paragraphs:
        embedding = encode_text(para)  # , tokenizer, emb_model
        embeddings.append(embedding)

    # Convert to NumPy array
    # embeddings = np.array(embeddings)
    # Build Faiss index
    # faiss_index = build_faiss_index(embeddings)   # 不需要可以注释掉，包括返回参数的 faiss_index
    # print(len(truncated_paragraphs), len(new_paragraphs))
    return new_paragraphs  # Returning new_paragraphs and a placeholder None value


class PartitionMlpTextSplitter(CharacterTextSplitter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def split_text(self, text: str) -> List[str]:
        sent_list = mlp_article_partition(text)
        return sent_list


if __name__ == '__main__':
    article = ('Postgresql数据库简介  一、PostgreSQL的起源与发展 '
               'PostgreSQL，作为一个著名的开源关系型数据库管理系统（RDBMS），其历史可追溯到1986年，最初由加利福尼亚大学伯克利分校的计算机科学教授Michael '
               'Stonebraker及其研究团队开发的一个项目——POSTGRES。该项目的目标是克服当时流行的数据库系统在灵活性、二次开发和复杂数据处理方面的局限。1996年，这个项目正式命名为PostgreSQL'
               '，以表明它是POSTGRES项目的后续作品，并包含了SQL语言的支持。 二、PostgreSQL的特点与优势 # 2.1 高度兼容SQL标准 '
               'PostgreSQL的一个显著特点是对SQL标准的高度遵循，它支持大多数SQL:2011标准，并且还扩展了许多新的特性，例如存储过程、触发器、视图等。# 2.2 高级数据类型和全文搜索 '
               '除了基本的数据类型外，PostgreSQL还支持数组、JSON/JSONB、hstore（键值对存储）等高级数据类型。同时，它还内置了强大的全文搜索功能。# 2.3 复杂查询和索引 '
               'PostgreSQL中的查询优化器可以处理复杂的查询，并且能够使用各种索引技术，比如B-tree、Hash、GiST、SP-GiST、GIN和BRIN等，来提高查询效率。# 2.4 并发与事务 '
               'PostgreSQL具有MVCC（多版本并发控制）机制，保证了在多用户并发访问时数据的一致性和隔离性。它还支持四级事务隔离，即读未提交、读已提交、可重复读和串行化。# 2.5 扩展性 '
               'PostgreSQL被设计为高度可扩展。用户可以定义自己的数据类型、函数、操作符甚至是自定义语言处理器。此外，其插件架构也允许第三方开发和集成更多功能。# 2.6 安全性与可靠性 '
               '安全性方面，PostgreSQL提供了强大的认证机制，包括LDAP、SCRAM-SHA-256、证书等多种方式。在可靠性方面，它支持在线备份、点对点复制、同步复制等功能，确保数据的安全和完整性。# '
               '2.7 社区支持与生态系统 作为一个开源项目，PostgreSQL拥有一个庞大而活跃的社区，这为用户提供了丰富的资源，如详尽的文档、多样的扩展和便捷的支持服务。PostgreSQL'
               '的生态系统中包含了许多工具和接口，使得它可以轻松地与其他软件集成。  三、PostgreSQL的架构 '
               'PostgreSQL采用客户端/服务器模型。服务器端负责数据的存储、查询处理、事务管理和网络通信等核心功能。客户端则通过各种接口与服务器进行交互，执行SQL命令。# 3.1 进程架构 '
               '在PostgreSQL中，每个客户端连接都由一个独立的进程（backend process）处理。这种设计简化了共享数据的管理，并使得系统可以有效地运行在多用户环境下。 # 3.2 存储系统 '
               'PostgreSQL的存储系统使用“写前日志”（Write-Ahead Logging, WAL）机制保证数据的原子性和持久性。WAL机制通过在实际修改数据之前记录变更日志来实现这一点。# 3.3 '
               '查询处理 查询处理涉及解析、规划和执行SQL语句。PostgreSQL的查询优化器会选择最佳的执行路径，从而提高查询的性能。 四、使用场景 '
               'PostgreSQL适用于多种应用场景，并且尤其擅长处理复杂查询和大型数据库。以下是一些常见的使用案例：# 4.1 企业级应用 '
               '大型企业经常需要处理庞大的数据量和高并发请求，PostgreSQL以其稳定性和可扩展性成为不错的选择。# 4.2 '
               '地理信息系统（GIS）PostGIS是PostgreSQL的一个扩展，它添加了地理空间对象的支持，使得PostgreSQL可以广泛应用于地理空间数据的存储和查询。# 4.3 网络应用 '
               '许多Web应用和服务使用PostgreSQL作为后端数据库，因为它提供了灵活的数据模型和强大的查询能力。# 4.4 数据分析 '
               'PostgreSQL的高级聚合函数、窗口函数和其他分析功能使得它适合于数据挖掘和在线分析处理（OLAP）。 五、与其他数据库的比较 与其他流行的数据库如MySQL、Oracle、SQL '
               'Server相比，PostgreSQL在某些方面提供了独有的优势。例如，它在标准SQL的支持、数据类型多样性以及扩展性方面通常被认为是领先的。同时，在开源数据库中，PostgreSQL'
               '经常被誉为最接近于商业数据库的产品，拥有与高端数据库相媲美的功能。然而，相比于一些其他数据库，PostgreSQL在一些特定环境下的性能可能不是最优的。例如，MySQL在Web'
               '应用和读密集型应用中可能会表现得更好，这主要得益于其简单的架构和高效的读操作。而对于需要高度可用性和分布式特性的场景，如NoSQL数据库Cassandra和MongoDB可能更为适合。 '
               '六、未来趋势与挑战 PostgreSQL正处于持续发展之中。随着云计算和大数据技术的普及，PostgreSQL'
               '社区正在逐步推出更多针对云环境优化的特性，同时也在改进其水平扩展能力，以便更好地处理大规模数据集。一方面，PostgreSQL'
               '需要不断提升其性能，以满足数据量剧增的需求；另一方面，它还需要在易用性、管理工具和维护性上做出改进，以降低用户的使用门槛和运营成本。随着人工智能和机器学习的兴起，PostgreSQL'
               '也在探索集成更多智能数据处理的特性。  结论 '
               '总体来看，PostgreSQL以其强大的功能集、严格的标准兼容性、开放的扩展性和稳固的社区支持，在数据库领域中占有重要的地位。无论是传统的企业级应用、新兴的Web服务还是复杂的GIS'
               '系统，PostgreSQL都能提供一个坚实可靠的数据管理平台。随着技术的不断进步和社区的不懈努力，PostgreSQL未来的发展令人期待。')
    new_paragraphs = PartitionMlpTextSplitter().split_text(article)
    print(len(new_paragraphs))