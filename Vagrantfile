Vagrant.configure("2") do |config|  # 2-latest version of vagrant API
  # tells vagrant the image we want to base our server on
  config.vm.box = "ubuntu/xenial64"
  # network configuration: forwards port 8080 on guest os to port 8080 on host
  config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 8080, host: 8080
  # provisioning script
  config.vm.provision "shell", inline: <<-SHELL
    # Update and upgrade the server packages.
    sudo apt-get update
    sudo apt-get -y upgrade
    # Set Ubuntu Language
    sudo locale-gen en_GB.UTF-8
    # Install Python, SQLite and pip
    sudo apt-get install -y python3-dev sqlite python-pip
    # Upgrade pip to the latest version.
    sudo pip install --upgrade pip
    # Install and configure python virtualenvwrapper.
    sudo pip install virtualenvwrapper
    if ! grep -q VIRTUALENV_ALREADY_ADDED /home/ubuntu/.bashrc; then
        echo "# VIRTUALENV_ALREADY_ADDED" >> /home/ubuntu/.bashrc
        echo "WORKON_HOME=~/.virtualenvs" >> /home/ubuntu/.bashrc
        echo "PROJECT_HOME=/vagrant" >> /home/ubuntu/.bashrc
        echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/ubuntu/.bashrc
    fi
  SHELL

end
