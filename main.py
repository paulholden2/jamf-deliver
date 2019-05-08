import sys
import os
import pysftp
import csv

delivered_suffix = '_Delivered Prod'

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

output_dir = '\\\\stria-prod1\\CID01559 - jamf\\JID01157 - CaaS for Contracts into SpringCM\\Output'

def deliver_dir(dir, sftp):
    remote_dir = '/Admin/Stria Deliveries'
    pdf_files = []
    load_file = None
    sftp.chdir(remote_dir)
    for file in os.listdir(dir):
        file_full_path = os.path.join(dir, file)
        if not os.path.isfile(file_full_path):
            continue
        if file.endswith('pdf'):
            pdf_files.append(file_full_path)
        elif file.endswith('csv'):
            load_file = file_full_path
    if load_file is None:
        print('No load file found for %s' % dir)
        return
    for file in pdf_files:
        res = sftp.put(file)
        print(file)
        print(res)
        sys.stdout.flush()
    # Load file upload
    res = sftp.put(load_file)
    print(load_file)
    print(res)
    sys.stdout.flush()
    # Mark delivery directory as delivered
    os.rename(dir, dir + delivered_suffix)

for dir in os.listdir(output_dir):
    # Canonical path of delivery directory
    delivery_dir = os.path.join(output_dir, dir)
    # Skip things that aren't folders
    if not os.path.isdir(delivery_dir):
        continue
    # Don't deliver if marked as delivered
    if dir.endswith(delivered_suffix):
        continue
    conn = pysftp.Connection(host='sftpna21.springcm.com', username='solutionsteam@stria.com.jamf', private_key='C:\\Users\\PHolden\\.ssh\\solutionsteam@stria.com.jamf',cnopts=cnopts)
    deliver_dir(delivery_dir, conn)
    conn.close()
