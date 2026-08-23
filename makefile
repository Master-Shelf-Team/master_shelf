run_front:
	streamlit run frontend/app.py

run_api:
	uvicorn mastershelf.api.fast:app --reload

test:
	pytest tests
