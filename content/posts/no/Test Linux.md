---
title:
date: 2025-01-01
image:
categories:
tags:
draft: true
---
<!--more-->

---
### **Phần 1: Linux Commands**

**1. What does the 'pwd' command do?**
*   [a] Lists the current directory
*   [b] Changes the current directory
*   [c] Prints the working directory
*   [d] Create new directory

**2. Which command is used to create a new directory?**
*   [a] touch
*   [b] mkfile
*   [c] mkdir
*   [d] cdir

**3. What command is used to move up one directory level?**
*   [a] cd ..
*   [b] cd ~
*   [c] cd /
*   [d] cd -

**4. Which command is used to remove an empty directory?**
*   [a] del
*   [b] rdir
*   [c] rmdir
*   [d] rm -r

**5. What command is used to copy files?**
*   [a] cpy
*   [b] mv
*   [c] cp
*   [d] dup

**6. Which command is used to rename or move files and directories?**
*   [a] rn
*   [b] cp
*   [c] mpv
*   [d] mv

**7. What is the command to view the contents of a file?**
*   [a] type
*   [b] cat
*   [c] show
*   [d] file

**8. Which command is used to create a new file?**
*   [a] mkfile
*   [b] create
*   [c] touch
*   [d] new

**9. What is the command to search for files?**
*   [a] search
*   [b] grep
*   [c] find
*   [d] locate

**10. Which command shows the amount of free space on filesystems?**
*   [a] free
*   [b] fdisk
*   [c] df
*   [d] du

**11. What command is used to show disk usage of files and directories?**
*   [a] diskuse
*   [b] df
*   [c] du
*   [d] diskinfo

**12. Which command is used to change file permissions?**
*   [a] permit
*   [b] chown
*   [c] chmod
*   [d] chperm

**13. What does the 'whoami' command do?**
*   [a] Shows current user
*   [b] Lists all users
*   [c] Shows user info
*   [d] Prints user ID

**14. Which command is used to view processes?**
*   [a] ps
*   [b] proc
*   [c] top
*   [d] procs

**15. What does the 'tee' command do?**
*   [a] Reads stdin and writes to stdout and files
*   [b] Sorts two files
*   [c] Merges two files
*   [d] Splits a file into two

**16. Which command is used to substitute characters in a text stream?**
*   [a] sub
*   [b] swap
*   [c] tr
*   [d] replace

**17. What is the difference between these operators '>' and '>>'?**
*   [a] '>' overwrites, '>>' appends
*   [b] '>>' overwrites, '>' appends
*   [c] '>' redirects stderr, '>>' redirects stdout
*   [d] No difference

**18. Which option of 'ls' command shows file permissions?**
*   [a] -p
*   [b] -a
*   [c] -f
*   [d] -l

**19. What is the purpose of the '/etc/passwd' file?**
*   [a] Stores user passwords
*   [b] Stores group information
*   [c] Stores user account information
*   [d] Stores system settings

**20. Which command is used to edit the crontab file?**
*   [a] crontab -e
*   [b] edit crontab
*   [c] vi crontab
*   [d] crontab -vi

---

### **Phần 2: Advanced Linux & Scripting Scenarios**

**21. Liam needs to find all files in the /var/log directory and its subdirectories that have been modified within the last 7 days. He wants to copy these files to a backup directory. Which command combination should he use to accomplish this task?**
*   [a] `find /var/log -type f -mtime -7 -exec cp {} /backup/ \;`
*   [b] `find /var/log -type f -mdays -7 | xargs cp -t /backup/`
*   [c] `find /var/log -type f -ctime -7 -exec mv {} /backup/ ;`
*   [d] `find /var/log -type f -atime -7 | xargs mv -t /backup/`

**22. Sophia is analyzing a log file that contains various types of entries. She wants to extract all lines that match the pattern "ERROR" followed by a timestamp in the format "YYYY-MM-DD HH:MM:SS" and save them to a separate file named errors.log. Which command should she use?**
*   [a] `grep "ERROR \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}" logfile.txt > errors.log`
*   [b] `sed -n '/ERROR \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/p' logfile.txt > errors.log`
*   [c] `awk '/ERROR \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/' logfile.txt > errors.log`
*   [d] `grep "ERROR [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}" logfile.txt > errors.log`

**23. Ethan is troubleshooting a performance issue on a Linux server. He suspects that a process is consuming excessive CPU resources. Which command should he use to identify the top CPU-consuming processes in real-time, displaying the results in a readable format?**
*   [a] `ps aux --sort=-%cpu | head`
*   [b] `top -b -n 1 -o %CPU`
*   [c] `htop --sort-key CPU% --delay=1`
*   [d] `pidstat -u -p ALL -r 1`

**24. Olivia needs to find all occurrences of a specific IP address (192.168.1.100) in a large log file (access.log) and replace them with the string "REDACTED_IP". She wants to perform this operation in-place, modifying the original file. Which sed command should she use?**
*   [a] `sed -i 's/192.168.1.100/REDACTED_IP/g' access.log`
*   [b] `sed -i '/192.168.1.100/d' access.log`
*   [c] `sed -i 's/REDACTED_IP/192.168.1.100/g' access.log`
*   [d] `sed -i '/192.168.1.100/REDACTED_IP/g' access.log`

**25. Noah is setting up a cronjob to backup a specific directory (/data) every day at midnight. He wants to ensure that the backup script runs with root privileges and redirects both standard output and standard error to a log file (/var/log/backup.log). Which crontab entry should he use?**
*   [a] `0 0 * * * /path/to/backup.sh /data &> /var/log/backup.log`
*   [b] `@daily root /path/to/backup.sh /data > /var/log/backup.log 2>&1 G28`
*   [c] `0 0 * * * root /path/to/backup.sh /data >> /var/log/backup.log 2>&1`
*   [d] `@midnight /path/to/backup.sh /data &> /var/log/backup.log`

**26. Emma is investigating a security breach on a Linux server. She suspects that an attacker may have modified some system files. To identify any files that have been modified within the last 24 hours, excluding directories, she wants to use the find command with the appropriate options and save the output to a file named modified_files.txt. Which command should she execute?**
*   [a] `find / -type f -mtime -1 > modified_files.txt`
*   [b] `find / -type f -ctime -1 -print0 | xargs -0 ls -l > modified_files.txt`
*   [c] `find / -type f -mtime -1 -ls | grep -v "^d" > modified_files.txt`
*   [d] `find / -type f -mtime -1 -exec ls -l {}; | tee modified_files.txt`

**27. Daniel is analyzing a large log file (server.log) that contains timestamps in various formats. He needs to extract all lines where the timestamp matches the format "[YYYY-MM-DD HH:MM:SS]" and the log level is either "ERROR" or "CRITICAL". He wants to store the extracted lines in a new file named filtered_logs.txt while preserving the original log file. Which command should he use?**
*   [a] `grep -E '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.*(ERROR|CRITICAL)' server.log > filtered_logs.txt`
*   [b] `sed -n '/[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}].*(ERROR|CRITICAL)/p' server.log > filtered_logs.txt`
*   [c] `awk '/[[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}]/ && /ERROR|CRITICAL/' server.log > filtered_logs.txt`
*   [d] `perl -ne 'print if /\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]/ && /ERROR|CRITICAL/' server.log > filtered_logs.txt`

**28. Natalie needs to monitor the disk space usage of a specific directory (/var/log) on a Linux server. She wants to receive an email alert whenever the disk space usage exceeds 90%. The email should be sent to admin@example.com with the subject "Disk Space Alert" and the body containing the output of the df command for the /var/log directory. Which script should she use to accomplish this task?**
*   [a]
    ```bash
    while true; do
    if [ $(df -h /var/log | awk 'NR==2 {print $5}' | cut -d'%' -f1) -gt 90 ]; then
    df -h /var/log | mail -s "Disk Space Alert" admin@example.com
    fi
    sleep 300
    done
    ```
*   [b]
    ```bash
    while true; do
    used_space=$(df -h /var/log | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    if [ $used_space -gt 90 ]; then
    echo "Disk space usage for /var/log exceeds 90%." | mail -s "Disk Space Alert" admin@example.com
    fi
    sleep 5m
    done
    ```
*   [c]
    ```bash
    while true; do
    used_space=$(du -sh /var/log | awk '{print $1}' | cut -d'%' -f1)
    if [ $used_space -gt 90 ]; then
    du -sh /var/log | mail -s "Disk Space Alert" admin@example.com
    fi
    sleep 300
    done
    ```
*   [d]
    ```bash
    while true; do
    if [ $(df -h /var/log | awk 'NR==2 {print $5}' | cut -d'%' -f1) -gt 90 ]; then
    echo "Disk space usage for /var/log exceeds 90%." | mail -s "Disk Space Alert" admin@example.com
    fi
    sleep 5m
    done
    ```

**29. Michael is troubleshooting a network issue on a Linux server. He wants to identify all active network connections and their corresponding processes. Additionally, he needs to sort the output based on the number of connections per process in descending order. Which command combination should he use?**
*   [a] `netstat -tunapl | awk '{print $7}' | cut -d'/' -f1 | sort | uniq -c | sort -nr`
*   [b] `ss -tunapl | awk '{print $NF}' | cut -d':' -f2 | sort | uniq -c | sort -nr`
*   [c] `lsof -i -n -P | awk '{print $1}' | sort | uniq -c | sort -nr`
*   [d] `ps aux | awk '{print $11}' | cut -d'/' -f1 | sort | uniq -c | sort -nr`

**30. Sarah is managing a Git repository on a Linux server. She wants to create a bash script that automatically pushes any changes to the remote repository every hour. The script should navigate to the repository directory (/opt/myrepo), add all changes, commit with a timestamp, and push to the remote origin. If there are no changes, the script should not perform any actions. Which script should she create?**
*   [a]
    ```bash
    #!/bin/bash
    cd /opt/myrepo
    if ! git diff-index --quiet HEAD --; then
    git add .
    git commit -m "Automatic commit at $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin master
    fi
    ```
*   [b]
    ```bash
    #!/bin/bash
    cd /opt/myrepo
    git add .
    git commit -m "Automatic commit at $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin master
    ```
*   [c]
    ```bash
    #!/bin/bash
    if [ "$(git status -s)" ]; then
    cd /opt/myrepo
    git add .
    git commit -m "Automatic commit at $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin master
    fi
    ```
*   [d]
    ```bash
    #!/bin/bash
    cd /opt/myrepo
    if [ -n "$(git status --porcelain)" ]; then
    git add .
    git commit -m "Automatic commit at $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin master
    fi
    ```

---

### **Phần 3: Ansible**

**31. What is the default inventory file used by Ansible?**
*   [a] ansible.cfg
*   [b] /etc/ansible/hosts
*   [c] inventory.yml
*   [d] ansible.ini

**32. Which of the following is NOT a valid Ansible module?**
*   [a] copy
*   [b] file
*   [c] apt
*   [d] sudo

**33. You have a playbook named "webserver.yml" that configures a web server. Which command would you use to run the playbook with verbose output?**
*   [a] `ansible-playbook webserver.yml -v`
*   [b] `ansible-playbook -v webserver.yml`
*   [c] `ansible-playbook --verbose webserver.yml`
*   [d] `ansible-playbook webserver.yml -verbose`

**34. You need to create a reusable task that can be included in multiple playbooks. The task should install a list of packages defined in a variable named "required_packages". Which of the following would be the correct way to define this reusable task?**
*   [a]
    ```yaml
    - name: Install required packages
      apt:
        name: "{{ item }}"
        state: present
      loop: "{{ required_packages }}"
    ```
*   [b]
    ```yaml
    - name: Install required packages
      apt:
        name: "{{ required_packages }}"
        state: present
    ```
*   [c]
    ```yaml
    - name: Install required packages
      apt:
        name:
          - "{{ required_packages }}"
        state: present
    ```
*   [d]
    ```yaml
    - name: Install required packages
      apt:
        name: "{{ required_packages }}"
        state: present
      with_items: "{{ required_packages }}"
    ```

**35. You have a playbook that needs to execute a command on a remote server and capture its output. The command is stored in a variable named "remote_command". You want to store the output in a variable named "command_output" and display it using the debug module. Which of the following playbook snippets would accomplish this?**
*   [a]
    ```yaml
    - name: Execute command and capture output
      command: "{{ remote_command }}"
      register: command_output
    - name: Display command output
      debug:
        var: command_output
    ```
*   [b]
    ```yaml
    - name: Execute command and capture output
      shell: "{{ remote_command }}"
      register: command_output
    - name: Display command output
      debug:
        var: command_output.stdout
    ```
*   [c]
    ```yaml
    - name: Execute command and capture output
      command: "{{ remote_command }}"
      register: result
    - name: Display command output
      debug:
        var: result.stdout
    ```
*   [d]
    ```yaml
    - name: Execute command and capture output
      shell: "{{ remote_command }}"
      register: result
    - name: Display command output
      debug:
        msg: "{{ result.stdout }}"
    ```

---

### **Phần 4: Terraform**

**36. What is the purpose of the "terraform init" command?**
*   [a] To create a new Terraform configuration file
*   [b] To initialize a new Terraform working directory
*   [c] To apply the changes defined in the Terraform configuration
*   [d] To destroy the resources created by Terraform

**37. Which of the following is the correct file extension for a Terraform configuration file?**
*   [a] .tf
*   [b] .yaml
*   [c] .json
*   [d] .config

**38. What is the purpose of the "terraform plan" command?**
*   [a] To create a new Terraform module
*   [b] To initialize the Terraform working directory
*   [c] To generate an execution plan without applying changes
*   [d] To apply the changes defined in the Terraform configuration

**39. Which of the following is the correct syntax to define a variable in Terraform?**
*   [a] `variable "instance_type" = "t2.micro"`
*   [b]
    ```hcl
    variable "instance_type" {
      default = "t2.micro"
    }
    ```
*   [c] `var instance_type = "t2.micro"`
*   [d]
    ```hcl
    var "instance_type" {
      value = "t2.micro"
    }
    ```

**40. What is the purpose of the "terraform apply" command?**
*   [a] To create a new Terraform resource
*   [b] To generate an execution plan without applying changes
*   [c] To apply the changes defined in the Terraform configuration
*   [d] To destroy the resources created by Terraform

**41. Which of the following is the correct syntax to define a data source in Terraform?**
*   [a]
    ```hcl
    data "aws_ami" "example" {
      most_recent = true
      owners      = ["self"]
    }
    ```
*   [b]
    ```hcl
    resource "aws_ami" "example" {
      most_recent = true
      owners      = ["self"]
    }
    ```
*   [c]
    ```hcl
    module "aws_ami" "example" {
      most_recent = true
      owners      = ["self"]
    }
    ```
*   [d]
    ```hcl
    provider "aws_ami" "example" {
      most_recent = true
      owners      = ["self"]
    }
    ```

**42. What is the purpose of the "terraform state" command?**
*   [a] To manage the state of Terraform resources
*   [b] To import existing resources into Terraform state
*   [c] To export the Terraform state to a remote backend
*   [d] To view the current Terraform state

**43. Which of the following is the correct syntax to define a module in Terraform?**
*   [a]
    ```hcl
    module "example" {
      source = "./modules/example"
      name   = "example-instance"
    }
    ```
*   [b]
    ```hcl
    resource "module" "example" {
      source = "./modules/example"
      name   = "example-instance"
    }
    ```
*   [c]
    ```hcl
    data "module" "example" {
      source = "./modules/example"
      name   = "example-instance"
    }
    ```
*   [d]
    ```hcl
    provider "module" "example" {
      source = "./modules/example"
      name   = "example-instance"
    }
    ```

**44. What is the purpose of the "terraform workspace" command?**
*   [a] To create a new Terraform configuration file
*   [b] To manage multiple environments within a single Terraform configuration
*   [c] To initialize a new Terraform working directory
*   [d] To view the current Terraform state

**45. Which of the following is the correct syntax to define a conditional expression in Terraform?**
*   [a] `if var.instance_count > 1 then [aws_instance.example[0].id] else []`
*   [b] `if (var.instance_count > 1) ? [aws_instance.example[0].id] : []`
*   [c] `var.instance_count > 1 ? [aws_instance.example[0].id] : []`
*   [d]
    ```hcl
    if (var.instance_count > 1) {
      [aws_instance.example[0].id]
    } else { [] }
    ```

---

### **Phần 5: Git**

**46. What command is used to initialize a new Git repository?**
*   [a] git init
*   [b] git start
*   [c] git new
*   [d] git create

**47. Which command is used to view the commit history of a Git repository?**
*   [a] git history
*   [b] git commit
*   [c] git log
*   [d] git list

**48. What is the purpose of the "git stash" command?**
*   [a] To permanently delete uncommitted changes
*   [b] To temporarily save uncommitted changes
*   [c] To create a new branch
*   [d] To merge branches

**49. Which command is used to rebase the current branch onto another branch?**
*   [a] git rebase [branch]
*   [b] git merge [branch]
*   [c] git reset [branch]
*   [d] git checkout [branch]

**50. What is the purpose of the "git reflog" command?**
*   [a] To view the commit history
*   [b] To view the branch hierarchy
*   [c] To view the stash list
*   [d] To view the reference log of all Git actions