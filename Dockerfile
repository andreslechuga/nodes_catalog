FROM selenium/standalone-chrome

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install selenium
RUN python3 -m pip install requests
RUN python3 -m pip install pandas
RUN python3 -m pip install xlrd

ADD get_catalog.py /

CMD ["python3", "./get_catalog.py"]
