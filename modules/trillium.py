from PyPDF2 import PdfReader
import re

def parse(filename):
    reader = PdfReader(filename)
    total_pages = reader.numPages
    dict = []

    for page_num in range(0, total_pages):
        page = reader.pages[page_num]
        extracted_text = page.extract_text()
        temp = extracted_text.split("Date Code\n")[1]
        temp = temp.split("\nTotal Amounts")[0]
        # print(repr(temp))
        a = re.split("([0-9].00\\n)", temp)
        a.pop(0)
       
        for n, b in enumerate(a):
            if n%2 == 0:
                temp_dict = {}
                temp_dict["company"] = "Trillium"
                temp_dict["quantity"] = b.split(".00\n")[0]
            else:
                c = b.split("\n")
                print(c)
                temp_dict["size"] = c[0].split()[0]
                temp_dict["product"] = c[0].split()[1].capitalize()
                # print(c[1])
                if "Notes:" in c[1]:
                    temp_dict["color"] = c[2][1:].capitalize()
                    temp_dict["color"] = temp_dict["color"].replace("Asst","Assorted")
                    temp_dict["pack_size"] = c[3].split("/")[0]
                    temp_dict["code"] = c[4]
                    temp_dict["upc"] = c[5].strip(" ")
                else:
                    temp_dict["pack_size"] = c[1].split("/")[0]
                    temp_dict["code"] = c[2]
                    temp_dict["upc"] = c[3].strip(" ")

                #SPECIAL CASES
                if "May Include Aeonium" in c[2]:
                    temp_dict["color"] = "Assorted"
                    temp_dict["pack_size"] = c[5].split("/")[0]
                    temp_dict["code"] = c[6]
                    temp_dict["upc"] = c[7].strip(" ")

                dict.append(temp_dict)
        return(dict)

if __name__ == "__main__":
    print(parse("purchase-order-3895181.pdf"))
    print("-----")
    print(parse("purchase-order-3895602.pdf"))
    print("-----")
    # print(parse("purchase-order-3895501.pdf"))
