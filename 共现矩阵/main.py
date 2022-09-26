import os.path
from typing import List
import re

import nltk
from nltk.corpus import stopwords


TXT_FILE_PATH = r"./source/欧洲芯片法.txt"
SAVE_CSV_FILE_PATH = r"./matrix.csv"


def read_content_from_file(path: str) -> List[str]:
    validLines = []
    with open(path, 'r', encoding='utf-8')as txt:
        lines = txt.readlines()
        handle_lines(lines)

    return validLines


def handle_lines(lines: List[str]):
    """
    处理所有的文本段
    :param lines: 文本段
    :return:
    """
    newLines = []

    for line in lines:
        if "..." in line:
            continue
        line = re.sub(r'http\S+', '', line)
        line = re.sub('[^a-zA-Z.?!]+', ' ', line)
        sentences = get_sentence_from_line(line)
        if len(sentences) == 0:
            continue
        else:
            for sen in sentences:
                newLines.append(sen)

    allStemming = stemming_lines(newLines)
    allStemming.sort()
    matrix = create_occurrence_matrix(newLines, allStemming)
    matrix = sort_matrix(matrix)

    save_matrix2csv(matrix)


def get_sentence_from_line(line: str) -> List[str]:
    sentenceList = []
    if "." in line:
        for sen in line.split("."):
            sentenceList.append(sen)
    else:
        sentenceList.append(line)

    questionList = []
    for sen in sentenceList:
        if "?" in sen:
            for sen in sen.split("?"):
                questionList.append(sen)
        else:
            questionList.append(sen)

    exclamationList = []
    for question in questionList:
        if "!" in question:
            for q in question.split("!"):
                exclamationList.append(q)
        else:
            exclamationList.append(question)

    result = []
    for exclamation in exclamationList:
        s = re.sub('[^a-zA-Z]+', ' ', exclamation)
        s.strip()
        if s != "" and len(s) > 20:
            result.append(s)

    return result


def create_occurrence_matrix(lines: List[str], stemming: List[str]) -> List[List]:
    """
    根据全文所有的词根和所有的文本分段，生成二维的共线矩阵
    :param lines: 所有单词长度大于10的文本段
    :param stemming: 全文所有的词根
    :return: 返回一个共现矩阵的二维数组
    """
    stemmingMap = dict()
    matrixHead = [""]
    for index in range(len(stemming)):
        matrixHead.append(stemming[index])
        stemmingMap[stemming[index]] = index + 1

    matrix = [matrixHead]
    for index in range(len(stemming)):
        row = get_list_by_count(len(stemming), stemming[index])
        matrix.append(row)

    for line in lines:
        stem = stemming_line(line)
        for i in range(len(stem)-1):
            for j in range(i+1, len(stem)):
                matrix[stemmingMap[stem[j]]][stemmingMap[stem[i]]] += 1
                matrix[stemmingMap[stem[i]]][stemmingMap[stem[j]]] += 1

    return matrix


def stemming_line(line: str) -> List[str]:
    """
    从一段文本中提取出所有的词干
    :param line: 一个字符串
    :return: 返回一个词干列表
    """
    tokens = nltk.word_tokenize(line)
    porter = nltk.PorterStemmer()
    stem = [porter.stem(t) for t in tokens]

    return remove_stopwords_from_list(stem)


def stemming_lines(lines: List[str]) -> List[str]:
    """
    从所有的文本集合中提取出所有的词干
    :param lines: 所有的文本列表
    :return: 返回一个词干列表
    """
    stemmingList = []
    s = set()
    for line in lines:
        tokens = nltk.word_tokenize(line)
        porter = nltk.PorterStemmer()
        stem = [porter.stem(t) for t in tokens]
        for item in stem:
            s.add(item)

    for item in s:
        stemmingList.append(item)

    return remove_stopwords_from_list(stemmingList)


def remove_stopwords_from_list(words: List[str]) -> List[str]:
    """
    去除单词列表中所有的停用词
    :param words: 单词列表
    :return: 返回去除停用词的单词列表
    """
    newWords = []
    for word in words:
        flag = False
        for item in stop:
            if word == item:
                flag = True
                break
        if not flag:
            newWords.append(word)

    return newWords


def get_list_by_count(count: int, word: str) -> List:
    """
    根据指定单词和长度生成数组
    :param count: 0的个数
    :param word: 数组首个元素
    :return:
    """
    row = [word]
    for index in range(count):
        row.append(0)
    return row


def sort_matrix(matrix: List[List]) -> List[List]:
    sumList = []

    count = len(matrix)
    for i in range(1, count):
        sum = 0
        for j in range(1, count):
            sum += matrix[i][j]
        sumList.append([sum, i])

    sumList = sorted(sumList, key=lambda item: item[0], reverse=True)

    newMatrixHead = ['']
    for item in sumList:
        newMatrixHead.append(matrix[0][item[1]])

    newMatrix = [newMatrixHead]
    for i in sumList:
        row = [matrix[0][i[1]]]
        for j in sumList:
            row.append(matrix[i[1]][j[1]])
        newMatrix.append(row)

    for index in range(1, len(newMatrix)):
        newMatrix[index][index] = 0

    return newMatrix


def save_matrix2csv(matrix: List[List]):
    """
    将二维数组保存成csv文件
    :param matrix: 二维数据，共现矩阵
    :return:
    """
    if os.path.exists(SAVE_CSV_FILE_PATH):
        os.remove(SAVE_CSV_FILE_PATH)

    with open(SAVE_CSV_FILE_PATH, 'w', encoding='utf-8')as m:
        for item in matrix:
            for i in item:
                m.write(str(i) + ",")
            m.write("\n")


if __name__ == '__main__':
    # nltk.download('punkt')
    # nltk.download('stopwords')
    stop = stopwords.words('english')
    read_content_from_file(TXT_FILE_PATH)

