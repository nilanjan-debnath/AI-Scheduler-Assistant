echo "BUILD START"

python3.9 -m venv venv
source venv/bin/activate

python3.9 -m pip install --upgrade pip
pip install -r requirements.txt

python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput
python3.9 manage.py collectstatic --noinput --clear

echo "BUILD END"
