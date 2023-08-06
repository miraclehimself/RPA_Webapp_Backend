from src.models.function import FunctionGroup, Functions, db
from src.utils import serializeList

functionGroupList = [
  {
    "group_name": "Browser",
    "description": "Browser related task"
  },
  {
      "group_name": "CSV",
      "description": "CSV related task"
  }
]

functionsList = {
  "Browser": [
    {
      "function_name": "Open Browser",
      "description": "Opens a web browser",
      "input": [
        {"name": "url", "type": "url", "required": False}
      ],
      "output": [
        {"type": "browser_id"},
        {"type": "page_id"}
      ],
      "options": [
          {"name": "Browser", "type": "enum", "options": [
              "Chrome"], "required": True, "default": "Chrome"},
          {"name": "Maximized", "type": "boolean", "required": True, "default": True}
      ]
    },
    {
      "function_name": "Open Link",
      "description": "Visit a link on a webpage",
      "input": [
        {"name": "url", "type": "url", "required": True},
        {"name": "Browser", "type": "browser_id", "required": False},
        {"name": "Page Id", "type": "page_id", "required": False}
      ],
      "output": [
        {"type": "page_id"}
      ],
      "options": [
        {"name": "Time out", "type": "integer",
          "required": True, "default": 30},
        {"name": "Open in same tab", "type": "boolean", "required": True}
      ]
    },
    {
      "function_name": "Close Browser",
      "description": "Closes an open web browser",
      "input": [
        {"name": "Browser", "type": "browser_id", "required": False}
      ],
      "output": [
      ],
      "options": [
      ]
    },
    {
      "function_name": "Close Tab",
      "description": "Closes an open tab",
      "input": [
        {"name": "Browser", "type": "browser_id", "required": False},
        {"name": "Page Id", "type": "page_id", "required": False}
      ],
      "output": [
      ],
      "options": [
      ]
    },
    {
      "function_name": "Switch Tab",
      "description": "Switches to a different tab",
      "input": [
        {"name": "Page Id", "type": "page_id", "required": True}
      ],
      "output": [
        {"type": "page_id"}
      ],
      "options": [
      ]
    },
    {
      "function_name": "Go Back",
      "description": "Go back in history",
      "input": [
        {"name": "Page Id", "type": "page_id", "required": False},
        {"name": "Times", "type": "integer", "required": True, "default": 1}
      ],
      "output": [
      ],
      "options": [
      ]
    },
    {
      "function_name": "Go Forward",
      "description": "Go forward in history",
      "input": [
        {"name": "Page Id", "type": "page_id", "required": False},
        {"name": "Times", "type": "integer", "required": True, "default": 1}
      ],
      "output": [
      ],
      "options": [
      ]
    },
    {
      "function_name": "Refresh",
      "description": "Refresh a web page",
      "input": [
        {"name": "Page Id", "type": "page_id", "required": False}
      ],
      "output": [
      ],
      "options": [
      ]
    },
    {
      "function_name": "Screenshot",
      "description": "Screenshot a webpage",
      "input": [
        {"name": "Page Id", "type": "page_id", "required": False},
        {"name": "Save file path", "type": "path", "required": True}
      ],
      "output": [
        {"type": "path"}
      ],
      "options": [
      ]
    },
    {
      "function_name": "Alert",
      "description": "Handle an alert on the web page",
      "input": [
        {"name": "Page Id", "type": "page_id", "required": False}
      ],
      "output": [
        {"type": "text"}
      ],
      "options": [
        {"name": "Action", "type": "enum", "options": ["accept", "cancel", "input"],"required": False},
        {"name": "Input text", "type": "text", "required": False}
      ]
    },
    {
      "function_name": "Save Image",
      "description": "Save Images on a webpage",
      "input": [
        {"name": "Page Id", "type": "page_id", "required": False},
        {"name": "Selector Type", "type": "enum", "required": True, "options": ['xpath', 'id', 'css selector', 'class name'], 'default': 'xpath'},
        {"name": "Selector", "type": "text", "required": True},
        {"name": "Save file path", "type": "path", "required": True}
      ],
      "output": [
        {"type": "path"}
      ],
      "options": [
      ]
    },
    {
      "function_name": "Wait Element",
      "description": "Waits for an element",
      "input": [
        {"name": "Page Id", "type": "page_id", "required": False},
        {"name": "Selector Type", "type": "enum", "required": True, "options": ['xpath', 'id', 'css selector', 'class name'], 'default': 'xpath'},
        {"name": "Selector", "type": "text", "required": True}
      ],
      "output": [
      ],
      "options": [
        {"name": "Condition", "type": "enum", "options": ["To appear", "To disappear"],"required": True, "deafult": "To Appear"},
        {"name": "Time out", "type": "integer", "required": True, "default": 30},
      ],
    },
    {
      "function_name": "Click Element",
      "description": "Clicks an element",
      "input": [
        {"name": "Page Id", "type": "page_id", "required": False},
        {"name": "Selector Type", "type": "enum", "required": True, "options": ['xpath', 'id', 'css selector', 'class name'], 'default': 'xpath'},
        {"name": "Selector", "type": "text", "required": True}
      ],
      "output": [
      ],
      "options": [
        {"name": "Click type", "type": "enum", "options": ["Single click", "Double click"],"required": True, "default": "Single click"}
      ],
    },
    {
      "function_name": "Type text",
      "description": "Type text in an element",
      "input": [
        {"name": "Page Id", "type": "page_id", "required": False},
        {"name": "Selector Type", "type": "enum", "required": True, "options": ['xpath', 'id', 'css selector', 'class name'], 'default': 'xpath'},
        {"name": "Selector", "type": "text", "required": True},
        {"name": "Text", "type": "text", "required": True}
      ],
      "output": [
      ],
      "options": [
        {"name": "Press Enter", "type": "boolean","required": True, "default": False},
        {"name": "Clear before typing", "type": "boolean", "required": True, "default": False}
      ],
    },
    {
      "function_name": "Get Value",
      "description": "Get value of an element in a webpage",
      "input": [
        {"name": "Page Id", "type": "page_id", "required": False},
        {"name": "Selector Type", "type": "enum", "required": True, "options": ['xpath', 'id', 'css selector', 'class name'], 'default': 'xpath'},
        {"name": "Selector", "type": "text", "required": True},
        {"name": "Text", "type": "text", "required": True}
      ],
      "output": [
        {"type": "value"}
      ],
      "options": [
        {"name": "Press Enter", "type": "boolean","required": True, "default": False},
        {"name": "Clear before typing", "type": "boolean", "required": True, "default": True}
      ],
    },
    {
      "function_name": "Get Data Dict",
      "description": "Get list of data from various element",
      "input": [
        {"name": "Properties", "type": "list", "required": True, 'properties': [
          {"name": "Selector Type", "type": "enum", "required": True, "options": [
              'xpath', 'id', 'css selector', 'class name'], 'default': 'xpath'},
          {"name": "Selector", "type": "text", "required": True},
          {"name": "Name", "type": "text", "required": True, "default": "AUTO"}
        ]},
        {"name": "Page Id", "type": "page_id", "required": False},
      ],
      "output": [
        {"type": "data_dict"}
      ],
      "options": [
      ],
    }
  ],
  "CSV": [
    {
      "function_name": "Read CSV",
      "description": "Reads a csv",
      "input": [
        {"name": "File path", "type": "path", "required": True}
      ],
      "output": [
        {"type": "data_dict"},
      ],
      "options": [
        {"name": "Separator", "type": "enum", "options": [
            "Comma", "Tab", "Semicolon"], "required": True, "default": "Comma"},
        {"name": "Encoding", "type": "enum", "required": True, "options": [
            "UTF-8"], "default": "UTF-8"}
      ]
    },
    {
      "function_name": "Write CSV",
      "description": "Writes data to a csv",
      "input": [
        {"name": "File path", "type": "path", "required": True},
        {"name": "Data", "type": "data_dict", "required": False}
      ],
      "output": [
      ],
      "options": [
        {"name": "Separator", "type": "enum", "options": [
            "Comma", "Tab", "Semicolon"], "required": True, "default": "Comma"},
        {"name": "Encoding", "type": "enum", "required": True, "options": [
            "UTF-8"], "default": "UTF-8"},
        {"name": "headers", "type": "boolean", "required": True, "default": True}
      ]
    },
    {
      "function_name": "Merge CSV",
      "description": "Merges sperate csv to single CSV",
      "input": [
        {"name": "Input File Paths", "type": "list", "required": True, 'properties': [
          {"name": "File path", "type": "path", "required": True},
        ]}
      ],
      "output": [
        {"name": "Output File path", "type": "path", "required": True}
      ],
      "options": [
        {"name": "Separator", "type": "enum", "options": [
            "Comma", "Tab", "Semicolon"], "required": True, "default": "Comma"},
        {"name": "Encoding", "type": "enum", "required": True, "options": [
            "UTF-8"], "default": "UTF-8"},
        {"name": "headers", "type": "boolean", "required": True, "default": True}
      ]
    },
    {
      "function_name": "Split CSV",
      "description": "Split a single CSV to multiple csv",
      "input": [
        {"name": "File path", "type": "path", "required": True},
        {"name": "Max rows", "type": "integer", "required": False, "default": 100},
        {"name": "Output Dir", "type": "path", "required": True},
        {"name": "Output Name", "type": "text", "required": True},
      ],
      "output": [
        {"name": "Out Directory", "type": "path", "required": True},
      ],
      "options": [
        {"name": "Separator", "type": "enum", "options": [
            "Comma", "Tab", "Semicolon"], "required": True, "default": "Comma"},
        {"name": "Encoding", "type": "enum", "required": True, "options": [
            "UTF-8"], "default": "UTF-8"},
        {"name": "headers", "type": "boolean", "required": True, "default": True}
      ]
    },
  ]
}
def updateFuncs():
  Functions.query.delete()
  FunctionGroup.query.delete()
  for i in functionGroupList:
    fg = FunctionGroup(**i)
    db.session.add(fg)
    db.session.commit()
    for j in functionsList[fg.group_name]:
      func = Functions(group_id=fg.id, **j)
      db.session.add(func)
  db.session.commit()
  return getFunc()



def getFunc():
  query = """SELECT group_id, group_name, description, function_list


  FROM "rpa-test"."function_group" AS fg
  INNER JOIN(
    SELECT group_id, json_agg(json_build_object('function_name', function_name, 'description', description, 'options', options, 'id', id, 'input', input, 'output', output)) AS function_list
    FROM   "rpa-test"."functions"
    GROUP  BY group_id
  ) AS fl
  ON fg.id = fl.group_id"""
  data = db.session.execute(query).mappings().all()

  return serializeList(data)

