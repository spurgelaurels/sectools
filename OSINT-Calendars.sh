#/bin/bash


while IFS= read -r user; do
  page_content=$(curl -s "https://calendar.google.com/calendar/u/0/embed?src=$user")
  
  
  if [[ $page_content == *"Moved Temporarily"* ]]; then
    echo -e "\e[32m$user calendar is not shared"
  else echo -e "\e[31m$user calendar is PUBLIC"
  fi


done < UserList.txt
