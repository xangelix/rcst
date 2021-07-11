#!/usr/bin/bash

mkdir -p /home/gitpod/.ssh/
echo $SSH_KEY_B64 | base64 -di > /home/gitpod/.ssh/id_rsa
echo "--SSH Private Key Imported--"
echo "IF YOU ENTER PASSSWORD WRONG, RUN: './.gitpod.init_signing.sh'"
echo $GPG_KEY_B64 | base64 -di > /home/gitpod/pkey.key
gpg --pinentry-mode=loopback --import /home/gitpod/pkey.key
echo "--GPG Private Key Imported--"
git config --global user.signingkey $GPG_KEY_ID
git config --global commit.gpgsign true
echo "--GPG Private Key Set In Git--"
test -r ~/.bash_profile && echo 'export GPG_TTY=$(tty)' >> ~/.bash_profile
echo 'export GPG_TTY=$(tty)' >> ~/.profile
echo "--GPG Private Key Set In Bash--"
printf "allow-loopback-pinentry\ndefault-cache-ttl 34560000\nmax-cache-ttl 34560000\ndefault-cache-ttl-ssh 34560000\nmax-cache-ttl-ssh 34560000" >> /home/gitpod/.gnupg/gpg-agent.conf
echo "pinentry-mode loopback" >> /home/gitpod/.gnupg/gpg.conf
gpg-connect-agent reloadagent /bye
touch temp.txt
gpg --pinentry-mode=loopback --sign temp.txt
rm -f temp.txt temp.txt.gpg
echo "--GPG Initialization Workaround Complete--"
git config --global user.email $GIT_EMAIL
echo "--Git Email Set--"
