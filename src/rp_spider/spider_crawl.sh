while true  
do  
  echo 'Running scheduled spider crawl (5 min intervals)...'
  sleep 300
  scrapy crawl anonme
  sleep 300
done