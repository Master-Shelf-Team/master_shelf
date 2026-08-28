reinstall_package:
	@pip uninstall -y mastershelf || :
	@pip install -e .
	@python -m spacy download en_core_web_sm

run_front:
	streamlit run frontend/app.py

run_pierre:
	streamlit run frontend/app_Pierre.py

run_api:
	uvicorn mastershelf.api.fast:app --reload

test:
	pytest tests

run_baseline:
	python -m mastershelf.main
