from .text_script import getText

class CodeBlock():
  def __init__(self, head, block):
    self.head = head
    self.block = block

  def __str__(self, indent=""):
    result = indent + self.head + ":\n"
    indent += "  "
    for block in self.block:
      if isinstance(block, CodeBlock):
        result += block.__str__(indent)
      else:
        result += indent + block + "\n"
    return result


def transformNodes(nodes):
  tNodes = {}
  for node in nodes:
    tNodes[node['id']] = node['data']
  return tNodes


def flowScript(links, nodes):
  nodes = transformNodes(nodes)
  nodeList = []
  print(nodes)
  txt = "output = {'browserid': [], 'pageid': [], 'path': [], 'value': [], 'dataobject': []}\n"
  for link in links:
    txt += getText(nodes[link['source']], nodeList)
    nodeList.append(nodes[link['source']]['label'])
    txt += getText(nodes[link['target']], nodeList)
    nodeList.append(nodes[link['target']]['label'])
  return txt

def triggerScript(trigger, flow):
  flow = flow.split('\n')
  script = """"""
  if trigger['type'] == 'FILE_SYSTEM':
    if trigger['item'] == 'File Created':
      script = f"filepath = os.path.join(r'{trigger['property']['directory']}', '{trigger['property']['file_name']}')\nstart = True\n" + str(CodeBlock("while True", [CodeBlock(
          f"if start and os.path.exists(filepath)", ["print('file exists already')", "break"]), "start = False", CodeBlock(f"if os.path.exists(filepath)", flow + ['break'])]))

    elif trigger['item'] == 'File Deleted':
      script = "start = True\n" + str(CodeBlock("while True", [CodeBlock(
          f"if start and not os.path.exists(filepath)", ["print('file does not exists')", "break"]), "start = False", CodeBlock(f"if not os.path.exists(os.path.join(filepath)", flow + ['break'])]))
    elif trigger['item'] == 'File Modified':
      script = "now = time.time()\n" + str(CodeBlock("while True", [CodeBlock(
          f"if not os.path.exists(os.path.join(filepath)"), ["print('file does not exists')", "break", CodeBlock(f"if os.path.getmtime(os.path.join(filepath) > now", flow + ['break'])]]))
  return script

def scheduleScript(schedule, flow):
  return True

