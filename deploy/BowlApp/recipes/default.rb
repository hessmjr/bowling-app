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

# # start flask app
# execute "start app" do
#     command "flask BowlApp"
# end
# python_execute 'myapp.py' do
#   user 'myuser'
# end
