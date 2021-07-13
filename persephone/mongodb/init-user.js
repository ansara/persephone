require('dotenv').config()

const db = require('db')

console.log("Creating non-admin user")

//create non admin user
db.createUser({
    user: process.env.MONGO_USER,
    pwd: process.env.MONGO_USER_PASSWORD,
    roles: [
      {
        role: 'readWrite',
        db: 'persephone'
      }
    ]
  })