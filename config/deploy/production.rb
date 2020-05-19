server '165.22.71.2', port: 22, roles: [:web, :app, :db], primary: true
set :stage,              :production
set :branch,             'master'