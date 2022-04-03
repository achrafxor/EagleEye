# EagleEye
## _best yaml multiple files comparateur ever_



EagleEye is multiple files yaml comparateur ansible module that shows  conflicts between multiple folders and files it is very useful for obtaining a good visibility when deploying in multiple environments.


## setup



```sh
clone repository
cd repository
touch ansible.cfg
add this code to ansible.cfg 
[defaults]
library= your path to EagleEye.py
```



## usage
```sh
this module accept three parameters 
folder: your path to your folder that may contains many subfolders
exclude: list of excluded folder that you dont want to use them
file: the file name which you will compare in each folder

```
## result
```sh
the module will return every conflict in each file from each folder and will return also the source of conflict

```



