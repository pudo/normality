

upload:
	python setup.py sdist bdist_wheel upload


clean:
	rm -rf dist build