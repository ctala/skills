#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import zipfile
import binascii
import string
import itertools as its
import multiprocessing
import argparse
import json
from typing import Optional

try:
    import pyzipper
    HAS_PYZIPPER = True
except ImportError:
    pyzipper = None
    HAS_PYZIPPER = False

CHARSET_DIGITS = string.digits
CHARSET_LOWER = string.ascii_lowercase
CHARSET_UPPER = string.ascii_uppercase
CHARSET_SYMBOLS = string.punctuation
OUT_DIR_DEFAULT = "unzipped_files"

# 全局 Agent 模式标志
AGENT_MODE = False

def agent_print(msg):
    """在 Agent 模式下静默，在普通模式下打印"""
    if not AGENT_MODE:
        print(msg)

def agent_output(status, data=None, message=""):
    """Agent 模式专属 JSON 输出"""
    if AGENT_MODE:
        print(json.dumps({"status": status, "data": data, "message": message}, ensure_ascii=False))

def is_zip_encrypted(file_path):
    with zipfile.ZipFile(file_path) as zf:
        for info in zf.infolist():
            if info.flag_bits & 0x1:
                return True
    return False

def fix_zip_encrypted(file_path, temp_path):
    with zipfile.ZipFile(file_path) as zf, zipfile.ZipFile(temp_path, "w") as temp_zf:
        for info in zf.infolist():
            clean_info = info
            if clean_info.flag_bits & 0x1:
                clean_info.flag_bits ^= 0x1
            temp_zf.writestr(clean_info, zf.read(info.filename))

def get_crc(zip_file, fz):
    key = 0
    file_list = [name for name in fz.namelist() if not name.endswith('/')]
    if not file_list: return

    for filename in file_list:
        getSize = fz.getinfo(filename).file_size
        if 0 < getSize <= 6:
            if AGENT_MODE:
                # Agent 模式下自动同意 CRC 碰撞
                sw = 'y'
            else:
                sw = input(f'[!] 监测到 {filename} 大小为 {getSize} 字节，是否尝试 CRC32 碰撞爆破？（y/n）')
                
            if sw.lower() == 'y':
                getCrc = fz.getinfo(filename).CRC
                agent_print(f'[+] {filename} 文件的CRC值为：{getCrc}')
                if crack_crc(filename, getCrc, getSize):
                    key += 1
    if key >= len(file_list) and len(file_list) > 0:
        msg = f'所有文件均已通过CRC32碰撞破解完成'
        agent_print(f'[*] {msg}')
        agent_output("success", {"method": "crc32"}, msg)
        os._exit(0)

def crack_crc(filename, crc, size):
    dic = its.product(string.printable, repeat=size)
    agent_print(f"[+] 开始进行CRC32碰撞破解······")
    for s in dic:
        s = ''.join(s).encode()
        if crc == (binascii.crc32(s)):
            content = s.decode()
            agent_print(f'[*] 破解成功！{filename} 内容为：{content}')
            agent_output("success", {"filename": filename, "content": content}, "CRC32碰撞破解成功")
            return True
    return False

def _find_first_file_in_zip(zf) -> Optional[str]:
    try:
        for info in zf.infolist():
            if not info.filename.endswith('/'): return info.filename
    except:
        try:
            for name in zf.namelist():
                if not name.endswith('/'): return name
        except: return None
    return None

def _clean_and_create_outdir(out_dir: str):
    if os.path.exists(out_dir):
        try: shutil.rmtree(out_dir)
        except: pass
    os.makedirs(out_dir, exist_ok=True)

def crack_password(zip_file: str, password: str, status: dict, out_dir: str):
    if status["stop"]: return False
    pwd_bytes = password.encode('utf-8')
    is_correct = False

    try:
        if HAS_PYZIPPER:
            with pyzipper.AESZipFile(zip_file, 'r') as zf:
                first_file = _find_first_file_in_zip(zf)
                if first_file: zf.read(first_file, pwd=pwd_bytes)
                else: zf.testzip(pwd=pwd_bytes)
                is_correct = True
        else:
            with zipfile.ZipFile(zip_file, 'r') as zf:
                first_file = _find_first_file_in_zip(zf)
                if first_file: zf.read(first_file, pwd=pwd_bytes)
                else: zf.testzip(pwd=pwd_bytes)
                is_correct = True
    except:
        is_correct = False

    if is_correct:
        with status["lock"]:
            if status["stop"]: return
            status["stop"] = True

        agent_print(f'\n\n[+] 恭喜您！密码破解成功, 密码为：{password}')
        try:
            _clean_and_create_outdir(out_dir)
            if HAS_PYZIPPER:
                with pyzipper.AESZipFile(zip_file, 'r') as zf: zf.extractall(path=out_dir, pwd=pwd_bytes)
            else:
                with zipfile.ZipFile(zip_file, 'r') as zf: zf.extractall(path=out_dir, pwd=pwd_bytes)
            
            with zipfile.ZipFile(zip_file) as zf_info:
                filenames = zf_info.namelist()
                agent_print(f"\n[*] 已自动提取 {len(filenames)} 个文件到 '{out_dir}'")
                agent_output("success", {"password": password, "extracted_files": filenames, "out_dir": out_dir}, "密码破解并解压成功")
        except Exception as e:
            agent_print(f"\n[!] 密码正确，但解压出错: {e}")
            agent_output("partial_success", {"password": password, "error": str(e)}, "密码正确但解压失败")

        os._exit(0)
    else:
        with status["lock"]:
            status["tried_passwords"].append(password)
        return False

def generate_numeric_dict():
    numeric_dict = []
    for length in range(1, 7):
        for num in its.product(string.digits, repeat=length):
            numeric_dict.append(''.join(num))
    return numeric_dict, len(numeric_dict)

def display_progress(status, start_time):
    if AGENT_MODE: return # Agent 模式下关闭进度条刷屏
    while not status["stop"]:
        time.sleep(0.1)
        with status["lock"]:
            passwords_cracked = len(status["tried_passwords"])
            total_passwords = status["total_passwords"]
            current_time = time.time()
            elapsed_time = current_time - start_time
            avg_cracked = int(passwords_cracked / elapsed_time) if elapsed_time > 0 else 0

            if total_passwords > 0:
                progress = passwords_cracked / total_passwords * 100
                remaining_time = (total_passwords - passwords_cracked) / avg_cracked if avg_cracked > 0 else 0
                remaining_time_str = time.strftime('%H:%M:%S', time.gmtime(remaining_time))
            else:
                progress = 0.0
                remaining_time_str = "N/A"

            current_password = status["tried_passwords"][-1] if passwords_cracked > 0 else ""
            print(f"\r[-] 进度：{progress:.2f}%，剩余：{remaining_time_str}，"
                  f"时速：{avg_cracked}个/s，尝试:{current_password:<20}", end="", flush=True)

def adjust_thread_count(max_limit=128):
    try: return min(max_limit, multiprocessing.cpu_count() * 4)
    except: return 16

def count_passwords(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except: return 0

def load_passwords_in_chunks(file_path, chunk_size=1000000):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        chunk = []
        for line in f:
            chunk.append(line.strip())
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk: yield chunk

def parse_mask(mask):
    charsets = []
    i = 0
    while i < len(mask):
        char = mask[i]
        if char == '?':
            if i + 1 < len(mask):
                placeholder = mask[i+1]
                if placeholder == 'd': charsets.append(CHARSET_DIGITS)
                elif placeholder == 'l': charsets.append(CHARSET_LOWER)
                elif placeholder == 'u': charsets.append(CHARSET_UPPER)
                elif placeholder == 's': charsets.append(CHARSET_SYMBOLS)
                elif placeholder == '?': charsets.append('?')
                else: charsets.append(mask[i:i+2])
                i += 2
            else:
                charsets.append('?')
                i += 1
        else:
            charsets.append(char)
            i += 1
    total = 1
    for c in charsets:
        if len(c) > 0: total *= len(c)
    return charsets, max(1, total)

def execute_cracking(zip_file, iterator, total_passwords, status, out_dir, fail_msg):
    status["total_passwords"] = total_passwords
    status["tried_passwords"] = []
    start_time = time.time()
    max_threads = adjust_thread_count()
    
    agent_print(f"[+] 密码总数: {total_passwords:,} | 线程数: {max_threads}")

    display_thread = threading.Thread(target=display_progress, args=(status, start_time))
    display_thread.daemon = True
    display_thread.start()

    try:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            if isinstance(iterator, list) or type(iterator).__name__ == 'generator':
                while not status["stop"]:
                    chunk = list(its.islice(iterator, 100000)) if type(iterator).__name__ == 'generator' else iterator
                    if not chunk: break
                    futures = {executor.submit(crack_password, zip_file, p, status, out_dir) for p in chunk}
                    for f in as_completed(futures):
                        if status["stop"]: break
                    if isinstance(iterator, list): break # 列表只跑一次
            else: # 处理文件分块生成器
                for chunk in iterator:
                    if status["stop"]: break
                    futures = {executor.submit(crack_password, zip_file, p, status, out_dir) for p in chunk}
                    for f in as_completed(futures):
                        if status["stop"]: break
    finally:
        if not status["stop"]:
            agent_print(f'\n[-] {fail_msg}')
            agent_output("failed", None, fail_msg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ZipCracker - 高级ZIP密码破解工具 (OpenClaw Optimized)")
    parser.add_argument("zip_file", help="要破解的ZIP文件路径")
    parser.add_argument("dictionary", nargs="?", default=None, help="自定义字典文件或目录")
    parser.add_argument("-o", "--out", default=OUT_DIR_DEFAULT, help="解压输出目录")
    parser.add_argument("-m", "--mask", help="掩码攻击 (例如: ?d?d?d?d)")
    parser.add_argument("--agent", action="store_true", help="Agent 模式 (静默输出 JSON)")
    
    args = parser.parse_args()
    AGENT_MODE = args.agent

    if not AGENT_MODE:
        print(r"""                          
     ______          ____                _   [*]Hx0战队      
    |__  (_)_ __    / ___|_ __ __ _  ___| | _____ _ __ 
      / /| | '_ \  | |   | '__/ _ |/ __| |/ / _ \ '__|
     / /_| | |_) | | |___| | | (_| | (__|   <  __/ |   
    /____|_| .__/___\____|_|  \__,_|\___|_|\_\___|_|   
           |_| |_____|                                 
    #Coded By Asaotomo         OpenClaw Agent Ready
        """)

    if not os.path.exists(args.zip_file):
        agent_print(f"[!] 错误: 文件 '{args.zip_file}' 未找到。")
        agent_output("error", None, f"文件未找到: {args.zip_file}")
        sys.exit(1)

    # 处理伪加密
    is_truly_encrypted = False
    if is_zip_encrypted(args.zip_file):
        agent_print(f'[!] 检测到伪加密，尝试修复...')
        fixed_zip_name = args.zip_file + ".fixed.tmp"
        try:
            fix_zip_encrypted(args.zip_file, fixed_zip_name)
            with zipfile.ZipFile(fixed_zip_name) as fixed_zf: fixed_zf.testzip()
            
            _clean_and_create_outdir(args.out)
            with zipfile.ZipFile(fixed_zip_name) as fixed_zf:
                fixed_zf.extractall(path=args.out)
                filenames = fixed_zf.namelist()
                
            os.remove(fixed_zip_name)
            agent_print(f"[*] 伪加密修复并解压成功！提取 {len(filenames)} 个文件。")
            agent_output("success", {"method": "pseudo_encryption_fix", "extracted_files": filenames}, "伪加密修复成功")
            sys.exit(0)
        except Exception:
            is_truly_encrypted = True
            agent_print(f'[+] 修复失败，确认为真加密。')
            if os.path.exists(fixed_zip_name): os.remove(fixed_zip_name)
    else:
        agent_print(f'[!] 文件未加密，可直接解压！')
        agent_output("info", None, "文件未加密")
        sys.exit(0)

    if is_truly_encrypted:
        try:
            with zipfile.ZipFile(args.zip_file) as zf: get_crc(args.zip_file, zf)
        except zipfile.BadZipFile:
            agent_output("error", None, "损坏的ZIP文件")
            sys.exit(1)
        
        status = { "stop": False, "tried_passwords": [], "lock": threading.Lock(), "total_passwords": 0 }

        if args.mask:
            charsets, total = parse_mask(args.mask)
            if total > 100_000_000_000 and not AGENT_MODE:
                choice = input(f"[!] 警告：掩码将生成 {total:,} 种组合。继续？ (y/n): ")
                if choice.lower() != 'y': sys.exit(0)
            generator = (''.join(p) for p in its.product(*charsets))
            execute_cracking(args.zip_file, generator, total, status, args.out, "掩码破解失败")
        
        elif args.dictionary:
            if os.path.isfile(args.dictionary):
                total = count_passwords(args.dictionary)
                execute_cracking(args.zip_file, load_passwords_in_chunks(args.dictionary), total, status, args.out, "字典破解失败")
            # 目录逻辑可按需扩展
        else:
            if os.path.exists('password_list.txt'):
                total = count_passwords('password_list.txt')
                execute_cracking(args.zip_file, load_passwords_in_chunks('password_list.txt'), total, status, args.out, "内置字典破解失败")
            if not status["stop"]:
                numeric_dict, total = generate_numeric_dict()
                execute_cracking(args.zip_file, numeric_dict, total, status, args.out, "纯数字字典破解失败")