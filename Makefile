
clean:
	find . -name *.pyc | xargs rm -rf
	find . -name *.pyo | xargs rm -rf
	rm -rf log/*

