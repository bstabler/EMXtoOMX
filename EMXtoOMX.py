
#Read and write OMX matrices from/to the databank
#Ben Stabler, ben.stabler@rsginc.com, 05/06/16
#Can export mfs, mos, and mds, but only one type at a time and only all by number or by name
#Arguments: emme_project scenario omx_file_name -i|e mat1 mat2 matN
#SET EMMEPY="C:\Program Files\INRO\Emme\Emme 4\Emme-4.2.5\Python27\python.exe"
#Example export: %EMMEPY% EMXtoOMX.py New_Project.emp 3001 C:\projects\mats.omx -e mf1 mf2
#Example import: %EMMEPY% EMXtoOMX.py New_Project.emp 3001 C:\projects\mats.omx -i mf1 mf2
#Example export: %EMMEPY% EMXtoOMX.py New_Project.emp 3001 C:\projects\mats.omx -e mfsurvey mftime
#Example import: %EMMEPY% EMXtoOMX.py New_Project.emp 3001 C:\projects\mats.omx -i mfsurvey mftime
######################################################################

#load libraries
import inro.modeller as m
import inro.emme.desktop.app as d
import sys, os.path, os, omx

#run command line version
if __name__ == "__main__":

    #start EMME desktop 
    empFile = sys.argv[1]
    scenarioNum = sys.argv[2]
    omxFile = sys.argv[3]
    ioMode = sys.argv[4]
    desktop = d.start_dedicated(False, "bts", empFile)
    
    #open a database if needed and attach a modeller session
    if desktop.data_explorer().active_database() is None:
      desktop.data_explorer().databases()[0].open()
      print("open first project database: " + desktop.data_explorer().active_database().name())
    else:
      print("using active database: " + desktop.data_explorer().active_database().name())
    m = m.Modeller(desktop)
    
    #determine if import or export mode
    if ioMode == "-e":
        export = True
    else:
        export = False

    #get location of bank
    bankDir = os.path.dirname(m.emmebank.path)
    
    #assume full filename for omx
    omx_file = omxFile

    #get matrix names from command line argument
    mats = []
    for i in range(5,len(sys.argv)):
        mats.append(sys.argv[i])

    #determine if export by names or numbers
    if (mats[0][2].isdigit()):
      exportByNumber = True
    else:
      exportByNumber = False
      
    #export matrices
    if export:
      
      export_to_omx = m.tool("inro.emme.data.matrix.export_to_omx")
      export_to_omx(mats, omx_file)

      omxFile = omx.openFile(omx_file,"a")
      matNames = omxFile.listMatrices()
        
      #remove appended names so mat names are just numbers or just names
      if exportByNumber:
        matsLookup = dict(zip(map(lambda x: x.split("_")[0], matNames), matNames))
      else:
        matsLookup = dict(zip(map(lambda x: x.split("_")[1], matNames), matNames))

      for i in range(len(matsLookup.keys())):
          omxFile[matsLookup.keys()[i]] = omxFile[matsLookup.values()[i]]
          del omxFile[matsLookup.values()[i]]
      omxFile.close()
      print(",".join(mats) + " -> " + omx_file)

    #else import
    else:

      #map matrix names in file to matrix numbers in bank if needed
      matNames = omx.openFile(omx_file).listMatrices()
      
      if exportByNumber:
        
        if "_" in matNames[0]:
          matsLookup = dict(map(lambda x: x.split("_"), matNames))
          matsDict = {}
          for aMat in mats:
            if aMat in matsLookup.keys():
              matsDict[aMat + "_" + matsLookup[aMat]] = aMat
        else:
          matsDictAll = dict(zip(matNames, matNames))
          matsDict = {}
          for aMat in mats:
            if aMat in matsDictAll.keys():
              matsDict[aMat] = aMat
      
      else: 

        if "_" in matNames[0]:
          matsLookup = dict(map(lambda x: x.split("_"), matNames))
          matsLookup = dict((v,k) for k,v in matsLookup.iteritems()) #flip
          matsDict = {}
          for aMat in mats:
            if aMat in matsLookup.keys():
              matsDict[matsLookup[aMat] + "_" + aMat] = matsLookup[aMat]
        else:
          matsDictAll = dict(zip(matNames, matNames))
          matsDict = {}
          for aMat in mats:
            if aMat[2:] in matsDictAll.keys():
              matNum = None
              for possibleMat in m.emmebank.matrices(): #find matrix number, remove "mf"
                if possibleMat.name == aMat[2:]:
                  matNum = possibleMat.id
                  break
              if matNum is not None:
                matsDict[aMat[2:]] = matNum

      #import matrices
      import_from_omx = m.tool("inro.emme.data.matrix.import_from_omx")
      scen = m.emmebank.scenario(scenarioNum)
      import_from_omx(omx_file, matsDict, 'zone_number', scen)
      print(omx_file + " -> " + ",".join(mats))
      