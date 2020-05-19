set :repo_url,                'git@github.com:devteamepic/worker.git'
set :application,             'worker'
set :user,                    'root'
set :pty,                     false
set :use_sudo,                false
set :deploy_via,              :remote_cache
set :deploy_to,               "/home/#{fetch(:user)}/#{fetch(:application)}"
set :ssh_options,             { forward_agent: true, user: fetch(:user), keys: %w(~/.ssh/id_rsa.pub) }

task :restart_docker do
    on roles(:app) do
        execute "docker-compose stop"
        execute "docker-compose build"
        execute "docker-compose up -d"
    end
end

after "deploy", "restart_docker"