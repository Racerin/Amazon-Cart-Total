import os
from lxml import etree

def calc_total():
    file_name = "Amazon.com.html"
    file_path = os.path.join(os.getcwd(), file_name)

    xpath1 = r"//span[@class='a-price-whole']"
    xpath2 = r"//span[@class='a-price-fraction']"

    with open(file_path, encoding="utf8") as file:
        doc = file.readlines()
        text = "\n".join(doc)
        assert isinstance(text, str), type(text)

        tree = etree.HTML(text)
        whole_num_cash = tree.xpath(xpath1)
        fraction_num_cash = tree.xpath(xpath2)
        moneys = list()
        for ele_pair in zip(whole_num_cash, fraction_num_cash):
            cost_text = ".".join(ele.text.strip() for ele in ele_pair)
            cost = float(cost_text)
            moneys.append(cost)
        print("This is how much it cost: ${:.2f}".format(sum(moneys)))