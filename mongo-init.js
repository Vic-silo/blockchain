db = db.getSiblingDB('blockchain');
db.createUser({
  user: "admin",
  pwd: "admin",
  roles: [{ role: "readWrite", db: "blockchain" }]
});