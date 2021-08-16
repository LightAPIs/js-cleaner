# -*- coding: utf-8 -*-

import os
import io
import re
import argparse
from log import Logger


def read_file_2_list(path):
    read_list = []
    if path and (os.path.exists(path)):
        with io.open(path, mode="r", encoding="utf-8") as f:
            read_list = f.read().splitlines()  # 不读入行尾的换行符
    return read_list


def is_empty_dir(dir_path):
    """[判定目录是否为空]

    Args:
        dir_path ([String]): [目录路径]

    Returns:
        [boolean]: [为空时返回 True]
    """
    dir_status = False
    if not os.listdir(dir_path):
        dir_status = True
    return dir_status


def not_empty_string(value):
    if re.match(r"^\s*\n$", value):
        return False
    return True


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="油猴脚本代码整理器")
    ap.add_argument("-i", "--input", required=True, help="文件所在目录")
    ap.add_argument("-o", "--output", required=True, help="结果输出目录")

    args = vars(ap.parse_args())
    xlog = Logger("DEBUG", "log")

    xlog.info("************************************************")
    xlog.info("文件所在目录: " + args["input"])
    xlog.info("结果输出目录: " + args["output"])
    xlog.info("************************************************")

    xlog.info("开始整理代码...")
    if os.path.isdir(args["input"]) and os.path.isdir(args["output"]):
        if not is_empty_dir(args["input"]):
            for root, _dirs, files in os.walk(args["input"]):
                for filename in files:
                    input_file = root + "\\" + filename
                    file_ext = os.path.splitext(input_file)[1]
                    if file_ext in [".js"]:
                        xlog.info("读取 " + input_file)
                        code_list = read_file_2_list(input_file)
                        res_header_list = []
                        res_code_list = []
                        version = '0.0.1'
                        is_header = True
                        for code in code_list:
                            if is_header:
                                if re.match(
                                        r"^//\s+(@[a-z]+|==/?UserScript==)",
                                        code):
                                    res_header_list.append(code + "\n")
                                    if re.match(r"^//\s+@version\s+([0-9.])", code):
                                        version = re.sub(
                                            r"^//\s+@version\s+([0-9.])", r"\1", code)
                                else:
                                    is_header = False
                                    res_code_list.append(
                                        re.sub(r"^\s*(//\s*|/\*\*?|\*).*", "",
                                               code) + "\n")
                            else:
                                res_code_list.append(
                                    re.sub(r"^\s*(//\s*|/\*\*?|\*).*", "",
                                           code) + "\n")
                        res_code_list = list(
                            filter(not_empty_string, res_code_list))
                        xlog.info("处理 " + input_file + " 完成，开始生成新文件...")
                        output_file = args["output"] + "\\" + filename
                        output_file = output_file.replace(
                            ".js", "_v" + version + ".js")
                        with io.open(output_file, mode="w",
                                     encoding="utf-8") as f:
                            f.writelines(res_header_list)
                            f.writelines(["\n"])
                            f.writelines(res_code_list)
                        xlog.info("生成 " + output_file + " 完成。")
            xlog.debug("所有操作处理完成。")
        else:
            xlog.warning("输入目录下不存在文件。")
    else:
        xlog.error("所输入的参数不是目录！")
