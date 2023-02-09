const express = require('express');
const app = express();
const cors = require('cors');
const dotenv = require('dotenv');
const { response } = require('express');
dotenv.config();

const dbService = require('./dbService');

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended  : false}));


//create
app.post('/insert', (request, response) => {
    //console.log(request.body);
    //console.log()
    const { name } = request.body;
    const db = dbService.getDbServiceInstance();
    const result = db.insertNewName(name);
    result 
    .then(data => response.json({ data: data}))
    .catch(err => console.log(err));

});


//read
app.get('/getAll', (request, response) => {
    const db = dbService.getDbServiceInstance();

    const result = db.getAllData();

    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));
    // response.json({
    //     success: true
    // });

    // console.log('test');
});


//update


//delete

//search
app.get('/search/:name', (request, response) => {
    const { name } = request.params;
    const db = dbService.getDbServiceInstance();

    const result = db.searchByName(name);

    result
    .then(data => response.json({data : data}))
    .catch(err => console.log(err));

})


app.listen(process.env.PORT, () => console.log('App is running'));