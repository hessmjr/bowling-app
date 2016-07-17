# create new user
user "mark" do
  supports :manage_home => true
  home "/home/mark"
  action :create
end

execute "apt-get update" do
  command "apt-get update"
end
