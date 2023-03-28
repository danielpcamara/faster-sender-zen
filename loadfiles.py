import os
import xml.etree.ElementTree as ET
from models import XML, get_valid, has_something
import re
import asyncio
import aiohttp
import time


def load_to_database(rootdir, skip):
    i = 0

    print(f"Geting Dirs...")
    dirs = listdirs(rootdir)

    t = len(dirs)
    for folder in dirs:
        i += 1
        if i < skip: continue  # SKIP CODE

        start = time.time()
        print(f"{i} / {t} - Geting Files of {folder}...")
        amount_of_xml = 0
        for file in os.listdir(folder):
            if file.endswith(".xml"):
                path = os.path.join(folder, file)
                amount_of_xml += 1
                obj = XML(
                    Path=path,
                    File=file,
                    Valid=int(XML_valid(path))
                )
                try:
                    obj.save(force_insert=True)
                except Exception:
                    pass
                update_xml_propriety(path)

        if amount_of_xml == 0:
            continue
        # sys.exit("STOP!")

        end = time.time()
        total_time = end - start

        print(f"{i} / {t} - It took {total_time} second(s) to load {amount_of_xml} file(s)")

    print(f"All File(s) loaded.")


def update_xml_propriety(path):
    row = XML.get(XML.Path == path)
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        if root.tag in ['CFe', 'CFeCanc']:
            type_xml = root.tag
        elif root.tag in ['resNFe']:
            type_xml = 'skip'
        else:
            try:
                type_xml = re.search('(?<=[}])([a-z]|[A-Z]){6,13}', root.tag).group(0)
            except AttributeError:
                type_xml = 'error'
    except ET.ParseError:
        type_xml = 'error'

    if 'nfe' in type_xml or 'NFe' in type_xml:
        api_xml = "importarxmlnfearray"
    elif 'cte' in type_xml or 'CTe' in type_xml:
        api_xml = "importarxmlcteosarray"
    elif 'cfe' in type_xml or 'CFe' in type_xml:
        api_xml = "importarxmlcfearray"
    else:
        api_xml = "error"
    row.Type = type_xml
    row.api = api_xml
    row.save()


def listdirs(rootdir):
    dirs = [rootdir]
    for it in os.scandir(rootdir):
        if it.is_dir():
            dirs.append(it.path)
            dirs.extend(listdirs(it.path))
    return dirs


def XML_valid(path):
    try:
        tree = ET.parse(path)
        ok = True
    except ET.ParseError:
        ok = False
    return ok


def send_valid_new(mainurl, token, simult_quant, sleep_time):
    while has_something():
        start = time.time()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(send_xml(mainurl, token, simult_quant))

        end = time.time()
        total_time = end - start
        x = 1
        print(f"It took {total_time} second(s) to make the API call(s)")
        time.sleep(sleep_time)


def get_tasks(session, mainurl, token, simult_quant):
    tasks = []
    xml_files = get_valid(simult_quant)
    i = 0
    for xml in xml_files:
        i += 1
        headers = {}
        try:
            with open(xml.Path, 'r', encoding='utf-8') as f:
                file = f.read()
        except:
            with open(xml.Path, 'r', encoding='ANSI') as f:
                file = f.read()
        file = file.replace('"', '\\"')
        if xml.api == 'importarxmlnfearray':
            payload = f'[{{"Xml": "{file}","Format": true}}]'
        else:
            payload = f'{{"data": [{{"Xml": "{file}","Format": true}}]}}'
        url = f"https://{mainurl}.app.questorpublico.com.br/api/v1/{token}/{xml.api}"
        tasks.append(asyncio.create_task(
            session.post(url, headers=headers, data=payload)
        ))
    return tasks


async def send_xml(mainurl, token, simult_quant):
    # timeout_seconds = 5 # em segundos
    # session_timeout = aiohttp.ClientTimeout(total=None, sock_connect=timeout_seconds, sock_read=timeout_seconds)
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, mainurl, token, simult_quant)
        xml_files = get_valid(simult_quant)
        try:
            responses = await asyncio.gather(*tasks)
            for (resp, xml) in zip(responses, xml_files):
                text = await resp.text()
                code = resp.status
                xml.update_status(code, text)  # Save Status and Response
        except aiohttp.client_exceptions.ServerTimeoutError:
            pass
