aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 637423258937.dkr.ecr.eu-central-1.amazonaws.com
docker build -t findit_api .
docker tag findit_api:latest 637423258937.dkr.ecr.eu-central-1.amazonaws.com/bot_api:latest
docker push 637423258937.dkr.ecr.eu-central-1.amazonaws.com/bot_api:latest