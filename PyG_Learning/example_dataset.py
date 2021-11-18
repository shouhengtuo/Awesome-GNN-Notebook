import torch
import torch.nn.functional as F
import torch_geometric
from torch_geometric.nn import GCNConv
from typing import Mapping, Optional, Callable, List
import os.path as osp
from torch_geometric.data import InMemoryDataset, download_url
from torch_geometric.io import read_planetoid_data
torch_geometric.seed_everything(2021)
class Planetoid(InMemoryDataset):
    url = 'https://github.com/kimiyoung/planetoid/raw/master/data'  # 在线下载的地址
    def __init__(self, root: str, name: str, split: str = "public",
                 num_train_per_class: int = 20, num_val: int = 500,
                 num_test: int = 1000, transform: Optional[Callable] = None,
                 pre_transform: Optional[Callable] = None):
        '''
        root: 根文件夹目录：xxx\planetoid-master\data
        name: 数据集：Cora, CiteSeer, PubMed
        split: public, full, random
                public -> Revisiting Semi-Supervised Learning with Graph Embeddings (fixed split)
                full -> 所有节点除了验证集和测试集之外都用于训练 -> FastGCN
                random -> train, validation, and test sets -> num_train_per_class, num_val, num_test
        num_train_per_class: 每一个类中训练集的个数
        num_val: 验证集个数
        num_test: 测试集个数
        transform (callable, optional): torch_geometric.data.Data -> transformed version (default: obj: None)
        pre_transform (callable, optional): torch_geometric.data.Data -> transformed version (default: obj: None)
                                            The data object will be transformed before being saved to disk.
        '''
        self.name = name
        # 传入父类: root: 数据集根目录文件路径, transform: None, pre_transform: None
        super().__init__(root, transform, pre_transform)    # 进入父类 InMemoryDataset 根据传入参数执行初始化
        # 加载处理好的保存在本地的数据之后进行数据集的分割
        self.data, self.slices = torch.load(self.processed_paths[0])

        self.split = split
        assert self.split in ['public', 'full', 'random']

        if split == 'full':
            data = self.get(0)
            data.train_mask.fill_(True)
            data.train_mask[data.val_mask | data.test_mask] = False
            self.data, self.slices = self.collate([data])

        elif split == 'random':
            data = self.get(0)
            data.train_mask.fill_(False)
            for c in range(self.num_classes):
                idx = (data.y == c).nonzero(as_tuple=False).view(-1)
                idx = idx[torch.randperm(idx.size(0))[:num_train_per_class]]
                data.train_mask[idx] = True

            remaining = (~data.train_mask).nonzero(as_tuple=False).view(-1)
            remaining = remaining[torch.randperm(remaining.size(0))]

            data.val_mask.fill_(False)
            data.val_mask[remaining[:num_val]] = True

            data.test_mask.fill_(False)
            data.test_mask[remaining[num_val:num_val + num_test]] = True

            self.data, self.slices = self.collate([data])
    @property
    def raw_dir(self) -> str:
        return osp.join(self.root, self.name, 'raw')

    @property
    def processed_dir(self) -> str:
        return osp.join(self.root, self.name, 'processed')

    @property
    def raw_file_names(self) -> List[str]:
        names = ['x', 'tx', 'allx', 'y', 'ty', 'ally', 'graph', 'test.index']
        return [f'ind.{self.name.lower()}.{name}' for name in names]

    @property
    def processed_file_names(self) -> str:
        return 'data.pt'

    def download(self):
        for name in self.raw_file_names:
            download_url('{}/{}'.format(self.url, name), self.raw_dir)

    def process(self):  # 在子类 Planetoid 中重写该方法
        data = read_planetoid_data(self.raw_dir, self.name) # 读取数据
        data = data if self.pre_transform is None else self.pre_transform(data) # 如果存在预处理则执行
        torch.save(self.collate([data]), self.processed_paths[0])   # 保存在本地

    def __repr__(self) -> str:
        return f'{self.name}()'

class GCN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(dataset.num_node_features, 16)
        self.conv2 = GCNConv(16, dataset.num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)

        return F.log_softmax(x, dim=1)
        
dataset = Planetoid(root='D:\GNN_and_Applications\Awesome-GNN-Notebook\PyG_Learning\planetoid-master\data', name='Cora')
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model = GCN().to(device)
# data = dataset[0].to(device)
# optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

# model.train()
# for epoch in range(200):
#     optimizer.zero_grad()
#     out = model(data)
#     loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
#     loss.backward()
#     optimizer.step()

# model.eval()
# pred = model(data).argmax(dim=1)
# correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
# acc = int(correct) / int(data.test_mask.sum())
# print('Accuracy: {:.4f}'.format(acc))