//setup_db.js
// MongoDB setup script
db = db.getSiblingDB('trending_topics');

// Create collection with schema validation
db.createCollection('trends', {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: ["_id", "nameoftrend1", "nameoftrend2", "nameoftrend3", "nameoftrend4", "nameoftrend5", "datetime", "ip_address"],
         properties: {
            _id: {
               bsonType: "string",
               description: "must be a string and is required"
            },
            nameoftrend1: {
               bsonType: "string",
               description: "must be a string and is required"
            },
            nameoftrend2: {
               bsonType: "string",
               description: "must be a string and is required"
            },
            nameoftrend3: {
               bsonType: "string",
               description: "must be a string and is required"
            },
            nameoftrend4: {
               bsonType: "string",
               description: "must be a string and is required"
            },
            nameoftrend5: {
               bsonType: "string",
               description: "must be a string and is required"
            },
            datetime: {
               bsonType: "date",
               description: "must be a date and is required"
            },
            ip_address: {
               bsonType: "string",
               description: "must be a string and is required"
            }
         }
      }
   }
});

// Create indexes
db.trends.createIndex({ "datetime": 1 });
db.trends.createIndex({ "ip_address": 1 });

// Create user (optional)
db.createUser({
  user: "trendingapp",
  pwd: "password",
  roles: [
    { role: "readWrite", db: "trending_topics" }
  ]
});

print("Database setup completed successfully!");