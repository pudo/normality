
test:
	python setup.py test


upload:
	git push
	python setup.py sdist bdist_wheel upload


clean:
	rm -rf dist build
