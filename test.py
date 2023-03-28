from models import XML, CreateBase, get_valid
import requests


def test_get():
    query = get_valid(1000)

    print(list(query.dicts()))


def test_Update():
    v = get_valid(1)[0]
    v.update_status(2000, "OK")
    print(v)
    pass


def has_something():
    return len(get_valid(1)) > 0


def send_one(id, main_url, token):
    testxml = XML.get(XML.id == id)
    headers = {}
    try:
        with open(testxml.Path, 'r', encoding='utf-8') as f:
            file = f.read()
    except:
        with open(testxml.Path, 'r', encoding='ANSI') as f:
            file = f.read()
    #file = re.sub('\n', '', file)
    file = file.replace('"', '\\"')
    if testxml.api == 'importarxmlnfearray':
        payload = f'[{{"Xml": "{file}","Format": true}}]'
    else:
        payload = f'{{"data": [{{"Xml": "{file}","Format": true}}]}}'
    url = f"https://{main_url}.app.questorpublico.com.br/api/v1/{token}/{testxml.api}"
    resp = requests.post(url, headers=headers, data=payload)
    text = resp.text
    code = resp.status_code
    testxml.update_status(code, text)
    print(f'URL:{url}')
    print(f'data:{payload}')
    print(f'the resposse was code:{code}')
    pass


if __name__ == '__main__':
    CreateBase()
    main_url = "escritorio_contabil"
    token = "119c963a17e4bca679a247ca0b11af93"
    row = 261720
    send_one(row, main_url, token)
