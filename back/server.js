const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs-extra');
const path = require('path');
const csv = require('csv-parser');

const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.json());

app.post('/save', (req, res) => {
    const data = req.body.suites;
    const csvData = convertToCSV(data);
    const filePath = path.join(__dirname, 'suites.csv');
    fs.writeFileSync(filePath, csvData);
    res.send({ message: 'Data saved to CSV', filePath });
});

function convertToCSV(objArray) {
    const array = typeof objArray !== 'object' ? JSON.parse(objArray) : objArray;
    let str = 'id,nbRooms,surface,nbFenetre,price,annee,balcon,garage,note,price_category,ville\n';

    for (const suite of array) {
        let line = `${suite.id},${suite.nbRooms},${suite.surface},${suite.nbFenetre},${suite.price},${suite.annee},${suite.balcon},${suite.garage},${suite.note},${suite.price_category},${suite.ville}`;
        str += line + '\n';
    }

    return str;
}

app.get('/suites', (req, res) => {
    const results = [];
    fs.createReadStream(path.join(__dirname, 'suites.csv'))
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', () => {
            res.json(results);
        });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
