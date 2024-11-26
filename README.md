健康 App 心率資料分析程式
簡介
這是一個用於處理iPhone中健康App檔案的小程式。

-解析健康 App 的心率資料。
-計算並輸出所有心率資料。
-繪製最近十個月的平均心率變化圖表。

細節
程式語言：Python
依賴套件：
pandas：資料處理
matplotlib：繪製圖表
xml.etree.ElementTree：解析XML資料


1. 準備環境
請先確認你的電腦環境中已安裝以下軟體：

Python 版本：3.10 或以上
必要套件：安裝所需套件
<!-- pip install pandas matplotlib -->

2. 將 XML 檔案放置於專案目錄
從健康App匯出XML檔案後，將檔案放在專案目錄下，命名為 export.xml。

3. 執行程式
運行程式以處理資料：
<!-- python health.py -->

4. 產生圖表及紀錄檔
執行完成後，將圖表及紀錄檔分別儲存為heart.png及output.txt，位於專案目錄。


程式結構

.
├── health.py   # 主程式碼
├── export.xml  # 健康App匯出的XML檔案
├── output.txt  # 輸出的心率詳細資料
└── heart.png   # 輸出的心率趨勢圖表


#注意事項
XML檔案需為健康App匯出的格式，其他格式可能無法正確解析。
若資料有缺失，程式會跳過無效資料以確保結果正確性。

未來規劃
支援更多輸出格式（如 CSV 或 JSON）。
添加多檔案處理功能。
增強圖表的互動性。

聯絡方式
若有問題及任何想提供給我的建議，歡迎聯絡我：
chymeon@gmail.com