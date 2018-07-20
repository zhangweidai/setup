import bpy
import utils
from utils import printf
import os
global cache, mode
from pathlib import Path
from shutil import copyfile
currentPath = None
materialTemplate = "wood05"

category = dict()
category["plaster"] = "textures"
category["marble"] = "textures"
category["stone"] = "rock"
category["metal"] = "metal"
category["road"] = "rock"
category["wood"] = "wood"
category["wall"] = "rock"

def categoryMapping(name):
    for b in category.keys():
        if b in name.lower():
            return category[b]
    return ""


def iterateTexturePaths():
    for root, dirs, filenames in os.walk(utils.texturesPath):
        name = os.path.basename(root)
        for kth in dirs:
            fromPath_K = str(root + "\\" + kth)
            if (kth == "4K" or kth == "3K" or kth == "6K"):
                saveFor(fromPath_K, name, root, kth) 

def getFromFolder(fromPath_K, lookingFor):
    retPath = ""
    for root, dirs, filenames in os.walk(fromPath_K):
        for f in filenames:
            if lookingFor in f.lower():
                retPath = root + "/" + str(f)
                #utils.printf("Found for " + retPath)
                return retPath
    return retPath

hasRough_ = 1
def getImageReplacement(filepath, fromPath_K):
    global hasRough_
#     utils.printf("Need replacement for " + filepath + " from " + fromPath_K)
    l_filepath = filepath.lower()
    lookingFor = ""
    if "_nrm" in l_filepath:
        lookingFor = "nrm"
    elif "_col" in l_filepath:
        lookingFor = "col"
    elif "_gloss" in l_filepath:
        lookingFor = "gloss"
        hasRough_ = 1
    elif "_roughness" in l_filepath:
        lookingFor = "gloss"
        hasRough_ = 1
    else:
        return ""

    retPath = getFromFolder(fromPath_K, lookingFor)
    if retPath != "":
        return retPath

    if lookingFor == "gloss":
        retPath = getFromFolder(fromPath_K, "roughness")
        if retPath != "":
            hasRough_ = 0

    if retPath != "":
        return retPath

    utils.printf("NOT FOUND for " + lookingFor)
    return ""


def treeHelper(fromPath_K, nodeTree):
    global foundAll
    for node in nodeTree.nodes:
        if "Image Texture" in node.name:
            purpose = str(node.image.filepath)
            replacement = getImageReplacement(purpose, fromPath_K)
            if not replacement:
                printf("No Image replacement for {}".format(purpose))
                foundAll = False
            else:
                node.image.filepath = replacement
        if node.name == "Group":
            treeHelper(fromPath_K, node.node_tree)

def copyPreview(rootTextPath, dirname, kth):
    prevFile = None
    for root, dirs, filenames in os.walk(rootTextPath):
        for f in filenames:
            if "sphere.jpg" in f.lower():
#                 printf("Preview is " + f)
                prevFile = str(root + "\\" + f)

    if not prevFile:
        printf("Could not find preview")
        return

    cat = categoryMapping(dirname)
    if not cat:
        print("Could not determine category")
        return

    destination = "{}/{}/{}_{}.jpg".format(utils.dynaPath, cat, dirname, kth)
    copyfile(prevFile, destination)
#     bpy.ops.wm.save_as_mainfile(filepath=destination)

foundAll = None
def saveFor(fromPath_K, dirname, rootTextPath, kth):
    global foundAll
    foundAll = True
    iterateBase(fromPath_K, dirname, kth)
    if not foundAll:
        return
    copyPreview(rootTextPath, dirname, kth)
    bpy.ops.wm.save_as_mainfile(filepath="{}/{}_{}.blend".format(utils.dynaPath, dirname, kth), copy=True)

def updateInverter(nodeTree):
    for node in nodeTree.nodes:
        if "GlossInverter" in node.name:
            node.inputs[0].default_value = hasRough_
            break
   

def iterateBase(fromPath_K, dirname, kth):
    global materialTemplate
    M = bpy.data.materials
    mat = M.get(materialTemplate)
    if not mat:
        print("Could not find")
        return
    treeHelper(fromPath_K, mat.node_tree)
    updateInverter(mat.node_tree) 

    materialTemplate = dirname + "_" +  kth
    printf("Processed " + materialTemplate)
    mat.name = materialTemplate

printf("start", start = True, done = True) 
iterateTexturePaths()
printf("end", done = True) 
