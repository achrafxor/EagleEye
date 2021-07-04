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
    return cleanedReaders

#with given a list of filename as key and  vars as values this#function return a list of conflict in each file
def checkConflicts(filesVariables):
     #objective {"rcc":{"lab":["eureka","zipkin"]}}
     #           file    ref    confliiiiiiicts
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
    #folder=sys.argv[1]
    exclude_list=["lab","prp","prd","rci","rcc"]

    #end declaration section
    print("lfolder")
    print("exclude")
    print("file")




    filesVariables=fetchVarsFromFile(file,folder,exclude)
    conflicts=checkConflicts(filesVariables)
    #checkConflicts(filesVariables)
    result=dict(
      changed=False,
      conflicts=conflicts,
    )

    module.exit_json(**result)













if __name__== '__main__':
  main()
