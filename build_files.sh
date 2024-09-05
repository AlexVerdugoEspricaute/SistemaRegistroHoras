# build_files.sh
#!/bin/bash
pip install -r requirements.txt
python manage.py collectstatic --noinput