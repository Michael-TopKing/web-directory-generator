# Web 目錄產生工具
從 **dirsearch** 和 **katana** 的掃描結果中，快速提取乾淨的網站目錄列表。

### ✨ 功能特色
- 自動識別並移除檔案名稱（.php、.aspx、.jpg 等）
- 支援 HTTP / HTTPS
- 自動去除重複目錄
- 可使用 `--max-depth` 限制目錄深度
- 輸出詳細統計資訊

### 📖 使用方式
python generate_web_directories.py \
  --dirsearch dirsearch.txt \
  --katana katana.txt \
  --output web_directories.txt

參數說明
* --dirsearch ：dirsearch 結果檔案（必填）
* --katana ：katana 結果檔案（必填）
* --output ：輸出檔案路徑（選填，預設 web_directories.txt）
* --max-depth ：最大目錄深度限制（選填，預設無限制）

範例指令
# 基本使用
python generate_web_directories.py --dirsearch results.txt --katana urls.txt

# 限制目錄深度為 4 層
python generate_web_directories.py --dirsearch results.txt --katana urls.txt --max-depth 4

