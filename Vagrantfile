# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure(2) do |config|

    # use ubuntu 64 bit box
    config.vm.box = "ubuntu/trusty64"

    # forward ports to host computer
    config.vm.network :forwarded_port, guest: 5000, host: 7878

    # Berksfile setup
    config.berkshelf.berksfile_path = "deploy/Berksfile"
    config.berkshelf.enabled = true

    # allow host to access files within VM
    config.vm.synced_folder ".", "/home/mark/BowlApp"

    # provision vagrant box with chef
    config.omnibus.chef_version = '12.10.24'
    config.vm.provision "chef_solo" do |chef|
        chef.channel = "stable"
        chef.version = "12.10.24"
        chef.add_recipe "BowlApp::default"
    end
end
