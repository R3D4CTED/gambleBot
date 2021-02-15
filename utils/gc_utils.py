import sys
import os
import io
from contextlib import redirect_stdout
import subprocess



text_file = open("rc.conf", "w")
text_file.write("[GC]\ntype = drive\nscope = drive\nservice_account_file = accounts/1.json\nservice_account_file_path = accounts/")
text_file.close()


SRflag = ("--transfers 50 -v --stats-one-line --stats=15s --ignore-existing --drive-server-side-across-configs --drive-chunk-size 128M --drive-acknowledge-abuse --drive-keep-revision-forever")
vrflag = ('--verbose=2')
rmflag = ('--drive-use-trash=true --verbose=2 --fast-list')

if os.path.isdir('.\\accounts'):
  print('Accounts folder found.')

else:
  print("Account folder containing SA's JSON not found")
  exit()

#print('Choose what you like to do')  
#MD = input("A.Copy\nB.Move\nC.Sync\nD.Dedupes\nE.RemoveDirs\nF.Size\nG.Dir listing\nNOTE:Read Rclone Documentations for more info on these operations\nOperation(Chose either A/B/C/D/E/F/G): ")
MD = 'Z'
def command_line_output():
  """ To read all the output from command line and return. """


def copy(src_id, dest_id):
  cmd = (f'gclone --config=rc.conf copy GC:{{{src_id}}} GC:{{{dest_id}}} {SRflag}')
  output = str(subprocess.run(cmd, capture_output=True).stderr)
  return output



if MD == "B":
  print("Move Selected\nIt will MOVE content from SRC to DST\n")
  SRC = input("Provide SRC Folder ID\n")
  DST = input("Provide DST Folder ID\n")
  cmd = ('gclone --config=rc.conf move GC:{'+SRC+'} GC:{'+DST+'} '+SRflag)
  os.system(cmd)

elif MD == "C":
  print("Sync Selected\nIt will Sync content of SRC to DST (it will delete any extra files that are there only in DST use it with caution)\n")
  SRC = input("Provide SRC Folder ID\n")
  DST = input("Provide DST Folder ID\n")
  cmd = ('gclone --config=rc.conf sync GC:{'+SRC+'} GC:{'+DST+'} '+SRflag)
  os.system(cmd)

elif MD == "D":
  print("Dedupe selected\nIt will delete any duplicate files present in given Folder ID [it compares md5 and naming]\n")
  DP = input("select delete mode\nA.interactive\nB.newest\nC.oldest\nD.largest\nE.smallest\n")
  SRC = input("Provide Folder ID\n")
  if DP == "A":
     print("Interactive Mode selected\n")
     cmd = ('gclone --config=rc.conf dedupe --dedupe-mode interactive GC:{'+SRC+'} '+vrflag)
     os.system(cmd)
  elif DP == 'B':
     print('Newest Mode selected\n')
     cmd = ('gclone --config=rc.conf dedupe --dedupe-mode newest GC:{'+SRC+'} '+vrflag)
     os.system(cmd)   
  elif DP == 'C':
     print('Oldest Mode selected\n')
     cmd = ('gclone --config=rc.conf dedupe --dedupe-mode oldest GC:{'+SRC+'} '+vrflag)
     os.system(cmd)
  elif DP == 'D':
     print('Largest Mode selected\n')
     cmd = ('gclone --config=rc.conf dedupe --dedupe-mode largest GC:{'+SRC+'} '+vrflag)
     os.system(cmd)
  elif DP == 'E':
     print('smallest Mode selected\n')
     cmd = ('gclone --config=rc.conf dedupe --dedupe-mode smallest GC:{'+SRC+'} '+vrflag)
     os.system(cmd)     

elif MD == "E":
  print("RemoveDirs Selected\nRemoves Empty Directory From the given Folder ID\n")
  SRC = input("Provide Folder ID\n") 
  cmd = ('gclone --config=rc.conf rmdirs GC:{'+SRC+'} '+rmflag)
  os.system(cmd)

elif MD == "F":
  print("Size selected\nIt will give the Size of the folder ID\n")
  SRC = input("Provide Folder ID\n") 
  cmd = ('rclone --config=rc.conf size GC:{'+SRC+'} ')
  os.system(cmd)

elif MD == "G":
  print("Directory Listing\nIt will list the content of the give folder ID into text named file.txt\n")
  if os.path.isfile('file.txt'):
    os.remove("file.txt")
    print("File.txt Removed!")
  SRC = input("Provide Folder ID\n") 
  cmd = ('gclone --config=rc.conf ls GC:{'+SRC+'} >> file.txt')  
  os.system(cmd)  

else :
  print ("ERROR!!!\n")