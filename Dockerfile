FROM python:3.10-slim

# install packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git unzip wget fontconfig imagemagick fonts-symbola \
    libmagick++-dev gcc ffmpeg python3-dev && rm -rf /var/lib/apt/lists/*

# Set work dir as root
WORKDIR /

# copy all the files from project to container
COPY ./ ./

# set work dir as src kinda like cd-ing into it and staying there
WORKDIR /src

# Configure imagemagick settings
RUN sed -i '/<policy domain="path" rights="none" pattern="@\*"/d' /etc/ImageMagick-6/policy.xml
RUN cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g'> /etc/ImageMagick-6/policy.xml
RUN sed -i_bak 's/rights="none" pattern="PDF"/rights="read | write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml

# install verdana font for crab command
RUN wget --progress=dot:giga "https://www.dafontfree.io/download/verdana/?wpdmdl=71901&refresh=6362eb8bd1a9e1667427211&ind=1612703173429&filename=verdana-font-family.zip" -O font.zip
RUN unzip font.zip -d font
RUN cp -r font/* /usr/local/share/fonts

# reload font cache
RUN fc-cache -f -v

# Install required packages from requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

# run the bot :)
CMD ["python3", "main.py"]