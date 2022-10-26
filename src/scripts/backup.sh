path=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export PGPASSWORD="Replace With PSQL Password"
name=`date +%d_%m_%Y`
mkdir -p $path/backups
pg_dump -Fc -h <psql server ip> -U <username> <database_name> -f $path/backups/$name.dump