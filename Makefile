reinstall_package:
	@pip uninstall -y mastershelf || :
	@pip install -e .

run_front:
	streamlit run frontend/app.py

run_api:
	uvicorn mastershelf.api.fast:app --reload

test:
	pytest tests
