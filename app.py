from flask import Flask,request
import boto3,os
import time
from PIL import Image
import access

from werkzeug.utils import secure_filename

api = Flask(__name__)
ACCESS_KEY = access.ACCESS_KEY
SECRET_KEY = access.SECRET_KEY
bucket_name = access.bucket_name

s3 = boto3.client(
   "s3",
   aws_access_key_id=ACCESS_KEY,
   aws_secret_access_key=SECRET_KEY
)
bucket_resource = s3
@api.route('/uploadFiles', methods=['POST'])
def upload_files():
    try:
        img = request.files['files']
        print(img.filename)
        filed, ext = os.path.splitext(img.filename)
        print(ext)
        # ext = str(ext)
        if (ext != '.png' and ext != '.jpg' and ext != '.jpge'):
            return ('Only Accepting .png,.jpg and .jpge Files')
        original = '/home/muthu/Pictures/upload/' + str(img.filename)
        padam = Image.open(original)
        width, height = padam.size

        if (width > 512 or height > 512):
            message = "Image Dimension should not more than 512*512 and Yours is {}*{} (w,h) ".format(width,height)
            return message
        width = str(width)
        height = str(height)
        print('width = '+width)
        print('height = '+height)

        filename = ''
        if img:
            ts = int(time.time())
            filename = str(ts)+secure_filename(img.filename)
            img.save(filename)
            ts = int(time.time())
            key = filename
            ExtraArgs = {
                "ContentType": 'image/jpeg',
            }

            bucket_resource.upload_file(
                Bucket=bucket_name,
                Filename=filename,
                Key=key,
                ExtraArgs = ExtraArgs
            )
            url = ("https://{}.s3.ap-south-1.amazonaws.com/").format(bucket_name)
            url = str(url) + str(filename)
            return ("Muthu You Made It ! \n URL = {} ").format(url)
    except Exception as e:
        return (str(e))
    return ('0')


if __name__ == '__main__':
    api.run(debug=True)