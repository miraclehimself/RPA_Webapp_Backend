def getText(node, nodeList):
  dataInput = node['input']
  # options = (node['options']) if 'options' in node else None
  options = None
  txt = ""
  if node['label'] == "Open Browser":
    if dataInput['url'] != '':
      txt += f"browserid, pageid = Browser.openBrowser(url = r'{dataInput['url']}' {(f', options = {options}' )if options else ''})\n"
    else:
      txt += f"browserid, pageid = Browser.openBrowser({(f', options = {options}' )if options else ''})\n"
    txt += "output['browserid'].append(browserid)\n"
    txt += "output['pageid'].append(pageid)\n"
    # return {'status': 'OK', 'data': txt}
    return txt
  if node['label'] == "Open Link":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt = ""
    txt += f"pageid = Browser.goToUrl(output['browserid'][-1], output['pageid'][-1], r'{dataInput['url']}'{(f', options = {options}' )if options else ''})\n"
    txt += "output['pageid'].append(pageid)\n"
    return txt
  if node['label'] == "Close Browser":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += "Browser.closeBrowser(output['browserid'][-1])\n"
    txt += "output['browserid'].pop()\n"
    return txt
  if node['label'] == "Close Tab":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"Browser.closeTab(output['browserid'][-1], {(dataInput['pageid'])if  'pageid' in dataInput else None} or output['pageid'][-1])\n"
    txt += "output['pageid'].pop()\n"
    return txt
  if node['label'] == "Switch Tab":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"pageid = Browser.switchTab(output['browserid'][-1],{dataInput['pageid']})\n"
    txt += "output['pageid'].append(pageid)\n"
    return txt
  if node['label'] == "Go Back":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"Browser.goBackHistory(output['browserid'][-1],{(dataInput['pageid'])if  'pageid' in dataInput else None} or output['pageid'][-1], {dataInput['times']})\n"
    return txt
  if node['label'] == "Go Forward":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"Browser.goForwardHistory(output['browserid'][-1],{(dataInput['pageid'])if  'pageid' in dataInput else None} or output['pageid'][-1], {dataInput['times']})\n"
    return txt

  if node['label'] == "Click Element":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"Browser.elementClick(output['browserid'][-1],{(dataInput['pageid'])if  'pageid' in dataInput else None} or output['pageid'][-1], {dataInput['method']}, {dataInput['element']})\n"
    return txt

  if node['label'] == "Refresh":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"Browser.refreshPage(output['browserid'][-1],{(dataInput['pageid'])if  'pageid' in dataInput else None} or output['pageid'][-1])\n"
    return txt

  if node['label'] == "Type Text":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"Browser.elementInput(output['browserid'][-1],{(dataInput['pageid'])if  'pageid' in dataInput else None} or output['pageid'][-1], {dataInput['method']}, {dataInput['element']}, {dataInput['keylist']})\n"
    return txt

  if node['label'] == "Wait Element":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"Browser.waitElement(output['browserid'][-1],{(dataInput['pageid'])if  'pageid' in dataInput else None} or output['pageid'][-1], {dataInput['method']}, {dataInput['element']})\n"
    return txt

  if node['label'] == "Save Image":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"path = Browser.saveImage(output['browserid'][-1],{(dataInput['pageid'])if  'pageid' in dataInput else None} or output['pageid'][-1], {dataInput['method']}, {dataInput['element']}, {dataInput['savefilepath']})\n"
    txt += "output['path'].append(path)\n"
    return txt

  if node['label'] == "Screenshot":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"path = Browser.screenShot(output['browserid'][-1],{(dataInput['pageid'])if  'pageid' in dataInput else None} or output['pageid'][-1], {dataInput['savefilepath']})\n"
    txt += "output['path'].append(path)\n"
    return txt
  if node['label'] == "Get Data Dict":
    if 'Open Browser' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"dataobject = Browser.getDataTable(output['browserid'][-1], {(dataInput['pageid'])if  'pageid' in dataInput else None} or output['pageid'][-1], {dataInput['properties']})\n"
    txt += "output['dataobject'].append(dataobject)\n"
    return txt
  if node['label'] == "Write CSV":
    if 'Get Data Dict' not in nodeList:
      # return {'status': 'ERR', 'data': "No opened brower for open link"}
      return ""
    txt += f"CSV.saveDictToCSV(output['dataobject'][-1], r'{dataInput['file path']}' or output['path'][-1] {(f', options = {options}' )if options else ''})\n"
    return txt

  if node['label'] == "Read CSV":
    txt += f"dataobject = CSV.dataFromCSV(r'{dataInput['file path']}' or output['path'][-1] {(f', options = {options}' )if options else ''})\n"
    txt += "output['dataobject'].append(dataobject)\n"
    return txt
  
  if node['label'] == "Split CSV":
    txt += f"path = CSV.dataFromCSV(r'{dataInput['file path']}' or output['path'][-1], {dataInput['outputdir']}, {dataInput['outputname']}  {(f', options = {options}' )if options else ''})\n"
    txt += "output['path'].append(path)\n"
    return txt

  return ""
