
test:
	python setup.py test

upload:
	git push
	python setup.py sdist bdist_wheel upload -r pypi

clean:
	rm -rf dist build
