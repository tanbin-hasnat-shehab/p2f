
import requests
import json
import os
import random

class Request_Firebase():
    def __init__(self,*args,**kwargs):
        self.project_id=kwargs.get('project_id','')
        self.url='https://'+str(self.project_id)+'-default-rtdb.firebaseio.com'
        #self.url=kwargs.get('url','https://requestfirebase108-default-rtdb.firebaseio.com')      #16 gmail

    def input_data(self,*args,**kwargs):
        self.path=kwargs.get('path','raaf')
        self.data=kwargs.get('data',{})
        self.data_url = f'{self.url}/{self.path}.json'
        response = requests.patch(self.data_url, data=json.dumps(self.data))
        if response.status_code == 200:
            print("Data successfully added to Firebase.")
        else:
            print(f"Failed to add data. Status code: {response.status_code}")


    def show_data(self,*args,**kwargs):
        self.path=kwargs.get('path','/')
        self.data_url = f'{self.url}/{self.path}.json'
        response = requests.get(self.data_url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    def delete_data(self,*args,**kwargs):
        self.path=kwargs.get('path','')
        data_url = f'{self.url}/{self.path}.json'
        response = requests.delete(data_url)

        if response.status_code == 200:
            print("Data successfully deleted from Firebase.")
        else:
            print(f"Failed to delete data. Status code: {response.status_code}")


class Request_Firebase_Storage():
    def __init__(self,*args,**kwargs):
        self.firebase_project_id = kwargs.get('project_id','requestfirebase108')  #"pp1123435454"   #requestfirebase108
        self.storage_url = f"https://firebasestorage.googleapis.com/v0/b/{self.firebase_project_id}.appspot.com/o/"
        pass
    def upload_file(self,*args,**kwargs):
        local_file_path=kwargs.get('file_name','')
        l1=local_file_path.split('.')
        ext=l1[-1]
        
        file_name_only=''
        if len(l1)==2:
            file_name_only=l1[0]
        else:
            l1=l1.pop()
            for i in l1:
                file_name_only=file_name_only+i
        path=kwargs.get('path','ss_')
        random_num=random.randint(10000,20000)
        destination_blob_name=path+'|'+file_name_only+'_'+str(random_num)+'.'+ext
        upload_url = f"{self.storage_url}{destination_blob_name}"
        with open(local_file_path, "rb") as file:
            response = requests.post(upload_url, files={"file": (os.path.basename(local_file_path), file)})
        
        if response.status_code == 200:
            print(f"File {local_file_path} uploaded to {destination_blob_name}.")
        else:
            print(f"Failed to upload {local_file_path} - Status Code: {response.status_code}")

    # Function to download a file from Firebase Storage
    def download_files(self,*args,**kwargs):
        path=kwargs.get('path','')
        local_folder='downloads'
        list_url = f"{self.storage_url}?prefix=&delimiter=/"
        response = requests.get(list_url)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            for item in items:
                blob_name = item["name"]
                blob_arr=blob_name.split('|')
                if blob_arr[0]==path:
                    local_file_path = os.path.join(local_folder, blob_name.replace("|", "_"))
                    download_url = f"{self.storage_url}{blob_name}?alt=media"
                    print(download_url)
                    
                    self.download_single_file(download_url, local_file_path)
            
            print(f"All files from '{path}' downloaded to '{local_folder}'.")
        else:
            print(f"Failed to list files in '{path}' - Status Code: {response.status_code}")
    def download_single_file(self,download_url, local_file_path):
        response = requests.get(download_url)
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            with open(local_file_path, "wb") as file:
                file.write(response.content)
            print(f"File downloaded to {local_file_path}.")
        else:
            print(f"Failed to download file - Status Code: {response.status_code}")

    def delete_files(self,*args,**kwargs):
        path=kwargs.get('path','')
        # List all files in the specified folder
        list_url = f"{self.storage_url}?prefix=&delimiter=/"
        response = requests.get(list_url)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            for item in items:
                blob_name = item["name"]
                blob_arr=blob_name.split('|')
                if blob_arr[0]==path:
                    self.delete_file(blob_name)
            
            print(f"All files in folder '{path}' deleted.")
        else:
            print(f"Failed to list files in folder '{path}' - Status Code: {response.status_code}")
    def delete_file(self,blob_name):
        delete_url = f"{self.storage_url}{blob_name}"
        response = requests.delete(delete_url)
        
        if response.status_code == 204:
            print(f"File {blob_name} deleted.")
        else:
            print(f"Failed to delete {blob_name} - Status Code: {response.status_code}")
    def folder_list(self):
        list_url = f"{self.storage_url}?prefix=&delimiter=/"
        response = requests.get(list_url)
        folder_names=[]
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            for item in items:
                blob_name = item["name"]
                blob_arr=blob_name.split('|')
                first_name=blob_arr[0]
                if first_name not in folder_names:
                    folder_names.append(first_name)
        return folder_names
