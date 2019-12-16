freeze:
	python3 application.py build

sync: freeze
	aws s3 sync s3://dalwilliams.info build