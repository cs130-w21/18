#!/bin/sh
export ALLOW_ORIGINS='*'
export DATABASE_URL='postgres://imtcpfztrmkocz:40a5aab09192287bb73e61c72ae811cb419795481385c0bb0701e6d31297a027@ec2-3-214-3-162.compute-1.amazonaws.com:5432/d79u9984qishrm'
export FRONT_END_URI='https://test-fe-130.herokuapp.com'
export JWT_SECRET='psst...idontlikeshawnmendez...sshhh'
export SPOTIFY_REDIRECT_URI='https://musaic-13018.herokuapp.com/login/callback'
ENV=${1:-0}
echo $ENV
tmp_dir=$(mktemp -d)
if [ $ENV -eq 0 ]
then
    echo "0 env = ${ENV}"
    python3 -m venv $tmp_dir
    . "${tmp_dir}/bin/activate"
    pip install -r requirements.txt
else
    echo "1 env = ${ENV}"
    . "${ENV}/bin/activate"
fi
gunicorn main:app &
SERVER_PID=$!
pytest
kill $SERVER_PID
deactivate
rm -rf $tmp_dir
