from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime, timedelta

def getCryptoData(symbol, coinName):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--incognito") # Gizli sekmede aç
    driver = webdriver.Chrome(chromeOptions)
    driver.maximize_window()
    driver.delete_all_cookies()

    driver.get(symbol)
    driver.implicitly_wait(10) # Sayfa direkt açılmıyo 10sn bekle
    priceData = []
    maxRuntime = 20 # Saniye cinsinden çalışma süresi (Her birinde x saniye)

    startTime = datetime.now()

    while (datetime.now() - startTime).seconds < maxRuntime:
        try:
            priceInfo = driver.find_element(By.XPATH, '/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]/span[1]')
            price = priceInfo.text

            currentDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            currentDate, currentTime = currentDateTime.split()

            priceData.append({"Date": currentDate, "Time": currentTime, "Price": price, "Coin": coinName})

            print("Date:", currentDate, "Time:", currentTime, "Instant Price:", price)

            sleep(10) # 10 saniyede bir çek 
        except Exception as e:
            print("Error:", e)
            break

    driver.quit()
    return priceData

# Burada tek tek sayfaları açıp verileri çekecek ama csv dosyasına en son yazacak
BtcData = getCryptoData("https://tr.tradingview.com/chart/?symbol=CRYPTO%3ABTCUSD", "BTC")
EthData = getCryptoData("https://tr.tradingview.com/chart/?symbol=CRYPTO%3AETHUSD", "ETH")
DogeData = getCryptoData("https://tr.tradingview.com/chart/?symbol=CRYPTO%3ADOGEUSD", "DOGE")
ShibaData = getCryptoData("https://tr.tradingview.com/chart/?symbol=CRYPTO%3ASHIBUSD", "SHIBA")

CryptocurrencyDataDf = pd.DataFrame(BtcData + EthData + DogeData + ShibaData)
CryptocurrencyDataDf.to_csv("CryptocurrencyData.csv", index=False)
