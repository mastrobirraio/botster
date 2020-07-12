clean:
	rm -rf dist/*

package:
	python setup.py sdist
	python setup.py bdist_wheel
