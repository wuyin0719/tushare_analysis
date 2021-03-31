{
  "items": [
    {
      "abnormal": false,
      "createTime": "2021-03-27 13:59:33",
      "curtWorker": {
        "alias": "WY",
        "avatar": "",
        "id": 1343406557605824,
        "name": "WY",
        "type": {
          "name": "用户",
          "otid": 1
        }
      },
      "id": 1343446214571072,
      "label": "",
      "name": "工序_1343409280214080",
      "oldStatus": 17,
      "ownedClan": {
        "checkStatus": 1,
        "closed": false,
        "des": "test",
        "icon": "7bc6727d2aa14fc48109f0aa56b3fafa",
        "id": 1343407116465216,
        "name": "test",
        "obj": {
          "id": 1343407116465216,
          "type": {
            "otid": 2
          }
        },
        "pos": {
          "id": 0,
          "name": "系统",
          "type": {
            "name": "系统",
            "otid": 0
          }
        },
        "type": {
          "name": "用户组",
          "otid": 2
        },
        "uTime": "2021-03-27 11:20:27",
        "user": {
          "avatar": "",
          "id": 1343406557605824,
          "type": {
            "name": "用户",
            "otid": 1
          }
        }
      },
      "procedure": {
        "craft": {
          "id": 1343409248138304
        },
        "feeding": false,
        "form": {
          "x": 500,
          "y": 82
        },
        "genRule": {
          "arguments": [],
          "des": "根据配比值，默认任务生成规则",
          "enable": true,
          "id": 1343409280234561,
          "name": "默认任务生成规则",
          "ruleId": "cn.bluethink.ecs.rule.task.gen.GxDefaultTaskGenRule",
          "ruleType": 1,
          "type": {
            "name": "规则",
            "otid": 2007
          }
        },
        "id": 1343409280214080,
        "level": 1,
        "name": "工序_1343409280214080",
        "outputSchema": {
          "dataType": {
            "author": {
              "alias": "WY",
              "avatar": "",
              "id": 1343406557605824,
              "name": "WY",
              "type": {
                "name": "用户",
                "otid": 1
              }
            },
            "category": 1,
            "clan": {
              "id": 1343407116465216,
              "name": "",
              "type": {
                "name": "用户组",
                "otid": 2
              }
            },
            "code": "utf8",
            "description": "<p></p>",
            "dim": 0,
            "fileRules": [
              {
                "count": 1,
                "description": "",
                "directory": false,
                "entry": true,
                "nameDuplicated": false,
                "pattern": "*.shp"
              },
              {
                "count": 1,
                "description": "",
                "directory": false,
                "entry": false,
                "nameDuplicated": false,
                "pattern": "*.xls"
              },
              {
                "count": 1,
                "description": "",
                "directory": false,
                "entry": false,
                "nameDuplicated": false,
                "pattern": "*.doc"
              }
            ],
            "id": 1343410650293312,
            "logo": "",
            "name": "cc",
            "reusable": true,
            "type": {
              "name": "数据类型",
              "otid": 2001
            },
            "version": "1"
          },
          "id": 1343409280226368,
          "inheritFrom": null,
          "label": false,
          "type": {
            "name": "数据范式",
            "otid": 2002
          }
        },
        "planHours": 0,
        "priority": 3,
        "qStandard": [],
        "qc": false,
        "qcFailRule": {
          "arguments": [],
          "des": "默认质检规则",
          "enable": true,
          "id": 1343409280234560,
          "name": "默认质检规则",
          "ruleId": "cn.bluethink.ecs.rule.task.gen.GxDefaultTaskQcFailRule",
          "ruleType": 5,
          "type": {
            "name": "规则",
            "otid": 2007
          }
        },
        "qcMeasure": 0,
        "qcSchema": {
          "dataType": {
            "category": null,
            "id": null,
            "type": {
              "name": "数据类型",
              "otid": 2001
            }
          },
          "id": 1343409280226369,
          "inheritFrom": null,
          "label": false,
          "type": {
            "name": "数据范式",
            "otid": 2002
          }
        },
        "type": {
          "name": "工序",
          "otid": 2005
        },
        "unit": 1,
        "workMeasure": 0,
        "workRule": {
          "content": "",
          "id": 1343409280238656,
          "name": "",
          "options": [],
          "procedure": {
            "id": 1343409280214080,
            "type": {
              "name": "工序",
              "otid": 2005
            },
            "workerInherit": null
          },
          "type": {
            "name": "作业细则",
            "otid": 2009
          }
        },
        "workerInherit": null
      },
      "project": {
        "beginTime": "2021-03-27 13:58:55",
        "category": 1,
        "craft": {
          "id": 1343409248138304,
          "type": {
            "name": "工艺",
            "otid": 2004
          }
        },
        "createTime": "2021-03-27 13:58:47",
        "deadline": "2021-03-27 23:59:59",
        "des": "",
        "id": 1343446026253376,
        "manager": {
          "id": 1343406557605824,
          "type": {
            "name": "用户",
            "otid": 1
          }
        },
        "measure": 1,
        "name": "project",
        "obj": {
          "id": 1343446026253376,
          "name": "project",
          "type": {
            "name": "项目",
            "otid": 2201
          }
        },
        "pos": {
          "id": 1343407116465216,
          "type": {
            "otid": 2
          }
        },
        "priority": 1,
        "status": 2,
        "storage": {
          "host": "C:\\Users\\吴隐\\Desktop\\arcgis\\c#\\ArcMapAddin1\\ArcMapAddin1\\Images",
          "protocol": "file://"
        },
        "type": {
          "name": "项目",
          "otid": 2201
        },
        "uTime": "2021-03-27 13:58:55",
        "unit": 1,
        "user": {
          "id": 1343406557605824,
          "type": {
            "name": "用户",
            "otid": 1
          }
        },
        "workAlone": false,
        "workload": 101111
      },
      "qc": false,
      "sn": "ECS_SN_NULL",
      "status": 32,
      "takeTime": "2021-03-27 14:02:18",
      "type": {
        "name": "任务",
        "otid": 2202
      },
      "version": 1616824938413
    }
  ],
  "pageItems": 0,
  "pageNo": 0,
  "pageSize": 0,
  "totalItems": 1,
  "totalPages": 0
}

     ESRI.ArcGIS.Geodatabase.IWorkspaceFactory wksFact;                 wksFact = new ShapefileWorkspaceFactory();
     ESRI.ArcGIS.Geodatabase.IFeatureWorkspace featWrk;
     featWrk = (IFeatureWorkspace)wksFact.OpenFromFile(gxObj.Parent.FullName, 0);
     ESRI.ArcGIS.Geodatabase.IFeatureClass fClass;
     fClass = featWrk.OpenFeatureClass(gxObj.Name);
     ESRI.ArcGIS.Carto.IFeatureLayer lyr;
     lyr = new FeatureLayer();
     lyr.FeatureClass = fClass;                 lyr.Name = gxObj.Name;                  ESRI.ArcGIS.ArcMapUI.IMxDocument mxDoc = (ESRI.ArcGIS.ArcMapUI.IMxDocument)(m_application.Document); //ERROR IS HERE AT M_application                 IMap map = mxDoc.FocusMap;                 map.AddLayer(lyr);

"{\r\n  \"author\": {\r\n    \"alias\": \"WY\",\r\n    \"avatar\": \"\",\r\n    \"id\": 1343406557605824,\r\n    \"name\": \"WY\",\r\n    \"type\": {\r\n      \"name\": \"用户\",\r\n      \"otid\": 1\r\n    }\r\n  },\r\n  \"category\": 1,\r\n  \"clan\": {\r\n    \"id\": 1343407116465216,\r\n    \"name\": \"\",\r\n    \"type\": {\r\n      \"name\": \"用户组\",\r\n      \"otid\": 2\r\n    }\r\n  },\r\n  \"code\": \"utf8\",\r\n  \"description\": \"<p></p>\",\r\n  \"dim\": 0,\r\n  \"fileRules\": [\r\n    {\r\n      \"count\": 1,\r\n      \"description\": \"\",\r\n      \"directory\": false,\r\n      \"entry\": true,\r\n      \"nameDuplicated\": false,\r\n      \"pattern\": \"*.shp\"\r\n    },\r\n    {\r\n      \"count\": 1,\r\n      \"description\": \"\",\r\n      \"directory\": false,\r\n      \"entry\": false,\r\n      \"nameDuplicated\": false,\r\n      \"pattern\": \"*.xls\"\r\n    },\r\n    {\r\n      \"count\": 1,\r\n      \"description\": \"\",\r\n      \"directory\": false,\r\n      \"entry\": false,\r\n      \"nameDuplicated\": false,\r\n      \"pattern\": \"*.doc\"\r\n    }\r\n  ],\r\n  \"id\": 1343410650293312,\r\n  \"logo\": \"\",\r\n  \"name\": \"cc\",\r\n  \"reusable\": true,\r\n  \"type\": {\r\n    \"name\": \"数据类型\",\r\n    \"otid\": 2001\r\n  },\r\n  \"version\": \"1\"\r\n}"



dim pLayer as ILayer  For i = 0 To LayerCount - 1   pLayer = pMap.Layer(i)
If TypeOf pLayer Is IFeatureLayer Then
'Vector   ElseIf TypeOf pLayer Is IRasterLayer Then     'Raster       End If next i