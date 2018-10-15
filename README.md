`only partially done: need to fill in gaps`

# info_scheming_web_app

sudo apt-get update
sudo apt-get install git

# following guide here

Setup Instance
Open up HTTP and HTTPS in Security Group

Create A Record in Route 53

sudo touch /etc/nginx/sites-available/bryanfweber.com
sudo chown -R $USER:$USER /etc/nginx/sites-available/bryanfweber.com

vi /etc/nginx/sites-available/bryanfweber.com

server {
listen 80;
server_name bryanfweber.com;
location / {
proxy_pass http://127.0.0.1:8000/;
}
}

sudo ln -f -s /etc/nginx/sites-available/bryanfweber.com /etc/nginx/sites-enabled/bryanfweber.com
sudo service nginx restart

sudo apt-get install software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx
#use certbot nginx plugin for certificate installation
sudo certbot --nginx 

## install pip / files


## github setup - https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/

ssh-keygen -t rsa -b 4096 -C "bryan@looker.com"
eval "$(ssh-agent -s)"
ssh-add -k ~/.ssh/id_rsa

### add id_rsa.pem to github repo

pip install virtualenv

virtualenv venv
source ./venv/bin/activate



pip install -r requirements.txt
curl 
git clone git@github.com:bryan-at-looker/info_scheming.git
