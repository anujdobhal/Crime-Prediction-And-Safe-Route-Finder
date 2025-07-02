const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const googleMapsClient = require('@google/maps').createClient({
  key: 'YOUR_API_KEY'
});

const app = express();
app.use(express.json()); 
const port = 8080;

app.set('view engine', 'ejs');



app.get('/', (req, res) => {
  res.render('home');
});

app.get('/map', (req, res) => {
  res.render('map');
});

app.get('/adminlogin', (req, res) => {
  res.render('adminlogin');
});
app.get('/admin', (req, res) => {
  res.render('adminportal');
});

app.post('/process-coords', (req, res) => {
    const inputdata = req.body;

    const python = spawn('python', ['./utility/prediction.py']);
    let result = '';

    python.stdout.on('data', (data) => {
        result += data.toString();
    });

    python.stderr.on('data', (data) => {
        console.error(`Python error: ${data}`);
    });

    python.on('close', (code) => {
        const score = parseInt(result.trim(), 10);
        res.json({ result: score });
    });

    python.stdin.write(JSON.stringify(inputdata));
    python.stdin.end();
});

app.post('/add-crime', (req, res) => {
    const { latitude, longitude, crimeType, crimeTime } = req.body;
    console.log('Received:', latitude, longitude, crimeType, crimeTime);

    const child = spawn('python', ['./utility/add_data.py', latitude, longitude, crimeType, crimeTime]);

    child.stderr.on('data', (data) => {
        console.error('Python error:', data.toString());
    });

    child.on('close', (code) => {
        if (code === 0) {
            res.json({ success: true });
        } else {
            res.status(500).json({ success: false });
        }
    });
});
app.post('/train-model', (req, res) => {
    const scriptPath = path.join(__dirname, 'utility', 'trainer.py');
    const python = spawn('python', [scriptPath]);

    let output = '';

    python.stdout.on('data', (data) => {
        output += data.toString(); // collect stdout
    });

    python.stderr.on('data', (data) => {
        console.error(`Training Error: ${data.toString()}`);
    });

    python.on('close', (code) => {
        if (code === 0) {
            res.json({ success: true, message: output.trim() }); // send output back
        } else {
            res.status(500).json({ success: false, message: 'Training failed.' });
        }
    });
});


app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
