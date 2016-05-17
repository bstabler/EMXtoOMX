
#Read and write OMX matrices from/to the databank
#Ben Stabler, ben.stabler@rsginc.com, 05/06/16
#Can export mfs, mos, and mds, but only one type at a time
#Arguments: emme_project scenario omx_file_name -i|e mat1 mat2 matN
#SET EMMEPY="C:\Program Files\INRO\Emme\Emme 4\Emme-4.2.5\Python27\python.exe"
#Example export: %EMMEPY% EMXtoOMX.py myproj.emp 9999 mats.omx -e mf1 mf2 mf3
#Example import: %EMMEPY% EMXtoOMX.py myproj.emp 9999 mats.omx -i mf1 mf2 mf3
######################################################################

#load libraries
import inro.modeller as m
import inro.emme.desktop.app as d
import sys, os.path, os, omx

#run command line version
if __name__ == "__main__":

    #start EMME desktop and attach a modeller session
    empFile = sys.argv[1]
    scenarioNum = sys.argv[2]
    omxFile = sys.argv[3]
    ioMode = sys.argv[4]
    desktop = d.start_dedicated(False, "bts", empFile)
    m = m.Modeller(desktop)
    
    #determine if import or export mode
    if ioMode == "-e":
        export = True
    else:
        export = False

    #get location of bank
    bankDir = os.path.dirname(m.emmebank.path)
    omx_file = os.path.join(bankDir, "emmemat", omxFile)

    #get matrix names from command line argument
    mats = []
    for i in range(5,len(sys.argv)):
        mats.append(sys.argv[i])

    #export matrices
    if export:
      
      export_to_omx = m.tool("inro.emme.data.matrix.export_to_omx")
      export_to_omx(mats, omx_file)
      
      #remove appended names so mat names are just numbers
      exportByNumber = True
      if exportByNumber:
        omxFile = omx.openFile(omx_file,"a")
        matNames = omxFile.listMatrices()
        matsLookup = dict(map(lambda x: x.split("_"), matNames))
        for i in range(len(matsLookup.keys())):
            omxFile[matsLookup.keys()[i]] = omxFile[matNames[i]]
            del omxFile[matNames[i]]
        omxFile.close()
      print(",".join(mats) + " -> " + omx_file)

    #else import
    else:

      #map matrix names in file to matrix numbers in bank if needed
      matNames = omx.openFile(omx_file).listMatrices()
      if "_" in matNames[0]:
        matsLookup = dict(map(lambda x: x.split("_"), matNames))
        matsDict = {}
        for aMat in mats:
          if aMat in matsLookup.keys():
            matsDict[aMat + "_" + matsLookup[aMat]] = aMat
      else:
        matsDict = dict(zip(matNames, matNames))
        
      #import matrices
      import_from_omx = m.tool("inro.emme.data.matrix.import_from_omx")
      scen = m.emmebank.scenario(scenarioNum)
      import_from_omx(omx_file, matsDict, 'zone_number', scen)
      print(omx_file + " -> " + ",".join(mats))
      