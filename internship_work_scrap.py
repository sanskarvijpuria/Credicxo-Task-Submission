import json
from selenium import webdriver
import time
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException   
'''
def get_proxies():
  # We are using the URL which is set to retrieve US proxies having more than 90% uptime
  URL ="http://www.freeproxylists.net/"

  #Using seleium instead of request and bs4 here. It was sending to recaptch page when using them.
  driver = webdriver.Chrome('./operadriver.exe')
  driver.get(URL)
  country=webdriver.support.ui.Select(driver.find_element_by_xpath("//*[@id='form1']/table/tbody/tr[2]/td[1]/select"))
  country.select_by_value('US')
  time.sleep(4)
  submit=driver.find_element_by_xpath("//*[@id='form1']/table/tbody/tr[3]/td/input")
  submit.click()
  time.sleep(3)
  #To select every row with the IP address in it
  table_rows = driver.find_elements_by_css_selector("table.DataGrid > tbody >tr.Odd, .Even")
  proxies = []
  for i in range(0,len(table_rows)):
    if len(table_rows[i].find_elements_by_class_name("adsbygoogle")) > 0:
      continue
    else:
      print(table_rows[i])
      details = table_rows[i].text.split()
      print(details)
      ip, port = details[0], details[1]
      proxies.append(ip + ":"+ port)  
  driver.close()
  return proxies

url = "http://httpbin.org/ip"
proxies = get_proxies()
for i in range(len(proxies)):
    proxy = proxies[i]
    try:
        response = requests.get(url, proxies = {"http":proxy, "https":proxy})
    except:
        # if the proxy Ip is pre occupied
        proxies.pop(i)
        print("Not Available")


proxies = get_proxies()
'''

def driver_proxy(ip):
  ip = ip
  
  chrome_options = Options()
  chrome_options.add_argument('--proxy-server=%s' % ip)
  driver = webdriver.Chrome('./operadriver.exe', options=chrome_options)
  return driver

   
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def scrap(driver):
  products = driver.find_elements_by_css_selector("#Div1.product")
  scrap_data =[]
  for prod in products:
    title = prod.find_element_by_class_name("catalog-item-name")
    brand = prod.find_element_by_class_name("catalog-item-brand")
    price = prod.find_element_by_class_name("price")
    status = prod.find_element_by_class_name("status")
    if status.text=='Out of Stock':
        in_stock = False
    else:
        in_stock = True

    scrap_data.append(
      {
          "price" : price.text,
          "title" : title.text,
          "stock" : in_stock,
          "brand" : brand.text
      }
    )
  if check_exists_by_xpath(driver, "//*[@id='MainContent_dpProductsTop']//a[not(contains(@class, 'aspNetDisabled')) and text()='Next']"):
    element = driver.find_element_by_xpath("//*[@id='MainContent_dpProductsTop']//a[text()='Next']")
    driver.execute_script("arguments[0].click();", element)
    scrap_data.extend(scrap(driver))
    
  return scrap_data



def main():
  url = "https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1"
  driver = webdriver.Chrome('./operadriver.exe')
  driver.get(url)
  result_scraped= scrap(driver)
  driver.quit()
  with open('result_scraped.json', 'w') as output:
    json.dump(result_scraped,output, indent=4)
main()


'''
i=0
while i<len(proxies):
  try:
    driver = driver_proxy(proxies[i])
    print("Proxy:" ,proxies[i] )
    main()
    i = i+1
  except:
    i = i+1
    continue
'''