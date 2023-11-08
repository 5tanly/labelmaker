from selenium import webdriver
from selenium.webdriver.common.by import By

# Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import os
import time
from PIL import Image
from io import BytesIO
from pathlib import Path

import modules.foliera
import modules.trillium

#Enable colors on Windows systems
os.system('color')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def update_html(element_name, element_data):
    element = driver.find_element(By.ID, element_name)
    driver.execute_script(
        f"arguments[0].innerText = '{element_data}'", element)

def hide_html(element_name):
    element = driver.find_element(By.ID, element_name)
    driver.execute_script(f"arguments[0].style.visibility = 'hidden'", element)

def hide_style():
    element = driver.find_element(By.CLASS_NAME, "section1")
    driver.execute_script(f"arguments[0].style.display = 'none'", element)

    element = driver.find_element(By.CLASS_NAME, "section2")
    driver.execute_script(f"arguments[0].style.gridColumn = '1/3'", element)

    element = driver.find_element(By.CLASS_NAME, "section2>div")
    driver.execute_script(f"arguments[0].style.paddingLeft = '160px'", element)

    element = driver.find_element(By.CLASS_NAME, "section3")
    driver.execute_script(f"arguments[0].style.gridColumn = '1/3'", element)

def reset_label():
    #Resets the label so the font is sized correctly
    list = ["company","product","code","color","tag1","tag2","tag3","tag4", "tag5"]
    for l in list:
        update_html(l, "@@@")

def render_label(company,product,size,color,pack_size,upc,price,quantity,code,pot_cover,tag1="",tag2="",tag3="",tag4="",tag5=""):
    reset_label()
    update_html("tag1", tag1)
    update_html("tag2", tag2)
    update_html("tag3", tag3)
    update_html("tag4", tag4)
    update_html("tag5", tag5)

    if company:
        update_html("company", company)
    else:
        hide_style()

    update_html("product", f"{pack_size}x{size}\" {product}")
    update_html("code", code)
    update_html("color", color)
    if pot_cover:
        update_html("tag2", "Pot Cover")
    else:
        update_html("tag2", "")
    if price:
        update_html("tag4", price)
    elif upc:
        update_html("tag4", "UPC")
    else:
        update_html("tag4", "")

    take_screenshot(driver.get_screenshot_as_png(), quantity)

def take_screenshot(image, count):
    # Converting PNG from RGBA to RGB so it can go into a PDF file
    pnga = Image.open(BytesIO(image))
    pnga.load()
    png = Image.new("RGB", pnga.size, (255, 255, 255))
    png.paste(pnga, mask=pnga.split()[3])
    for c in range(0, int(count)):
        pnglist.append(png)

print("foliera - f")    
print("trillium - t")     
company = input("^use the options above\nEnter company:\n")
filepath = input("Drag the label file into this window and press enter:\n")
filepath = filepath.strip("'")
pnglist = []
current_dir = os.getcwd()

start = time.time()

print("starting webdriver...")
options = Options()
options.headless = True
if options.headless:
    options.add_argument("--window-size=1200,800")
else:
    options.add_argument("--window-size=1200,924")
service = Service(executable_path=f'{current_dir}/chromedriver', log_path=os.devnull)
driver = webdriver.Chrome(options=options, service=service)
driver.get(f'file:///{current_dir}/web/index.html')

labelError = False

if company == "f":
    renderer = modules.foliera.parse(filepath)
if company == "t":
    renderer = modules.trillium.parse(filepath)
    
for label in renderer:
    print(f"rendering label: {label}")
    try:
        render_label(company=label.get('company', ''),
                    product=label.get('product', ''),
                    size=label.get('size', ''),
                    color=label.get('color', ''),
                    pack_size=label.get('pack_size', ''),
                    upc=label.get('upc', ''),
                    price=label.get('price', ''),
                    quantity=label.get('quantity', ''),
                    code=label.get('code', ''),
                    pot_cover=label.get('pot_cover', ''),
                    tag1=label.get('tag1', ''),
                    tag2=label.get('tag2', ''),
                    tag3=label.get('tag3', ''),
                    tag4=label.get('tag4', ''),
                    tag5=label.get('tag5', ''),)
    except:
        labelError = True
        print(f"{bcolors.BOLD}{bcolors.FAIL}\n{label}\nThis label did NOT render correctly! You MUST print it manually!\n{bcolors.ENDC}")

driver.close()

end = time.time()

timer = (end-start) * 10**3/1000
print(f"\ncreated {len(pnglist)} labels in {round(timer,2)} seconds ({round(len(pnglist)/timer,2)} l/s)\n")

print("saving to pdf...")
filename = filepath.rsplit('/', 1)[-1].split(".")[0]
save_path = Path(current_dir) / "_labels" / filename
pnglist[0].save(f"{save_path}-LABELS.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=pnglist[1:])
print(f"\nfile saved to {save_path}-LABELS.pdf")

if labelError:
    print(f"{bcolors.BOLD}{bcolors.FAIL}\nONE OR MORE LABELS DID NOT RENDER CORRECTLY! YOU MUST PRINT IT MANUALLY!{bcolors.ENDC}")
print(f"{bcolors.WARNING}\n(!) VERIFY LABELS (!)\n{bcolors.ENDC}")
