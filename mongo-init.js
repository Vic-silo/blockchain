db = db.getSiblingDB('db_name');
db.createUser({
  user: "user",
  pwd: "pwd",
  roles: [{ role: "readWrite", db: "db_name" }]
});
