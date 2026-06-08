import requests

# 1. 擴大水源：同時抓取 台灣、全球體育、全球娛樂頻道
SOURCES = {
    "台灣綜合": "https://iptv-org.github.io/iptv/countries/tw.m3u",
    "全球體育": "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "全球娛樂": "https://iptv-org.github.io/iptv/categories/entertainment.m3u"
}

# 2. 智慧過濾設定
# ❌ 黑名單：包含這些字眼的頻道直接丟掉
BLACKLIST = ["大愛", "daai", "goodtv", "唯心", "佛", "宗教", "church", "gospel", "bible", "god", "islam", "buddha", "法界", "生命電視"]

#  想找的關鍵字（不分大小寫）：體育、綜藝、電影、熱門電視台
WANTED = ["sport", "體育", "運動", "綜藝", "娛樂", "movie", "電影", "show", "tvbs", "ebc", "東森", "華視", "中視", "台視"]

def fetch_and_filter():
    all_filtered_channels = []
    
    for category, url in SOURCES.items():
        print(f"📥 正在從【{category}】抓取清單...")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue
            
            lines = response.text.splitlines()
            current_name = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF"):
                    if "," in line:
                        current_name = line.split(",")[-1].strip()
                elif line.startswith("http") and current_name:
                    name_lower = current_name.lower()
                    
                    # 檢查黑名單
                    is_blacklisted = any(bad_word in name_lower for bad_word in BLACKLIST)
                    if is_blacklisted:
                        continue
                    
                    # 如果是台灣頻道，預設保留 (除非在黑名單內)
                    # 如果是全球體育/娛樂，則需要符合我們想要的關鍵字 (或者是亞洲/中文頻道)
                    if category == "台灣綜合":
                        all_filtered_channels.append({"name": f"[台灣] {current_name}", "url": line})
                    else:
                        # 檢查是否符合想要的關鍵字
                        is_wanted = any(good_word in name_lower for good_word in WANTED)
                        if is_wanted:
                            all_filtered_channels.append({"name": f"[{category}] {current_name}", "url": line})
                            
        except Exception as e:
            print(f"❌ 抓取 {category} 失敗: {e}")
            
    return all_filtered_channels

def test_url(url):
    """快速測試網址是否有效"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.head(url, timeout=3, headers=headers)
        if response.status_code in [200, 206, 301, 302]:
            return True
    except:
        pass
    return False

def main():
    candidate_channels = fetch_and_filter()
    print(f"🔍 經過關鍵字過濾後，剩餘 {len(candidate_channels)} 個候選頻道，開始進行連線測試...")
    
    valid_channels = []
    TARGET_COUNT = 40  # ⚙️ 這次把目標提高到 40 個優質頻道！
    
    for ch in candidate_channels:
        if len(valid_channels) >= TARGET_COUNT:
            print(f"🎯 已集滿 {TARGET_COUNT} 個可用頻道，停止測試。")
            break
            
        print(f"正在測試: {ch['name']} -> ", end="")
        if test_url(ch['url']):
            print("✅ 存活")
            valid_channels.append(ch)
        else:
            print("❌ 失效")
            
    # 寫入 M3U
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in valid_channels:
            f.write(f"#EXTINF:-1, {ch['name']}\n")
            f.write(f"{ch['url']}\n")
            
    print(f"🎉 大功告成！已過濾掉宗教台，並精選出 {len(valid_channels)} 個體育/娛樂/綜合頻道！")

if __name__ == "__main__":
    main()
