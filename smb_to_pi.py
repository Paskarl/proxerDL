import os
from tqdm import tqdm
from smb.SMBConnection import SMBConnection
import shutil

smb_server_ip = "192.168.178.00"
smb_server_name = "raspberry.local"
smb_share_name = "SHARE"
smb_user_name = "USER"
smb_password = "USER"


file_path = ""
folder_path = ''
conn = SMBConnection(smb_user_name, smb_password, 'client', smb_server_name, use_ntlm_v2=True)
conn.connect(smb_server_ip)

for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        with open(file_path, 'rb') as f:
            file_size = os.path.getsize(file_path)
            file_path = file_path.replace(folder_path, '').replace('\\', '/').lstrip('/')
            end_folder_path = "\\test\\"
            end_path = end_folder_path + file_path
            conn.storeFile(smb_share_name, end_path, f, show_progress=True)
            conn.storeFile(smb_share_name, "/test", f, show_progress=True)
        
if conn:
    print("Datei übertragen")
    conn.close()
    
else:
    print("Fehler bruder du weischt")
    
    
    