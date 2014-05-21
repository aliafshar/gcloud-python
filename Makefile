
env = env
bin = $(env)/bin
pip = $(bin)/pip
py = $(bin)/py

test: env testdeps 
	$(bin)/nosetests

testdeps:
	$(pip) install unittest2 nose

deps:
	$(pip) install -e .

env:
	virtualenv env
	make deps
	make testdeps

clean:
	rm -rf env
