default:
	@echo "Examples:"
	@echo "    make run          # Starts a Flask development server locally"
	@echo "    make production   # Starts the production server, sets up logging to logs/"
	@echo "    make clean        # Cleans all directors"
	@echo "    make test         # Runs unit tests"

setup:
	virtualenv env
	. env/bin/activate
	pip install -r requirements.txt

run:
	./stuybulletin/manage.py devserver -p 5000

production:
	./stuybulletin/manage.py --config_prod -p 5000 -l logs devserver

clean:
	rm -rf *~
	rm -rf *\#
	rm -rf .\#*

test:	
	py.test --cov-report html --cov app tests
