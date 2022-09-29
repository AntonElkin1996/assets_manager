import os

class Paths():
    workingDirPath = ''

    bundles = os.path.join(workingDirPath, 'bundles')
    icons = os.path.join(workingDirPath, 'icons')
    objectsDb = os.path.join(workingDirPath, 'ObjectsPrototypes.json')
    tools = os.path.join(os.getcwd(), 'tools')
    assets = workingDirPath
    audio = os.path.join(workingDirPath, 'audio')
    particles = os.path.join(workingDirPath, 'particles')
    creationModeInventory = os.path.join(workingDirPath, 'CreationModeInventory.json')
    blocksDb = os.path.join(workingDirPath, 'CubePrototypes.json')
    template = os.path.join(os.getcwd(), 'template')
    world = os.path.join(workingDirPath, 'world')
    artWorkspace = os.path.join(os.getcwd(), 'Art_workspace')
    textures = os.path.join(workingDirPath, 'textures')

    @staticmethod
    def getDir(dirName):
        if dirName == 'Release':
            Paths.workingDirPath = os.path.join(os.getcwd(), dirName, 'assets')
        else:
            Paths.workingDirPath = os.path.join(os.getcwd(), 'Art_workspace', dirName, 'assets')

        Paths.bundles = os.path.join(Paths.workingDirPath, 'bundles')
        Paths.icons = os.path.join(Paths.workingDirPath, 'icons')
        Paths.objectsDb = os.path.join(Paths.workingDirPath, 'ObjectsPrototypes.json')
        Paths.assets = Paths.workingDirPath
        Paths.audio = os.path.join(Paths.workingDirPath, 'audio')
        Paths.particles = os.path.join(Paths.workingDirPath, 'particles')
        Paths.creationModeInventory = os.path.join(Paths.workingDirPath, 'CreationModeInventory.json')
        Paths.blocksDb = os.path.join(Paths.workingDirPath, 'CubePrototypes.json')
        Paths.world = os.path.join(Paths.workingDirPath, 'world')
        Paths.textures = os.path.join(Paths.workingDirPath, 'textures')
