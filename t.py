import requests
import time

API_KEY = '18772kx945fu4ukvu4fyk'
CREATE_FOLDER_URL = 'https://api.streamwish.com/api/folder/create'
CLONE_FILE_URL = 'https://api.streamwish.com/api/file/clone'
GET_FILE_INFO_URL = 'https://api.streamwish.com/api/file/info'

def create_folder(folder_name, parent_id=0, description=''):
    response = requests.get(
        CREATE_FOLDER_URL,
        params={
            'key': API_KEY,
            'name': folder_name,
            'parent_id': parent_id,
            'descr': description
        }
    )
    data = response.json()
    if data['status'] == 200:
        return data['result']['fld_id']
    else:
        raise Exception(f"Failed to create folder: {data['msg']}")

def clone_file(file_code, title=None, folder_id=None):
    params = {
        'key': API_KEY,
        'file_code': file_code
    }
    if title:
        params['file_title'] = title
    if folder_id:
        params['fld_id'] = folder_id

    response = requests.get(CLONE_FILE_URL, params=params)
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Erro ao decodificar a resposta JSON. Resposta bruta: {response.text}")
        raise
    if data['status'] == 200:
        return data['result']
    else:
        raise Exception(f"Failed to clone file: {data['msg']}")

def get_file_info(file_code):
    response = requests.get(
        GET_FILE_INFO_URL,
        params={'key': API_KEY, 'file_code': file_code}
    )
    data = response.json()
    if data['status'] == 200:
        return data['result'][0] if isinstance(data['result'], list) else data['result']
    else:
        raise Exception(f"Failed to get file info: {data['msg']}")

def main():
    urls = []
    print("Digite as URLs para clonar e pressione Enter duas vezes para finalizar a lista:")
    while True:
        url = input()
        if url.strip() == "":
            break
        urls.append(url)
    
    folder_name = input("Digite o nome da pasta onde os arquivos serão clonados: ")
    folder_id = create_folder(folder_name)

    # Determine o número de zeros com base na quantidade total de URLs
    total_urls = len(urls)
    num_digits = len(str(total_urls))

    for index, url in enumerate(urls):
        file_code = url.split('/')[-1]  # Extrai o código do arquivo da URL
        file_info = get_file_info(file_code)
        
        # Nomeia o arquivo conforme a pasta e a posição, adicionando zeros à esquerda
        file_title = f"{folder_name} - EP{str(index + 1).zfill(num_digits)}"

        print(f"Clonando o arquivo {file_title}...")
        try:
            result = clone_file(file_code, title=file_title, folder_id=folder_id)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao clonar o arquivo: {e}")
            continue

        # Exibir a resposta da API para depuração
        print(f"Resposta da API: {result}")
        
        if 'url' in result and 'filecode' in result:
            print(f"Arquivo clonado com sucesso. URL: {result['url']}, Código do arquivo: {result['filecode']}")
        else:
            print(f"Arquivo clonado com sucesso, mas a resposta não contém 'url' ou 'filecode': {result}")
        
        # Aguarda 1.5 segundos antes de processar o próximo (ou ajuste conforme necessário)
        time.sleep(1.5)

if __name__ == "__main__":
    main()
