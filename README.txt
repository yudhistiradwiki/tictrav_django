Nama venv yang dibuat = tictravenv


(Membuat virtual env sehingga tidak tabrakan)
python -m venv tictravenv

(Aktivasi virtual env)
tictravenv\Scripts\activate.bat

(Hapus env)
rm -r tictravenv

(Mmebuat requirements)
pip freeze > requirements.txt  

(Instalasi package menggunakan pip)
pip install -r requirements.txt
