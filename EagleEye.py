from ansible.module_utils.basic import *
import sys
import os

#crawl directory and bring all directory after excluding some of them

def crawlDirectory(directory,exclude_list):
    dirs=os.listdir(directory)
    for i in exclude_list:
        if i not in dirs:
            return -1
        dirs.remove(i)
    return dirs
#return list of vars from specific file from different directory
def fetchVarsFromFile(file,directory,exclude_list):
    cleanedReaders={}
    obj={}
    readers={}
    directory_list=crawlDirectory(directory,exclude_list)
    #open all files
    for dir in directory_list:
        path=directory+"/"+dir+"/"+file
        with open(path) as f:
           reader =f.readlines()
           obj[directory+"/"+dir+"/"+file]=reader
           readers.update(obj)
        obj={}

    for key,values in readers.items():
        cleanedReaders[key]=[]
        for value in values:
            if len(value.split())>0:
                if value.split()[0]=="-":
                   cleanedReaders[key].append(value.split()[1])
                if value.split()[0][-1]==":":
                   cleanedReaders[key].append(value.split()[0])

    return cleanedReaders

#with given a list of filename as key and  vars as values this#function return a list of conflict in each file
def checkConflicts(filesVariables):

     conflicts={}
     listOfKeys=list(filesVariables)
     lenght=len(filesVariables)
     index=0
     for key,values in filesVariables.items():
         conflicts[key]={}
     for  i  in range(0,lenght):
           for j in range(0,lenght):
               if(i==j):
                   continue
               for src in filesVariables[listOfKeys[i]]:
                   exist=False
                   for ref in filesVariables[listOfKeys[j]]:
                           if  src == ref:
                               exist=True
                               break

                   if exist==False:
                        pattern=src+"found in"+listOfKeys[i]+"but not found in"+listOfKeys[j]
                        if listOfKeys[i] not in conflicts[listOfKeys[j]].keys():
                            conflicts[listOfKeys[j]][listOfKeys[i]]=[]
                        conflicts[listOfKeys[j]][listOfKeys[i]].append(src)
     return conflicts












def main():
    module=AnsibleModule(
      argument_spec=dict(
        folder =dict(required=True, type='str'),
        exclude=dict(required=True, type='list'),
        file=dict(required=True, type='str'),

      )
    )


    #declare vars here
    folder=module.params.get('folder')
    exclude=module.params.get('exclude')
    file=module.params.get('file')
    filesVariables={}
    #end variable declaration

    filesVariables=fetchVarsFromFile(file,folder,exclude)
    conflicts=checkConflicts(filesVariables)
    # improving the display
    for key,value in conflicts.items():
       splittedPath=key.split("/")
       new_key="base ==>" + splittedPath[-2]+"/"+splittedPath[-1]
       conflicts[new_key]=conflicts.pop(key)
       for key2 ,value2 in value.items():
          splittedPath2=key2.split("/")
          new_key2=" ref ==>" + splittedPath2[-2]+"/"+splittedPath2[-1]
          value[new_key2]=value.pop(key2)
          index=0
          for i  in range(len(value2)):
              value2[i]="+ " +value2[i]







    result=dict(
      changed=False,
      conflicts=conflicts,

    )

    module.exit_json(**result)













if __name__== '__main__':
  main()
