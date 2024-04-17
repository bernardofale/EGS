Para correr o docker:
sudo docker-compose up --build

Caso esteja a ficar stuck:
sudo docker volume rm $(sudo docker volume ls -qf dangling=true)
