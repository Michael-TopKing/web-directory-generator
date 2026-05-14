#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web 目錄產生工具
從 dirsearch 和 katana 輸出中提取乾淨的目錄路徑
"""

import argparse
import os
from urllib.parse import urlparse, urlunparse
from collections import defaultdict


def is_file_path(path: str) -> bool:
    """判斷路徑最後一段是否為檔案（常見副檔名）"""
    if not path or path.endswith('/'):
        return False
    
    last_segment = path.strip('/').split('/')[-1]
    file_extensions = {
        '.php', '.asp', '.aspx', '.jsp', '.jspx', '.html', '.htm', '.js', 
        '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.txt',
        '.xml', '.json', '.log', '.bak', '.zip', '.tar', '.gz'
    }
    return any(last_segment.lower().endswith(ext) for ext in file_extensions)


def extract_directory_url(url: str, max_depth: int = None) -> str | None:
    """從單一 URL 提取目錄 URL"""
    try:
        parsed = urlparse(url.strip())
        if not parsed.netloc:
            return None

        path = parsed.path.rstrip('/')
        
        # 如果是根目錄，直接返回
        if not path or path == '/':
            directory_url = urlunparse((parsed.scheme, parsed.netloc, '/', '', '', ''))
            return directory_url

        # 移除檔案名稱
        if is_file_path(path):
            path = '/'.join(path.split('/')[:-1])
        
        # 確保以 / 開頭
        if not path.startswith('/'):
            path = '/' + path

        # 限制深度
        if max_depth is not None:
            segments = [seg for seg in path.split('/') if seg]
            if len(segments) > max_depth:
                segments = segments[:max_depth]
                path = '/' + '/'.join(segments)

        directory_url = urlunparse((
            parsed.scheme, 
            parsed.netloc, 
            path if path else '/', 
            '', '', ''
        ))
        return directory_url

    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description="Web 目錄產生工具 - 從 dirsearch/katana 結果提取目錄")
    parser.add_argument('--dirsearch', required=True, help='dirsearch 結果檔案路徑')
    parser.add_argument('--katana', required=True, help='katana 結果檔案路徑')
    parser.add_argument('--output', default='web_directories.txt', help='輸出檔案路徑 (預設: web_directories.txt)')
    parser.add_argument('--max-depth', type=int, default=None, help='最大目錄深度限制 (預設: 無限制)')

    args = parser.parse_args()

    # 檢查檔案是否存在
    for file_path in [args.dirsearch, args.katana]:
        if not os.path.isfile(file_path):
            print(f"❌ 錯誤：檔案不存在 -> {file_path}")
            return

    all_urls = set()
    stats = {'total': 0, 'valid': 0}

    # 讀取兩個檔案
    for file_path in [args.dirsearch, args.katana]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        all_urls.add(line)
                        stats['total'] += 1
        except Exception as e:
            print(f"❌ 讀取檔案失敗 {file_path}：{e}")
            return

    # 提取目錄
    directories = set()
    domains = set()

    for url in all_urls:
        dir_url = extract_directory_url(url, args.max_depth)
        if dir_url:
            directories.add(dir_url)
            parsed = urlparse(dir_url)
            domains.add(parsed.netloc)
            stats['valid'] += 1

    # 排序輸出（先按域名，再按路徑）
    sorted_dirs = sorted(directories, key=lambda x: (urlparse(x).netloc.lower(), urlparse(x).path))

    # 寫入檔案
    try:
        os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            for d in sorted_dirs:
                f.write(d + '\n')
        
        print(f"\n✅ 完成！")
        print(f"   處理 URL 總數   : {stats['total']:,}")
        print(f"   唯一域名數     : {len(domains):,}")
        print(f"   唯一目錄數     : {len(directories):,}")
        print(f"   輸出檔案       : {args.output}")
        
        if args.max_depth:
            print(f"   深度限制       : {args.max_depth}")

    except Exception as e:
        print(f"❌ 寫入檔案失敗：{e}")


if __name__ == "__main__":
    main()
