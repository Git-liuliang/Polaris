import os ,sys
from Polaris.settings import BASE_DIR
import time

def createdir(user):
    homedir = os.path.join(BASE_DIR, "abbs", user)
    if not os.path.isdir(homedir):
        os.mkdir(homedir)
        backupfile = os.path.join(homedir,"backupfile")
        os.mkdir(backupfile)

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
def  store_upload_file(user,file):
    current_time = time.strftime('%Y%m%d',time.localtime(time.time()))
    backupfile_dir = os.path.join(BASE_DIR,"abbs",user, "backupfile",current_time)
    if not os.path.isdir(backupfile_dir):
        os.mkdir(backupfile_dir)

    storename = '%s%s'%(file.name ,time.time())
    store_dir = os.path.join(backupfile_dir,storename)
    path = default_storage.save(store_dir, ContentFile(file.read()))
    return path







