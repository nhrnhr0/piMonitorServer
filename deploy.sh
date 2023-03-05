git pull
source env/bin/activate
pip install -r requierments.txt
python manage.py migrate 
env/bin/python manage.py collectstatic --noinput
sudo systemctl daemon-reload
sudo systemctl restart daphne
sudo systemctl restart nginx

echo 'done'
