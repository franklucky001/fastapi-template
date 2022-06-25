runtime:devel
	docker build -f dockerfiles/Dockerfile -t $(namespace):$(version) .

runtime-gpu:devel-gpu
	docker build -f dockerfiles/gpu/Dockerfile  -t $(namespace):cu113-$(version) .

devel:requirement
	docker build -f dockerfiles/Dockerfile.devel  -t $(namespace):devel-$(version) .

devel-gpu:requirement
	docker build -f dockerfiles/gpu/Dockerfile.devel  -t $(namespace):cu113-devel-$(version) .

requirement:
	rm -f requirements.txt
	poetry export -f requirements.txt --output requirements.txt --without-hashes

deploy:runtime
	docker tag $(namespace):$(version) $(remote_namespace):latest
	docker push $(remote_namespace):latest

deploy-gpu:runtime-gpu
	docker tag $(namespace):cu113-$(version) $(remote_namespace):latest
	docker push $(remote_namespace):latest
