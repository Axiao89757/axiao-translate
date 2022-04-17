# 分割句子
def cut_sentences(content):
    # 结束符号，包含中文和英文的
    end_flag = ['?', '!', '.', '？', '！', '。', '…']

    content_len = len(content)
    sentences = []
    tmp_char = ''
    for idx, char in enumerate(content):
        # 拼接字符
        tmp_char += char

        # 判断是否已经到了最后一位
        if (idx + 1) == content_len:
            sentences.append(tmp_char)
            break

        # 判断此字符是否为结束符号
        if char in end_flag:
            # 再判断下一个字符是否为结束符号，如果不是结束符号，则切分句子
            next_idx = idx + 1
            if not content[next_idx] in end_flag:
                sentences.append(tmp_char)
                tmp_char = ''
    return sentences


# 动态获取窗口长度
def adapt_size(text):
    widths = ['150x100', '280x150', '410x200', '540x250', '590x250', '650x300']
    if len(text) >= 500:
        return widths[5]
    elif len(text) >= 400:
        return widths[4]
    elif len(text) >= 300:
        return widths[3]
    elif len(text) >= 200:
        return widths[2]
    elif len(text) >= 100:
        return widths[1]
    else:
        return widths[0]

