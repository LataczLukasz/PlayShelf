const express = require('express');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;

app.set('view engine', 'ejs'); // Możesz użyć EJS jako silnika szablonów
app.set('views', __dirname + '/views'); // Ustaw katalog dla widoków

app.get('/games', async (req, res) => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/games/', {
            headers: {
                Accept: 'application/json'
            }
        });
        const games = response.data.games; // Odbieranie danych gier
        res.render('games', { games }); // Renderowanie widoku z danymi gier
    } catch (error) {
        console.error('Błąd podczas pobierania danych:', error);
        res.status(500).send('Wystąpił błąd podczas pobierania danych z API.');
    }
});

app.listen(PORT, () => {
    console.log(`Serwer działa na http://localhost:${PORT}`);
});
