#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install pdfminer3


# In[3]:


from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io

def pdf2text(path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(path, 'rb') as fh:

        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    data = text.split("\n\n")

    for i in range (0, len(data)):
        data[i] = " ".join(data[i].split())
    for i in range(0, len(data)):
        data[i] = data[i].replace('-\n', '')
        data[i] = data[i].replace('\n', ' ')
    return data
path = 'D:/MyDoc/Deep_learning/Yim_A_Gift_From_CVPR_2017_paper.pdf'
pdf2text(path)


# In[ ]:




