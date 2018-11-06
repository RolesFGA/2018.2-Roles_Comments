default:
	
	docker build . -t docker-django
	docker run --rm -p 8002:8002 -v `pwd`:"/app" -w "/app" --name product-microservice -it docker-django bash
