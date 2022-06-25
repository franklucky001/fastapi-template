runtime:devel
	docker build -f dockerfiles/Dockerfile -t $(namespace):devel-$(version) .

runtime-gpu:devel-gpu
	docker build -f dockerfiles/gpu/Dockerfile  -t $(namespace):$(version) .

devel:
	docker build -f dockerfiles/Dockerfile.devel  -t $(namespace):cu113-devel-$(version) .

devel-gpu:
	docker build -f dockerfiles/gpu/Dockerfile.devel  -t $(namespace):cu113-$(version) .
