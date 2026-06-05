#!/bin/bash

rm -rf tempdir
mkdir -p tempdir/templates
mkdir -p tempdir/static

cp sample_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

cat > tempdir/Dockerfile <<EOF
FROM python
RUN pip install flask
COPY ./static /home/myapp/static/
COPY ./templates /home/myapp/templates/
COPY sample_app.py /home/myapp/
EXPOSE 9999
CMD python /home/myapp/sample_app.py
EOF

cd tempdir
docker build -t sampleapp .

docker rm -f samplerunning 2>/dev/null

docker run -t -d -p 9999:9999 --name samplerunning sampleapp

docker ps -a
