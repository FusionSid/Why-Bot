path=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export PGPASSWORD="Replace With PSQL Password"
name=`date +%m_%d_%Y`
mkdir -p $path/backups
pg_dump -Fc -h 168.138.102.186 -U sid whybot -f $path/backups/$name.dump