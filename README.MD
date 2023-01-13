



# 安裝 gcloud CLI 並使用 GCLOUD APP ENGINE
1. 跟這此頁步驟安裝：https://cloud.google.com/sdk/docs/install
2. 安裝好後，在你的專案資料夾輸入: <path_to_gc_sdk>/google-cloud-sdk/bin/gcloud init
3. 編輯.gcloudignore，把不想要上傳到APP Engine的內容排除
4. 設定app.yaml，此檔案可以為你設定這個網站所需，包含環境變數/啟動流程/python版本，預設他會根據你的requirements.txt安裝你的python library，所以不需要把pip install -r requirements.txt寫進去。可以參考app_sample.yaml。
5. 執行 gcloud app deploy，會跟你確定部署的目標，確認後就可以檢查是否有部署上去囉！