from PyPDF2 import PdfReader
import re

def renderer(filename):
    if re.search("(PurchaseOrder-WESGRE-)\d{2}-\w{3}-\d{2}.{0,}\.pdf", filename):
        from modules.foliera import parse
    elif re.search("(purchase-order-)\d{7}\.pdf", filename):
        from modules.trillium import parse
    return parse(filename)

if __name__ == "__main__":
   pass