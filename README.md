# EMXtoOMX

Read and write OMX matrices from/to the EMME databank. Can export mfs, mos, 
and mds, but only one type at a time.  Uses the active databank in the project 
or else the first databank.

Arguments: emme_project scenario omx_file_name -i|e mat1 mat2 matN

#Example usage

SET EMMEPY="C:\Program Files\INRO\Emme\Emme 4\Emme-4.2.5\Python27\python.exe"

### Example export
%EMMEPY% EMXtoOMX.py myproj.emp 9999 C:\projects\mats.omx -e mf1 mf2 mf3

### Example import
%EMMEPY% EMXtoOMX.py myproj.emp 9999 C:\projects\mats.omx -i mf1 mf2 mf3
