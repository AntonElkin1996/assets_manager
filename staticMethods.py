import json

class StaticMethods():
    @staticmethod
    def getCreationModeInventoryState(pathToCreationModeInventory):
        with open(pathToCreationModeInventory, 'r', encoding='utf8') as obj_cm:
            creationModeInventoryDict = json.load(obj_cm)
        cmState = {}
        currList = []
        currType = creationModeInventoryDict['pages'][0]['page_name'].rsplit('_')[0]
        for type in creationModeInventoryDict['pages']:
            if type['page_name'].startswith(currType):
                for page in type['blocks']:
                    for item in page:
                        currList.append(item.rsplit('::')[1])
            else:
                currList.clear()
                currType = type['page_name'].rsplit('_')[0]
                for page in type['blocks']:
                    for item in page:
                        currList.append(item.rsplit('::')[1])
            cmState[currType] = list(currList)

        return cmState

    @staticmethod
    def addObjectInCreationModeInventory(cmState, name, type):
        currList = cmState[type]
        if name not in currList:
            currList.append(name)
        cmState[type] = currList

    @staticmethod
    def deleteObjectFromCreationModeInventory(cmState, selectedNames, type):
        currList = cmState[type]
        for item in selectedNames:
            if item in currList:
                currList.remove(item)
        cmState[type] = currList

    @staticmethod
    def isExistsInCreationModeInventory(cmState, name, type):
        if name in cmState[type]:
            return True
        else:
            return False

    @staticmethod
    def updateCreationModeInventoryFile(cmState, pathToCreationModeInventory):
        dictToDump = {}
        pages = []
        for type in cmState:
            print(type)
            pageNumber = 1
            typeObj = {}
            pageWithBlocks = []
            blocks = []
            for item in cmState[type]:
                if len(blocks) < 15:
                    blocks.append(type + '::' + item)
                    if item == cmState[type][-1]:
                        typeObj['page_name'] = type + '_' + str(pageNumber)
                        if type == 'blocks':
                            typeObj['description'] = 'Only Blocks Here'
                        elif type == 'particles':
                            typeObj['description'] = 'Only Particles Here'
                        elif type == 'objects':
                            typeObj['description'] = 'Only Interactive Objects'
                        pageWithBlocks.append(list(blocks))
                        blocks.clear()
                        typeObj['blocks'] = list(pageWithBlocks)
                        pageWithBlocks.clear()
                        pages.append(dict(typeObj))
                        typeObj.clear()

                else:
                    if item == cmState[type][-1]:
                        print(item)
                        if len(pageWithBlocks) < 8:
                            pageWithBlocks.append(list(blocks))
                            blocks.clear()

                        if len(pageWithBlocks) >= 8:
                            print('yes')
                            typeObj['page_name'] = type + '_' + str(pageNumber)
                            if type == 'blocks':
                                typeObj['description'] = 'Only Blocks Here'
                            elif type == 'particles':
                                typeObj['description'] = 'Only Particles Here'
                            elif type == 'objects':
                                typeObj['description'] = 'Only Interactive Objects'
                            typeObj['blocks'] = list(pageWithBlocks)
                            print(typeObj)

                            pages.append(dict(typeObj))
                            pageNumber += 1
                            blocks.clear()
                            pageWithBlocks.clear()
                            typeObj.clear()

                        blocks.append(type + '::' + item)

                        typeObj['page_name'] = type + '_' + str(pageNumber)
                        if type == 'blocks':
                            typeObj['description'] = 'Only Blocks Here'
                        elif type == 'particles':
                            typeObj['description'] = 'Only Particles Here'
                        elif type == 'objects':
                            typeObj['description'] = 'Only Interactive Objects'
                        pageWithBlocks.append(list(blocks))
                        blocks.clear()
                        typeObj['blocks'] = list(pageWithBlocks)
                        pageWithBlocks.clear()
                        pages.append(dict(typeObj))
                        typeObj.clear()

                    elif len(pageWithBlocks) < 8:
                        pageWithBlocks.append(list(blocks))
                        blocks.clear()
                        if len(pageWithBlocks) >= 8:
                            typeObj['page_name'] = type + '_' + str(pageNumber)
                            if type == 'blocks':
                                typeObj['description'] = 'Only Blocks Here'
                            elif type == 'particles':
                                typeObj['description'] = 'Only Particles Here'
                            elif type == 'objects':
                                typeObj['description'] = 'Only Interactive Objects'
                            typeObj['blocks'] = list(pageWithBlocks)
                            print(typeObj)

                            pages.append(dict(typeObj))
                            pageNumber += 1
                            blocks.clear()
                            pageWithBlocks.clear()
                            typeObj.clear()
                        blocks.append(type + '::' + item)

                    else:
                        typeObj['page_name'] = type + '_' + str(pageNumber)
                        if type == 'blocks':
                            typeObj['description'] = 'Only Blocks Here'
                        elif type == 'particles':
                            typeObj['description'] = 'Only Particles Here'
                        elif type == 'objects':
                            typeObj['description'] = 'Only Interactive Objects'
                        typeObj['blocks'] = list(pageWithBlocks)
                        print(typeObj)

                        pages.append(dict(typeObj))
                        pageNumber += 1
                        blocks.clear()
                        pageWithBlocks.clear()
                        typeObj.clear()
                        blocks.append(type + '::' + item)

        dictToDump['pages'] = pages
        with open(pathToCreationModeInventory, 'w', encoding='utf8') as obj_cm:
            json.dump(dictToDump, obj_cm, indent=3, ensure_ascii=False, separators=(',', ': '))

    @staticmethod
    def setFontSizeHead(app):
        screen_rect = app.desktop().screenGeometry()
        w = screen_rect.width()
        size = w // 76
        return size

    @staticmethod
    def setFontSizeCaption(app):
        screen_rect = app.desktop().screenGeometry()
        w = screen_rect.width()
        size = w // 150
        return size







