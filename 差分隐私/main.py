import time

import numpy as np
from typing import List


def number_add_laplace_noise(value: float, limits: float, precision: int) -> float:
    """
    数值类型的值添加拉普拉斯噪声
    :param value: 需要添加噪声的值
    :param limits: 添加的噪声范围
    :param precision: 返回值需要保留几位小数
    :return: 返回添加噪声后的值
    """
    newValue = np.random.laplace(loc=value, scale=limits, size=1)[0]
    newValue = round(newValue, precision)
    return newValue


def enumerate_add_noise(real: str, probability: float, enumerateList: List[str]) -> str:
    """
    枚举类型的数据添加噪声
    :param real: 真实的数据
    :param probability: 返回真实数据的概率（0~1之间的浮点数）,只保留两位小数
    :param enumerateList: 枚举类型所有值的集合
    :return: 添加噪声后的值
    """
    probability = round(probability, 2)
    h = hash(time.time())
    if ((h % 100) / 100) < probability:
        return real
    else:
        h = hash(time.time())
        count = len(enumerateList)
        return enumerateList[(h % count)]


if __name__ == '__main__':
    newNumber = number_add_laplace_noise(100, 1, 0)
    print(newNumber)

    newEnumerate = enumerate_add_noise("Female", 0.2, ["Male", "Female"])
    print(newEnumerate)
