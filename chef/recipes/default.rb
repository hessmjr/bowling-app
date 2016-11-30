# update linux
execute "update" do
    command "apt-get update"
end

# recipes for installing mongodb
include_recipe "mongodb::10gen_repo"
include_recipe "mongodb::default"

# python runtime version and app requirements
python_runtime '2'
pip_requirements '/home/mark/BowlApp/requirements.txt'

# supervisor setup
include_recipe "supervisor"

cookbook_file "/etc/supervisord.conf" do
    source "supervisord.conf"
    mode 0644
end

# Start supervisor to handle start and restarting API
supervisor_service "BowlApp" do
    action :enable
    directory "/home/mark/BowlApp"
    command "python api.py"
    stdout_logfile "/home/mark/BowlApp/supervisord_out.txt"
    stdout_logfile_maxbytes "50MB"
    redirect_stderr true
end
