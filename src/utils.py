from pynput.keyboard import Key, Controller

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
def adapt_size(text, format):
    widths = ['200', '400', '500', '590', '650']
    heights = ['70', '100', '200', '250', '300']
    num = str(70 + text.count('\n') * 25)
    if len(text) >= 300:
        return widths[4], heights[4] if format else num
    elif len(text) >= 200:
        return widths[3], heights[3] if format else num
    elif len(text) >= 100:
        return widths[2], heights[2] if format else num
    elif len(text) >= 10:
        return widths[1], heights[1] if format else num
    else:
        return widths[0], heights[0] if format else num



# 执行复制操作
def do_ctrl_c():
    kb = Controller()
    kb.press(Key.ctrl)
    kb.press("c")
    kb.release(Key.ctrl)
    kb.release("c")

