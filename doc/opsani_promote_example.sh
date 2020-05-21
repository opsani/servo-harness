# For yq
apt update && apt install software-properties-common -y
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CC86BB64
add-apt-repository ppa:rmescandon/yq

apt update && apt install git wget yq -y

mkdir -p ~/.ssh
echo ${secrets.getValue("github_ssh_key")} | base64 -d > ~/.ssh/id_rsa
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa

git config --global user.email "ben@opsani.com"
git config --global user.name "Ben Burdick"

wget https://gist.githubusercontent.com/benburdick/b68ee2e899eb93139e02edcde0ea0d25/raw/4df6751ff4a9b721c08901e609c6f8098a0d8aef/promote.sh -q -O promote.sh && chmod +x promote.sh

./promote.sh ${workflow.variables.cpu} ${workflow.variables.mem} ${app.name}

sleep 60
