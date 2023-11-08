from PyPDF2 import PdfReader
import re

def parse(filename):
    reader = PdfReader(filename)
    total_pages = reader.numPages
    dict = []

    for page_num in range(0, total_pages):
        page = reader.pages[page_num]
        extracted_text = page.extract_text()
        temp = extracted_text.split("Sent To:")[0]
        # print(temp)
        # a = re.split("[0-9][0-9][0-9][0-9][0-9][0-9]", temp)
        a = re.split("(?<!\d)\d{6}(?!\d)", temp)
        # print(a)
        # a = re.split(r"\D(\d{6})\D", " "+temp+" ")
        # print(a)
        a.pop(0)
        # print(a)
        for n, b in enumerate(a):
            # print("B:",repr(b))
            # print(repr(b))
            c = b.split("This Product Total")
            # print("C:",c)
            # d = c[0].splitlines()
            d = c[0].splitlines()
            d.pop(0)
            print("D:",d)
            if not d:
                # If "d" is an empty list, skip it.
                break

            e = {}
            e["product"] = d[0].split()[0].capitalize()
            try:
                e["size"] = re.search("[0-9]\"",d[0]).group().strip("\"")
                # Search for pot sizes ranging from 0-9 with a " after it
            except:
                pass

            # Grab the last columns content
            e["code"] = d[len(d)-1]

            try:
                # Remove useless information from the color, and fix colors
                e["color"] = d[0].split("\" ")[1].replace("w/Mylar","")
                e["color"] = e["color"].replace("Asst","Assorted")
                e["color"] = e["color"].replace("Flamingo","")
            except:
                pass

            if "w/Mylar" in d[0]:
                e["pot_cover"] = True

            # If the column contains a * then get quantity from the next column over
            if "*"in d[len(d)-2]:
                e["quantity"] = d[len(d)-3]
            else:
                e["quantity"] = d[len(d)-2]

            for i,j in enumerate(d):
                if "BX" in j:
                    e["pack_size"] = d[i].strip("BX")
                    e["tag5"] = "Box"
                elif "TR" in j:
                    e["pack_size"] = d[i].strip("TR")
                    e["tag5"] = "Tray"

                if "$" in j:
                    e["price"] = d[i].strip("$")

                # Search for UPC code in 0-00000-00000-0 format
                if re.search("[0-9]-[0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9]-[0-9]", j):
                    e["upc"] = d[i]
                # Search for UPC code in 00000000 format (IKEA)
                elif re.search("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]", j):
                    e["upc"] = d[i]

            #SPECIAL CASES
            if "tripod" in d[0].lower():
                e["product"] = "Succulent Tripod Planter"
                del e["color"]

            if "heart shaped" in d[0].lower():
                e["product"] = "Heart Shaped Planter"
                del e["color"]

            if "glass cyl" in d[0].lower():
                e["product"] = "Anthurium in Glass"
                e["size"] =  "4"

            if "sample" in d[0].lower():
                e["color"] = "Sample"
                for i,j in enumerate(d):
                    if "POTS" in j:
                        e["pack_size"] = d[i-1]
                        e["quantity"] = "1"

            dict.append(e)
    return(dict)

if __name__ == "__main__":
   pass
