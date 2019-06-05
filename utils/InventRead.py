
import logging
import time
import zipfile
import os
import re
from logging.handlers import RotatingFileHandler
# logging settings
today_time = time.strftime('%Y-%m-%d', time.localtime())

logger = logging.getLogger('PCMode')
handler = RotatingFileHandler('logs/Invent.log',
                              maxBytes=1024*1000*10, backupCount=2, encoding='utf-8')
handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def deal_files(zip_file_path):
    name = os.path.splitext(os.path.basename(zip_file_path))[0]
    dirname = os.path.dirname(zip_file_path)
    dst_dir_name = os.path.join(dirname, name)
    if not os.path.exists(dst_dir_name):
        f = zipfile.ZipFile(zip_file_path, 'r')
        for filename in f.namelist():
            f.extract(filename, dirname)

class InventRead():
    def __init__(self):
        self.titleStr = None
        self.abstractStr = None
        self.descriptionStr = None
        self.claimsStr = None
        self.mainClass = None

    def jiexi(self, xml_path):

        with open(xml_path, 'r', encoding='utf-8') as xml_file:
            content = xml_file.read()
        title_pattern = r'<business:InventionTitle id=(.*?)>(.*?)</business:InventionTitle>'
        abstract_pattern = r'<business:Abstract(.*?)>(.*?)</business:Abstract>'
        description_pattern = r'<business:Description(.*?)>(.*?)</business:Description>'
        claims_pattern = re.compile(r'<business:ClaimText>(.*?)</business:ClaimText>')
        mainClass_pattern = r'<business:ClassificationIPCR(.*?)>(.*?)<base:Text>(.*?)</base:Text>(.*?)</business:ClassificationIPCR>'
        replace_pattern = re.compile(r'<.+?>')
        class_replace_pattern = re.compile(r'\(.+?\)')

        title_node = re.search(title_pattern, content, re.M|re.S)
        if not title_node == None:
            self.titleStr = replace_pattern.sub('', title_node.group(2)).strip().replace('\n', '').replace(' ', '')
        else:
            logger.error('title parser error  Caused by:  ' + xml_path)

        abs_node = re.search(abstract_pattern, content, re.M|re.S)
        if not abs_node == None:
            contentabs = abs_node.group(2)
            Paragraphs_pattern = re.compile(r'<base:Paragraphs num=(.*?)>(.*?)</base:Paragraphs>')
            abstractStr0 = ''
            try:
                Paragraphs_list = re.findall(Paragraphs_pattern, contentabs)
                if len(Paragraphs_list) > 0:

                    for each in Paragraphs_list:
                        abstractStr0 = abstractStr0 + each[1] + '\n'
                self.abstractStr = abstractStr0.strip()
            except:
                self.abstractStr = None
                logger.error('abstract parser error  Caused by:  ' + xml_path)
        else:
            logger.error('abstract parser error  Caused by:  ' + xml_path)

        description_node = re.search(description_pattern, content, re.M|re.S)
        if not description_node == None:
            self.descriptionStr = replace_pattern.sub('', description_node.group(2)).strip().replace(' ', '')
        else:
            logger.error('description parser error  Caused by:  ' + xml_path)

        claimsList = claims_pattern.findall(content)
        if len(claimsList) > 0:
            claimsStr0 = ''
            for each in claimsList:
                claimsStr0 = claimsStr0 + each + '\n'
            self.claimsStr = claimsStr0.strip()
        else:
            logger.error('claims parser error  Caused by:  ' + xml_path)

        mainclass_node = re.search(mainClass_pattern, content, re.M | re.S)
        if not mainclass_node == None:
            self.mainClass = class_replace_pattern.sub('', mainclass_node.group(3)).strip().replace(' ', '')
        else:
            logger.error('mainclass parser error  Caused by:  ' + xml_path)

if __name__ == "__main__":
    xml_path = r'C:\Users\user\Desktop\发明\CN102017001132074CN00001079338270BFULZH20190521CN000\CN102017001132074CN00001079338270BFULZH20190521CN000.XML'
    example = InventRead()
    example.jiexi(xml_path)
    print(example.titleStr, '\n******\n', example.abstractStr, '\n******\n', example.descriptionStr, '\n******\n',
          example.claimsStr, '\n******\n', example.mainClass)
