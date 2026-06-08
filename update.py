import requests

# 定義多國水源
SOURCES = {
    "tw": "https://iptv-org.github.io/iptv/countries/tw.m3u",
    "jp": "https://iptv-org.github.io/iptv/countries/jp.m3u",
    "sports": "https://iptv-org.github.io/iptv/categories/sports.m3u"
}

def get_channels(url):
    """取得單一來源的所有頻道"""
    try:
        response = requests.get(url, timeout=10)
        lines = response.text.splitlines()
        channels = []
        name = ""
        for line in lines:
            if line.startswith("#EXTINF"):
                name = line.split(",")[-1].strip()
            elif line.startswith("http"):
                channels.append({"name": name, "url": line})
        return channels
    except:
        return []

def main():
    for lang_code, url in SOURCES.items():
        print(f"🔄 正在處理: {lang_code}...")
        all_channels = get_channels(url)
        
        valid_channels = []
        # 每個分類只取前 20 個活著的頻道
        for ch in all_channels:
            if len(valid_channels) >= 20: break
            
            # 這裡簡單測試，為了省時間只測前 20 個
            try:
                if requests.head(ch['url'], timeout=2).status_code == 200:
                    valid_channels.append(ch)
            except: continue
        
        # 關鍵：依照 lang_code 寫入不同的檔案
        filename = f"{lang_code}.m3u"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for ch in valid_channels:
                f.write(f"#EXTINF:-1, {ch['name']}\n{ch['url']}\n")
        print(f"✅ {filename} 已更新，包含 {len(valid_channels)} 個頻道。")

if __name__ == "__main__":
    main()
