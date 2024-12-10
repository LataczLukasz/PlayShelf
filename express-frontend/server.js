const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Ustaw Pug jako silnik szablonów
app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'views'));

// Strona główna
app.get('/', async (req, res) => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/games/', {
            headers: {
                'Accept': 'application/json'
            }
        });
        const games = response.data.games;
        res.render('index', { games });
    } catch (error) {
        console.error('Błąd podczas pobierania gier:', error);
        res.status(500).send('Wystąpił błąd podczas pobierania gier.');
    }
});

// Uruchom serwer
app.listen(PORT, () => {
    console.log(`Serwer działa na http://localhost:${PORT}`);
});
