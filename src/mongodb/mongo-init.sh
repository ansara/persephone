set -e

mongo <<EOF

use persephonedb

db.createUser({
  user: '$MONGO_USER',
  pwd: '$MONGO_PASSWORD',
  roles: [{
    role: 'readWrite',
    db: 'persephonedb'
  }]
})
EOF