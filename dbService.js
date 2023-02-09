const mysql = require('mysql');
const dotenv = require('dotenv');
let instance = null;
dotenv.config();

const connection = mysql.createConnection({

    user: process.env.USER,
    password: process.env.PASSWORD,
    database: process.env.DATABASE,
    port: process.env.DB_PORT,
    host: process.env.HOST
});

connection.connect((err) => {
    if(err){
        console.log(err.message)
    }
    console.log('DB ' + connection.state);
    //console.log(process.env['USER'])
});

class dbService {
    static getDbServiceInstance() {
        return instance ? instance : new dbService();
    }

    async getAllData() {
        try{
            const response = await new Promise((resolve, reject) => {
                const query = "SELECT * FROM users;";

                connection.query(query, (err, results) => {
                    if (err) reject(new Error(err.message))
                    resolve(results);
                });
            });
            //console.log(response);
            return response;

        } catch (error) {
            console.log(error);
        }
    }

    async insertNewName(name) {
        try{
            const insertId = await new Promise((resolve, reject) => {
                const query = "INSERT INTO users (name) VALUES (?);";

                connection.query(query, [name],  (err, result) => {
                    if (err) reject(new Error(err.message))
                    resolve(result.insertId);
                });
            });
            return {
                id: insertId,
                name : name
            };
            //console.log(insertId);
        } catch (error) {
            console.log(error);
        }
    }

    async searchByName(name) {
        try{
            const response = await new Promise((resolve, reject) => {
                const query = "SELECT * FROM users WHERE name = ?;";

                connection.query(query, [name], (err, results) => {
                    if (err) reject(new Error(err.message))
                    resolve(results);
                });
            });
            //console.log(response);
            return response;
        } catch (error) {
            console.log(error);
        }
    }


}

module.exports = dbService;