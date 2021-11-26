#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6


import numpy as np
from torchvision import datasets, transforms
from utils.Detective import tensor_deteciteve

def mnist_iid(dataset, num_users):
    """
    Sample I.I.D. client data from MNIST dataset
    :param dataset: variable :  <class 'torch.Tensor'> :  torch.Size([60000, 28, 28]) -> train_data
    :param num_users:   客户端个数 clients num
    :return: dict of image index (num_clients)
    """
    # set() 函数创建一个无序不重复元素集, 可进行关系测试, 删除重复数据, 还可以计算交集, 差集, 并集等。
    # np.random.choice(ndarray, int, replace = True, p = None)
    # replace: True 表示可以取相同数字, False 表示不可以取相同数字.
    # p: 与数组 ndarray 相对应，表示取数组 ndarray 中每个元素的概率, 默认为选取每个元素的概率相同.
    
    # local dataset num
    num_items = int(len(dataset)/num_users) 
    # dict_users -> 所有客户端数据 samples 的索引字典, all_idxs -> 所有数据 samples 的索引列表
    dict_users, all_idxs = {}, [i for i in range(len(dataset))]
    # 基于 clients num 执行循环
    for i in range(num_users):
        # 基于字典 data structure 分配每个 client 的数据 samples -> set() + np.random.choice(ndarray, int)
        dict_users[i] = set(np.random.choice(all_idxs, num_items, replace=False))
        # 从所有数据 samples 的索引列表中删除已经分配的数据 samples
        all_idxs = list(set(all_idxs) - dict_users[i])
    return dict_users


def mnist_noniid(dataset, num_users):
    """
    Sample non-I.I.D client data from MNIST dataset
    :param dataset:
    :param num_users:
    :return: dict of image index (num_clients)
    """
    # 将全部的 data 分成 200 组, 每一组 300 个数据 sample (num_users = 100, 60000/100 = 200 x 300)
    # 根据 clients 的数量, 需要从 0-199 中采样两组对应 2 x 300 = 600 个数据 sample 作为 client 的索引
    num_shards, num_imgs = 200, 300
    idx_shard = [i for i in range(num_shards)]
    dict_users = {i: np.array([], dtype='int64') for i in range(num_users)}
    # idxs -> min: 0, max: 59999, size: 60000
    idxs = np.arange(num_shards*num_imgs)
    # 获取 mnist 数据训练集标签 variable :  <class 'numpy.ndarray'> :  (60000,)
    labels = dataset.train_labels.numpy()

    # sort labels (label 排序保证 Non-I.I.D)
    # 二维数组切片
    # argsort(ndarray) 函数返回的数组值从小到大的索引
    # argsort(-ndarray) 函数返回的数组值从大到小的索引
    # 拼接数据 sample 索引和标签 variable :  <class 'numpy.ndarray'> :  (2, 60000)
    idxs_labels = np.vstack((idxs, labels))
    # dim0: 数据 sample 的索引, dim1: 相应的 label
    # 按照标签排序得到对应索引 variable :  <class 'numpy.ndarray'> :  (2, 60000)
    idxs_labels = idxs_labels[:,idxs_labels[1,:].argsort()]
    # 按照标签从 0-9 的数据 sample 索引
    idxs = idxs_labels[0,:]

    # divide and assign
    for i in range(num_users):
        # 随机选择 0-199 中的两组
        rand_set = set(np.random.choice(idx_shard, 2, replace=False))
        # 删除对应的 rand_set
        idx_shard = list(set(idx_shard) - rand_set)
        # concatenate
        for rand in rand_set:
            dict_users[i] = np.concatenate((dict_users[i], idxs[rand*num_imgs:(rand+1)*num_imgs]), axis=0)
    return dict_users


def cifar_iid(dataset, num_users):
    """
    Sample I.I.D. client data from CIFAR10 dataset
    :param dataset:
    :param num_users:
    :return: dict of image index
    """
    num_items = int(len(dataset)/num_users)
    dict_users, all_idxs = {}, [i for i in range(len(dataset))]
    for i in range(num_users):
        dict_users[i] = set(np.random.choice(all_idxs, num_items, replace=False))
        all_idxs = list(set(all_idxs) - dict_users[i])
    return dict_users


if __name__ == '__main__':
    dataset_train = datasets.MNIST('../data/mnist/', train=True, download=True,
                                   transform=transforms.Compose([
                                       transforms.ToTensor(),
                                       transforms.Normalize((0.1307,), (0.3081,))
                                   ]))
    num = 100
    d = mnist_noniid(dataset_train, num)
