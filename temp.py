import json
import re

# 要转换的Markdown文件路径
markdown_file_path = 'test.md'

def parse_markdown_file(path):
    # 预编译正则表达式以提高效率
    title_pattern = re.compile(r'^(#{1,6})\s*(.*)', re.MULTILINE)
    keywords_pattern = re.compile(r'^Keywords:\s*(.+)$', re.MULTILINE)
    summary_pattern = re.compile(r'^Summary:\s*(.+)$', re.MULTILINE)
    example_pattern = re.compile(r'^Example:\s*\n?```(?:[a-zA-Z]+)?\n(.*?)\n```$', re.MULTILINE | re.DOTALL)
    
    # 使用一个字典来存储我们将要提取的元素
    content_dict = {
        "file_name": path,
        "titles": [],
        "keywords": [],
        "summary": "",
        "example": ""
    }

    try:
        with open(path, 'r', encoding='utf-8') as md_file:
            content = md_file.read()

        titles_matches = title_pattern.finditer(content)
        for match in titles_matches:
            title_text = match.group(2).strip()  # 清除标题文本两侧的空格
            content_dict['titles'].append(title_text)  # 将标题添加到列表中

        # 打印所有找到的标题
        if content_dict['titles']:
            titles_tuple = tuple(content_dict['titles'])  # 将标题列表转换为元组
            print(f"Found titles: {titles_tuple}")  # 以元组形式打印标题
        else:
            print("No titles found")

        # 提取标题
        keywords_match = keywords_pattern.search(content)
        if keywords_match:
            keywords = [keyword.strip() for keyword in keywords_match.group(1).split(',')]
            print(f"Found keywords: {keywords}")  # Debug print
            content_dict['keywords'] = keywords
        else:
            print("No keywords found")  # Debug print
        
        summary_match = summary_pattern.search(content)
        if summary_match:
            summary = summary_match.group(1).strip()
            print(f"Found summary: {summary}")  # Debug print
            content_dict['summary'] = summary
        else:
            print("No summary found")  # Debug print
        
        example_match = example_pattern.search(content)
        if example_match:
            example = example_match.group(1).strip()
            print(f"Found example: {example}")  # Debug print
            content_dict['example'] = example
        else:
            print("No example found")  # Debug print

    except IOError as e:
        print(f'Error reading file {path}: {e}')
        return None
    
    return content_dict

# 解析Markdown文件
parsed_content = parse_markdown_file(markdown_file_path)
if parsed_content:
    # 写入JSON文件
    output_json_path = 'output.json'
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(parsed_content, json_file, indent=4, ensure_ascii=False)
    
    # 输出到控制台
    print(f'Markdown file {markdown_file_path} has been converted to JSON file {output_json_path}')
