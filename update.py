import requests

# 1. 這裡模擬你收集到的直播源網址 (通常會寫爬蟲去抓，這裡先手動放入)
candidate_urls = [
    "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", # 這是一個開源的測試用串流 (永遠存活)
    "http://fake-broken-link.com/live.m3u8",             # 這是一個故意寫錯、失效的連結
]

def test_url(url):
    """測試網址是否有效"""
    try:
        # 設定 timeout 避免卡住，並加上 headers 偽裝成一般的瀏覽器
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=5, headers=headers)
        
        # HTTP 狀態碼 200 代表連線成功
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def main():
    print("🚀 開始測試直播源...")
    valid_urls = []

    # 2. 逐一測試每個網址
    for url in candidate_urls:
        print(f"正在測試: {url}")
        if test_url(url):
            print("  ✅ 存活")
            valid_urls.append(url)
        else:
            print("  ❌ 失效")

    # 3. 將存活的網址打包成 M3U 檔案
    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n") # 這是 M3U 檔案必須要有的開頭
        for index, url in enumerate(valid_urls):
            f.write(f"#EXTINF:-1, 測試頻道 {index + 1}\n") # 頻道名稱
            f.write(f"{url}\n")

    print(f"🎉 更新完成！共保留 {len(valid_urls)} 個可用頻道，已存入 live.m3u。")

if __name__ == "__main__":
    main()
