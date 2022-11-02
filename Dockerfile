FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends git unzip wget fontconfig imagemagick fonts-symbola libmagick++-dev gcc ffmpeg python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /
COPY ./ ./
WORKDIR /src

# THERE IS MORE LINeS FOR GETTING IMAGEMAGIK WORKING THAN LINES OF NORMAL DOCKER SHIT BRUHHH
RUN sed -i '/<policy domain="path" rights="none" pattern="@\*"/d' /etc/ImageMagick-6/policy.xml
RUN cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g'> /etc/ImageMagick-6/policy.xml
RUN sed -i_bak 's/rights="none" pattern="PDF"/rights="read | write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml
RUN wget "https://www.dafontfree.io/download/verdana/?wpdmdl=71901&refresh=6362eb8bd1a9e1667427211&ind=1612703173429&filename=verdana-font-family.zip" -O font.zip
RUN unzip font.zip -d font
RUN cp -r font/* /usr/local/share/fonts
RUN fc-cache -f -v

RUN pip install -r requirements.txt --no-cache-dir
CMD ["python3", "main.py"]