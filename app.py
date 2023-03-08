from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/table-binance', methods=['GET'])
def table_binance_view():
    import requests
    from bs4 import BeautifulSoup

    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver


    import chromedriver_autoinstaller
    chromedriver_autoinstaller.install()

    def customChrome():
        option = Options()
        option.page_load_strategy = 'eager'
        option.add_argument("--enable-extensions")
        option.add_argument('--headless')
        driver = webdriver.Chrome(options=option)
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(200)
        driver.maximize_window()
        return driver


    driver = customChrome()
    driver.get('https://www.binance.com/vi/futures-activity/leaderboard')
    ele = driver.find_element('xpath', "//tr[@class='bn-table-row bn-table-row-level-0']")

    data = driver.page_source

    soup = BeautifulSoup(data, 'html.parser')

    list_table = []
    list_table.append(['Thì trường', 'Đang chạy', 'ROI', 'Số lần sao chép', 'PNL(USDT)', 'Hoạt động'])
    result = {}
    result['row'] = []
    for i in soup.find_all('tr', attrs={'class': 'bn-table-row bn-table-row-level-0'}):
        z = [x.text for x in i.find_all('td', attrs={'class': 'bn-table-cell'})]
        result['row'].append(z)

    return jsonify(result)


if __name__ == '__main__':
    app.run()
