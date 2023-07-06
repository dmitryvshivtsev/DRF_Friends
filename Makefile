.PHONY: docker, clean_docker

docker:
	docker build -t django_friends:vk .
	docker run -d --name dj_friends -p 80:8000 django_friends:vk

clean_docker:
	docker stop dj_friends
	docker rm dj_friends

style:
	black .