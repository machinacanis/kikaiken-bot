from io import BytesIO


class MessageModel:
    content: list[str]  # 文本内容，可以多行，每行是一个字符串
    image: list[BytesIO | str]  # 图片内容，可以多张，每张是一个BytesIO对象或一个图片链接
    is_paged: bool  # 是否分页，如果为True，则将展示分页内容
    paged_content: list[str]  # 分页内容，每页是一个字符串行
    rows_per_page: int  # 每页行数，如果is_paged为True，则该值有效

    def get_page_count(self) -> int:
        """
        计算分页数量
        """
        if not self.is_paged:
            return 1
        return len(self.paged_content)

    def add_content(self, content: str | list[str]):
        if isinstance(content, str):
            self.content.append(content)
        elif isinstance(content, list):
            self.content.extend(content)
        else:
            raise TypeError("content must be str or list[str]")

    def add_image(self, image: BytesIO | str | list[BytesIO | str]):
        if isinstance(image, BytesIO) or isinstance(image, str):
            self.image.append(image)
        elif isinstance(image, list):
            self.image.extend(image)
        else:
            raise TypeError("image must be BytesIO or str or list[BytesIO or str]")

    def add_paged_content(self, paged_content: str | list[str]):
        if not self.is_paged:
            self.is_paged = True
        if isinstance(paged_content, str):
            self.paged_content.append(paged_content)
        elif isinstance(paged_content, list):
            self.paged_content.extend(paged_content)
        else:
            raise TypeError("paged_content must be str or list[str]")

    def get_content(self):
        return "\n".join(self.content)

    def get_paged_content(self, page_num: int = 1):
        if not self.is_paged:
            return self.get_content()
        # 根据每页行数计算起始行和结束行
        start_row = (page_num - 1) * self.rows_per_page
        end_row = page_num * self.rows_per_page
        return "\n".join(self.paged_content[start_row:end_row])

    def get_image(self, index: int = 0):
        return self.image[index]


def create_message(content: str | list[str] = None, image: BytesIO | str | list[BytesIO | str] | None = None,
                   paged_content: str | list[str] | None = None, rows_per_page: int = 15):
    message = MessageModel()
    if content:
        message.add_content(content)
    if image:
        message.add_image(image)
    if paged_content:
        message.add_paged_content(paged_content)
    message.rows_per_page = rows_per_page
    return message
