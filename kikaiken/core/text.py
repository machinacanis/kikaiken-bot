def text_global_exception():
    return ">>> 「Kikaiken System」 \n\n发生了意料之外的情况！\n异常信息已被上传到主脑，也许晚点再试试？"


def text_find_no_result():
    return ">>> 「Kikaiken System」 \n\n没有找到任何相关结果噢？"


def text_need_no_paging(paged_result: str, result_count: int):
    return f">>> 「Kikaiken System」 \n\n找到了 {result_count} 条结果！\n{paged_result}"


def text_need_paging(paged_result: str, result_count: int, page_num: int, total_page: int):
    return f">>> 「Kikaiken System」 \n\n找到了 {result_count} 条结果！第 {page_num}/{total_page} 页：\n{paged_result}\n添加参数 -p [页码] 即可翻页~"


def text_paging_too_large(total_page: int):
    return f">>> 「Kikaiken System」 \n\n没有这么多页啦，总共就只有 {total_page} 页噢！"


def text_add_group_into_white_list(group_id: int):
    return f">>> 「Kikaiken System」 \n\n群聊 {group_id} 已经被我加进白名单了！"


def text_remove_group_from_white_list(group_id: int):
    return f">>> 「Kikaiken System」 \n\n群聊 {group_id} 已经被我从白名单中移除了！"


def text_add_user_into_black_list(user_id: int):
    return f">>> 「Kikaiken System」 \n\n用户 {user_id} 已经被我加进黑名单了，呼呼，消消气吧？"


def text_remove_user_from_black_list(user_id: int):
    return f">>> 「Kikaiken System」 \n\n用户 {user_id} 已经被我从黑名单中移除了！"


def text_be_kicked_from_group(group_id: int):
    return f">>> 「Kikaiken System」 \n\n群聊 {group_id} 把我踢出去了，岂有此理！"


def text_be_muted_in_group(group_id: int, oprator_id: int):
    return f">>> 「Kikaiken System」 \n\n群聊 {group_id} 里的管理员 {oprator_id} 把我禁言了，我什么都没干，信我啊！"
