from jcamp import jcamp_readfile
import urllib.request
import urllib.parse
import re
import os


def get_coordinates (file_path : str):
    # reading jcamp file
    jcamp_dict = jcamp_readfile(file_path)
    return {"x":jcamp_dict["x"], "y":jcamp_dict["y"]}





def get_jdx_link (name: str) :
    url = "https://webbook.nist.gov/cgi/cbook.cgi"
    values = {
        "Name" : name.strip(),
        "Units" : "SI"
    }

    url_values = urllib.parse.urlencode(values)
    data = url_values.encode('ascii')
    req = urllib.request.Request(url, data)
    
    with urllib.request.urlopen(req) as response :
        page = str(response.read())



    #extracting CAS no. from html
    cas_registry_patt = "CAS Registry Number:\<\/strong\> (\d*)-(\d*)-(\d*)"
    
    try :
        cas_registry_no = "".join(re.findall(cas_registry_patt, page)[0])
    except :
        return None, None


    #re-directing to IR link 
    ir_values = {
        "JCAMP" : cas_registry_no,
        "Index" : "1",
        "Type" : "IR",
    }

    url_ir_values = urllib.parse.urlencode(ir_values)
    jdx_link = url + "?" + url_ir_values
    
    return jdx_link, cas_registry_no






def download_and_save_file(link, name, location):
    # name is CAS no. in general 

    import requests
    try:
        response = requests.get(link, stream=True)
        response.raise_for_status()
        
        os.makedirs(location, exist_ok=True)
        file_path = os.path.join(location, name)

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


