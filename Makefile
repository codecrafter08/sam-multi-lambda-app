.PHONY: clean build deploy

clean:
	rm -rf build
	rm -rf common_db_layer/python/
	rm -rf db_helper/db.sqlite3

build: clean
		mkdir -p build/employee_service
		mkdir -p build/payroll_service
		mkdir -p build/salesjob_service
		mkdir -p build/entity_service
		mkdir -p build/db_helper
		mkdir -p build/public_apis
		mkdir -p build/root_service
		mkdir -p build/constants_service
		mkdir -p build/auth_service
		mkdir -p build/entity_disputes_service
		mkdir -p build/sales_job_service_overview
		cp -r employee_service/* build/employee_service/
		cp -r payroll_service/* build/payroll_service/
		cp -r salesjob_service/* build/salesjob_service/
		cp -r entity_service/* build/entity_service/
		cp -r db_helper/* build/db_helper/
		cp -r public_apis/* build/public_apis/
		cp -r root_service/* build/root_service/
		cp -r constants_service/* build/constants_service/
		cp -r auth_service/* build/auth_service/
		cp -r entity_disputes_service/* build/entity_disputes_service/
		cp -r sales_job_service_overview/* build/sales_job_service_overview/
		pip3.12 install --upgrade -r common_db_layer/requirements.txt -t common_db_layer/python
		cp db_helper/db_models.py common_db_layer/python/

deploy: build
		sam build
		export AWS_PROFILE=codecrafet08aws
		sam deploy --guided
