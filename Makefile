.ONESHELL:

run-tests:
	@ pytest --cov-report term-missing --cov=cbi_webengines

requirements:
	@ python3 -m pipenv requirements > requirements.txt

pypi:
	@ rm -rf ./build
	@ rm -rf ./dist
	@ rm -rf ./*.egg-info
	@ python3 setup.py bdist_wheel
	@ python3 -m twine upload --config-file .pypirc --repository pypi dist/* 
