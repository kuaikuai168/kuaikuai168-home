import requests

# 1. 直接定位到 GitHub 最強大的開源直播源專案（這裡以台灣頻道清單為例，裡面有上百個頻道）
SOURCE_M3U_URL = "https://iptv-org.github.io/iptv/countries/tw.m3u"

def fetch_channels_from_github(source_url):
    """從遠端公開專案抓取並解析所有頻道"""
    print("📥 正在從遠端庫抓取最新頻道清單...")
    try:
        response = requests.get(source_url, timeout=10)
        if response.status_code != 200:
            return []
        
        lines = response.text.splitlines()
        channels = []
        current_name = "未命名頻道"
        
        # 簡單的 M3U 檔案解析邏輯
        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF"):
                # 抓取逗號後面的頻道中文/英文名稱
                if "," in line:
                    current_name = line.split(",")[-1].strip()
            elif line.startswith("http"):
                channels.append({"name": current_name, "url": line})
        return channels
    except Exception as e:
        print(f"❌ 抓取失敗: {e}")
        return []

def test_url(url):
    """快速測試網址是否有效 (使用 HEAD 請求比 GET 快 10 倍)"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        # 使用 requests.head 只抓取網頁標頭，不下載影片內容，速度極快
        response = requests.head(url, timeout=3, headers=headers)
        if response.status_code in [200, 206, 301, 302]:
            return True
    except:
        pass
    return False

def main():
    # 抓取候選清單
    all_channels = fetch_channels_from_github(SOURCE_M3U_URL)
    print(f"總共找到 {len(all_channels)} 個候選頻道，開始篩選...")
    
    valid_channels = []
    TARGET_COUNT = 25  # ⚙️ 設定你想要的目標頻道數量（例如：25 個）
    
    for ch in all_channels:
        # 如果已經收集到足夠的頻道，就提早結束測試，避免 GitHub 跑太久
        if len(valid_channels) >= TARGET_COUNT:
            print(f"🎯 已達到目標數量 {TARGET_COUNT} 個頻道，停止測試。")
            break
            
        print(f"正在測試: {ch['name']} -> ", end="")
        if test_url(ch['url']):
            print("✅ 存活")
            valid_channels.append(ch)
        else:
            print("❌ 失效")
            
    # 寫入全新的 live.m3u 檔案
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in valid_channels:
            f.write(f"#EXTINF:-1, {ch['name']}\n")
            f.write(f"{ch['url']}\n")
            
    print(f"🎉 任務完成！共成功篩選出 {len(valid_channels)} 個優質頻道，已寫入 live.m3u！")

if __name__ == "__main__":
    main()
