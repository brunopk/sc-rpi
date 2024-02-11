USAGE="Usage: ./upload.sh <rpi username> <rpi address> <rpi folder>"
if [ -z $1 ]; then
  echo 'Missing argument: <rpi username>'
  echo $USAGE
  exit 1
fi
if [ -z $2 ]; then
  echo 'Missing argument: <rpi address>'
  echo $USAGE
  exit 1
fi
if [ -z $3 ]; then
  echo 'Missing argument: <rpi folder>'
  echo $USAGE
  exit 1
fi

if [ -a dist ]; then
  echo 'Removing previously created dist/ folder ...'
  rm -rf dist
fi

if [ -a dist.tar.gz ]; then
  echo 'Removing previously created dist.tar.gz file ...'
  rm dist.tar.gz
fi

echo 'Creating new dist/ folder'
mkdir dist/

echo 'Copying files ...'
cp -r ../lib dist
cp -r ../doc dist
# if neccessary, copy scripts from ./ folder one by one to dist/
cp -r ../src dist
cp ../config.ini dist
cp ../pyproject.toml dist
cp ../README.md dist
cp ../run_server.py dist

echo 'Removing all __pycache__ folders ...'
rm -rf **/**/__pycache__
rm -rf **/**/**/__pycache__

echo 'Compressing dist/ folder into dist.tar.gz'
tar -zcf dist.tar.gz dist

echo Uploading dist.tar.gz to $3/dist.tar.gz in $2
scp -r dist.tar.gz $1@$2:$3  


